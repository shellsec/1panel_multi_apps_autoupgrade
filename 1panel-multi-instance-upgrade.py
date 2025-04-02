# shellsec
import requests
import time
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class OnePanelMultiUpgrader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.instances = self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                instances = config.get('instances', [])
                
                # Validate URLs
                for instance in instances:
                    if not instance['url'].startswith(('http://', 'https://')):
                        raise ValueError(f"Invalid URL format in config: {instance['url']}")
                    if 'your-' in instance['url'].lower():
                        raise ValueError(f"Placeholder URL found: {instance['url']}")
                
                return instances
        except Exception as e:
            print(f"加载配置文件出错: {str(e)}")
            return []
    
    def login(self, instance):
        """登录单个1Panel实例"""
        session = requests.Session()
        base_url = instance['url'].rstrip('/')
        
        print(f"\n[步骤1] 访问首页获取Cookies: {base_url}/")
        session.get(f"{base_url}/")
        
        login_url = f"{base_url}/api/v1/auth/login"
        print(f"[步骤2] 提交登录请求: {login_url}")
        
        login_data = {
            "name": instance['username'],
            "password": instance['rsapassword'],
            "ignoreCaptcha": True,
            "captcha": "",
            "captchaID": "cv2abf4VztaeNx0ZcB7t",
            "authMethod": "session",
            "language": "zh"
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': base_url,
                'Referer': f"{base_url}/",
                'EntranceCode': '',
                'SecurityEntrance': ''
            }
            
            response = session.post(
                login_url, 
                json=login_data,
                headers=headers,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    print(f"{base_url} 登录成功")
                    return session, base_url
                else:
                    print(f"{base_url} 登录失败: {result.get('message', '未知错误')}")
            else:
                print(f"{base_url} 错误: 非200状态码 ({response.status_code})")
            
            return None, None
        except Exception as e:
            print(f"{base_url} 登录时发生异常: {str(e)}")
            return None, None
    
    def process_instance(self, instance):
        """处理单个实例的升级流程"""
        session, base_url = self.login(instance)
        if not session:
            return False
            
        # 检查应用更新
        print(f"[步骤3] 检查应用更新: {base_url}")
        updates_url = f"{base_url}/api/v1/apps/installed/search"
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Referer': f'{base_url}/apps/upgrade',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "page": 1,
                "pageSize": 20,
                "name": "",
                "tags": [],
                "update": True,
                "sync": True
            }
            
            response = session.post(
                updates_url,
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    data = result.get('data', {})
                    apps = data.get('items') if data.get('items') is not None else []
                    updates = []
                    
                    for app in apps:
                        if app.get('canUpdate'):
                            updates.append({
                                'name': app.get('name', ''),
                                'current': app.get('version', ''),
                                'new': app.get('latestVersion', ''),
                                'id': app.get('id')
                            })
                    
                    if not updates:
                        print(f"[步骤4] 没有可用的应用更新")
                        return True
                    
                    print(f"[步骤4] 发现 {len(updates)} 个可用应用更新")
                    
                    # 执行每个应用的升级
                    for update in updates:
                        print(f"[步骤5] 正在升级 {update['name']} 从 {update['current']} 到 {update['new']}")
                        
                        # 获取应用版本详情
                        versions_url = f"{base_url}/api/v1/apps/installed/update/versions"
                        versions_payload = {"appInstallID": update.get('id')}
                        versions_response = session.post(versions_url, json=versions_payload, headers=headers)
                        
                        if versions_response.status_code == 200:
                            versions_result = versions_response.json()
                            if versions_result.get('code') == 200 and versions_result.get('data'):
                                first_version = versions_result['data'][0]
                                detail_id = first_version.get('detailId')
                                
                                # 执行升级
                                upgrade_url = f"{base_url}/api/v1/apps/installed/op"
                                upgrade_payload = {
                                    "detailId": detail_id,
                                    "operate": "upgrade",
                                    "installId": update.get('id'),
                                    "backup": True,
                                    "pullImage": True,
                                    "version": first_version.get('version'),
                                    "dockerCompose": ""
                                }
                                
                                upgrade_response = session.post(upgrade_url, json=upgrade_payload, headers=headers)
                                
                                if upgrade_response.status_code == 200:
                                    upgrade_result = upgrade_response.json()
                                    if upgrade_result.get('code') == 200:
                                        print(f"[步骤6] {update['name']} 升级已开始")
                                        time.sleep(5)  # 添加短暂延迟避免请求过载
                                    else:
                                        print(f"[步骤6] {update['name']} 升级失败: {upgrade_result.get('message', '未知错误')}")
                                else:
                                    print(f"[步骤6] {update['name']} 升级请求失败: {upgrade_response.status_code}")
                            else:
                                print(f"[步骤5] 获取 {update['name']} 版本信息失败: {versions_result.get('message', '未知错误')}")
                        else:
                            print(f"[步骤5] 获取 {update['name']} 版本信息请求失败: {versions_response.status_code}")
                    
                    return True
                else:
                    print(f"[步骤3] 检查应用更新失败: {result.get('message', '未知错误')}")
                    return False
            else:
                print(f"[步骤3] 检查应用更新请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[步骤3] 检查应用更新异常: {str(e)}")
            return False
    
    def run_upgrades(self, max_workers=3):
        """并发执行多个实例的升级"""
        print(f"\n=== 开始批量升级 {len(self.instances)} 个1Panel实例 ===")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.process_instance, self.instances))
        
        success_count = sum(1 for r in results if r)
        print(f"\n=== 升级完成 ===")
        print(f"成功处理: {success_count}/{len(self.instances)}")
        
        return success_count == len(self.instances)

if __name__ == "__main__":
    # # 创建配置文件示例
    # config_example = {
    #     "instances": [
    #         {
    #             "url": "http://192.168.1.1:27055",
    #             "username": "4bf8df",
    #             "password": "4bf8df==",
    #             "rsapassword": "4bf8df"
    #         },
    #         # 可以添加更多实例
    #     ]
    # }
    
    # # 保存示例配置文件
    # with open('1panel_multi_config.json', 'w', encoding='utf-8') as f:
    #     json.dump(config_example, f, indent=4, ensure_ascii=False)
    
    # print("已创建示例配置文件: 1panel_multi_config.json")
    # print("请修改配置文件后重新运行脚本")
    
    # 实际使用时取消下面注释
    upgrader = OnePanelMultiUpgrader("1panel_multi_config.json")
    upgrader.run_upgrades()

        #     // 如果需要添加第二个实例，请确保提供真实的URL和认证信息
        # // {
        # //     "url": "http://实际IP或域名:端口",
        # //     "username": "实际用户名",
        # //     "password": "实际密码",
        # //     "rsapassword": "实际RSA加密密码"
        # // }
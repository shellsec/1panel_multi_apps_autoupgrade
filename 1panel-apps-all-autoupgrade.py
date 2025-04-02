# shellsec
import requests
import time
from bs4 import BeautifulSoup

class OnePanelUpgrader:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self):
        """登录1Panel面板"""
        print(f"\n[步骤1] 访问首页获取Cookies: {self.base_url}/")
        self.session.get(f"{self.base_url}/")
        
        login_url = f"{self.base_url}/api/v1/auth/login"
        print(f"[步骤2] 提交登录请求: {login_url}")
        login_data = {
            "name": self.username,
            "password": "mKQM1Wco9ktYaxdmeg==",
            # password 需要在 1panel 登录页面 F12抓/api/v1/auth/login的password加密后的值
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
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/",
                'EntranceCode': '',
                'SecurityEntrance': ''
            }
            
            # 添加cookies
            cookies = {
                'rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX18zIcZLTVFdP1b5wlGdBD4NYkqwAAe1sOwtNk0vpWXQA2J3yweGITHQ',
                'locale': 'zh-Hans',
                'rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX1%2B46F1cOc8FdUuH1jJkfxLqszLf4Ot%2B9BVmgwgtlp68slinRVvBTOz8KQeeuT5RWbEqtW4JdIYvIA%3D%3D',
                'rl_user_id': 'RudderEncrypt%3AU2FsdGVkX184PPeBaHHVhMJUE07lDj05uH2ETgX6Ahtlvu0yTabXsDqt9E%2BJnqnTlwbTz0E8ezOKYiPCFeS56a8%2BIFucTqK9%2BdV%2FpBmR6Yl1B8OwVi%2BN9IanNM8X9xNxfeilygPlYE7GXvt%2BBi%2Bnfh3hc7zN3DPqmZqxjvQspvc%3D',
                'rl_trait': 'RudderEncrypt%3AU2FsdGVkX18xhNqrSx5%2F%2F0uxjyToPOsSLXNEqmNqGmTEuKBcLC9yWnKjD3bXlD2j6D4XV7OBb8uI85XOQDNBr6ifq4St5oti0FsvBJJDL1OmBETZDLiwnNHX7va%2BoTDSzCqSW813zVVYWBt0BD5QYw%3D%3D',
                'rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2B9RT34SMNFSbmeLeVY%2B1JaGBLpjX5KbEKngAqk8azAOfrJcTRCq71F3YL7g%2B5OP3mGctslek47tbrIO3AzNj4WYYqE88y%2FsksFe8RigMHG0djolUmVHqXrG5OhwAqcdJK1h9zDg4D0Ag%3D%3D',
                'panel_public_key': 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF0cHpaZ2cxc0RuOTB2ZUtLWmlpdQo2cmN1elRueTJSMEtFNXNQVEwwQ01od0t5ZkgvS21PTjFMVmxRN3J5UzM0by84ZENoN3JPUi80YndNVEVwV2ZGCmJEdE5VT1dlYktXUjlxR1RENUVocm14eFFOaTRvbC9kSllGT1JIeDlibTNJNlJtNWxBQ3JxU1RQMDloMjlqcVUKR3dCQ2JtMXUwUTVwZmthaDV5N2txbGh4bFM0a2cvNDVHMDNKcjJoY0VIdC92aVZqOEozNEJCNGU3MWJjKzJDMAo5Ykx2TnNQa01JM1ZvbkFnZXJJYlR6UjNGazhMK3VySEhBZGRqcmJzYXcvdFZsMkpheW1FTzZLR1o5TlpqSkZtCm9VYzY5QW9tcDMzdWE2Zm5SNTBhcWlDYXRVZzA0dTYxcDNnUWFKWjhEOXovNlFYSEZaUU14T1N0R0Z0ZlhleFUKdVFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg%3D%3D',
                'rl_page_init_referrer': 'rudderencrypt%3au2fsdgvkx19kx8nrbeo%2fgem2qwwxjkbwd3lekxu7f22inmo7qdb3ers8xrl%2f4xe1'
            }
            
            response = self.session.post(
                login_url, 
                json=login_data,
                headers=headers,
                cookies=cookies,
                allow_redirects=False
            )
            
            print(f"登录响应状态码: {response.status_code}")
            print(f"登录响应内容: {response.text[:200]}...")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('code') == 200:
                        self.logged_in = True
                        print("登录成功")
                        return True
                    else:
                        print(f"登录失败: {result.get('message', '未知错误')}")
                except ValueError:
                    print("错误: 响应不是有效的JSON格式")
            else:
                print(f"错误: 非200状态码 ({response.status_code})")
            
            return False
        except Exception as e:
            print(f"登录时发生异常: {str(e)}")
            return False

    def check_updates(self):
        """检查可用更新"""
        if not self.logged_in:
            print("请先登录")
            return False
            
        updates_url = f"{self.base_url}/api/v1/apps/installed/search"
        print(f"\n[步骤3] 检查应用更新: {updates_url}")
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Referer': f'{self.base_url}/apps/upgrade',
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
            
            response = self.session.post(
                updates_url,
                json=payload,
                headers=headers
            )
            
            print(f"更新检查响应状态码: {response.status_code}")
            print(f"更新检查响应内容: {response.text[:500]}...")
            
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
                    
                    return updates if updates else None
                else:
                    print(f"更新检查失败: {result.get('message', '未知错误')}")
            else:
                print(f"错误: 非200状态码 ({response.status_code})")
            
            return None
        except Exception as e:
            print(f"检查更新时出错: {str(e)}")
            return None

    def get_app_versions(self, app_install_id):
        """获取应用可更新版本"""
        if not self.logged_in:
            print("请先登录")
            return None
            
        versions_url = f"{self.base_url}/api/v1/apps/installed/update/versions"
        print(f"\n[步骤4] 获取应用版本信息: {versions_url}")
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Referer': f'{self.base_url}/apps/upgrade',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "appInstallID": app_install_id
            }
            
            response = self.session.post(
                versions_url,
                json=payload,
                headers=headers
            )
            
            print(f"版本检查响应状态码: {response.status_code}")
            print(f"版本检查响应内容: {response.text[:500]}...")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    # 返回完整的版本信息列表而不仅仅是版本号
                    return result.get('data', [])
                else:
                    print(f"版本检查失败: {result.get('message', '未知错误')}")
            else:
                print(f"错误: 非200状态码 ({response.status_code})")
            
            return None
        except Exception as e:
            print(f"检查版本时出错: {str(e)}")
            return None

    def perform_upgrade(self, app_name, app_install_id, version=None):
        """执行应用升级"""
        upgrade_url = f"{self.base_url}/api/v1/apps/installed/op"
        print(f"\n[步骤5] 提交升级请求: {upgrade_url}")
        
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Referer': f'{self.base_url}/apps/upgrade'
            }
            
            payload = {
                "detailId": None,  # 需要从版本检查响应中获取
                "operate": "upgrade",
                "installId": app_install_id,
                "backup": True,
                "pullImage": True,
                "version": version,
                "dockerCompose": ""
            }
            
            # 先获取detailId
            versions = self.get_app_versions(app_install_id)
            if versions and isinstance(versions, list) and len(versions) > 0:
                # 假设第一个版本项包含detailId
                first_version = versions[0]
                if hasattr(first_version, 'get'):
                    payload["detailId"] = first_version.get('detailId')
            
            response = self.session.post(
                upgrade_url,
                json=payload,
                headers=headers
            )
            
            print(f"升级响应状态码: {response.status_code}")
            print(f"升级响应内容: {response.text[:200]}...")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    print(f"√ {app_name} 升级已开始")
                    return True
                else:
                    print(f"! 升级失败: {result.get('message', '未知错误')}")
            else:
                print(f"! 错误: 非200状态码 ({response.status_code})")
            
            return False
        except Exception as e:
            print(f"升级 {app_name} 时出错: {str(e)}")
            return False

    def auto_upgrade_all(self):
        """自动升级所有可用更新"""
        print("\n=== 开始自动升级流程 ===")
        if not self.login():
            return False
            
        updates = self.check_updates()
        if not updates:
            print("没有可用的更新")
            print("\n=== 升级流程结束 ===")
            return True
            
        print(f"\n发现 {len(updates)} 个可用更新:")
        for update in updates:
            print(f"\n应用名称: {update['name']}")
            print(f"当前版本: {update['current']}")
            
            # 获取可升级版本
            versions = self.get_app_versions(update.get('id'))
            if versions:
                # 修改为提取版本号并显示
                version_numbers = [v.get('version') for v in versions if v.get('version')]
                print(f"可升级版本列表: {', '.join(version_numbers)}")
                # 使用第一个可升级版本作为目标版本
                target_version = versions[0].get('version')
            else:
                print("! 无法获取可升级版本")
                continue
            
            # 执行升级
            print(f"\n正在升级 {update['name']} 到版本 {target_version}...")
            if not self.perform_upgrade(update['name'], update.get('id'), target_version):
                print(f"! 升级 {update['name']} 失败")
            else:
                print(f"√ {update['name']} 升级已开始")
            
            time.sleep(5)
            
        print("\n=== 升级流程结束 ===")
        return True

if __name__ == "__main__":
    # 配置你的1Panel信息
    PANEL_URL = "http://192.168.1.1:27055"  # 移除末尾斜杠
    USERNAME = "4bf8df"
    PASSWORD = "4bf8df"
    upgrader = OnePanelUpgrader(PANEL_URL, USERNAME, PASSWORD)
    upgrader.auto_upgrade_all()
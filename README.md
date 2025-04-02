# 1Panel Apps应用自动化升级脚本

## 项目介绍
本项目包含两个自动化升级脚本：
1. `1panel-apps-all-autoupgrade.py` - 单实例升级脚本
2. `1panel-multi-instance-upgrade.py` - 多实例并发升级脚本

通过登录 1Panel 面板，检查可用更新，获取应用可更新版本，并执行升级操作，实现应用程序的自动化升级。

踩坑已测试-应用商店-apps-自动升级
1、可以使用 watchtower 来自动更新，使用上比较繁琐，需要手动添加镜像标签，不适用
因为有的镜像是指定了版本号的，而不是latest版本，一般watchtower是监控latest版本更新的
自动更新 Docker 容器基础镜像的工具 --label com.centurylinklabs.watchtower.enable=true
2、1panel的面板设置有API 接口开启，见api_routes.py
开启和调试接口后，发现接口只有查询应用，没有升级应用的接口，有点搞笑

## 功能特点
### 单实例脚本功能
- 自动登录 1Panel 面板
- 检查所有已安装应用的可用更新
- 获取每个应用的可更新版本列表
- 自动升级所有可用更新的应用程序

### 多实例脚本功能
- 支持多1Panel实例并发升级
- 支持RSA加密密码存储
- 配置文件管理多个1Panel实例
- 并发执行升级任务提高效率

## 使用方法
### 单实例脚本配置
在脚本文件 `1panel-apps-all-autoupgrade.py` 中，配置以下信息：

1、1Panel面板设置-安全-安全入口 关闭，测试过开启的话登录老失败（安全入口设置为空时，则取消安全入口）
2、1panel-apps-all-autoupgrade.py
22行代码处修改
"password": "mKQM1Wco9ktYaxdmeg==",
# PASSWORD 需要在 1panel 登录页面 F12抓/api/v1/auth/login的password加密后的值
最下面 配置你的1Panel信息
```python
PANEL_URL = "http://192.168.1.1:27055"  # 移除末尾斜杠
USERNAME = "4c26e"
PASSWORD = "4bf8d"
```

### 多实例脚本配置
1. 创建配置文件 `1panel_multi_config.json`:
```json
```
2. 运行多实例脚本:
```bash
python 1panel-multi-instance-upgrade.py
```
### 运行脚本
确保你已经安装了所需的依赖库（`requests` 和 `beautifulsoup4`），然后运行以下命令：
```bash
python 1panel-apps-all-autoupgrade.py
```

## 依赖
本项目依赖以下 Python 库：
- `requests`：用于发送 HTTP 请求。
- `beautifulsoup4`：用于解析 HTML 内容。

你可以使用以下命令安装这些依赖：
```bash
pip install requests beautifulsoup4
```

## 结果展示
python .\1panel-apps-all-autoupgrade.py

=== 开始自动升级流程 ===

[步骤1] 访问首页获取Cookies: http://192.168.1.1:27055/
[步骤2] 提交登录请求: http://192.168.1.1:27055/api/v1/auth/login
登录响应状态码: 200
登录响应内容: {"code":200,"message":"","data":{"name":"4c26e3a0fa","token":"","mfaStatus":""}}...
登录成功

[步骤3] 检查应用更新: http://192.168.1.1:27055/api/v1/apps/installed/search
更新检查响应状态码: 200
更新检查响应内容: {"code":200,"message":"","data":{"total":1,"items":[{"id":12,"name":"siyuan","appID":311,"appDetailID":3718,"version":"3.1.22","status":"Running","message":"","httpPort":6806,"httpsPort":0,"path":"/opt/1panel/apps/siyuan/siyuan","canUpdate":true,"icon":"iVBORw0KGgoAAAANSUhEUgAAALQAAAC0CAYAAAA9zQYyAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAvNSURBVHhe7d1rcxzFFQbg7p7ZlYVjikolEAL4JiFsQqVClW3JutTGtqybCfkV+ZYflT+RFGBJKwXdLOwkNhAwjovEyYckhJuFZWt3ZzrnzPaqjK3L7mpnp7vnfb5I2wZco3...

发现 1 个可用更新:

应用名称: siyuan
当前版本: 3.1.22

[步骤4] 获取应用版本信息: http://192.168.1.1:27055/api/v1/apps/installed/update/versions
版本检查响应状态码: 200
版本检查响应内容: {"code":200,"message":"","data":[{"version":"3.1.26","detailId":3977,"dockerCompose":""},{"version":"3.1.25","detailId":3947,"dockerCompose":""},{"version":"3.1.24","detailId":3841,"dockerCompose":""},{"version":"3.1.23","detailId":3803,"dockerCompose":""}]}...
可升级版本列表: 3.1.26, 3.1.25, 3.1.24, 3.1.23

正在升级 siyuan 到版本 3.1.26...

[步骤5] 提交升级请求: http://192.168.1.1:27055/api/v1/apps/installed/op

[步骤4] 获取应用版本信息: http://192.168.1.1:27055/api/v1/apps/installed/update/versions
版本检查响应状态码: 200
版本检查响应内容: {"code":200,"message":"","data":[{"version":"3.1.26","detailId":3977,"dockerCompose":""},{"version":"3.1.25","detailId":3947,"dockerCompose":""},{"version":"3.1.24","detailId":3841,"dockerCompose":""},{"version":"3.1.23","detailId":3803,"dockerCompose":""}]}...
升级响应状态码: 200
升级响应内容: {"code":200,"message":"","data":{}}...
√ siyuan 升级已开始
√ siyuan 升级已开始

=== 升级流程结束 ===

## 无可用升级的话

更新检查响应状态码: 200
更新检查响应内容: {"code":200,"message":"","data":{"total":0,"items":null}}...
没有可用的更新

## 注意事项
- 请确保你的 1Panel 面板地址、用户名和密码正确。
- 脚本中的登录信息和请求头中的 Cookie 信息可能需要根据实际情况进行调整。
- 脚本在执行升级操作时会自动备份应用程序。

## 贡献
如果你有任何建议或改进，请随时提交 Issue 或 Pull Request。
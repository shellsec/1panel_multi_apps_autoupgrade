# shellsec
import json
import aiohttp
import time
import hashlib

# Example handler for /apps/checkupdate
async def check_app_update(request):
    return json.dumps({
        "status": "success",
        "message": "App update information retrieved."
    })

# Example handler for /apps/detail/{appId}/{version}/{type}"
async def get_app_detail(request):
    return json.dumps({
        "status": "success",
        "message": "App detail retrieved."
    })

# Example handler for /apps/details/{id}"
async def get_app_details(request):
    return json.dumps({
        "status": "success",
        "message": "App details retrieved."
    })

# Example handler for /apps/ignored
async def get_ignored_app(request):
    return json.dumps({
        "status": "success",
        "message": "Ignored app information retrieved."
    })

# Example handler for /apps/install
async def install_app(request):
    return json.dumps({
        "status": "success",
        "message": "App installed successfully."
    })

# Example handler for /apps/installed/check
async def check_installed_app(request):
    return json.dumps({
        "status": "success",
        "message": "Installed app checked."
    })

# You can add more handlers and integrate them with the API definitions as needed.

# 新的请求逻辑示例
async def new_api_request():
    # url = "http://192.168.1.1:38442/api/v1/ai/gpu/load"  # 测试没问题
    # url = "http://192.168.1.1:38442/api/v1/apps/checkupdate"  # 测试没问题
    url = "http://192.168.1.1:38442/api/v1/apps/installed/list"  
    timestamp = str(int(time.time()))
    system_key = 'apikey'  # 替换为实际的系统密钥
    expected_token = hashlib.md5(f'1panel{system_key}{timestamp}'.encode()).hexdigest()
    headers = {
        "1Panel-Token": expected_token,
        "1Panel-Timestamp": timestamp
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.text()
                    return data
                elif response.status == 500:
                    import logging
                    logging.error(f"请求失败，状态码: {response.status}, 错误信息: record not found")
                    return None
                else:
                    import logging
                    logging.error(f"请求失败，状态码: {response.status}")
                    return None
    except Exception as e:
        print(f"发生异常: {e}")
        return None

        

# 验证请求头的函数
async def validate_token(request):
    panel_token = request.headers.get('1Panel-Token')
    panel_timestamp = request.headers.get('1Panel-Timestamp')
    system_key = 'apikey'  # 检查此处面板 API 密钥是否存在拼写或格式错误，若有则进行修正
    expected_token = hashlib.md5(f'1panel{system_key}{panel_timestamp}'.encode()).hexdigest()
    if panel_token != expected_token:
        return False
    return True

# 新的GET请求处理函数
async def new_get_request(request):
    return json.dumps({
        "status": "success",
        "message": "新的GET请求处理成功。"
    })

# 新的POST请求处理函数
async def apps_installed_check(request):
    import json
    import aiohttp
    import time
    import hashlib
    url = 'http://192.168.1.1:38442/api/v1/apps/installed/check'
    timestamp = str(int(time.time()))
    system_key = 'apikey'
    expected_token = hashlib.md5(f'1panel{system_key}{timestamp}'.encode()).hexdigest()
    headers = {
        '1Panel-Token': expected_token,
        '1Panel-Timestamp': timestamp,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "key": "1",
        "name": "openresty"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.text()
                    return json.dumps({
                        "status": "success",
                        "message": "新的POST请求处理成功。",
                        "data": result
                    }, ensure_ascii=False)
                else:
                    import logging
                    logging.error(f"请求失败，状态码: {response.status}")
                    return json.dumps({
                        "status": "failed",
                        "message": f"请求失败，状态码: {response.status}"
                    })
    except Exception as e:
        print(f"发生异常: {e}")
        return json.dumps({
            "status": "failed",
            "message": f"发生异常: {e}"
        })

if __name__ == '__main__':
    import asyncio
    import types
    request = types.SimpleNamespace(headers={})
    result = asyncio.run(new_api_request())
    print(result)
    result = asyncio.run(apps_installed_check(request))
    print(result)
    
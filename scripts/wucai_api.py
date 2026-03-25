import os
import requests
import json
import sys

# 区域配置表：管理域名映射与 Token 获取链接
REGION_CONFIG = {
    'cn': {
        'base': 'https://api.wucai.site',
        'token_url': 'https://marker.dotalk.cn/#/personSetting/openapi'
    },
    'eu': {
        'base': 'https://eu.wucainote.com',
        'token_url': 'https://eu.wucainote.com/#/personSetting/openapi'
    },
    'us': {
        'base': 'https://us.wucainote.com',
        'token_url': 'https://us.wucainote.com/#/personSetting/openapi'
    }
}

def call_wucai(endpoint, params=None):
    """
    执行五彩 API 请求的核心函数
    """
    # 1. 获取并校验环境变量
    token = os.getenv('WUCAI_API_TOKEN', '').strip()
    region = os.getenv('WUCAI_REGION', 'cn').lower()
    
    # 自动识别并修正区域配置
    config = REGION_CONFIG.get(region, REGION_CONFIG['cn'])
    
    # Token 缺失拦截：直接返回带区域链接的友好提示
    if not token or not token.startswith('wct-'):
        return {
            "code": 10010, 
            "message": f"Missing or invalid WUCAI_API_TOKEN. Please get your OpenClaw Token from: {config['token_url']}"
        }

    # 2. 构造请求地址
    clean_endpoint = endpoint.lstrip('/')
    full_url = f"{config['base']}/apix/openapi/aiagent/{clean_endpoint}"
    
    # 3. 构造 Headers (包含固定 Client-ID 和 UA 伪装)
    headers = {
        "Authorization": token,
        "X-Client-ID": "56",
        "Content-Type": "application/json",
        "User-Agent": "WuCai-OpenClaw-Agent/1.0"
    }

    try:
        # 4. 发起 POST 请求，强制 15s 超时
        response = requests.post(
            full_url, 
            json=params or {}, 
            headers=headers, 
            timeout=15
        )
        
        # 尝试解析业务 JSON
        try:
            return response.json()
        except ValueError:
            return {
                "code": response.status_code, 
                "message": f"Server error (Non-JSON). Status: {response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        return {"code": -1, "message": "Connection timed out (15s). Please check your network or region setting."}
    except requests.exceptions.RequestException as e:
        return {"code": -1, "message": f"Network Error: {str(e)}"}

if __name__ == "__main__":
    """
    CLI 入口：支持从 Stdin 或 命令行参数读取 JSON
    """
    if len(sys.argv) < 2:
        print(json.dumps({"code": -1, "message": "Usage: echo '<json>' | python wucai_api.py <endpoint>"}))
        sys.exit(1)
        
    endpoint_arg = sys.argv[1]
    params_data = {}

    # 优先从管道 (Stdin) 读取数据，完美解决引号冲突问题
    try:
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read().strip()
            if raw_input:
                params_data = json.loads(raw_input)
        elif len(sys.argv) > 2:
            # 兼容模式：从第二个命令行参数读取
            params_data = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"code": -1, "message": "Invalid JSON input."}))
        sys.exit(1)
            
    # 执行并输出结果给 AI (stdout)
    print(json.dumps(call_wucai(endpoint_arg, params_data), ensure_ascii=False))
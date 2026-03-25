import os
import requests
import json
import sys


def read_clipped_content(url):
    """
    抓取并返回五彩剪藏文章的 Markdown 原文
    """
    if not url:
        return {"code": -1, "message": "Missing clipping URL."}

    # 模拟浏览器 Header，防止被反爬虫拦截
    headers = {
        "User-Agent": "WuCai-OpenClaw-Reader/1.0 (Mozilla/5.0)",
        "Accept": "text/markdown, text/plain, text/html"
    }

    try:
        # 设置 20s 超时，因为长文章下载和渲染可能较慢
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code == 200:
            # 获取原文内容
            content = response.text

            # 简单的内容长度截断（防止超过 AI 上下文限制，建议保留前 10000 字）
            max_chars = 10000
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n...(Content truncated for brevity)..."

            return {
                "code": 1,
                "data": {
                    "content": content,
                    "url": url,
                    "length": len(content)
                },
                "message": "Success"
            }
        else:
            return {
                "code": response.status_code,
                "message": f"Failed to fetch content. HTTP Status: {response.status_code}"
            }

    except requests.exceptions.Timeout:
        return {"code": -1, "message": "Read content timeout (20s)."}
    except Exception as e:
        return {"code": -1, "message": f"Reader Error: {str(e)}"}


if __name__ == "__main__":
    """
    CLI 入口：echo '{"url": "..."}' | python read_clipped.py
    """
    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            params = json.loads(input_data) if input_data else {}
        else:
            params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}

        target_url = params.get('url') or params.get('clipp_url')
        print(json.dumps(read_clipped_content(target_url), ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"code": -1, "message": f"Invalid Input: {str(e)}"}))

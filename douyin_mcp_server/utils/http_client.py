"""HTTP客户端工具"""

import requests
from typing import Optional, Dict, Any

# 请求头，模拟移动端访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
}


def make_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, 
                 **kwargs) -> requests.Response:
    """
    发送HTTP请求
    
    参数:
    - url: 请求URL
    - method: 请求方法，默认GET
    - headers: 自定义请求头，默认使用移动端HEADERS
    - **kwargs: 其他requests参数
    
    返回:
    - Response对象
    """
    if headers is None:
        headers = HEADERS.copy()
    else:
        headers = {**HEADERS, **headers}
    
    return requests.request(method, url, headers=headers, **kwargs)

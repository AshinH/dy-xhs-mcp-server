#!/usr/bin/env python3
"""
下载小红书无水印视频
"""

import requests
import sys
from pathlib import Path

# 视频链接
video_url = "http://sns-video-hs.xhscdn.com/stream/1/110/114/01e9455a5363b85d010370019b36f0a286_114.mp4"

# 保存文件名
filename = "年入300万_数字游民在苏州.mp4"

print(f"📥 开始下载视频...")
print(f"📎 链接: {video_url}")
print(f"💾 保存为: {filename}")
print()

try:
    # 下载视频
    response = requests.get(video_url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r下载进度: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
    
    print()
    print(f"✅ 下载完成!")
    print(f"📁 文件保存位置: {Path(filename).absolute()}")
    print(f"📊 文件大小: {downloaded / 1024 / 1024:.2f} MB")
    
except Exception as e:
    print(f"❌ 下载失败: {e}")
    sys.exit(1)
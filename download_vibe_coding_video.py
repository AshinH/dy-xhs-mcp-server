#!/usr/bin/env python3
"""
下载 Vibe Coding 小红书视频
"""

import requests
import sys
from pathlib import Path

# Vibe Coding 视频链接
video_url = "http://sns-video-bd.xhscdn.com/stream/79/110/259/01e9511b51605f48010370039b64d5261e_259.mp4"

# 保存文件名
filename = "什么是Vibe_Coding以及怎么使用.mp4"

print("🎬 开始下载 Vibe Coding 视频..."    print(f"📎 链接: {video_url}")
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
                    print(".1f"                    print()

    print("✅ 下载完成!"    print(f"📁 文件保存位置: {Path(filename).absolute()}")
    print(".2f"
    print("
🎉 Vibe Coding 视频下载成功！"    print("📝 视频主题: 什么是Vibe Coding，以及怎么使用？"    print("🏷️  相关标签: 人工智能、大模型、vibecoding、深度学习、AI工具"

except Exception as e:
    print(f"❌ 下载失败: {e}")
    sys.exit(1)
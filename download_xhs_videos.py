#!/usr/bin/env python3
"""
批量下载小红书视频
"""

import requests
import sys
import time
from pathlib import Path

# 视频信息
videos = [
    {
        "title": "什么是Vibe Coding，以及怎么使用",
        "url": "http://sns-video-bd.xhscdn.com/stream/79/110/259/01e9511b51605f48010370039b64d5261e_259.mp4",
        "filename": "什么是Vibe_Coding以及怎么使用.mp4"
    },
    {
        "title": "年入300万，数字游民在苏州能过什么生活",
        "url": "http://sns-video-bd.xhscdn.com/stream/1/110/259/01e9455a5363b85d010370039b36eb7afb_259.mp4",
        "filename": "年入300万_数字游民在苏州.mp4"
    }
]

def download_video(video_info):
    """下载单个视频"""
    url = video_info["url"]
    filename = video_info["filename"]
    title = video_info["title"]

    print(f"🎬 开始下载: {title}")
    print(f"📎 链接: {url}")
    print(f"💾 文件名: {filename}")
    print()

    try:
        # 发送请求
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        # 下载文件
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # 显示进度
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(".1f", end='', flush=True)

        print()  # 换行
        print("✅ 下载完成!")
        print(f"📁 保存位置: {Path(filename).absolute()}")
        print(f"📏 文件大小: {downloaded / 1024 / 1024:.2f} MB")
        print(f"📝 视频主题: {title}")
        print()

    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print()
        return False

    return True

def main():
    """主函数"""
    print("🎥 小红书视频批量下载器")
    print("=" * 60)
    print(f"📋 共找到 {len(videos)} 个视频")
    print()

    success_count = 0

    for i, video in enumerate(videos, 1):
        print(f"📥 下载视频 {i}/{len(videos)}")
        print("-" * 40)

        if download_video(video):
            success_count += 1
        else:
            print(f"⚠️  视频 {i} 下载失败")
            print()

        # 短暂延迟，避免请求过于频繁
        if i < len(videos):
            print("⏳ 准备下载下一个视频...")
            time.sleep(2)

    print("🎯 下载总结")
    print("=" * 60)
    print(f"✅ 成功下载: {success_count}/{len(videos)} 个视频")
    print(f"❌ 下载失败: {len(videos) - success_count} 个视频")
    print()
    print("📂 文件保存位置:")
    for video in videos:
        filepath = Path(video["filename"])
        if filepath.exists():
            print(f"   ✅ {video['filename']} ({filepath.absolute()})")
        else:
            print(f"   ❌ {video['filename']} (下载失败)")

    print()
    print("🎉 所有视频下载完成!")

if __name__ == '__main__':
    main()
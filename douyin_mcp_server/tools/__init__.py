"""MCP工具函数模块"""

from .douyin_tools import (
    get_douyin_download_link,
    extract_douyin_text,
    parse_douyin_video_info,
)
from .xiaohongshu_tools import (
    get_xiaohongshu_content,
    extract_xiaohongshu_text,
    extract_xiaohongshu_video_text,
    remove_xiaohongshu_video_watermark,
    get_xiaohongshu_images,
)

__all__ = [
    "get_douyin_download_link",
    "extract_douyin_text",
    "parse_douyin_video_info",
    "get_xiaohongshu_content",
    "extract_xiaohongshu_text",
    "extract_xiaohongshu_video_text",
    "remove_xiaohongshu_video_watermark",
    "get_xiaohongshu_images",
]

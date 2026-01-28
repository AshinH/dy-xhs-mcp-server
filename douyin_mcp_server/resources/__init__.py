"""MCP资源处理模块"""

from .douyin_resources import get_video_info
from .xiaohongshu_resources import get_xiaohongshu_note_info

__all__ = ["get_video_info", "get_xiaohongshu_note_info"]

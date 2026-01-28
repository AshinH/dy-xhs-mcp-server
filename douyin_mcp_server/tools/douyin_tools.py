"""抖音相关MCP工具"""

import json
import tempfile
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import Context

from ..services.douyin_service import DouyinService


def get_douyin_download_link(share_link: str) -> str:
    """
    获取抖音视频的无水印下载链接

    参数:
    - share_link: 抖音分享链接或包含链接的文本

    返回:
    - 包含下载链接和视频信息的JSON字符串
    """
    try:
        # 获取下载链接不需要API密钥，直接创建服务实例
        service = DouyinService.__new__(DouyinService)
        service.temp_dir = Path(tempfile.mkdtemp())
        video_info = service.parse_share_url(share_link)
        
        return json.dumps({
            "status": "success",
            "video_id": video_info["video_id"],
            "title": video_info["title"],
            "download_url": video_info["url"],
            "description": f"视频标题: {video_info['title']}",
            "usage_tip": "可以直接使用此链接下载无水印视频"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": f"获取下载链接失败: {str(e)}"
        }, ensure_ascii=False, indent=2)


async def extract_douyin_text(
    share_link: str,
    model: Optional[str] = None,
    ctx: Optional[Context] = None
) -> str:
    """
    从抖音分享链接提取视频中的文本内容

    参数:
    - share_link: 抖音分享链接或包含链接的文本
    - model: 语音识别模型（可选，默认使用paraformer-v2）
    - ctx: MCP上下文（可选）

    返回:
    - 提取的文本内容

    注意: 需要在config.json中配置API密钥
    """
    try:
        service = DouyinService(model=model)
        
        # 解析视频链接
        if ctx:
            ctx.info("正在解析抖音分享链接...")
        video_info = service.parse_share_url(share_link)

        # 直接使用视频URL进行文本提取
        if ctx:
            ctx.info("正在从视频中提取文本...")
        text_content = service.extract_text_from_video_url(video_info['url'])

        if ctx:
            ctx.info("文本提取完成!")
        return text_content

    except Exception as e:
        if ctx:
            ctx.error(f"处理过程中出现错误: {str(e)}")
        raise Exception(f"提取抖音视频文本失败: {str(e)}")


def parse_douyin_video_info(share_link: str) -> str:
    """
    解析抖音分享链接，获取视频基本信息

    参数:
    - share_link: 抖音分享链接或包含链接的文本

    返回:
    - 视频信息（JSON格式字符串）
    """
    try:
        # 解析视频信息不需要API密钥，直接创建服务实例
        service = DouyinService.__new__(DouyinService)
        service.temp_dir = Path(tempfile.mkdtemp())
        video_info = service.parse_share_url(share_link)
        
        return json.dumps({
            "video_id": video_info["video_id"],
            "title": video_info["title"],
            "download_url": video_info["url"],
            "status": "success"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        }, ensure_ascii=False, indent=2)

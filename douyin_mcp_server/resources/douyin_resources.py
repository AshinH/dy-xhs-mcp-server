"""抖音相关MCP资源"""

import json
import tempfile
from pathlib import Path

from ..services.douyin_service import DouyinService


def get_video_info(video_id: str) -> str:
    """
    获取指定视频ID的详细信息

    参数:
    - video_id: 抖音视频ID

    返回:
    - 视频详细信息
    """
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
    try:
        service = DouyinService.__new__(DouyinService)
        service.temp_dir = Path(tempfile.mkdtemp())
        video_info = service.parse_share_url(share_url)
        return json.dumps(video_info, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"获取视频信息失败: {str(e)}"

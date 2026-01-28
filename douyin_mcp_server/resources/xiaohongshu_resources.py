"""小红书相关MCP资源"""

import json

from ..services.xiaohongshu_service import XiaohongshuService


def get_xiaohongshu_note_info(note_id: str) -> str:
    """
    获取指定笔记ID的详细信息

    参数:
    - note_id: 小红书笔记ID

    返回:
    - 笔记详细信息
    """
    share_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    try:
        service = XiaohongshuService()
        note_info = service.parse_share_url(share_url)
        return json.dumps(note_info, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"获取笔记信息失败: {str(e)}"

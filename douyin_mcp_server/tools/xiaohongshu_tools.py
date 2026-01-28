"""小红书相关MCP工具"""

import json
from typing import Optional
from mcp.server.fastmcp import Context

from ..services.xiaohongshu_service import XiaohongshuService


def get_xiaohongshu_content(share_link: str) -> str:
    """
    获取小红书笔记的完整内容（视频/图文）

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 包含视频链接、文案、图片等完整信息的JSON字符串
    """
    try:
        service = XiaohongshuService()
        note_info = service.parse_share_url(share_link)
        
        return json.dumps({
            "status": "success",
            "note_id": note_info.get("note_id", ""),
            "title": note_info.get("title", ""),
            "description": note_info.get("desc", ""),
            "type": note_info.get("type", "unknown"),
            "video_url": note_info.get("video_url", ""),
            "images": note_info.get("images", []),
            "images_no_watermark": note_info.get("images", []),
            "author": note_info.get("author", {}),
            "tags": note_info.get("tags", []),
            "metrics": note_info.get("metrics", {}),
            "usage_tip": "images数组已去除水印参数，可以直接下载无水印图片"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": f"获取小红书内容失败: {str(e)}"
        }, ensure_ascii=False, indent=2)


def extract_xiaohongshu_text(share_link: str) -> str:
    """
    提取小红书笔记的文案内容

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 笔记的文案内容（纯文本）
    """
    try:
        service = XiaohongshuService()
        note_info = service.parse_share_url(share_link)
        
        # 组合标题和描述
        text_content = ""
        if note_info.get("title"):
            text_content += f"标题: {note_info['title']}\n\n"
        if note_info.get("desc"):
            text_content += note_info['desc']
        
        # 如果有标签，也加上
        if note_info.get("tags"):
            text_content += f"\n\n标签: {', '.join(note_info['tags'])}"
        
        return text_content if text_content else "未找到文案内容"
        
    except Exception as e:
        return f"提取小红书文案失败: {str(e)}"


async def extract_xiaohongshu_video_text(
    share_link: str,
    model: Optional[str] = None,
    ctx: Optional[Context] = None
) -> str:
    """
    从小红书视频笔记中提取语音文本内容

    参数:
    - share_link: 小红书分享链接或包含链接的文本
    - model: 语音识别模型（可选，默认使用paraformer-v2）
    - ctx: MCP上下文（可选）

    返回:
    - 提取的文本内容

    注意: 需要在config.json中配置API密钥
    """
    try:
        service = XiaohongshuService()
        
        # 解析笔记信息
        if ctx:
            ctx.info("正在解析小红书分享链接...")
        note_info = service.parse_share_url(share_link)
        
        # 检查是否有视频
        video_url = note_info.get("video_url")
        if not video_url:
            return "该笔记不是视频类型，无法提取语音内容"
        
        # 提取视频文本
        if ctx:
            ctx.info("正在从视频中提取文本...")
        text_content = service.extract_text_from_video_url(video_url)
        
        # 如果有文案，也加上
        desc = note_info.get("desc", "")
        if desc:
            text_content = f"文案内容: {desc}\n\n语音内容: {text_content}"
        
        if ctx:
            ctx.info("文本提取完成!")
        return text_content
        
    except Exception as e:
        if ctx:
            ctx.error(f"处理过程中出现错误: {str(e)}")
        raise Exception(f"提取小红书视频文本失败: {str(e)}")


def remove_xiaohongshu_video_watermark(share_link: str, output_path: Optional[str] = None) -> str:
    """
    使用AI技术移除小红书视频水印

    参数:
    - share_link: 小红书分享链接或包含链接的文本
    - output_path: 输出文件路径（可选，默认保存到temp目录）

    返回:
    - 处理结果的JSON字符串，包含无水印视频路径等信息

    注意: 需要安装OpenCV (opencv-python) 才能使用完整功能
    """
    try:
        service = XiaohongshuService()

        # 首先获取视频URL
        content_result = service.parse_share_url(share_link)
        video_url = content_result.get('video_url', '')

        if not video_url:
            return json.dumps({
                'status': 'error',
                'error': '未找到视频URL，无法进行水印移除'
            }, ensure_ascii=False, indent=2)

        print(f"🎬 开始处理视频水印移除...")
        print(f"📎 视频链接: {video_url}")

        # 使用AI移除水印
        result = service.remove_watermark_with_ai(video_url, output_path)

        if result['success']:
            return json.dumps({
                'status': 'success',
                'message': 'AI水印移除成功',
                'video_url': video_url,
                'output_path': result['output_path'],
                'method': result.get('method', 'AI处理'),
                'confidence': result.get('confidence', 0.0),
                'file_size': result.get('processed_size', 0),
                'frames_processed': result.get('frames_processed', 0),
                'watermark_detected': result.get('watermark_detected', False),
                'usage_tip': '处理后的无水印视频已保存，可以直接使用'
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                'status': 'error',
                'error': result.get('error', '水印移除失败'),
                'video_url': video_url,
                'suggestion': '建议使用专业的视频编辑软件手动移除水印'
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            'status': 'error',
            'error': f'AI水印移除处理异常: {str(e)}'
        }, ensure_ascii=False, indent=2)


def get_xiaohongshu_images(share_link: str) -> str:
    """
    获取小红书笔记中的所有图片链接

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 图片链接列表（JSON格式）
    """
    try:
        service = XiaohongshuService()
        note_info = service.parse_share_url(share_link)
        
        images = note_info.get("images", [])
        
        return json.dumps({
            "status": "success",
            "note_id": note_info.get("note_id", ""),
            "title": note_info.get("title", ""),
            "image_count": len(images),
            "images": images,
            "usage_tip": "图片链接已去除水印参数，可以直接下载无水印图片"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": f"获取图片失败: {str(e)}"
        }, ensure_ascii=False, indent=2)

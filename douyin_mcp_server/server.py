#!/usr/bin/env python3
"""
抖音和小红书内容提取 MCP 服务器

该服务器提供以下功能：
1. 抖音：解析分享链接获取无水印视频链接、提取文本内容
2. 小红书：解析分享链接获取视频/图文内容、提取文案和文章
3. 自动清理中间文件
"""

from mcp.server.fastmcp import FastMCP

# 导入工具和资源
from .tools import douyin_tools
from .tools import xiaohongshu_tools
from .resources import douyin_resources
from .resources import xiaohongshu_resources

# 创建 MCP 服务器实例
mcp = FastMCP(
    "Social Media Content Extractor MCP Server",
    dependencies=["requests", "ffmpeg-python", "tqdm", "dashscope", "beautifulsoup4"]
)

# ==================== 注册抖音工具 ====================

@mcp.tool()
def get_douyin_download_link(share_link: str) -> str:
    """
    获取抖音视频的无水印下载链接

    参数:
    - share_link: 抖音分享链接或包含链接的文本

    返回:
    - 包含下载链接和视频信息的JSON字符串
    """
    return douyin_tools.get_douyin_download_link(share_link)


@mcp.tool()
async def extract_douyin_text(
    share_link: str,
    model: str = None,
    ctx=None
) -> str:
    """
    从抖音分享链接提取视频中的文本内容

    参数:
    - share_link: 抖音分享链接或包含链接的文本
    - model: 语音识别模型（可选，默认使用paraformer-v2）

    返回:
    - 提取的文本内容

    注意: 需要在config.json中配置API密钥
    """
    return await douyin_tools.extract_douyin_text(share_link, model, ctx)


@mcp.tool()
def parse_douyin_video_info(share_link: str) -> str:
    """
    解析抖音分享链接，获取视频基本信息

    参数:
    - share_link: 抖音分享链接或包含链接的文本

    返回:
    - 视频信息（JSON格式字符串）
    """
    return douyin_tools.parse_douyin_video_info(share_link)


# ==================== 注册小红书工具 ====================

@mcp.tool()
def get_xiaohongshu_content(share_link: str) -> str:
    """
    获取小红书笔记的完整内容（视频/图文）

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 包含视频链接、文案、图片等完整信息的JSON字符串
    """
    return xiaohongshu_tools.get_xiaohongshu_content(share_link)


@mcp.tool()
def extract_xiaohongshu_text(share_link: str) -> str:
    """
    提取小红书笔记的文案内容

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 笔记的文案内容（纯文本）
    """
    return xiaohongshu_tools.extract_xiaohongshu_text(share_link)


@mcp.tool()
async def extract_xiaohongshu_video_text(
    share_link: str,
    model: str = None,
    ctx=None
) -> str:
    """
    从小红书视频笔记中提取语音文本内容

    参数:
    - share_link: 小红书分享链接或包含链接的文本
    - model: 语音识别模型（可选，默认使用paraformer-v2）

    返回:
    - 提取的文本内容

    注意: 需要在config.json中配置API密钥
    """
    return await xiaohongshu_tools.extract_xiaohongshu_video_text(share_link, model, ctx)


@mcp.tool()
def remove_xiaohongshu_video_watermark(
    share_link: str,
    output_path: str = None
) -> str:
    """
    使用AI技术移除小红书视频水印

    参数:
    - share_link: 小红书分享链接或包含链接的文本
    - output_path: 输出文件路径（可选，默认保存到temp目录）

    返回:
    - 处理结果的JSON字符串，包含无水印视频路径等信息

    注意: 需要安装OpenCV (opencv-python) 才能使用完整功能
    """
    return xiaohongshu_tools.remove_xiaohongshu_video_watermark(share_link, output_path)


@mcp.tool()
def get_xiaohongshu_images(share_link: str) -> str:
    """
    获取小红书笔记中的所有图片链接

    参数:
    - share_link: 小红书分享链接或包含链接的文本

    返回:
    - 图片链接列表（JSON格式）
    """
    return xiaohongshu_tools.get_xiaohongshu_images(share_link)


# ==================== 注册资源 ====================

@mcp.resource("douyin://video/{video_id}")
def get_video_info(video_id: str) -> str:
    """
    获取指定视频ID的详细信息

    参数:
    - video_id: 抖音视频ID

    返回:
    - 视频详细信息
    """
    return douyin_resources.get_video_info(video_id)


@mcp.resource("xiaohongshu://note/{note_id}")
def get_xiaohongshu_note_info(note_id: str) -> str:
    """
    获取指定笔记ID的详细信息

    参数:
    - note_id: 小红书笔记ID

    返回:
    - 笔记详细信息
    """
    return xiaohongshu_resources.get_xiaohongshu_note_info(note_id)


# ==================== 注册提示 ====================

@mcp.prompt()
def douyin_text_extraction_guide() -> str:
    """抖音视频文本提取使用指南"""
    return """
# 抖音视频文本提取使用指南

## 功能说明
这个MCP服务器可以从抖音分享链接中提取视频的文本内容，以及获取无水印下载链接。

## 环境变量配置
请确保设置了以下环境变量：
- `DASHSCOPE_API_KEY`: 阿里云百炼API密钥

## 使用步骤
1. 复制抖音视频的分享链接
2. 在Claude Desktop配置中设置环境变量 DASHSCOPE_API_KEY
3. 使用相应的工具进行操作

## 工具说明
- `extract_douyin_text`: 完整的文本提取流程（需要API密钥）
- `get_douyin_download_link`: 获取无水印视频下载链接（无需API密钥）
- `parse_douyin_video_info`: 仅解析视频基本信息
- `douyin://video/{video_id}`: 获取指定视频的详细信息

## Claude Desktop 配置示例
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": ["douyin-mcp-server"],
      "env": {
        "DASHSCOPE_API_KEY": "your-dashscope-api-key-here"
      }
    }
  }
}
```

## 注意事项
- 需要提供有效的阿里云百炼API密钥（通过环境变量）
- 使用阿里云百炼的paraformer-v2模型进行语音识别
- 支持大部分抖音视频格式
- 获取下载链接无需API密钥
"""


def main():
    """启动MCP服务器"""
    mcp.run()


if __name__ == "__main__":
    main()

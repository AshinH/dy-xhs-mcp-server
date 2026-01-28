"""抖音服务"""

import re
import json
import tempfile
import requests
from pathlib import Path
from typing import Optional, Dict
from urllib import request
from http import HTTPStatus
import dashscope
import ffmpeg

from ..config import CONFIG, DEFAULT_MODEL
from ..utils.http_client import HEADERS


class DouyinService:
    """抖音视频服务"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """初始化抖音服务"""
        if api_key is None:
            api_key = CONFIG.get("api_key", "")

        if not api_key:
            raise ValueError("未设置API密钥，请在config.json中配置或传入api_key参数")

        self.api_key = api_key
        self.model = model or CONFIG.get("model", DEFAULT_MODEL)
        self.temp_dir = Path(tempfile.mkdtemp())
        # 设置阿里云百炼API密钥
        dashscope.api_key = api_key
    
    def __del__(self):
        """清理临时目录"""
        import shutil
        if hasattr(self, 'temp_dir') and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def parse_share_url(self, share_text: str) -> dict:
        """从分享文本中提取无水印视频链接"""
        # 提取分享链接
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', share_text)
        if not urls:
            raise ValueError("未找到有效的分享链接")
        
        share_url = urls[0]
        share_response = requests.get(share_url, headers=HEADERS)
        video_id = share_response.url.split("?")[0].strip("/").split("/")[-1]
        share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
        
        # 获取视频页面内容
        response = requests.get(share_url, headers=HEADERS)
        response.raise_for_status()
        
        pattern = re.compile(
            pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
            flags=re.DOTALL,
        )
        find_res = pattern.search(response.text)

        if not find_res or not find_res.group(1):
            raise ValueError("从HTML中解析视频信息失败")

        # 解析JSON数据
        json_data = json.loads(find_res.group(1).strip())
        VIDEO_ID_PAGE_KEY = "video_(id)/page"
        NOTE_ID_PAGE_KEY = "note_(id)/page"
        
        if VIDEO_ID_PAGE_KEY in json_data["loaderData"]:
            original_video_info = json_data["loaderData"][VIDEO_ID_PAGE_KEY]["videoInfoRes"]
        elif NOTE_ID_PAGE_KEY in json_data["loaderData"]:
            original_video_info = json_data["loaderData"][NOTE_ID_PAGE_KEY]["videoInfoRes"]
        else:
            raise Exception("无法从JSON中解析视频或图集信息")

        data = original_video_info["item_list"][0]

        # 获取视频信息
        video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
        desc = data.get("desc", "").strip() or f"douyin_{video_id}"
        
        # 替换文件名中的非法字符
        desc = re.sub(r'[\\/:*?"<>|]', '_', desc)
        
        return {
            "url": video_url,
            "title": desc,
            "video_id": video_id
        }
    
    async def download_video(self, video_info: dict, ctx) -> Path:
        """异步下载视频到临时目录"""
        from mcp.server.fastmcp import Context
        
        filename = f"{video_info['video_id']}.mp4"
        filepath = self.temp_dir / filename
        
        if ctx:
            ctx.info(f"正在下载视频: {video_info['title']}")
        
        response = requests.get(video_info['url'], headers=HEADERS, stream=True)
        response.raise_for_status()
        
        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        
        # 异步下载文件，显示进度
        with open(filepath, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and ctx:
                        await ctx.report_progress(downloaded, total_size)
        
        if ctx:
            ctx.info(f"视频下载完成: {filepath}")
        return filepath
    
    def extract_audio(self, video_path: Path) -> Path:
        """从视频文件中提取音频"""
        audio_path = video_path.with_suffix('.mp3')
        
        try:
            (
                ffmpeg
                .input(str(video_path))
                .output(str(audio_path), acodec='libmp3lame', q=0)
                .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            )
            return audio_path
        except Exception as e:
            raise Exception(f"提取音频时出错: {str(e)}")
    
    def extract_text_from_video_url(self, video_url: str) -> str:
        """从视频URL中提取文字（使用阿里云百炼API）"""
        try:
            # 发起异步转录任务
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=self.model,
                file_urls=[video_url],
                language_hints=['zh', 'en']
            )
            
            # 等待转录完成
            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )
            
            if transcription_response.status_code == HTTPStatus.OK:
                # 获取转录结果
                for transcription in transcription_response.output['results']:
                    if 'transcription_url' in transcription:
                        url = transcription['transcription_url']
                        result = json.loads(request.urlopen(url).read().decode('utf8'))

                        # 保存结果到临时文件
                        temp_json_path = self.temp_dir / 'transcription.json'
                        with open(temp_json_path, 'w') as f:
                            json.dump(result, f, indent=4, ensure_ascii=False)

                        # 提取文本内容
                        if 'transcripts' in result and len(result['transcripts']) > 0:
                            return result['transcripts'][0]['text']
                        else:
                            return "未识别到文本内容"
                    else:
                        # 检查是否有错误信息
                        if transcription.get('code') == 'SUCCESS_WITH_NO_VALID_FRAGMENT':
                            return "视频中未检测到有效的音频内容，可能原因：视频过短、无音频、格式不支持"
                        elif transcription.get('subtask_status') == 'FAILED':
                            return f"语音识别失败: {transcription.get('message', '未知错误')}"
                        else:
                            return f"API响应异常: {transcription}"

            else:
                raise Exception(f"转录失败: {transcription_response.output.message}")
                
        except Exception as e:
            raise Exception(f"提取文字时出错: {str(e)}")
    
    def cleanup_files(self, *file_paths: Path):
        """清理指定的文件"""
        for file_path in file_paths:
            if file_path.exists():
                file_path.unlink()

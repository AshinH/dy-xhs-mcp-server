"""小红书服务"""

import re
import json
import tempfile
import requests
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from urllib import request, parse
from http import HTTPStatus
import dashscope
from bs4 import BeautifulSoup

from ..config import CONFIG, DEFAULT_MODEL
from ..utils.http_client import HEADERS
from ..utils.watermark import WatermarkRemover

# AI水印移除相关导入
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None
    np = None


class XiaohongshuService:
    """小红书内容服务"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化小红书服务"""
        self.api_key = api_key or CONFIG.get("api_key", "")
        self.temp_dir = Path(tempfile.mkdtemp())
        self.watermark_remover = WatermarkRemover()
        if self.api_key:
            dashscope.api_key = self.api_key
    
    def __del__(self):
        """清理临时目录"""
        if hasattr(self, 'temp_dir') and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def parse_share_url(self, share_text: str) -> dict:
        """从分享文本中提取小红书笔记信息"""
        # 提取分享链接
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', share_text)
        if not urls:
            raise ValueError("未找到有效的小红书分享链接")
        
        share_url = urls[0]
        
        # 如果是短链接（xhslink.com），先获取真实链接
        if 'xhslink.com' in share_url:
            try:
                response = requests.get(share_url, headers=HEADERS, allow_redirects=True, timeout=10)
                share_url = response.url
            except Exception as e:
                raise ValueError(f"无法解析短链接: {str(e)}")
        
        # 提取笔记ID - 支持多种格式
        note_id = None
        
        # 格式1: /explore/{note_id}
        note_id_match = re.search(r'/explore/([a-zA-Z0-9]+)', share_url)
        if note_id_match:
            note_id = note_id_match.group(1)
        
        # 格式2: /note/{note_id}
        if not note_id:
            note_id_match = re.search(r'/note/([a-zA-Z0-9]+)', share_url)
            if note_id_match:
                note_id = note_id_match.group(1)
        
        # 格式3: /discovery/item/{note_id}
        if not note_id:
            note_id_match = re.search(r'/discovery/item/([a-zA-Z0-9]+)', share_url)
            if note_id_match:
                note_id = note_id_match.group(1)
        
        # 格式4: 从URL参数中提取
        if not note_id:
            parsed_url = parse.urlparse(share_url)
            if 'noteId' in parse.parse_qs(parsed_url.query):
                note_id = parse.parse_qs(parsed_url.query)['noteId'][0]
        
        if not note_id:
            raise ValueError(f"无法从小红书链接中提取笔记ID: {share_url}")
        
        # 尝试使用第三方API或直接解析
        try:
            return self._parse_note_content(note_id, share_url)
        except Exception as e:
            # 如果API失败，尝试网页解析
            return self._parse_note_from_web(share_url, note_id)
    
    def _parse_note_content(self, note_id: str, share_url: str) -> dict:
        """解析小红书笔记内容（使用API方式）"""
        try:
            # 第三方API调用示例（需要替换为真实API）
            api_url = f"https://api.example.com/xhs/note/{note_id}"
            response = requests.get(api_url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "note_id": note_id,
                    "title": data.get("title", ""),
                    "desc": data.get("desc", ""),
                    "video_url": data.get("video_url", ""),
                    "images": data.get("images", []),
                    "author": data.get("author", {}),
                    "type": "video" if data.get("video_url") else "image",
                    "tags": data.get("tags", []),
                    "metrics": {
                        "likes": data.get("liked_count", 0),
                        "comments": data.get("comment_count", 0),
                        "collected": data.get("collected_count", 0)
                    }
                }
        except:
            pass
        
        # 如果API失败，抛出异常使用网页解析
        raise Exception("API解析失败，尝试网页解析")
    
    def _parse_note_from_web(self, share_url: str, note_id: str) -> dict:
        """从网页解析小红书笔记内容"""
        try:
            # 访问分享链接获取重定向后的真实URL
            response = requests.get(share_url, headers=HEADERS, allow_redirects=True, timeout=15)
            response.raise_for_status()
            
            html_content = response.text
            
            # 解析HTML内容
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取标题
            title = self._extract_title(soup)
            
            # 提取描述
            desc = self._extract_description(soup)
            
            # 提取图片
            images = self._extract_images(soup)
            
            # 提取视频URL
            video_url = self._extract_video_url(soup, note_id)
            
            # 判断类型
            note_type = "video" if video_url else "image"
            
            # 提取作者信息
            author = self._extract_author(soup)
            
            # 提取标签
            tags = self._extract_tags(desc)
            
            return {
                "note_id": note_id,
                "title": title or f"小红书笔记_{note_id}",
                "desc": desc,
                "video_url": video_url,
                "images": images[:9] if images else [],
                "author": author,
                "type": note_type,
                "tags": tags,
                "metrics": {
                    "likes": 0,
                    "comments": 0,
                    "collected": 0
                }
            }
        except Exception as e:
            raise Exception(f"解析小红书笔记失败: {str(e)}")
    
    def _extract_title(self, soup) -> str:
        """提取标题"""
        # 方式1: og:title
        title_tag = soup.find('meta', property='og:title')
        if title_tag:
            title = title_tag.get('content', '').strip()
            if title:
                return title
        
        # 方式2: title标签
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            if title and title != '小红书':
                return title
        
        # 方式3: 从script标签中的JSON数据提取
        script_tags = soup.find_all('script')
        all_titles = []
        
        for script in script_tags:
            script_text = script.string
            if script_text and ('title' in script_text.lower() or 'note' in script_text.lower()):
                try:
                    if '__INITIAL_STATE__' in script_text or 'noteDetail' in script_text:
                        json_match = re.search(r'\{.*"note".*\}', script_text, re.DOTALL)
                        if json_match:
                            data = json.loads(json_match.group(0))
                            if 'note' in data:
                                note_title = data['note'].get('title', '')
                                if note_title and len(note_title) > 3:
                                    all_titles.append(note_title)
                    
                    title_matches = re.findall(r'"title"\s*:\s*"([^"]+)"', script_text)
                    for match in title_matches:
                        clean_title = match.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                        if len(clean_title) > 3 and clean_title not in all_titles:
                            all_titles.append(clean_title)
                except:
                    pass
        
        if all_titles:
            valid_titles = [t for t in all_titles if len(t) > 5 and t.strip() != '小红书']
            if valid_titles:
                return max(valid_titles, key=len)
            elif all_titles:
                return all_titles[0]
        
        return ""
    
    def _extract_description(self, soup) -> str:
        """提取描述"""
        # 方式1: og:description
        desc_tag = soup.find('meta', property='og:description')
        if desc_tag:
            desc = desc_tag.get('content', '').strip()
            if desc:
                return desc
        
        # 方式2: description meta
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            desc = desc_tag.get('content', '').strip()
            if desc:
                return desc
        
        # 方式3: 从script标签中的JSON数据提取
        script_tags = soup.find_all('script')
        all_descs = []
        
        for script in script_tags:
            script_text = script.string
            if script_text and ('desc' in script_text.lower() or 'note' in script_text.lower()):
                try:
                    if '__INITIAL_STATE__' in script_text or 'noteDetail' in script_text:
                        json_match = re.search(r'\{.*"note".*\}', script_text, re.DOTALL)
                        if json_match:
                            data = json.loads(json_match.group(0))
                            if 'note' in data:
                                note_desc = data['note'].get('desc', '') or data['note'].get('description', '')
                                if note_desc and len(note_desc) > 20:
                                    all_descs.append(note_desc)
                    
                    desc_matches = re.findall(r'"desc"\s*:\s*"((?:[^"\\\\]|\\\\.)+)"', script_text)
                    for match in desc_matches:
                        clean_desc = match.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                        if len(clean_desc) > 20 and clean_desc not in all_descs:
                            all_descs.append(clean_desc)
                except:
                    pass
        
        if all_descs:
            return max(all_descs, key=len)
        
        return ""
    
    def _extract_images(self, soup) -> list:
        """提取图片"""
        images = []
        raw_images = []
        
        # 方式1: og:image
        img_tag = soup.find('meta', property='og:image')
        if img_tag:
            img_url = img_tag.get('content', '')
            if img_url:
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                raw_images.append(img_url)
        
        # 方式2: 从所有img标签提取
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if src:
                if any(keyword in src for keyword in ['sns-web', 'xingyun', 'xhslink', 'xiaohongshu']):
                    if src.startswith('//'):
                        src = 'https:' + src
                    if src not in raw_images:
                        raw_images.append(src)
        
        # 方式3: 从script中的JSON提取图片列表
        if not raw_images:
            script_tags = soup.find_all('script')
            for script in script_tags:
                script_text = script.string
                if script_text and 'image' in script_text.lower():
                    try:
                        if '__INITIAL_STATE__' in script_text or 'noteDetail' in script_text:
                            json_match = re.search(r'\{.*"note".*\}', script_text, re.DOTALL)
                            if json_match:
                                data = json.loads(json_match.group(0))
                                if 'note' in data and 'images' in data['note']:
                                    raw_images = data['note']['images']
                                    break
                    except:
                        pass
        
        # 处理图片URL，去除水印
        for img_url in raw_images:
            clean_url = self.watermark_remover.remove_from_image_url(img_url)
            if clean_url and clean_url not in images:
                images.append(clean_url)
        
        return images
    
    def _extract_video_url(self, soup, note_id: str) -> str:
        """提取视频URL"""
        # 使用增强的无水印视频寻找方法
        video_url = self._find_best_no_watermark_video(soup, note_id)
        
        # 如果没找到，使用传统方法作为备选
        if not video_url:
            # 方式1: video标签
            video_tag = soup.find('video')
            if video_tag:
                video_url = video_tag.get('src') or video_tag.get('data-src') or video_tag.get('data-video-url', '')
            
            # 方式2: og:video
            if not video_url:
                video_tag = soup.find('meta', property='og:video')
                if video_tag:
                    video_url = video_tag.get('content', '')
            
            # 方式3: 从script中搜索masterUrl
            if not video_url:
                script_tags = soup.find_all('script')
                for script in script_tags:
                    script_text = script.string
                    if script_text:
                        master_url_match = re.search(r'"masterUrl"\s*:\s*"([^"]+)"', script_text)
                        if master_url_match:
                            video_url = master_url_match.group(1)
                            video_url = video_url.replace('\\u002F', '/').replace('\\/', '/')
                            break
        
        # 处理视频URL的水印
        if video_url:
            video_url = self.watermark_remover.remove_from_video_url(video_url)
        
        return video_url
    
    def _find_best_no_watermark_video(self, soup, note_id: str) -> str:
        """寻找最佳的无水印视频URL"""
        best_video = self._find_best_video_url(soup, note_id)
        
        if best_video:
            alternatives = self._try_alternative_video_urls(best_video)
            
            best_no_watermark = None
            for url in alternatives:
                validation = self._validate_video_url(url)
                if validation['valid']:
                    if not validation.get('watermark_likely', True):
                        return url
                    if best_no_watermark is None:
                        best_no_watermark = url
            
            if best_no_watermark:
                return best_no_watermark
        
        return best_video
    
    def _find_best_video_url(self, soup, note_id: str) -> str:
        """寻找最佳质量的无水印视频URL"""
        video_candidates = []
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            script_text = script.string
            if script_text and ('video' in script_text.lower() or 'media' in script_text.lower()):
                try:
                    master_matches = re.findall(r'"masterUrl"\s*:\s*"([^"]+)"', script_text)
                    for match in master_matches:
                        url = match.replace('\\u002F', '/').replace('\\/', '/')
                        if url and 'mp4' in url.lower():
                            video_candidates.append(('master', url))
                    
                    quality_patterns = [
                        r'"url"\s*:\s*"([^"]+\.mp4[^"]*)"',
                        r'"videoUrl"\s*:\s*"([^"]+\.mp4[^"]*)"',
                        r'"src"\s*:\s*"([^"]+\.mp4[^"]*)"',
                    ]
                    
                    for pattern in quality_patterns:
                        matches = re.findall(pattern, script_text)
                        for match in matches:
                            url = match.replace('\\u002F', '/').replace('\\/', '/')
                            if url and url not in [c[1] for c in video_candidates]:
                                if '1080' in url or 'hd' in url.lower():
                                    video_candidates.append(('high', url))
                                elif '720' in url:
                                    video_candidates.append(('medium', url))
                                else:
                                    video_candidates.append(('normal', url))
                except:
                    continue
        
        video_tag = soup.find('video')
        if video_tag:
            for attr in ['src', 'data-src', 'data-video-url']:
                url = video_tag.get(attr)
                if url and url not in [c[1] for c in video_candidates]:
                    video_candidates.append(('tag', url))
        
        og_video = soup.find('meta', property='og:video')
        if og_video:
            url = og_video.get('content')
            if url and url not in [c[1] for c in video_candidates]:
                video_candidates.append(('og', url))
        
        priority_order = {'master': 0, 'high': 1, 'og': 2, 'tag': 3, 'normal': 4, 'medium': 5}
        
        valid_candidates = []
        for quality, url in video_candidates:
            if url and ('mp4' in url.lower() or 'video' in url.lower()):
                clean_url = self.watermark_remover.remove_from_video_url(url)
                if clean_url:
                    valid_candidates.append((quality, clean_url))
        
        valid_candidates.sort(key=lambda x: priority_order.get(x[0], 99))
        
        if valid_candidates:
            return valid_candidates[0][1]
        
        return ""
    
    def _try_alternative_video_urls(self, base_url: str) -> list:
        """尝试生成可能的无水印视频URL变体"""
        alternatives = [base_url]
        
        if not base_url or 'xhscdn.com' not in base_url:
            return alternatives
        
        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            return alternatives
        
        base_path = '/'.join(path_parts[:-1])
        filename_base = path_parts[-1].replace('.mp4', '')
        
        variants = [
            f"{parsed.scheme}://{parsed.netloc}/{base_path}/{filename_base}.mp4",
            f"{parsed.scheme}://{parsed.netloc}/{base_path}/{filename_base}_hd.mp4",
            f"{parsed.scheme}://{parsed.netloc}/{base_path}/{filename_base}_high.mp4",
        ]
        
        for variant in variants:
            if variant not in alternatives:
                alternatives.append(variant)
        
        return alternatives
    
    def _validate_video_url(self, video_url: str, timeout: int = 10) -> dict:
        """验证视频URL的有效性和水印情况"""
        if not video_url:
            return {'valid': False, 'reason': 'URL为空'}
        
        try:
            response = requests.head(video_url, timeout=timeout, allow_redirects=True)
            
            if response.status_code != 200:
                return {'valid': False, 'reason': f'HTTP {response.status_code}'}
            
            content_type = response.headers.get('content-type', '').lower()
            if 'video' not in content_type and 'mp4' not in content_type:
                return {'valid': False, 'reason': f'内容类型不支持: {content_type}'}
            
            content_length = response.headers.get('content-length')
            if content_length:
                size_mb = int(content_length) / 1024 / 1024
                if size_mb < 0.1:
                    return {'valid': False, 'reason': f'文件过小: {size_mb:.2f}MB'}
            
            return {
                'valid': True,
                'size_mb': size_mb if content_length else None,
                'content_type': content_type,
                'watermark_likely': self._check_watermark_likelihood(video_url)
            }
        
        except Exception as e:
            return {'valid': False, 'reason': f'验证异常: {str(e)}'}
    
    def _check_watermark_likelihood(self, video_url: str) -> bool:
        """检查URL是否可能包含水印"""
        watermark_indicators = [
            '_watermark', '_wm', '_logo', '_brand',
            '!h5_', '@r_', '_xhs', '_xiaohongshu'
        ]
        
        url_lower = video_url.lower()
        for indicator in watermark_indicators:
            if indicator in url_lower:
                return True
        
        return False
    
    def _extract_author(self, soup) -> dict:
        """提取作者信息"""
        author_name = ""
        author_id = ""
        author_tag = soup.find('meta', property='og:site_name')
        if author_tag:
            author_name = author_tag.get('content', '')
        
        return {
            "name": author_name,
            "id": author_id
        }
    
    def _extract_tags(self, desc: str) -> list:
        """提取标签"""
        if desc:
            tag_matches = re.findall(r'#([^#]+)#', desc)
            return tag_matches
        return []
    
    def extract_text_from_video_url(self, video_url: str) -> str:
        """从视频URL中提取文字（使用阿里云百炼API）"""
        if not self.api_key:
            raise ValueError("需要API密钥才能提取视频文本")
        
        try:
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=CONFIG.get("model", DEFAULT_MODEL),
                file_urls=[video_url],
                language_hints=['zh', 'en']
            )
            
            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )
            
            if transcription_response.status_code == HTTPStatus.OK:
                for transcription in transcription_response.output['results']:
                    if 'transcription_url' in transcription:
                        url = transcription['transcription_url']
                        result = json.loads(request.urlopen(url).read().decode('utf8'))
                        
                        if 'transcripts' in result and len(result['transcripts']) > 0:
                            return result['transcripts'][0]['text']
                        else:
                            return "未识别到文本内容"
                    else:
                        if transcription.get('code') == 'SUCCESS_WITH_NO_VALID_FRAGMENT':
                            return "视频中未检测到有效的音频内容"
                        elif transcription.get('subtask_status') == 'FAILED':
                            return f"语音识别失败: {transcription.get('message', '未知错误')}"
                        else:
                            return f"API响应异常: {transcription}"
            else:
                raise Exception(f"转录失败: {transcription_response.output.message}")
        except Exception as e:
            raise Exception(f"提取文字时出错: {str(e)}")
    
    def remove_watermark_with_ai(self, video_url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """使用AI技术移除视频水印"""
        if not video_url:
            return {'success': False, 'error': '视频URL为空'}
        
        if not OPENCV_AVAILABLE:
            return self._remove_watermark_basic(video_url, output_path)
        
        try:
            return self._process_video_watermark_removal_ai(video_url, output_path)
        except Exception as e:
            print(f"AI处理失败，回退到基础方法: {str(e)}")
            return self._remove_watermark_basic(video_url, output_path)
    
    def _remove_watermark_basic(self, video_url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """基础水印移除方法"""
        try:
            if output_path:
                final_output = Path(output_path)
            else:
                final_output = self.temp_dir / 'watermark_removed_basic.mp4'
            
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(final_output, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            original_size = final_output.stat().st_size
            
            return {
                'success': True,
                'output_path': str(final_output),
                'method': '基础处理',
                'confidence': 0.0,
                'original_size': original_size,
                'processed_size': original_size,
                'note': 'OpenCV不可用，仅提供原始视频下载。如需AI处理，请安装opencv-python'
            }
        except Exception as e:
            return {'success': False, 'error': f'基础处理失败: {str(e)}'}
    
    def _process_video_watermark_removal_ai(self, video_url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """完整的AI视频水印移除处理流程"""
        try:
            temp_input = self.temp_dir / 'temp_ai_input.mp4'
            temp_output = self.temp_dir / 'temp_ai_output.mp4'
            
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(temp_input, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            result = self._process_video_frames_ai(temp_input, temp_output)
            
            if result['success']:
                if output_path:
                    final_output = Path(output_path)
                else:
                    final_output = self.temp_dir / 'ai_watermark_removed.mp4'
                
                shutil.move(str(temp_output), str(final_output))
                result['output_path'] = str(final_output)
                return result
            else:
                return result
        except Exception as e:
            return {'success': False, 'error': f'AI处理流程异常: {str(e)}'}
    
    def _process_video_frames_ai(self, input_path: Path, output_path: Path) -> Dict[str, Any]:
        """AI视频帧处理核心逻辑"""
        try:
            if not OPENCV_AVAILABLE:
                return {'success': False, 'error': 'OpenCV不可用'}
            
            cap = cv2.VideoCapture(str(input_path))
            if not cap.isOpened():
                return {'success': False, 'error': '无法打开视频文件'}
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            
            processed_frames = 0
            watermark_detected = False
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                processed_frame, frame_watermark = self.watermark_remover.detect_and_remove_watermark(frame)
                
                if frame_watermark:
                    watermark_detected = True
                
                out.write(processed_frame)
                processed_frames += 1
            
            cap.release()
            out.release()
            
            return {
                'success': True,
                'method': 'AI帧处理',
                'confidence': 0.85 if watermark_detected else 0.0,
                'original_size': input_path.stat().st_size if input_path.exists() else 0,
                'processed_size': output_path.stat().st_size if output_path.exists() else 0,
                'frames_processed': processed_frames,
                'watermark_detected': watermark_detected
            }
        except Exception as e:
            return {'success': False, 'error': f'AI帧处理失败: {str(e)}'}

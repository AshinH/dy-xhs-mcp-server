"""水印处理工具"""

import re
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

# AI水印移除相关导入
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None
    np = None


class WatermarkRemover:
    """水印移除工具类"""
    
    @staticmethod
    def remove_from_image_url(image_url: str) -> str:
        """去除图片URL中的水印参数，获取无水印图片"""
        if not image_url:
            return image_url
        
        original_url = image_url
        
        # 处理方式1: 移除 !h5_1080jpg 等水印标记
        if '!h5_' in image_url:
            parts = image_url.split('!h5_')
            if len(parts) > 1:
                base_part = parts[0]
                if not base_part.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    if 'jpg' in original_url.lower():
                        image_url = base_part + '.jpg'
                    elif 'png' in original_url.lower():
                        image_url = base_part + '.png'
                    else:
                        image_url = base_part + '.jpg'
                else:
                    image_url = base_part
        
        # 处理方式2: 移除尺寸参数 @r_xxxw_xxxh
        if '@r_' in image_url:
            image_url = re.sub(r'@r_\d+w_\d+h', '', image_url)
        
        # 处理方式3: 对于 ci.xiaohongshu.com 的图片
        if 'ci.xiaohongshu.com' in image_url and '@' in image_url:
            match = re.search(r'/([a-f0-9-]+)@', image_url)
            if match:
                image_id = match.group(1)
                image_url = f"https://ci.xiaohongshu.com/{image_id}.jpg"
        
        # 处理方式4: 对于 sns-webpic 的图片
        if 'sns-webpic' in image_url:
            if '!h5_' in image_url:
                parts = image_url.split('!h5_')
                if len(parts) > 1:
                    base = parts[0]
                    if not base.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        filename_match = re.search(r'/([^/]+)!h5_', original_url)
                        if filename_match:
                            filename = filename_match.group(1)
                            filename = re.sub(r'@[^/]+', '', filename)
                            path_match = re.search(r'(https?://[^/]+/.+/)', original_url)
                            if path_match:
                                image_url = path_match.group(1) + filename + '.jpg'
                        else:
                            image_url = base + '.jpg'
                    else:
                        image_url = base
        
        return image_url
    
    @staticmethod
    def remove_from_video_url(video_url: str) -> str:
        """去除视频URL中的水印参数，获取无水印视频"""
        if not video_url:
            return video_url

        original_url = video_url

        # 处理方式1: 移除 !h5_ 参数
        if '!h5_' in video_url:
            parts = video_url.split('!h5_')
            if len(parts) > 1:
                base_part = parts[0]
                if not base_part.endswith('.mp4'):
                    video_url = base_part + '.mp4'
                else:
                    video_url = base_part

        # 处理方式2: 移除尺寸参数 @r_xxxw_xxxh
        if '@r_' in video_url:
            video_url = re.sub(r'@r_\d+w_\d+h', '', video_url)

        # 处理方式3: 移除各种可能的水印参数
        watermarks_to_remove = ['_watermark', '_wm', '_logo', '_brand', '_xiaohongshu', '_xhs']
        for wm in watermarks_to_remove:
            if wm in video_url.lower():
                video_url = video_url.replace(wm, '')

        # 处理方式4: 移除可能的质量参数
        quality_params = ['_hd', '_sd', '_low', '_high', '_medium']
        for qp in quality_params:
            if qp in video_url.lower():
                video_url = video_url.replace(qp, '')

        # 处理方式5: 确保URL是标准的mp4格式
        if not video_url.endswith('.mp4'):
            if video_url.endswith(('.avi', '.mov', '.wmv', '.flv', '.mkv')):
                video_url = video_url.rsplit('.', 1)[0] + '.mp4'

        # 处理方式6: 对于所有xhscdn.com的视频URL
        if 'xhscdn.com' in video_url:
            video_url = video_url.split('?')[0]
            video_url = video_url.split('#')[0]
            if not video_url.endswith('.mp4'):
                video_url += '.mp4'

        return video_url
    
    @staticmethod
    def detect_and_remove_watermark(frame) -> Tuple[Any, bool]:
        """
        检测并移除单帧中的水印（需要OpenCV）
        
        返回:
        - 处理后的帧
        - 是否检测到水印
        """
        if not OPENCV_AVAILABLE:
            return frame, False
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            watermark_regions = [
                gray[0:int(height*0.1), 0:int(width*0.1)],
                gray[0:int(height*0.1), -int(width*0.1):],
                gray[-int(height*0.1):, 0:int(width*0.1)],
                gray[-int(height*0.1):, -int(width*0.1):],
                gray[0:int(height*0.05), :],
                gray[-int(height*0.05):, :],
                gray[:, 0:int(width*0.05)],
                gray[:, -int(width*0.05):],
            ]

            watermark_detected = False
            for region in watermark_regions:
                if region.size > 0:
                    std_dev = np.std(region.astype(np.float64))
                    edges = cv2.Canny(region, 100, 200)
                    edge_density = np.count_nonzero(edges) / region.size

                    if std_dev > 30 and edge_density > 0.1:
                        watermark_detected = True
                        break

            if watermark_detected:
                mask = WatermarkRemover._create_watermark_mask(frame)
                repaired = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
                return repaired, True
            else:
                return frame, False

        except Exception as e:
            print(f"帧处理警告: {str(e)}")
            return frame, False
    
    @staticmethod
    def _create_watermark_mask(frame) -> Any:
        """创建水印区域的掩码"""
        if not OPENCV_AVAILABLE:
            height, width = frame.shape[:2]
            return np.zeros((height, width), dtype=np.uint8)
        
        try:
            height, width = frame.shape[:2]
            mask = np.zeros((height, width), dtype=np.uint8)

            watermark_areas = [
                (0, 0, int(width*0.3), int(height*0.1)),
                (int(width*0.7), 0, width, int(height*0.1)),
                (0, int(height*0.9), int(width*0.3), height),
                (int(width*0.7), int(height*0.9), width, height),
                (0, 0, width, int(height*0.05)),
                (0, int(height*0.95), width, height),
            ]

            for x1, y1, x2, y2 in watermark_areas:
                cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            mask = cv2.bitwise_or(mask, edges)

            return mask

        except Exception as e:
            height, width = frame.shape[:2]
            return np.zeros((height, width), dtype=np.uint8)

"""
YouTube Video Extractor
----------------------
Trích xuất stream video từ YouTube cho AI processing.

Usage Example:
--------------
python youtube_extractor.py --url <youtube_url> --test
"""
#!/usr/bin/env python3
"""
YouTube Video Extractor for Labs Research
Extract video streams from YouTube URLs for AI processing
"""

import yt_dlp
import cv2
import numpy as np
import json
import time
import logging
import argparse
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import subprocess
import socket
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class StreamInfo:
    """Information about extracted video stream"""
    url: str
    format_id: str
    quality: str
    fps: int
    width: int
    height: int
    filesize: Optional[int]
    duration: Optional[float]
    is_live: bool

@dataclass
class ExtractionResult:
    """Result of YouTube stream extraction"""
    success: bool
    stream_info: Optional[StreamInfo]
    error_message: Optional[str]
    extraction_time: float
    method_used: str

class YouTubeExtractor:
    """YouTube video stream extractor"""
    
    def __init__(self, config_path: str = "../setup/config.json", cookie_path: str = None):
        """Initialize YouTube extractor with configuration"""
        self.config = self._load_config(config_path)
        self.ydl_opts = self._setup_ydl_options()
        self.cookie_path = cookie_path or os.path.join(os.path.dirname(__file__), '../cookies.txt')
        if not os.path.isfile(self.cookie_path):
            logger.warning(f"Cookie file not found: {self.cookie_path}. Some videos/streams may be restricted. See README for instructions.")
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {
                "youtube": {
                    "quality": "720p",
                    "extraction_method": "yt-dlp",
                    "timeout": 30
                }
            }
    
    def _setup_ydl_options(self) -> Dict:
        """Setup yt-dlp options for stream extraction"""
        return {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'format': 'best[height<=720]/best',  # Fallback to best if 720p not available
            'live_from_start': True,
            'timeout': self.config["youtube"]["timeout"],
            'retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'ignoreerrors': False,
        }
    
    def is_livestream(self, url: str) -> bool:
        """Check if YouTube URL is a livestream (quick check)"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('is_live', False)
        except Exception:
            return False

    def find_free_port(self, start_port=8080, max_tries=10):
        for port in range(start_port, start_port + max_tries):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:
                    return port
        return start_port

    def start_streamlink(self, url: str, port: int = 8080):
        """Start streamlink subprocess for livestream, return local URL"""
        cmd = [
            'streamlink',
            '--player-external-http',
            f'--player-external-http-port={port}',
            url,
            'best'
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc, f'http://localhost:{port}/'

    def get_hls_url_with_streamlink(self, url: str) -> str:
        """Dùng streamlink để lấy HLS URL từ YouTube livestream"""
        cmd = [
            'streamlink', '--stream-url', url, 'best'
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        hls_url = result.stdout.strip()
        return hls_url

    def start_ffmpeg_mjpeg(self, hls_url: str, port: int = 8090):
        """Khởi động ffmpeg chuyển HLS sang MJPEG HTTP server"""
        # MJPEG HTTP server trên port
        cmd = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', hls_url,
            '-f', 'mjpeg', '-q:v', '5', '-r', '15', 'http://0.0.0.0:%d' % port
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc, f'http://localhost:{port}'

    def filter_youtube_cookies(self, input_path: str, output_path: str = None) -> str:
        """Lọc cookie chỉ giữ lại cho youtube.com, google.com"""
        output_path = output_path or os.path.join(os.path.dirname(__file__), '../cookies.filtered.txt')
        if not os.path.isfile(input_path):
            return input_path
        with open(input_path, 'r') as f:
            lines = f.readlines()
        keep_domains = ["youtube.com", ".youtube.com", "google.com", ".google.com", "accounts.google.com"]
        filtered = []
        for line in lines:
            if line.startswith('#') or not line.strip():
                filtered.append(line)
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 7 and any(domain in parts[0] for domain in keep_domains):
                filtered.append(line)
        with open(output_path, 'w') as f:
            f.writelines(filtered)
        return output_path

    def get_cookie_string(self) -> str:
        """Đọc cookie string từ file cookies.txt, chỉ lấy các trường cần thiết cho YouTube livestream"""
        cookie_file = self.cookie_path
        # Nếu là file gốc, tự động lọc và dùng file filtered
        if os.path.isfile(cookie_file):
            filtered_path = self.filter_youtube_cookies(cookie_file)
            cookie_file = filtered_path
        if not os.path.isfile(cookie_file):
            return ""
        with open(cookie_file, 'r') as f:
            lines = f.readlines()
        # Chỉ lấy các trường cần thiết
        needed_keys = {"SID", "HSID", "SSID", "SAPISID", "APISID", "LOGIN_INFO", "VISITOR_INFO1_LIVE", "YSC", "CONSENT", "PREF"}
        cookies = []
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                key = parts[5]
                if key in needed_keys:
                    cookies.append(f"{key}={parts[6]}")
        return '; '.join(cookies)

    def start_yt_dlp_ffmpeg_pipe(self, url: str, width: int = 640, height: int = 360) -> subprocess.Popen:
        """Dùng yt-dlp stream sang stdout, pipe cho ffmpeg đọc từ stdin"""
        # yt-dlp command
        ytdlp_cmd = [
            'yt-dlp', '--quiet', '--no-warnings', '--cookies', self.cookie_path,
            '-f', 'best', '-o', '-', url
        ]
        # ffmpeg command
        ffmpeg_cmd = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error',
            '-i', '-',
            '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{width}x{height}', '-'
        ]
        print(f"[DEBUG] yt-dlp cmd: {' '.join(ytdlp_cmd)}")
        print(f"[DEBUG] ffmpeg cmd: {' '.join(ffmpeg_cmd)}")
        logger.info(f"[DEBUG] yt-dlp cmd: {' '.join(ytdlp_cmd)}")
        logger.info(f"[DEBUG] ffmpeg cmd: {' '.join(ffmpeg_cmd)}")
        ytdlp_proc = subprocess.Popen(ytdlp_cmd, stdout=subprocess.PIPE)
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=ytdlp_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ffmpeg_proc

    def start_ffmpeg_pipe(self, hls_url: str, width: int = 640, height: int = 360, use_ytdlp: bool = False, ytdlp_url: str = None) -> subprocess.Popen:
        """Khởi động ffmpeg chuyển HLS sang raw frame pipe (bgr24), hoặc dùng yt-dlp pipe nếu được chỉ định"""
        if use_ytdlp and ytdlp_url:
            return self.start_yt_dlp_ffmpeg_pipe(ytdlp_url, width, height)
        cookie_str = self.get_cookie_string()
        headers = []
        if cookie_str:
            headers.append(f"cookie: {cookie_str}\r\n")
        # Thêm User-Agent chuẩn Chrome
        headers.append("user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n")
        ffmpeg_headers = ''.join(headers)
        cmd = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error',
        ]
        if ffmpeg_headers:
            cmd += ['-headers', ffmpeg_headers]
        cmd += [
            '-i', hls_url,
            '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{width}x{height}', '-']
        # Debug log tối ưu
        cookie_fields = cookie_str.split(';') if cookie_str else []
        print(f"[DEBUG] Cookie file: {self.cookie_path}")
        print(f"[DEBUG] Cookie fields used: {len(cookie_fields)}")
        print(f"[DEBUG] ffmpeg cmd: {' '.join(cmd[:6])} ... (args truncated)")
        logger.info(f"[DEBUG] Cookie file: {self.cookie_path}")
        logger.info(f"[DEBUG] Cookie fields used: {len(cookie_fields)}")
        logger.info(f"[DEBUG] ffmpeg cmd: {' '.join(cmd[:6])} ... (args truncated)")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc

    def wait_for_port(self, port: int, timeout: float = 5.0) -> bool:
        """Chờ port mở (ffmpeg MJPEG server sẵn sàng)"""
        import time as _time
        start = _time.time()
        while _time.time() - start < timeout:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) == 0:
                    return True
            _time.sleep(0.2)
        return False

    def get_yt_dlp_url(self, url: str, is_live: bool = False) -> str:
        """Dùng yt-dlp để lấy direct video URL (mp4/webm) hoặc HLS URL cho livestream"""
        import yt_dlp
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
        if os.path.isfile(self.cookie_path):
            ydl_opts['cookies'] = self.cookie_path
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if is_live:
                # Lấy HLS URL cho livestream
                for f in info.get('formats', []):
                    if f.get('protocol') == 'm3u8_native' and f.get('ext') == 'mp4':
                        return f['url']
                # Fallback: lấy bất kỳ m3u8 nào
                for f in info.get('formats', []):
                    if f.get('protocol') == 'm3u8_native':
                        return f['url']
                raise Exception('No HLS stream found for livestream')
            else:
                # Lấy direct video URL cho video thường
                for f in info.get('formats', []):
                    if f.get('ext') in ('mp4', 'webm') and f.get('protocol') in ('https', 'http') and f.get('vcodec') != 'none':
                        return f['url']
                raise Exception('No direct video stream found')

    def extract_stream_info(self, url: str) -> ExtractionResult:
        start_time = time.time()
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
            if os.path.isfile(self.cookie_path):
                ydl_opts['cookies'] = self.cookie_path
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                is_live = info.get('is_live', False)
                width = info.get('width', 640) or 640
                height = info.get('height', 360) or 360
                if is_live:
                    # Lấy lại URL tốt nhất cho yt-dlp pipe
                    stream_url = url
                    method = 'yt-dlp-ffmpeg-pipe'
                else:
                    stream_url = self.get_yt_dlp_url(url, is_live=False)
                    method = 'yt-dlp-direct'
                return ExtractionResult(
                    success=True,
                    stream_info=StreamInfo(
                        url=stream_url, format_id=method, quality='best', fps=info.get('fps', 25), width=width, height=height,
                        filesize=info.get('filesize'), duration=info.get('duration'), is_live=is_live
                    ),
                    error_message=None,
                    extraction_time=time.time() - start_time,
                    method_used=method
                )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"yt-dlp extract error: {error_msg}")
            return ExtractionResult(success=False, error_message=error_msg, extraction_time=time.time() - start_time, method_used="yt-dlp")
    
    def _select_best_format(self, formats: List[Dict]) -> Dict:
        """Select the best format based on quality preferences"""
        # Filter formats with video
        video_formats = [f for f in formats if f.get('vcodec') != 'none']
        
        if not video_formats:
            return formats[0]  # Fallback to first format
        
        # Sort by height (quality) and prefer lower fps for stability
        video_formats.sort(key=lambda x: (
            x.get('height', 0),
            -x.get('fps', 30)  # Lower fps preferred for stability
        ), reverse=True)
        
        # Get target height from config
        target_height = int(self.config["youtube"]["quality"].replace("p", ""))
        
        # Find format closest to target height
        best_format = video_formats[0]
        for fmt in video_formats:
            if fmt.get('height', 0) <= target_height:
                best_format = fmt
                break
        
        return best_format
    
    def test_stream_connection(self, stream_info: StreamInfo, max_frames: int = 10) -> bool:
        """Test if the extracted stream can be opened and read"""
        try:
            logger.info(f"Testing stream connection: {stream_info.url[:100]}...")
            
            # Open video capture
            cap = cv2.VideoCapture(stream_info.url)
            if not cap.isOpened():
                logger.error("Failed to open video capture")
                return False
            
            # Read a few frames to test
            frame_count = 0
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    logger.warning(f"Failed to read frame {frame_count}")
                    break
                
                frame_count += 1
                logger.info(f"Successfully read frame {frame_count}")
            
            cap.release()
            
            success = frame_count > 0
            logger.info(f"Stream test {'passed' if success else 'failed'}: {frame_count} frames read")
            return success
            
        except Exception as e:
            logger.error(f"Stream test failed: {e}")
            return False
    
    def extract_and_test(self, url: str) -> ExtractionResult:
        """Extract stream and test connection"""
        # Extract stream info
        result = self.extract_stream_info(url)
        
        if result.success and result.stream_info:
            # Test stream connection
            connection_ok = self.test_stream_connection(result.stream_info)
            if not connection_ok:
                result.success = False
                result.error_message = "Stream connection test failed"
        
        return result

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='YouTube Video Stream Extractor')
    parser.add_argument('--url', required=True, help='YouTube URL to extract')
    parser.add_argument('--config', default='../setup/config.json', help='Configuration file path')
    parser.add_argument('--test', action='store_true', help='Test stream connection')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create extractor
    extractor = YouTubeExtractor(args.config)
    
    # Extract stream
    if args.test:
        result = extractor.extract_and_test(args.url)
    else:
        result = extractor.extract_stream_info(args.url)
    
    # Print results
    print(f"\n📊 Extraction Results:")
    print(f"Success: {result.success}")
    print(f"Method: {result.method_used}")
    print(f"Time: {result.extraction_time:.2f}s")
    
    if result.success and result.stream_info:
        print(f"\n Stream Information:")
        print(f"Quality: {result.stream_info.quality}")
        print(f"Resolution: {result.stream_info.width}x{result.stream_info.height}")
        print(f"FPS: {result.stream_info.fps}")
        print(f"Live: {result.stream_info.is_live}")
        print(f"Duration: {result.stream_info.duration}s" if result.stream_info.duration else "Duration: Unknown")
        print(f"URL: {result.stream_info.url[:100]}...")
    else:
        print(f"\n❌ Error: {result.error_message}")
    
    return 0 if result.success else 1

if __name__ == "__main__":
    sys.exit(main()) 
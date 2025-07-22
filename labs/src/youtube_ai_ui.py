"""
YouTube AI Integration UI
------------------------
Giao diện Tkinter hiển thị video YouTube và overlay AI đếm người real-time.

Usage Example:
--------------
python youtube_ai_ui.py
"""
#!/usr/bin/env python3

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import queue
from datetime import datetime
import sys
import os
from pathlib import Path
import subprocess
# Thêm import Pillow
from PIL import Image, ImageTk

# Add src to path
sys.path.append(str(Path(__file__).parent))

from youtube_extractor import YouTubeExtractor, StreamInfo, ExtractionResult
from ai_processor import AIProcessor, DetectionResult
from ai_people_counter_adapter import PeopleCounterAdapter
from config import (
    DEFAULT_SKIP_FRAMES, CONFIDENCE_THRESHOLD, DEFAULT_MAX_DISAPPEARED,
    TARGET_FPS, FPS_LOW_THRESHOLD, FPS_HIGH_THRESHOLD,
    MIN_SKIP_FRAMES, MAX_SKIP_FRAMES, MAX_DISAPPEARED_MULTIPLIER,
    get_max_disappeared, get_adaptive_skip_frames
)

class YouTubeAIUI:
    """Simple UI for YouTube AI integration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube AI Integration - Labs Research")
        self.root.geometry("1200x800")
        # Đặt link YouTube mặc định trước khi gọi setup_ui
        self.youtube_url_default = "https://www.youtube.com/watch?v=VSiQ7BLkZHw"
        # Khởi tạo line đếm 2 điểm trước khi dùng - FIX: Kéo hết màn hình
        self.line_start = [0, 240]  # default: trái giữa
        self.line_end = [640, 240]  # default: phải giữa - Sẽ được update theo canvas width
        self._dragging_point = None
        # Initialize components
        self.youtube_extractor = YouTubeExtractor()
        # Thay thế AIProcessor bằng PeopleCounterAdapter thực tế với tối ưu
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/detector'))
        prototxt = os.path.join(base_dir, 'MobileNetSSD_deploy.prototxt')
        model = os.path.join(base_dir, 'MobileNetSSD_deploy.caffemodel')
        self.skip_frames_var = tk.IntVar(value=DEFAULT_SKIP_FRAMES)  # Sử dụng config
        self.confidence_var = tk.DoubleVar(value=CONFIDENCE_THRESHOLD)  # Sử dụng config
        # self.max_disappeared_var = tk.IntVar(value=50) # Thêm input max_disappeared vào Control Panel
        self.ai_processor = PeopleCounterAdapter(
            prototxt, model,
            skip_frames=self.skip_frames_var.get(),
            resize_width=1920,  # Luôn detect trên frame gốc
            confidence=self.confidence_var.get(),
            max_disappeared=get_max_disappeared(self.skip_frames_var.get())  # Sử dụng config function
        )
        
        # Stream variables
        self.stream_info = None
        self.cap = None
        self.is_streaming = False
        self.frame_buffer = []  # Buffer để giảm lag
        self.max_buffer_size = 3  # Giữ tối đa 3 frame
        self.frame_queue = queue.Queue(maxsize=10)
        self.result_queue = queue.Queue(maxsize=10)
        self.frame_idx = 0  # Add frame_idx for UI
        
        # UI components
        self.setup_ui()
        
        # Start update loop
        self.update_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧪 YouTube AI Integration Research", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control Panel
        self.setup_control_panel(main_frame)
        
        # Video Display
        self.setup_video_display(main_frame)
        
        # Status Panel
        self.setup_status_panel(main_frame)
        
        # Log Panel
        self.setup_log_panel(main_frame)
    
    def setup_control_panel(self, parent):
        """Setup control panel"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Control Panel", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # URL input
        ttk.Label(control_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.url_var = tk.StringVar(value=self.youtube_url_default)
        self.url_entry = ttk.Entry(control_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10), columnspan=3)
        
        # Checkbox: Sử dụng cookies
        self.use_cookies_var = tk.BooleanVar(value=False)
        self.use_cookies_check = ttk.Checkbutton(control_frame, text="Sử dụng cookies đăng nhập", variable=self.use_cookies_var, command=self.toggle_cookies_entry)
        self.use_cookies_check.grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        
        # Cookie input (disabled mặc định)
        self.cookie_var = tk.StringVar(value="labs/cookies.txt")
        self.cookie_entry = ttk.Entry(control_frame, textvariable=self.cookie_var, width=50, state="disabled")
        self.cookie_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button (disabled mặc định)
        self.browse_btn = ttk.Button(control_frame, text="Browse", command=self.browse_cookie_file, state="disabled")
        self.browse_btn.grid(row=1, column=2, padx=(0, 10))
        
        # Start/Play/Stop button - Dùng 1 nút duy nhất, cập nhật text theo trạng thái
        self.stream_btn = ttk.Button(control_frame, text="Start", command=self.toggle_stream)
        self.stream_btn.grid(row=2, column=1, padx=(0, 10), pady=(5, 0), sticky=tk.W)
        
        # Nút đảo chiều in/out
        self.reverse_io = tk.BooleanVar(value=False)
        self.reverse_btn = ttk.Button(control_frame, text="🔄 Đảo chiều IN/OUT", command=self.toggle_reverse_io)
        self.reverse_btn.grid(row=2, column=2, padx=(0, 10), pady=(5, 0), sticky=tk.W)

        # AI Parameters
        ai_frame = ttk.LabelFrame(control_frame, text="🤖 AI Parameters", padding="5")
        ai_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        # Skip frames parameter
        ttk.Label(ai_frame, text="Skip frames:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.skip_frames_var = tk.IntVar(value=10)  # Default 10
        skip_frames_entry = ttk.Entry(ai_frame, textvariable=self.skip_frames_var, width=10)
        skip_frames_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        # Confidence parameter
        ttk.Label(ai_frame, text="Confidence:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.confidence_var = tk.DoubleVar(value=0.4)
        confidence_entry = ttk.Entry(ai_frame, textvariable=self.confidence_var, width=10)
        confidence_entry.grid(row=0, column=3, sticky=tk.W)

    def setup_video_display(self, parent):
        """Setup video display area"""
        video_frame = ttk.LabelFrame(parent, text="📹 Video Stream", padding="10")
        video_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        # Video canvas
        self.video_canvas = tk.Canvas(video_frame, width=640, height=480, bg="black")
        self.video_canvas.pack(expand=True, fill=tk.BOTH)
        self.video_canvas.bind('<Button-1>', self.on_canvas_click)
        self.video_canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.video_canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.video_canvas.bind('<Leave>', self.on_canvas_leave)
        # Video info
        self.video_info = ttk.Label(video_frame, text="No stream active", font=("Arial", 10))
        self.video_info.pack(pady=(10, 0))
        self._dragging_line = False
        self._last_frame = None  # Lưu frame cuối cùng để redraw khi kéo line

    def setup_status_panel(self, parent):
        """Setup status panel"""
        status_frame = ttk.LabelFrame(parent, text="📊 AI Processing Status", padding="10")
        status_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Status variables
        self.status_vars = {
            'stream_status': tk.StringVar(value="❌ No Stream"),
            'ai_status': tk.StringVar(value="❌ AI Not Active"),
            'people_count': tk.StringVar(value="People: 0"),
            'confidence': tk.StringVar(value="Confidence: 0.00"),
            'fps': tk.StringVar(value="FPS: 0.0"),
            'processing_time': tk.StringVar(value="Time: 0.000s")
        }
        # Status labels
        row = 0
        for label, var in self.status_vars.items():
            ttk.Label(status_frame, text=label.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Label(status_frame, textvariable=var, font=("Arial", 10, "bold")).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            row += 1
        # Progress bar
        ttk.Label(status_frame, text="Processing Progress:").grid(row=row, column=0, sticky=tk.W, pady=(10, 2))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        # Configure grid weights
        status_frame.columnconfigure(1, weight=1)

    def setup_log_panel(self, parent):
        """Setup log panel"""
        log_frame = ttk.LabelFrame(parent, text="📝 Activity Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=100)
        self.log_text.pack(expand=True, fill=tk.BOTH)
        # Configure grid weights
        parent.rowconfigure(3, weight=1)

    def toggle_reverse_io(self):
        self.reverse_io.set(not self.reverse_io.get())
        self.log_message(f"Đã {'đảo' if self.reverse_io.get() else 'khôi phục'} chiều IN/OUT!")

    # Trong setup_control_panel
    # self.stream_btn = ttk.Button(control_frame, text="Start", command=self.toggle_stream)
    # ...
    # Trong start_stream, update text nút:
    def start_stream(self):
        """
        Start stream processing.
        Lấy giá trị max_disappeared từ UI để truyền vào PeopleCounterAdapter.
        max_disappeared quyết định số frame mà object sẽ được giữ lại khi không còn detection mới.
        Giá trị nhỏ giúp bounding box biến mất nhanh hơn khi người đã đi khỏi khung hình, giá trị lớn giúp tracking ổn định hơn khi có occlusion hoặc detection miss.
        Edge case: Nếu đặt quá lớn, object sẽ tồn tại lâu dù đã biến mất; nếu quá nhỏ, object sẽ bị mất khi chỉ bị che khuất tạm thời.
        """
        if not self.stream_info:
            messagebox.showerror("Error", "No stream available. Please extract stream first.")
            return
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prototxt = os.path.join(base_dir, 'models', 'detector', 'MobileNetSSD_deploy.prototxt')
        model = os.path.join(base_dir, 'models', 'detector', 'MobileNetSSD_deploy.caffemodel')
        skip_frames = self.skip_frames_var.get()
        confidence = self.confidence_var.get()
        max_disappeared = 3 * skip_frames  # Theo tài liệu
        self.ai_processor = PeopleCounterAdapter(
            prototxt, model,
            skip_frames=skip_frames,
            resize_width=1920,
            confidence=confidence,
            max_disappeared=max_disappeared
        )
        
        self.is_streaming = True
        self.stream_btn.config(text="▶️ Play Now")
        # self.stop_btn.config(state="normal") # XÓA self.stop_btn và các dòng liên quan
        self.status_vars['ai_status'].set("✅ AI Active")
        
        # Log chi tiết thông tin stream và AI parameters
        log_msg = (
            f"[STREAM] format_id: {self.stream_info.format_id}, "
            f"is_live: {getattr(self.stream_info, 'is_live', None)}, "
            f"URL: {self.stream_info.url}, "
            f"method: {'ffmpeg-pipe' if self.stream_info.format_id in ('ffmpeg-pipe', 'yt-dlp-hls', 'yt-dlp-ffmpeg-pipe') else 'opencv'}, "
            f"AI params: skip_frames={skip_frames}, confidence={confidence}"
        )
        print(log_msg)
        self.log_message(log_msg)
        self.log_message("🚀 Starting stream processing...")
        
        # Start stream thread
        if self.stream_info.format_id in ('ffmpeg-pipe', 'yt-dlp-hls', 'yt-dlp-ffmpeg-pipe'):
            thread = threading.Thread(target=self._stream_thread_ffmpeg_pipe)
        else:
            thread = threading.Thread(target=self._stream_thread_opencv)
        thread.daemon = True
        thread.start()

    def _stream_thread_opencv(self):
        """Stream processing thread for direct video (mp4/webm)"""
        try:
            cap = cv2.VideoCapture(self.stream_info.url)
            if not cap.isOpened():
                self.root.after(0, lambda: self.log_message(f"❌ Failed to open video stream: {self.stream_info.url}"))
                return
            self.root.after(0, lambda: self.stream_btn.config(text="⏹️ Stop"))
            frame_count = 0
            start_time = time.time()
            while self.is_streaming:
                ret, frame = cap.read()
                if not ret:
                    self.root.after(0, lambda: self.log_message("❌ Failed to read frame from video stream"))
                    break
                try:
                    # Lấy line động 2 điểm từ UI
                    line_start = tuple(self.line_start)
                    line_end = tuple(self.line_end)
                    ai_result = self.ai_processor.process_frame(frame, line_start=line_start, line_end=line_end, reverse_io=self.reverse_io.get())
                    if not self.frame_queue.full():
                        self.frame_queue.put((frame, ai_result))
                    frame_count += 1
                    if frame_count % 30 == 0:
                        elapsed_time = time.time() - start_time
                        fps = frame_count / elapsed_time
                        self.root.after(0, lambda f=fps: self.status_vars['fps'].set(f"FPS: {f:.1f}"))
                        # Adaptive frame skip
                        new_skip = self.adaptive_frame_skipping(fps)
                        self.root.after(0, lambda: self.status_vars['processing_time'].set(f"Skip: {new_skip}"))
                except Exception as e:
                    self.root.after(0, lambda e=e: self.log_message(f"❌ Frame decode error: {e}"))
                    continue
            cap.release()
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Stream error (opencv): {e}"))
        finally:
            self.is_streaming = False

    def _stream_thread_ffmpeg_pipe(self):
        try:
            url = self.stream_info.url
            width, height = self.stream_info.width, self.stream_info.height
            extractor = YouTubeExtractor(cookie_path=self.cookie_var.get().strip())
            # Nếu là yt-dlp-ffmpeg-pipe thì dùng yt-dlp pipe
            if self.stream_info.format_id == 'yt-dlp-ffmpeg-pipe':
                proc = extractor.start_ffmpeg_pipe(url, width, height, use_ytdlp=True, ytdlp_url=url)
            else:
                proc = extractor.start_ffmpeg_pipe(url, width, height)
            self.root.after(0, lambda: self.stream_btn.config(text="⏹️ Stop"))
            frame_size = width * height * 3
            frame_count = 0
            valid_frame_count = 0
            start_time = time.time()
            while self.is_streaming:
                raw_frame = proc.stdout.read(frame_size)
                if not raw_frame:
                    self.root.after(0, lambda: self.log_message("❌ Failed to read frame from ffmpeg pipe (empty)"))
                    if proc.stderr:
                        err = proc.stderr.read().decode(errors='ignore')
                        self.root.after(0, lambda: self.log_message(f"[ffmpeg stderr] {err}"))
                        # Tự động cảnh báo nếu gặp lỗi truy cập
                        if any(x in err.lower() for x in ["403", "401", "denied", "forbidden", "unauthorized"]):
                            self.root.after(0, lambda: self.log_message("⚠️ Có thể cần đăng nhập và nhập cookies.txt để xem livestream này!"))
                    break
                if len(raw_frame) != frame_size:
                    self.root.after(0, lambda: self.log_message(f"⚠️ Incomplete frame: got {len(raw_frame)} bytes, expected {frame_size}. Skipping."))
                    continue
                try:
                    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))
                    # Lấy line động 2 điểm từ UI
                    line_start = tuple(self.line_start)
                    line_end = tuple(self.line_end)
                    ai_result = self.ai_processor.process_frame(frame, line_start=line_start, line_end=line_end, reverse_io=self.reverse_io.get())
                    if not self.frame_queue.full():
                        self.frame_queue.put((frame, ai_result))
                    frame_count += 1
                    valid_frame_count += 1
                    if frame_count % 30 == 0:
                        elapsed_time = time.time() - start_time
                        fps = frame_count / elapsed_time
                        self.root.after(0, lambda f=fps: self.status_vars['fps'].set(f"FPS: {f:.1f}"))
                        # Adaptive frame skip
                        new_skip = self.adaptive_frame_skipping(fps)
                        self.root.after(0, lambda: self.status_vars['processing_time'].set(f"Skip: {new_skip}"))
                        print(f"[DEBUG] Valid frames: {valid_frame_count} / {frame_count}")
                except Exception as e:
                    self.root.after(0, lambda e=e: self.log_message(f"❌ Frame decode error: {e}"))
                    continue
            proc.terminate()
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Stream error (ffmpeg pipe): {e}"))
        finally:
            self.is_streaming = False
    
    def clear_display(self):
        """Clear display and reset - Đơn giản hóa vì stop_stream đã xử lý hầu hết"""
        self.stop_stream()
        self.stream_info = None
        self.status_vars['stream_status'].set("❌ No Stream")
        self.log_message("🗑️ Display cleared")
    
    def update_ui(self):
        """Update UI elements - TỐI ƯU THEO CODE MẪU: CHỈ UPDATE KHI CÓ FRAME MỚI"""
        # Update video display
        try:
            if not self.frame_queue.empty():
                frame, ai_result = self.frame_queue.get_nowait()
                
                # Update status (chỉ update khi có thay đổi quan trọng)
                if hasattr(self, '_last_status_update'):
                    if ai_result['frame_idx'] - self._last_status_update > 15:  # Update mỗi 15 frame
                        self.status_vars['people_count'].set(f"In: {ai_result['total_in']} | Out: {ai_result['total_out']}")
                        self.status_vars['confidence'].set(f"Objects: {len(ai_result['objects'])}")
                        self.status_vars['processing_time'].set(f"Frame: {ai_result['frame_idx']}")
                        self._last_status_update = ai_result['frame_idx']
                else:
                    self.status_vars['people_count'].set(f"In: {ai_result['total_in']} | Out: {ai_result['total_out']}")
                    self.status_vars['confidence'].set(f"Objects: {len(ai_result['objects'])}")
                    self.status_vars['processing_time'].set(f"Frame: {ai_result['frame_idx']}")
                    self._last_status_update = ai_result['frame_idx']
                
                # Debug: Log status update (giảm frequency)
                if ai_result['frame_idx'] % 90 == 0:  # Log mỗi 90 frame
                    print(f"[DEBUG] Status Update: In={ai_result['total_in']}, Out={ai_result['total_out']}, Objects={len(ai_result['objects'])}")
                
                # Update progress bar
                progress = min(100, ai_result['frame_idx'] % 100)
                self.progress_var.set(progress)
                
                # Update video display
                self._update_video_display(frame, ai_result)
        
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(50, self.update_ui)  # ~20 FPS để giảm lag
    
    def _draw_overlay_on_frame(self, frame, ai_result):
        """
        Vẽ overlay thông tin hiện đại lên frame bằng OpenCV, cố định ở góc trên bên phải.
        Overlay nhỏ gọn, hiện đại với font nhỏ, layout đẹp mắt, màu sắc tối ưu.
        Không còn nháy, không vẽ overlay thông tin bằng canvas text nữa.
        """
        # Lấy thông tin
        total_in = ai_result.get('total_in', 0)
        total_out = ai_result.get('total_out', 0)
        objects_count = len(ai_result.get('objects', []))
        frame_idx = ai_result.get('frame_idx', 0)
        line_start = ai_result.get('line_start', (0, 0))
        line_end = ai_result.get('line_end', (0, 0))
        
        h, w = frame.shape[:2]
        
        # Thiết kế overlay hiện đại - nhỏ gọn hơn
        margin = 15
        padding = 8
        box_width = 180  # Giảm width
        box_height = 100  # Giảm height
        
        # Tạo background semi-transparent hiện đại
        overlay = frame.copy()
        # Background chính với góc bo tròn (simulate)
        cv2.rectangle(overlay, (w-box_width-margin, margin), (w-margin, margin+box_height), (20, 20, 20), -1)
        # Border mỏng
        cv2.rectangle(overlay, (w-box_width-margin, margin), (w-margin, margin+box_height), (60, 60, 60), 1)
        
        # Blend với alpha thấp hơn để hiện đại
        alpha = 0.3
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Font settings hiện đại
        font_small = cv2.FONT_HERSHEY_SIMPLEX
        font_tiny = cv2.FONT_HERSHEY_SIMPLEX
        
        # Vị trí text
        x_start = w - box_width - margin + padding
        y_start = margin + padding + 15
        
        # 1. Header - People Count (lớn nhất)
        count_text = f"IN: {total_in} | OUT: {total_out}"
        overlay_color = (0, 255, 100)
        cv2.putText(frame, count_text, (x_start, y_start), font_small, 0.5, overlay_color, 1, cv2.LINE_AA)
        # 2. Objects count
        obj_text = f"Objects: {objects_count}"
        cv2.putText(frame, obj_text, (x_start, y_start + 20), font_small, 0.4, overlay_color, 1, cv2.LINE_AA)
        # 3. Frame info
        frame_text = f"Frame: {frame_idx}"
        cv2.putText(frame, frame_text, (x_start, y_start + 35), font_small, 0.4, overlay_color, 1, cv2.LINE_AA)
        # 4. Line coordinates (nhỏ nhất)
        line_text = f"Line: ({line_start[0]},{line_start[1]}) - ({line_end[0]},{line_end[1]})"
        cv2.putText(frame, line_text, (x_start, y_start + 50), font_tiny, 0.3, overlay_color, 1, cv2.LINE_AA)
        # Bỏ status indicator 'LIVE'
        
        # Xác định hướng IN/OUT
        in_label = "IN↓"
        out_label = "OUT↑"
        # Vẽ text đầu line (IN↓) lệch lên trên
        cv2.putText(frame, in_label, (self.line_start[0]-10, self.line_start[1]-20), font_small, 0.7, (0,255,0), 2, cv2.LINE_AA)
        # Vẽ text cuối line (OUT↑) lệch xuống dưới
        cv2.putText(frame, out_label, (self.line_end[0]-10, self.line_end[1]+30), font_small, 0.7, (0,0,255), 2, cv2.LINE_AA)
        return frame

    def _update_video_display(self, frame, ai_result):
        """
        Update video display - overlay thông tin duy nhất bằng OpenCV, cố định góc trên phải, không nháy.
        """
        self._last_frame = frame
        self._last_ai_result = ai_result
        canvas_width = self.video_canvas.winfo_width()
        canvas_height = self.video_canvas.winfo_height()
        if canvas_width > 1 and canvas_height > 1:
            frame_resized = cv2.resize(frame, (canvas_width, canvas_height), interpolation=cv2.INTER_LINEAR)
            frame_with_overlay = self._draw_overlay_on_frame(frame_resized, ai_result)
            frame_rgb = cv2.cvtColor(frame_with_overlay, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image_pil)
            self.video_canvas.delete("bbox", "centroid", "obj_id", "overlay_text")
            self.video_canvas.delete("image")
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=image_tk, tags="image")
            self.video_canvas.image = image_tk
            # Vẽ bounding box, centroid, id nếu cần
            if ai_result.get('frame_idx', 0) % 3 == 0:
                self._draw_ai_overlay(ai_result, canvas_width, canvas_height, skip_info_overlay=True)
            self._redraw_canvas_line()
            if ai_result.get('frame_idx', 0) % 120 == 0:
                print(f"[DEBUG] UI Line: ({self.line_start[0]}, {self.line_start[1]}) -> ({self.line_end[0]}, {self.line_end[1]})")

    def _draw_ai_overlay(self, ai_result, width, height, skip_info_overlay=False):
        # Kiểm tra kiểu ai_result để lấy dữ liệu đúng
        if isinstance(ai_result, dict):
            people_in = ai_result.get('total_in', 0)
            people_out = ai_result.get('total_out', 0)
            objects = ai_result.get('objects', [])
            frame_idx = ai_result.get('frame_idx', 0)
        else:
            # fallback cho object kiểu cũ
            people_in = getattr(ai_result, 'people_count', 0)
            people_out = 0
            objects = []
            frame_idx = getattr(ai_result, 'frame_number', 0)
        
        # Log debug overlay mỗi 30 frame
        if frame_idx % 30 == 0:
            print(f"[DEBUG] Overlay: in={people_in}, out={people_out}, objects={len(objects)}, frame={frame_idx}")
            if len(objects) > 0:
                for i, obj in enumerate(objects):
                    print(f"[DEBUG] Object {i}: {obj}")
                    print(f"[DEBUG]   - box: {obj.get('box')} (type: {type(obj.get('box'))})")
                    print(f"[DEBUG]   - centroid: {obj.get('centroid')} (type: {type(obj.get('centroid'))})")
                    print(f"[DEBUG]   - id: {obj.get('id')}")
        
        # Xóa text cũ
        self.video_canvas.delete("overlay_text")
        
        # Vẽ overlay text - COMMENT LẠI: CHỈ DÙNG OVERLAY OPENCV
        # count_text = f"In: {people_in} | Out: {people_out}"
        # self.video_canvas.create_text(width - 10, 30, text=count_text, anchor=tk.E, fill="green", font=("Arial", 16, "bold"), tags="overlay_text")
        # obj_text = f"Objects: {len(objects)}"
        # self.video_canvas.create_text(width - 10, 60, text=obj_text, anchor=tk.E, fill="yellow", font=("Arial", 12), tags="overlay_text")
        # frame_text = f"Frame: {frame_idx}"
        # self.video_canvas.create_text(10, 30, text=frame_text, anchor=tk.W, fill="white", font=("Arial", 12), tags="overlay_text")
        
        # Debug info
        # debug_text = f"Line: {ai_result.get('line_start', 'N/A')} -> {ai_result.get('line_end', 'N/A')}"
        # self.video_canvas.create_text(10, 60, text=debug_text, anchor=tk.W, fill="cyan", font=("Arial", 10), tags="overlay_text")
        
        # Vẽ bounding boxes và centroids cho từng object
        for obj in objects:
            # Kiểm tra box và centroid có tồn tại và hợp lệ
            box = obj.get('box')
            centroid = obj.get('centroid')
            
            if box is not None and centroid is not None:
                obj_id = obj.get('id', '?')
                
                # Scale coordinates to canvas size
                scale_x = width / self._last_frame.shape[1] if hasattr(self, '_last_frame') and self._last_frame is not None else 1
                scale_y = height / self._last_frame.shape[0] if hasattr(self, '_last_frame') and self._last_frame is not None else 1
                
                # Vẽ bounding box
                x1, y1, x2, y2 = box
                x1_scaled = int(x1 * scale_x)
                y1_scaled = int(y1 * scale_y)
                x2_scaled = int(x2 * scale_x)
                y2_scaled = int(y2 * scale_y)
                
                self.video_canvas.create_rectangle(x1_scaled, y1_scaled, x2_scaled, y2_scaled, 
                                                 outline="lime", width=2, tags="bbox")
                
                # Vẽ centroid
                cx_scaled = int(centroid[0] * scale_x)
                cy_scaled = int(centroid[1] * scale_y)
                self.video_canvas.create_oval(cx_scaled-3, cy_scaled-3, cx_scaled+3, cy_scaled+3, 
                                            fill="red", outline="white", width=1, tags="centroid")
                
                # Vẽ object ID - GIỮ LẠI: Để nhận diện từng object
                self.video_canvas.create_text(cx_scaled, y1_scaled-10, text=f"ID:{obj_id}", 
                                            anchor=tk.S, fill="white", font=("Arial", 10, "bold"), tags="obj_id")

    def _redraw_canvas_line(self):
        self.video_canvas.delete('line_y')
        canvas_width = self.video_canvas.winfo_width()
        canvas_height = self.video_canvas.winfo_height()
        # Đảm bảo line không vượt quá canvas bounds
        self.line_start[0] = max(0, min(self.line_start[0], canvas_width))
        self.line_start[1] = max(0, min(self.line_start[1], canvas_height))
        self.line_end[0] = max(0, min(self.line_end[0], canvas_width))
        self.line_end[1] = max(0, min(self.line_end[1], canvas_height))
        # Vẽ line từ start đến end
        self.video_canvas.create_line(
            self.line_start[0], self.line_start[1], 
            self.line_end[0], self.line_end[1], 
            fill="red", width=2, dash=(4, 2), tags='line_y'
        )
        # Vẽ handles ở 2 đầu line
        handle_size = 6
        self.video_canvas.create_oval(
            self.line_start[0] - handle_size, self.line_start[1] - handle_size,
            self.line_start[0] + handle_size, self.line_start[1] + handle_size,
            fill="blue", outline="white", width=2, tags='line_y'
        )
        self.video_canvas.create_oval(
            self.line_end[0] - handle_size, self.line_end[1] - handle_size,
            self.line_end[0] + handle_size, self.line_end[1] + handle_size,
            fill="blue", outline="white", width=2, tags='line_y'
        )

    def toggle_cookies_entry(self):
        if self.use_cookies_var.get():
            self.cookie_entry.config(state="normal")
            self.browse_btn.config(state="normal")
        else:
            self.cookie_entry.config(state="disabled")
            self.browse_btn.config(state="disabled")

    def browse_cookie_file(self):
        file_path = filedialog.askopenfilename(
            title="Select cookies.txt file",
            filetypes=[("Cookies file", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.cookie_var.set(file_path)
            self.log_message(f"Selected cookie file: {file_path}")

    def toggle_stream(self):
        """Toggle stream processing - Gộp Extract và Start thành 1 nút"""
        if not self.is_streaming:
            # Nếu chưa có stream_info, extract trước
            if not self.stream_info:
                self.extract_stream()
            else:
                # Nếu đã có stream_info, start luôn
                self.start_stream()
        else:
            self.stop_stream()

    def extract_stream(self):
        """Extract YouTube stream"""
        url = self.url_var.get().strip()
        cookie_path = self.cookie_var.get().strip() if self.use_cookies_var.get() else ""
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if self.use_cookies_var.get() and not os.path.isfile(cookie_path):
            self.log_message(f"⚠️ Cookie file not found: {cookie_path}. Some videos/streams may be restricted.")
        self.log_message(f"Extracting stream from: {url}")
        self.stream_btn.config(state="disabled")
        thread = threading.Thread(target=self._extract_stream_thread, args=(url, cookie_path))
        thread.daemon = True
        thread.start()

    def _extract_stream_thread(self, url, cookie_path):
        try:
            extractor = YouTubeExtractor(cookie_path=cookie_path)
            result = extractor.extract_stream_info(url)
            if result.success and result.stream_info:
                self.root.after(0, self._on_stream_extracted, result)
            else:
                self.root.after(0, self._on_stream_failed, result.error_message)
        except Exception as e:
            self.root.after(0, self._on_stream_failed, str(e))

    def _on_stream_extracted(self, result):
        self.stream_info = result.stream_info
        self.log_message(f"✅ Stream extracted successfully!")
        self.log_message(f"   Quality: {result.stream_info.quality}")
        self.log_message(f"   Resolution: {result.stream_info.width}x{result.stream_info.height}")
        self.log_message(f"   FPS: {result.stream_info.fps}")
        self.status_vars['stream_status'].set("✅ Stream Ready")
        self.stream_btn.config(state="normal")
        self.log_message("🎯 Stream ready! Click 'Start Stream' to begin processing.")

    def _on_stream_failed(self, error):
        self.log_message(f"❌ Stream extraction failed: {error}")
        self.status_vars['stream_status'].set("❌ Stream Failed")
        self.stream_btn.config(state="normal")

    def on_canvas_click(self, event):
        x1, y1 = self.line_start
        x2, y2 = self.line_end
        if abs(event.x - x1) < 10 and abs(event.y - y1) < 10:
            self._dragging_point = 'start'
        elif abs(event.x - x2) < 10 and abs(event.y - y2) < 10:
            self._dragging_point = 'end'
        else:
            self._dragging_point = None

    def on_canvas_drag(self, event):
        if self._dragging_point == 'start':
            self.line_start = [event.x, event.y]
            if self._last_frame is not None:
                self._update_video_display(self._last_frame, self._last_ai_result)
        elif self._dragging_point == 'end':
            self.line_end = [event.x, event.y]
            if self._last_frame is not None:
                self._update_video_display(self._last_frame, self._last_ai_result)

    def on_canvas_release(self, event):
        self._dragging_point = None

    def on_canvas_leave(self, event):
        self._dragging_point = None

    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        # Limit log size
        if int(self.log_text.index('end-1c').split('.')[0]) > 1000:
            self.log_text.delete('1.0', '500.0')

    def adaptive_frame_skipping(self, current_fps, target_fps=TARGET_FPS):
        # Tự động điều chỉnh skip_frames dựa trên FPS thực tế
        skip_frames = self.skip_frames_var.get()
        if current_fps < target_fps * FPS_LOW_THRESHOLD:
            skip_frames = min(skip_frames + 1, MAX_SKIP_FRAMES)
        elif current_fps > target_fps * FPS_HIGH_THRESHOLD:
            skip_frames = max(skip_frames - 1, MIN_SKIP_FRAMES)
        self.skip_frames_var.set(skip_frames)
        return skip_frames

def main():
    """Main function"""
    root = tk.Tk()
    app = YouTubeAIUI(root)
    
    # Handle window close
    def on_closing():
        app.stop_stream()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 
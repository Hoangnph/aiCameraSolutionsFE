#!/usr/bin/env python3
"""
YouTube AI Integration UI
Simple UI to display YouTube stream and AI model processing
"""

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

class YouTubeAIUI:
    """Simple UI for YouTube AI integration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube AI Integration - Labs Research")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.youtube_extractor = YouTubeExtractor()
        self.ai_processor = AIProcessor()
        
        # Stream variables
        self.stream_info = None
        self.cap = None
        self.is_streaming = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.result_queue = queue.Queue(maxsize=10)
        
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
        self.url_var = tk.StringVar(value="https://www.youtube.com/watch?v=57w2gYXjRic")
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
        
        # Extract button
        self.extract_btn = ttk.Button(control_frame, text="🔍 Extract Stream", 
                                     command=self.extract_stream)
        self.extract_btn.grid(row=2, column=1, padx=(0, 10), pady=(5, 0), sticky=tk.W)
        
        # Start/Stop button
        self.stream_btn = ttk.Button(control_frame, text="▶️ Start Stream", 
                                    command=self.toggle_stream, state="disabled")
        self.stream_btn.grid(row=2, column=2, padx=(0, 10), pady=(5, 0), sticky=tk.W)
        
        # Clear button
        self.clear_btn = ttk.Button(control_frame, text="🗑️ Clear", 
                                   command=self.clear_display)
        self.clear_btn.grid(row=2, column=3, pady=(5, 0), sticky=tk.W)
        
        # Configure grid weights
        control_frame.columnconfigure(1, weight=1)
    
    def setup_video_display(self, parent):
        """Setup video display area"""
        video_frame = ttk.LabelFrame(parent, text="📹 Video Stream", padding="10")
        video_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Video canvas
        self.video_canvas = tk.Canvas(video_frame, width=640, height=480, bg="black")
        self.video_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Video info
        self.video_info = ttk.Label(video_frame, text="No stream active", 
                                   font=("Arial", 10))
        self.video_info.pack(pady=(10, 0))
    
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
            ttk.Label(status_frame, text=label.replace('_', ' ').title() + ":").grid(
                row=row, column=0, sticky=tk.W, pady=2)
            ttk.Label(status_frame, textvariable=var, font=("Arial", 10, "bold")).grid(
                row=row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            row += 1
        
        # Progress bar
        ttk.Label(status_frame, text="Processing Progress:").grid(
            row=row, column=0, sticky=tk.W, pady=(10, 2))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           maximum=100)
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
    
    def toggle_cookies_entry(self):
        if self.use_cookies_var.get():
            self.cookie_entry.config(state="normal")
            self.browse_btn.config(state="normal")
        else:
            self.cookie_entry.config(state="disabled")
            self.browse_btn.config(state="disabled")

    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Nếu có cảnh báo cần cookies, tự động bật checkbox và enable entry
        if "cookies.txt" in message and "cần đăng nhập" in message:
            self.use_cookies_var.set(True)
            self.toggle_cookies_entry()
        # Limit log size
        if int(self.log_text.index('end-1c').split('.')[0]) > 1000:
            self.log_text.delete('1.0', '500.0')
    
    def extract_stream(self):
        """Extract YouTube stream"""
        url = self.url_var.get().strip()
        # Nếu không dùng cookies, truyền path rỗng
        cookie_path = self.cookie_var.get().strip() if self.use_cookies_var.get() else ""
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if self.use_cookies_var.get() and not os.path.isfile(cookie_path):
            self.log_message(f"⚠️ Cookie file not found: {cookie_path}. Some videos/streams may be restricted.")
        self.log_message(f"Extracting stream from: {url}")
        self.extract_btn.config(state="disabled")
        
        # Run extraction in thread
        thread = threading.Thread(target=self._extract_stream_thread, args=(url, cookie_path))
        thread.daemon = True
        thread.start()
    
    def _extract_stream_thread(self, url, cookie_path):
        """Extract stream in background thread"""
        try:
            extractor = YouTubeExtractor(cookie_path=cookie_path)
            result = extractor.extract_stream_info(url)
            
            if result.success and result.stream_info:
                self.stream_info = result.stream_info
                self.root.after(0, self._on_stream_extracted, result)
            else:
                self.root.after(0, self._on_stream_failed, result.error_message)
        
        except Exception as e:
            self.root.after(0, self._on_stream_failed, str(e))
    
    def _on_stream_extracted(self, result):
        """Handle successful stream extraction"""
        self.log_message(f"✅ Stream extracted successfully!")
        self.log_message(f"   Quality: {result.stream_info.quality}")
        self.log_message(f"   Resolution: {result.stream_info.width}x{result.stream_info.height}")
        self.log_message(f"   FPS: {result.stream_info.fps}")
        
        self.status_vars['stream_status'].set("✅ Stream Ready")
        self.stream_btn.config(state="normal")
        self.extract_btn.config(state="normal")
    
    def _on_stream_failed(self, error):
        """Handle stream extraction failure"""
        self.log_message(f"❌ Stream extraction failed: {error}")
        self.status_vars['stream_status'].set("❌ Stream Failed")
        self.extract_btn.config(state="normal")
    
    def toggle_stream(self):
        """Toggle stream processing"""
        if not self.is_streaming:
            self.start_stream()
        else:
            self.stop_stream()
    
    def start_stream(self):
        """Start stream processing"""
        if not self.stream_info:
            messagebox.showerror("Error", "No stream available. Please extract stream first.")
            return
        self.is_streaming = True
        self.stream_btn.config(text="⏹️ Stop Stream")
        self.status_vars['ai_status'].set("✅ AI Active")
        # Log chi tiết thông tin stream
        log_msg = (
            f"[STREAM] format_id: {self.stream_info.format_id}, "
            f"is_live: {getattr(self.stream_info, 'is_live', None)}, "
            f"URL: {self.stream_info.url}, "
            f"method: {'ffmpeg-pipe' if self.stream_info.format_id in ('ffmpeg-pipe', 'yt-dlp-hls', 'yt-dlp-ffmpeg-pipe') else 'opencv'}"
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
            frame_count = 0
            start_time = time.time()
            while self.is_streaming:
                ret, frame = cap.read()
                if not ret:
                    self.root.after(0, lambda: self.log_message("❌ Failed to read frame from video stream"))
                    break
                try:
                    ai_result = self.ai_processor.process_frame(frame)
                    if not self.frame_queue.full():
                        self.frame_queue.put((frame, ai_result))
                    frame_count += 1
                    if frame_count % 30 == 0:
                        elapsed_time = time.time() - start_time
                        fps = frame_count / elapsed_time
                        self.root.after(0, lambda f=fps: self.status_vars['fps'].set(f"FPS: {f:.1f}"))
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"❌ Frame decode error: {e}"))
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
                    ai_result = self.ai_processor.process_frame(frame)
                    if not self.frame_queue.full():
                        self.frame_queue.put((frame, ai_result))
                    frame_count += 1
                    valid_frame_count += 1
                    if frame_count % 30 == 0:
                        elapsed_time = time.time() - start_time
                        fps = frame_count / elapsed_time
                        self.root.after(0, lambda f=fps: self.status_vars['fps'].set(f"FPS: {f:.1f}"))
                        print(f"[DEBUG] Valid frames: {valid_frame_count} / {frame_count}")
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"❌ Frame decode error: {e}"))
                    continue
            proc.terminate()
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Stream error (ffmpeg pipe): {e}"))
        finally:
            self.is_streaming = False
    
    def clear_display(self):
        """Clear display and reset"""
        self.stop_stream()
        self.stream_info = None
        self.status_vars['stream_status'].set("❌ No Stream")
        self.status_vars['ai_status'].set("❌ AI Not Active")
        self.status_vars['people_count'].set("People: 0")
        self.status_vars['confidence'].set("Confidence: 0.00")
        self.status_vars['fps'].set("FPS: 0.0")
        self.status_vars['processing_time'].set("Time: 0.000s")
        self.progress_var.set(0)
        
        # Clear video display
        self.video_canvas.delete("all")
        self.video_canvas.create_text(320, 240, text="No Video", 
                                     fill="white", font=("Arial", 20))
        
        self.log_message("🗑️ Display cleared")
    
    def update_ui(self):
        """Update UI elements"""
        # Update video display
        try:
            if not self.frame_queue.empty():
                frame, ai_result = self.frame_queue.get_nowait()
                
                # Update status
                self.status_vars['people_count'].set(f"People: {ai_result.people_count}")
                self.status_vars['confidence'].set(f"Confidence: {ai_result.confidence:.2f}")
                self.status_vars['processing_time'].set(f"Time: {ai_result.processing_time:.3f}s")
                
                # Update progress bar
                progress = min(100, ai_result.frame_number % 100)
                self.progress_var.set(progress)
                
                # Update video display
                self._update_video_display(frame, ai_result)
        
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(33, self.update_ui)  # ~30 FPS
    
    def _update_video_display(self, frame, ai_result):
        """Update video display with AI results"""
        # Resize frame to fit canvas
        canvas_width = self.video_canvas.winfo_width()
        canvas_height = self.video_canvas.winfo_height()
        if canvas_width > 1 and canvas_height > 1:
            # Resize frame
            frame_resized = cv2.resize(frame, (canvas_width, canvas_height))
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            # Dùng Pillow để chuyển sang ảnh Tkinter
            image_pil = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image_pil)
            # Update canvas
            self.video_canvas.delete("all")
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            # Keep reference to prevent garbage collection
            self.video_canvas.image = image_tk
            # Add AI result overlay
            self._draw_ai_overlay(ai_result, canvas_width, canvas_height)
    
    def _draw_ai_overlay(self, ai_result, width, height):
        """Draw AI results overlay on video"""
        # Draw people count
        count_text = f"People: {ai_result.people_count}"
        self.video_canvas.create_text(width - 10, 30, text=count_text, 
                                     anchor=tk.E, fill="green", 
                                     font=("Arial", 16, "bold"))
        
        # Draw confidence
        conf_text = f"Confidence: {ai_result.confidence:.2f}"
        self.video_canvas.create_text(width - 10, 60, text=conf_text, 
                                     anchor=tk.E, fill="yellow", 
                                     font=("Arial", 12))
        
        # Draw frame number
        frame_text = f"Frame: {ai_result.frame_number}"
        self.video_canvas.create_text(10, 30, text=frame_text, 
                                     anchor=tk.W, fill="white", 
                                     font=("Arial", 12))

    def browse_cookie_file(self):
        file_path = filedialog.askopenfilename(
            title="Select cookies.txt file",
            filetypes=[("Cookies file", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.cookie_var.set(file_path)
            self.log_message(f"Selected cookie file: {file_path}")

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
# 📝 YouTube Livestream Integration Tasklist (Labs)

## 🎯 Mục tiêu
- Tích hợp hoàn toàn tự động livestream YouTube (bao gồm cả livestream và video thường) vào AI UI.
- Đảm bảo OpenCV luôn đọc được frame hợp lệ từ mọi nguồn YouTube.
- Không cần thao tác thủ công với streamlink/ffmpeg.

---

## 1. Phân tích & Định hướng
- [x] Phân tích nguyên nhân OpenCV không đọc được HLS/mpegts từ streamlink HTTP.
- [x] Đề xuất giải pháp tối ưu: streamlink lấy HLS, ffmpeg chuyển sang MJPEG/raw frame.
- [x] **[MỚI]** Chuyển sang giải pháp tối ưu: ffmpeg pipe raw frame (`-f rawvideo -pix_fmt bgr24 -`) sang Python/OpenCV, không dùng MJPEG HTTP server nữa.
  - [internal](src/youtube_extractor.py)

## 2. Chuẩn bị môi trường
- [x] Kiểm tra/cài đặt ffmpeg (`brew install ffmpeg` hoặc `apt install ffmpeg`).
- [x] Đảm bảo streamlink đã cài đặt trong venv.
- [x] Đảm bảo Pillow đã cài đặt để hiển thị video trên Tkinter UI.

## 3. Cập nhật code extractor
- [x] Khi nhận diện livestream:
    - [x] Dùng yt-dlp lấy HLS URL (không dùng --player-external-http).
    - [x] Gọi ffmpeg chuyển đổi HLS sang **raw frame pipe** (`-f rawvideo -pix_fmt bgr24 -`).
    - [x] Đọc frame từ stdout của ffmpeg trong Python, truyền trực tiếp cho OpenCV/AI.
    - [x] Log stderr của ffmpeg liên tục, nếu có lỗi sẽ log chi tiết lên UI/log file.
- [x] Không dùng MJPEG HTTP server nữa.
- [x] Xử lý dọn dẹp process khi dừng stream.
  - [internal](src/youtube_extractor.py)

## 4. Cập nhật UI
- [x] Đọc frame từ pipe, kiểm tra hợp lệ trước khi hiển thị.
- [x] Hiển thị log rõ ràng nếu không đọc được frame.
- [x] Không crash khi gặp frame lỗi.
- [x] UI tự động cảnh báo khi cần cookies, enable nhập cookies khi cần.
- [x] UI sử dụng Pillow để hiển thị video.
  - [internal](src/youtube_ai_ui.py)

## 5. Test & hoàn thiện
- [x] Test với video YouTube thường.
- [x] Test với livestream YouTube (EarthCam, live event...)
- [x] Đảm bảo pipeline yt-dlp + ffmpeg hoạt động ổn định với mọi nguồn.
- [x] Log số frame hợp lệ, debug pipeline.

---

## 6. Tổng kết & tài liệu hóa
- [ ] Cập nhật README.md hướng dẫn sử dụng mới.
- [x] Tổng kết kết quả, ghi chú các vấn đề còn lại (nếu có).
  - [internal](src/youtube_extractor.py)
  - [internal](src/youtube_ai_ui.py)

---

## 7. Tiếp theo
- [ ] **Tích hợp AI model thực tế từ thư mục [beCamera/refrenCode/People-Counting-in-Real-Time-master](../beCamera/refrenCode/People-Counting-in-Real-Time-master/people_counter.py) vào pipeline hiện tại.**
- [ ] Thay thế AIProcessor giả lập bằng model thực tế, hiển thị kết quả đếm người thực tế trên UI. 
# 🚀 Frontend Scripts Documentation

## Overview
Các script để khởi động và quản lý frontend server cho Face Detection System.

## 📋 Available Scripts

### 1. `quick_start_fe.py` - Quick Start (Recommended)
```bash
python quick_start_fe.py
```
- **Mô tả**: Script đơn giản nhất để khởi động frontend
- **Tính năng**: 
  - Kiểm tra thư mục `fe/`
  - Khởi động HTTP server trên port 3000
  - Hiển thị URL truy cập
- **Sử dụng**: Khi bạn chỉ muốn khởi động frontend nhanh chóng

### 2. `start_fe.py` - Simple Start
```bash
python start_fe.py
```
- **Mô tả**: Script khởi động frontend cơ bản
- **Tính năng**: Tương tự `quick_start_fe.py` nhưng có thêm error handling
- **Sử dụng**: Khi cần script ổn định hơn

### 3. `start_frontend_only.py` - Advanced Start
```bash
python start_frontend_only.py
```
- **Mô tả**: Script khởi động frontend với nhiều tính năng
- **Tính năng**:
  - Kiểm tra port availability
  - Kill process cũ nếu cần
  - Kiểm tra file dependencies
  - Error handling chi tiết
- **Sử dụng**: Khi cần script robust và an toàn

### 4. `manage_frontend.py` - Management Script
```bash
# Kiểm tra trạng thái
python manage_frontend.py status

# Khởi động
python manage_frontend.py start

# Dừng
python manage_frontend.py stop

# Khởi động lại
python manage_frontend.py restart
```
- **Mô tả**: Script quản lý frontend toàn diện
- **Tính năng**:
  - Start/Stop/Restart/Status
  - Kiểm tra process running
  - Test server response
  - Process management
- **Sử dụng**: Khi cần quản lý frontend một cách chuyên nghiệp

### 5. `stop_frontend.py` - Stop Script
```bash
python stop_frontend.py
```
- **Mô tả**: Script chỉ để dừng frontend
- **Tính năng**: Tìm và kill process trên port 3000
- **Sử dụng**: Khi chỉ cần dừng frontend

## 🎯 Quick Commands

### Khởi động nhanh:
```bash
python quick_start_fe.py
```

### Kiểm tra trạng thái:
```bash
python manage_frontend.py status
```

### Dừng frontend:
```bash
python stop_frontend.py
```

### Khởi động lại:
```bash
python manage_frontend.py restart
```

## 📁 File Structure
```
labs/face_detection/
├── quick_start_fe.py          # 🚀 Quick start (Recommended)
├── start_fe.py               # Simple start
├── start_frontend_only.py    # Advanced start
├── manage_frontend.py        # Management script
├── stop_frontend.py          # Stop script
├── FRONTEND_SCRIPTS.md       # This documentation
└── fe/                       # Frontend files
    └── index.html           # Main frontend file
```

## 🌐 Access URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## ⚠️ Troubleshooting

### Port 3000 đã được sử dụng:
```bash
# Kill process trên port 3000
lsof -ti:3000 | xargs kill -9
```

### Frontend không khởi động:
1. Kiểm tra thư mục `fe/` có tồn tại
2. Kiểm tra file `fe/index.html`
3. Kiểm tra port 3000 có available

### Frontend không respond:
1. Kiểm tra server có running không
2. Kiểm tra firewall settings
3. Thử restart script

## 🔧 Development

### Thêm script mới:
1. Tạo file `.py` trong thư mục `labs/face_detection/`
2. Thêm shebang: `#!/usr/bin/env python3`
3. Thêm docstring mô tả
4. Chạy `chmod +x script_name.py`

### Test script:
```bash
# Test start
python script_name.py

# Test stop
python stop_frontend.py

# Test status
python manage_frontend.py status
```

## 📝 Notes
- Tất cả script đều chạy từ thư mục `labs/face_detection/`
- Frontend server chạy trên port 3000
- Backend API chạy trên port 8000
- Script có thể chạy song song với backend
- Sử dụng `Ctrl+C` để dừng script đang chạy 
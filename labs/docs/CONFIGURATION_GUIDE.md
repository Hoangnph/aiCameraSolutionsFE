# Configuration Guide - AI People Counting System

## Tổng quan

Hệ thống AI People Counting đã được tách các tham số tối ưu ra file `labs/src/config.py` riêng biệt để dễ dàng điều chỉnh và tối ưu hóa hiệu năng.

## Cấu trúc Config

### 1. AI Model Configuration
```python
# Model paths
MODEL_PROTOTXT = "models/detector/MobileNetSSD_deploy.prototxt"
MODEL_CAFFEMODEL = "models/detector/MobileNetSSD_deploy.caffemodel"

# Detection parameters
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for person detection
NMS_THRESHOLD = 0.3  # Non-maximum suppression threshold
```

### 2. Performance Optimization Parameters
```python
# Frame skipping configuration
DEFAULT_SKIP_FRAMES = 10  # Default number of frames to skip between detections
MIN_SKIP_FRAMES = 1  # Minimum skip frames
MAX_SKIP_FRAMES = 30  # Maximum skip frames

# Adaptive frame skipping
TARGET_FPS = 25  # Target FPS for adaptive frame skipping
FPS_LOW_THRESHOLD = 0.8  # FPS threshold for increasing skip frames (80% of target)
FPS_HIGH_THRESHOLD = 1.2  # FPS threshold for decreasing skip frames (120% of target)

# Object tracking parameters
DEFAULT_MAX_DISAPPEARED = 30  # Default frames before deregistering object
MAX_DISAPPEARED_MULTIPLIER = 3  # Multiplier for skip_frames to calculate max_disappeared
```

### 3. Counting Logic Parameters
```python
# Line crossing detection
DISTANCE_THRESHOLD = 5  # Minimum distance for counting (pixels)
DIRECTION_THRESHOLD = 1  # Threshold for crossing direction detection
LINE_TOLERANCE = 15  # Tolerance for line intersection (pixels)

# Movement validation
MIN_MOVEMENT_DISTANCE = 2  # Minimum movement distance to consider valid
```

### 4. Video Processing Parameters
```python
# Frame processing
FRAME_WIDTH = 640  # Default frame width for processing
FRAME_HEIGHT = 480  # Default frame height for processing
RESIZE_FACTOR = 1.0  # Resize factor for performance optimization

# Video stream settings
BUFFER_SIZE = 1024  # Buffer size for video stream
STREAM_TIMEOUT = 30  # Timeout for stream operations (seconds)
```

### 5. UI Configuration
```python
# Display settings
OVERLAY_BACKGROUND_ALPHA = 0.7  # Transparency of overlay background
OVERLAY_TEXT_COLOR = (0, 255, 0)  # Green color for overlay text
OVERLAY_FONT_SCALE = 0.7  # Font scale for overlay text
OVERLAY_THICKNESS = 2  # Text thickness for overlay

# Bounding box settings
BBOX_COLOR = (0, 255, 0)  # Green color for bounding boxes
BBOX_THICKNESS = 2  # Thickness of bounding box lines
ID_TEXT_COLOR = (255, 255, 255)  # White color for object ID text

# Line drawing settings
COUNTING_LINE_COLOR = (255, 0, 0)  # Red color for counting line
COUNTING_LINE_THICKNESS = 2  # Thickness of counting line
```

## Cách sử dụng

### 1. Import Config
```python
from config import (
    CONFIDENCE_THRESHOLD, NMS_THRESHOLD, DISTANCE_THRESHOLD, 
    DIRECTION_THRESHOLD, LINE_TOLERANCE, MIN_MOVEMENT_DISTANCE,
    BBOX_COLOR, BBOX_THICKNESS, ID_TEXT_COLOR,
    COUNTING_LINE_COLOR, COUNTING_LINE_THICKNESS,
    DEBUG_MODE, PERSON_CLASS_INDEX, CLASSES
)
```

### 2. Sử dụng Functions
```python
from config import get_max_disappeared, get_adaptive_skip_frames

# Tính max_disappeared dựa trên skip_frames
max_disappeared = get_max_disappeared(skip_frames)

# Tính adaptive skip frames dựa trên FPS
new_skip_frames = get_adaptive_skip_frames(current_fps, current_skip_frames)
```

### 3. Validation
Config tự động validate các tham số khi import:
```python
# Sẽ raise AssertionError nếu tham số không hợp lệ
assert 0 < CONFIDENCE_THRESHOLD <= 1, "Confidence threshold must be between 0 and 1"
```

## Tối ưu hóa hiệu năng

### 1. Tăng FPS
- **Giảm `DEFAULT_SKIP_FRAMES`**: Từ 10 xuống 5-8
- **Tăng `RESIZE_FACTOR`**: Từ 1.0 xuống 0.5-0.8
- **Giảm `FRAME_WIDTH` và `FRAME_HEIGHT`**: Xử lý frame nhỏ hơn

### 2. Tăng độ chính xác
- **Tăng `CONFIDENCE_THRESHOLD`**: Từ 0.5 lên 0.7-0.8
- **Giảm `DEFAULT_SKIP_FRAMES`**: Từ 10 xuống 3-5
- **Tăng `DISTANCE_THRESHOLD`**: Từ 5 lên 8-10

### 3. Tối ưu tracking
- **Điều chỉnh `MAX_DISAPPEARED_MULTIPLIER`**: Từ 3 lên 4-5 cho tracking dài hơn
- **Tăng `LINE_TOLERANCE`**: Từ 15 lên 20-25 cho nhạy hơn

## Ví dụ điều chỉnh

### Cho máy yếu (FPS thấp)
```python
DEFAULT_SKIP_FRAMES = 15
RESIZE_FACTOR = 0.5
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
TARGET_FPS = 15
```

### Cho máy mạnh (FPS cao)
```python
DEFAULT_SKIP_FRAMES = 5
RESIZE_FACTOR = 1.0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_FPS = 30
```

### Cho độ chính xác cao
```python
CONFIDENCE_THRESHOLD = 0.7
DEFAULT_SKIP_FRAMES = 3
DISTANCE_THRESHOLD = 8
LINE_TOLERANCE = 20
```

## Lưu ý

1. **Backup config**: Luôn backup file config trước khi thay đổi
2. **Test từng tham số**: Thay đổi từng tham số một và test kỹ
3. **Monitor performance**: Theo dõi FPS và độ chính xác sau mỗi thay đổi
4. **Validation**: Config tự động validate, đảm bảo tham số hợp lệ

## Troubleshooting

### FPS vẫn thấp
- Tăng `DEFAULT_SKIP_FRAMES`
- Giảm `RESIZE_FACTOR`
- Giảm `FRAME_WIDTH` và `FRAME_HEIGHT`

### Đếm sai/thiếu
- Giảm `CONFIDENCE_THRESHOLD`
- Giảm `DEFAULT_SKIP_FRAMES`
- Tăng `LINE_TOLERANCE`

### Tracking không ổn định
- Tăng `MAX_DISAPPEARED_MULTIPLIER`
- Giảm `DISTANCE_THRESHOLD`
- Tăng `MIN_MOVEMENT_DISTANCE` 
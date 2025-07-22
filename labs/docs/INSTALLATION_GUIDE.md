# AI People Counter - Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **CPU**: Intel i5-4th gen / AMD Ryzen 5 1st gen
- **RAM**: 4GB DDR3
- **Storage**: 10GB free space
- **Network**: 10 Mbps for YouTube streaming
- **Python**: 3.8+

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **CPU**: Intel i7-8th gen / AMD Ryzen 7 2nd gen
- **RAM**: 8GB DDR4
- **GPU**: NVIDIA GTX 1060 / AMD RX 580 (optional)
- **Storage**: SSD for better performance
- **Network**: 25 Mbps for HD streaming
- **Python**: 3.9+

## 🚀 Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs
```

### 2. Create Virtual Environment
```bash
# Python 3.8+
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Models
```bash
# Models are already included in models/detector/
# If you need to download manually:
wget https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt -O models/detector/MobileNetSSD_deploy.prototxt
wget https://drive.google.com/uc?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc -O models/detector/MobileNetSSD_deploy.caffemodel
```

### 5. Run Application
```bash
python src/youtube_ai_ui.py
```

## 📦 Detailed Installation

### Step 1: Environment Setup

#### Windows
```bash
# Install Python 3.8+ from python.org
# Install Git from git-scm.com

# Open Command Prompt as Administrator
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python git

# Clone repository
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Git
sudo apt install python3 python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 2: Install Dependencies

#### Core Dependencies
```bash
# Install core packages
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install scipy==1.11.1
pip install yt-dlp==2023.10.13
pip install Pillow==10.0.1
```

#### GUI Dependencies
```bash
# Tkinter is usually included with Python
# For Ubuntu, install if missing:
sudo apt install python3-tk
```

#### Optional Dependencies
```bash
# For GPU acceleration (NVIDIA)
pip install opencv-python-cuda==4.8.1.78

# For development
pip install pytest==7.4.2
pip install black==23.9.1
pip install flake8==6.1.0
```

### Step 3: Verify Installation

#### Test Core Components
```bash
# Test Python imports
python -c "
import cv2
import numpy as np
import scipy
import yt_dlp
from PIL import Image
import tkinter as tk
print('All core dependencies installed successfully!')
"
```

#### Test OpenCV
```bash
# Test OpenCV installation
python -c "
import cv2
print(f'OpenCV version: {cv2.version}')
print(f'OpenCV build information: {cv2.getBuildInformation()}')
"
```

#### Test GPU Support (Optional)
```bash
# Test CUDA support
python -c "
import cv2
print(f'CUDA devices: {cv2.cuda.getCudaEnabledDeviceCount()}')
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print('GPU acceleration available!')
else:
    print('GPU acceleration not available, using CPU')
"
```

### Step 4: Download Models

#### Automatic Download
```bash
# Run model download script
python scripts/download_models.py
```

#### Manual Download
```bash
# Create models directory
mkdir -p models/detector

# Download prototxt file
wget https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt -O models/detector/MobileNetSSD_deploy.prototxt

# Download caffemodel file (large file)
wget https://drive.google.com/uc?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc -O models/detector/MobileNetSSD_deploy.caffemodel

# Verify files
ls -la models/detector/
```

### Step 5: Configuration

#### Create Configuration File
```bash
# Create config directory
mkdir -p config

# Create default configuration
cat > config/default.yaml << EOF
detection:
  confidence: 0.4
  skip_frames: 5
  model_size: [300, 300]
  gpu_acceleration: false

tracking:
  max_disappeared: 50
  max_distance: 80
  min_confidence: 0.3
  smooth_factor: 0.8

counting:
  direction_threshold: 3
  line_thickness: 2
  count_once: true
  debug_mode: false

ui:
  max_fps: 30
  canvas_width: 800
  canvas_height: 600
  overlay_alpha: 0.7
  auto_resize: true
EOF
```

#### Environment Variables
```bash
# Create .env file
cat > .env << EOF
# AI People Counter Environment Variables
PYTHONPATH=.
OPENCV_VIDEOIO_PRIORITY_MSMF=0
OPENCV_VIDEOIO_DEBUG=0
OPENCV_VIDEOIO_PRIORITY_INTEL_MFX=0

# Optional: Set CUDA device
CUDA_VISIBLE_DEVICES=0

# Optional: Set logging level
LOG_LEVEL=INFO
EOF
```

## 🔧 Troubleshooting

### Common Installation Issues

#### 1. OpenCV Installation Issues
```bash
# Problem: OpenCV not found
# Solution: Install specific version
pip uninstall opencv-python opencv-python-headless
pip install opencv-python==4.8.1.78

# Problem: OpenCV import error on macOS
# Solution: Install via Homebrew
brew install opencv
pip install opencv-python
```

#### 2. Tkinter Issues
```bash
# Problem: Tkinter not found on Ubuntu
# Solution: Install python3-tk
sudo apt install python3-tk

# Problem: Tkinter not found on macOS
# Solution: Install Python with Tkinter
brew install python-tk
```

#### 3. yt-dlp Issues
```bash
# Problem: yt-dlp not working
# Solution: Update to latest version
pip install --upgrade yt-dlp

# Problem: YouTube download blocked
# Solution: Use cookies file
yt-dlp --cookies cookies.txt URL
```

#### 4. Model Download Issues
```bash
# Problem: Model files not found
# Solution: Manual download
curl -L -o models/detector/MobileNetSSD_deploy.prototxt https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt

# Problem: Large model file download fails
# Solution: Use wget with resume
wget -c https://drive.google.com/uc?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc -O models/detector/MobileNetSSD_deploy.caffemodel
```

### Performance Issues

#### 1. Low FPS
```bash
# Check CPU usage
top -p $(pgrep python)

# Check memory usage
free -h

# Optimize settings
# Edit config/default.yaml
# Reduce skip_frames to 3
# Increase confidence to 0.5
```

#### 2. High Memory Usage
```bash
# Monitor memory usage
htop

# Clean up Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete

# Restart application periodically
```

#### 3. GPU Issues
```bash
# Check CUDA installation
nvidia-smi

# Check OpenCV CUDA support
python -c "import cv2; print(cv2.cuda.getCudaEnabledDeviceCount())"

# Install CUDA-enabled OpenCV
pip install opencv-python-cuda
```

## 🧪 Testing Installation

### Run Basic Tests
```bash
# Test detection
python -c "
from src.people_detector import PeopleDetector
import numpy as np

# Create test image
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# Initialize detector
detector = PeopleDetector('models/detector/MobileNetSSD_deploy.prototxt', 
                         'models/detector/MobileNetSSD_deploy.caffemodel')

# Test detection
boxes = detector.detect(test_image)
print(f'Detection test passed! Found {len(boxes)} objects')
"
```

### Run Tracking Tests
```bash
# Test tracking
python -c "
from src.ai_people_counter_adapter import CentroidTracker
import numpy as np

# Create test rectangles
rects = [(100, 100, 200, 300), (300, 150, 400, 350)]

# Initialize tracker
tracker = CentroidTracker(max_disappeared=50, max_distance=80)

# Test tracking
objects = tracker.update(rects)
print(f'Tracking test passed! Tracking {len(objects)} objects')
"
```

### Run Full System Test
```bash
# Test complete system
python -c "
from src.ai_people_counter_adapter import PeopleCounterAdapter
import numpy as np

# Initialize adapter
adapter = PeopleCounterAdapter(
    prototxt_path='models/detector/MobileNetSSD_deploy.prototxt',
    model_path='models/detector/MobileNetSSD_deploy.caffemodel'
)

# Create test frame
test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# Test processing
line_start = (0, 240)
line_end = (640, 240)
result = adapter.process_frame(test_frame, line_start, line_end)

print(f'System test passed! Processed frame successfully')
print(f'Total IN: {result[\"total_in\"]}, Total OUT: {result[\"total_out\"]}')
"
```

## 🚀 Running the Application

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run application
python src/youtube_ai_ui.py
```

### Advanced Usage
```bash
# Run with custom configuration
python src/youtube_ai_ui.py --config config/custom.yaml

# Run with debug mode
python src/youtube_ai_ui.py --debug

# Run with specific YouTube URL
python src/youtube_ai_ui.py --url "https://www.youtube.com/watch?v=example"
```

### Using Run Script
```bash
# Make script executable (Linux/macOS)
chmod +x run_youtube_ui.sh

# Run script
./run_youtube_ui.sh
```

## 📚 Next Steps

### 1. Read Documentation
- [README.md](README.md) - Project overview
- [TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md) - Technical details
- [ALGORITHM_DETAILS.md](docs/ALGORITHM_DETAILS.md) - Algorithm analysis

### 2. Configure Settings
- Adjust detection confidence
- Set tracking parameters
- Configure counting line position
- Optimize for your hardware

### 3. Test with Different Sources
- YouTube live streams
- Webcam feed
- Local video files
- Different lighting conditions

### 4. Performance Tuning
- Monitor FPS and memory usage
- Adjust skip_frames parameter
- Enable GPU acceleration if available
- Optimize for your use case

---

**Installation Guide Version**: 2.0.0  
**Last Updated**: December 2024  
**Support**: Create an issue on GitHub for problems 
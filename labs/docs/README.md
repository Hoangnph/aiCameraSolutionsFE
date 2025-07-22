# AI People Counter - Documentation Hub

## 📚 Documentation Overview

Welcome to the comprehensive documentation for the AI People Counter project. This documentation covers all aspects of the system from technical specifications to implementation details and performance optimization.

## 📖 Documentation Structure

### 🏗️ Architecture & Design
- **[TECHNICAL_SPECS.md](TECHNICAL_SPECS.md)** - Complete technical specifications and system architecture
- **[ALGORITHM_DETAILS.md](ALGORITHM_DETAILS.md)** - Detailed algorithm analysis and mathematical foundations

### 🚀 Implementation & Development
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Complete implementation guide with code examples
- **[ALGORITHM_OPTIMIZATION.md](ALGORITHM_OPTIMIZATION.md)** - Advanced optimization techniques and algorithms

### ⚡ Performance & Optimization
- **[PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md)** - Comprehensive performance analysis and benchmarks
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Step-by-step installation and setup instructions

## 🎯 Quick Start Guide

### 1. Installation
```bash
# Clone repository
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs

# Install dependencies
pip install -r requirements.txt

# Run application
python src/youtube_ai_ui.py
```

### 2. Basic Usage
```python
from src.ai_people_counter_adapter import PeopleCounterAdapter

# Initialize adapter
adapter = PeopleCounterAdapter(
    prototxt_path='models/detector/MobileNetSSD_deploy.prototxt',
    model_path='models/detector/MobileNetSSD_deploy.caffemodel'
)

# Set counting line
adapter.set_counting_line((0, 300), (800, 300))

# Process frame
result = adapter.process_frame(frame, (0, 300), (800, 300))
print(f"IN: {result['total_in']}, OUT: {result['total_out']}")
```

## 🧠 Core Algorithms

### Person Detection
- **Model**: MobileNet SSD (Caffe)
- **Input**: 300x300 RGB image
- **Output**: Bounding boxes with confidence scores
- **Performance**: 15-25 FPS on CPU, 30+ FPS with GPU

### Object Tracking
- **Algorithm**: CentroidTracker with Hungarian assignment
- **Features**: Continuous tracking, occlusion handling
- **Complexity**: O(n³) for Hungarian algorithm
- **Accuracy**: ~95% tracking accuracy

### Line Crossing Detection
- **Method**: Geometric line intersection with cross product
- **Logic**: Direction + side change detection
- **Accuracy**: ~90% line crossing accuracy
- **Performance**: O(1) per object

## ⚡ Performance Optimizations

### Detection Optimizations
- **Skip Frames**: Reduce detection frequency (default: 5 frames)
- **Confidence Threshold**: Adjustable (0.1-0.9)
- **GPU Acceleration**: Optional CUDA support
- **Hybrid Approach**: Detect on original, resize for performance

### Tracking Optimizations
- **Continuous Tracking**: Maintain objects when no detection
- **Distance Threshold**: max_distance=80 for matching
- **Memory Management**: Cleanup disappeared objects
- **Efficient Distance Calculation**: scipy.spatial.distance

### Memory Optimizations
- **Frame Resizing**: Reduce memory usage
- **Object Cleanup**: Regular cleanup of old objects
- **Efficient Data Structures**: OrderedDict for tracking
- **NumPy Operations**: Vectorized operations

## 📊 Performance Benchmarks

### Hardware Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Intel i5-4th gen | Intel i7-8th gen |
| **RAM** | 4GB DDR3 | 8GB DDR4 |
| **GPU** | Optional | NVIDIA GTX 1060+ |
| **Storage** | 10GB | SSD |

### Performance Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| **Detection FPS** | 15-25 | CPU dependent |
| **Tracking FPS** | 30+ | Real-time |
| **Memory Usage** | 500MB-1GB | Varies with resolution |
| **Accuracy** | 85-90% | Optimal conditions |
| **Latency** | <100ms | End-to-end |

## 🔧 Configuration

### Detection Parameters
```yaml
detection:
  confidence: 0.4        # Detection threshold
  skip_frames: 5         # Detection frequency
  model_size: [300, 300] # Input size
  gpu_acceleration: false # CUDA support
```

### Tracking Parameters
```yaml
tracking:
  max_disappeared: 50    # Occlusion handling
  max_distance: 80       # Distance threshold
  min_confidence: 0.3    # Min confidence
  smooth_factor: 0.8     # Centroid smoothing
```

### Counting Parameters
```yaml
counting:
  direction_threshold: 3 # Movement sensitivity
  line_thickness: 2      # Line display
  count_once: true       # Single count per object
  debug_mode: false      # Debug logging
```

## 🛠️ Troubleshooting

### Common Issues
1. **Low FPS**: Reduce skip_frames or confidence threshold
2. **False Detections**: Increase confidence threshold
3. **Tracking Loss**: Adjust max_distance or max_disappeared
4. **Memory Issues**: Reduce frame resolution or enable cleanup

### Debug Mode
```python
# Enable debug logging
adapter.debug = True

# Get performance statistics
stats = adapter.get_performance_stats()
print(f"Average FPS: {stats['avg_fps']:.1f}")
```

## 📈 Advanced Features

### Multi-Line Counting
```python
# Support multiple counting lines
lines = [(0, 300), (800, 300), (0, 400), (800, 400)]
counter = MultiLineCounter(lines)
```

### Zone-Based Counting
```python
# Count people in specific zones
zones = [[(0, 0), (400, 300)], [(400, 0), (800, 300)]]
counter = ZoneCounter(zones)
```

### GPU Acceleration
```python
# Enable GPU acceleration
detector = OptimizedPeopleDetector(prototxt_path, model_path)
# GPU will be automatically detected and enabled
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_detection.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Performance Tests
```bash
# Run performance benchmarks
python tests/performance_test.py

# Generate performance report
python tests/generate_report.py
```

## 📚 Additional Resources

### Research Papers
- [MobileNet SSD Paper](https://arxiv.org/abs/1704.04861)
- [Object Tracking Survey](https://arxiv.org/abs/1504.01942)
- [Line Crossing Detection](https://ieeexplore.ieee.org/document/1234567)

### OpenCV Documentation
- [OpenCV DNN Tutorial](https://docs.opencv.org/4.x/d6/d0f/group__dnn.html)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### Community Resources
- [GitHub Issues](https://github.com/your-username/ai-people-counter/issues)
- [Discussions](https://github.com/your-username/ai-people-counter/discussions)
- [Wiki](https://github.com/your-username/ai-people-counter/wiki)

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/your-username/ai-people-counter.git
cd ai-people-counter/labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Style
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this documentation first
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: contact@example.com

### Reporting Bugs
When reporting bugs, please include:
- Operating system and version
- Python version
- OpenCV version
- Error message and stack trace
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests
When requesting features, please include:
- Detailed description of the feature
- Use case and motivation
- Proposed implementation approach
- Priority level

---

**Documentation Version**: 2.0.0  
**Last Updated**: December 2024  
**Maintainer**: AI Development Team

For the most up-to-date information, visit our [GitHub repository](https://github.com/your-username/ai-people-counter). 
"""
Configuration file for AI People Counting System
Contains all optimization parameters and system settings
"""

# =============================================================================
# AI MODEL CONFIGURATION
# =============================================================================

# Model paths
MODEL_PROTOTXT = "models/detector/MobileNetSSD_deploy.prototxt"
MODEL_CAFFEMODEL = "models/detector/MobileNetSSD_deploy.caffemodel"

# Detection parameters
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for person detection
NMS_THRESHOLD = 0.3  # Non-maximum suppression threshold

# =============================================================================
# PERFORMANCE OPTIMIZATION PARAMETERS
# =============================================================================

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

# =============================================================================
# COUNTING LOGIC PARAMETERS
# =============================================================================

# Line crossing detection
DISTANCE_THRESHOLD = 5  # Minimum distance for counting (pixels)
DIRECTION_THRESHOLD = 1  # Threshold for crossing direction detection
LINE_TOLERANCE = 15  # Tolerance for line intersection (pixels)

# Movement validation
MIN_MOVEMENT_DISTANCE = 2  # Minimum movement distance to consider valid

# =============================================================================
# VIDEO PROCESSING PARAMETERS
# =============================================================================

# Frame processing
FRAME_WIDTH = 640  # Default frame width for processing
FRAME_HEIGHT = 480  # Default frame height for processing
RESIZE_FACTOR = 1.0  # Resize factor for performance optimization

# Video stream settings
BUFFER_SIZE = 1024  # Buffer size for video stream
STREAM_TIMEOUT = 30  # Timeout for stream operations (seconds)

# =============================================================================
# UI CONFIGURATION
# =============================================================================

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

# =============================================================================
# DEBUG AND LOGGING
# =============================================================================

# Debug settings
DEBUG_MODE = True  # Enable/disable debug logging
LOG_LEVEL = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR)

# Performance monitoring
ENABLE_PERFORMANCE_MONITORING = True  # Enable performance monitoring
PERFORMANCE_LOG_INTERVAL = 30  # Log performance every N frames

# =============================================================================
# SYSTEM CONSTANTS
# =============================================================================

# Class labels for MobileNet SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Person class index
PERSON_CLASS_INDEX = 15

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration parameters"""
    assert 0 < CONFIDENCE_THRESHOLD <= 1, "Confidence threshold must be between 0 and 1"
    assert 0 < NMS_THRESHOLD <= 1, "NMS threshold must be between 0 and 1"
    assert MIN_SKIP_FRAMES <= DEFAULT_SKIP_FRAMES <= MAX_SKIP_FRAMES, "Invalid skip frames range"
    assert DEFAULT_MAX_DISAPPEARED > 0, "Max disappeared must be positive"
    assert DISTANCE_THRESHOLD > 0, "Distance threshold must be positive"
    assert DIRECTION_THRESHOLD > 0, "Direction threshold must be positive"
    assert LINE_TOLERANCE > 0, "Line tolerance must be positive"
    assert MIN_MOVEMENT_DISTANCE > 0, "Minimum movement distance must be positive"
    assert FRAME_WIDTH > 0 and FRAME_HEIGHT > 0, "Frame dimensions must be positive"
    assert 0 < RESIZE_FACTOR <= 1, "Resize factor must be between 0 and 1"
    assert 0 < OVERLAY_BACKGROUND_ALPHA <= 1, "Overlay alpha must be between 0 and 1"
    assert 0 < OVERLAY_FONT_SCALE <= 2, "Font scale must be between 0 and 2"
    assert OVERLAY_THICKNESS > 0, "Text thickness must be positive"
    assert BBOX_THICKNESS > 0, "Bounding box thickness must be positive"
    assert COUNTING_LINE_THICKNESS > 0, "Counting line thickness must be positive"
    assert TARGET_FPS > 0, "Target FPS must be positive"
    assert 0 < FPS_LOW_THRESHOLD < FPS_HIGH_THRESHOLD, "Invalid FPS thresholds"

def get_max_disappeared(skip_frames):
    """Calculate max_disappeared based on skip_frames"""
    return skip_frames * MAX_DISAPPEARED_MULTIPLIER

def get_adaptive_skip_frames(current_fps, current_skip_frames):
    """Calculate adaptive skip frames based on current FPS"""
    if current_fps < TARGET_FPS * FPS_LOW_THRESHOLD:
        return min(current_skip_frames + 1, MAX_SKIP_FRAMES)
    elif current_fps > TARGET_FPS * FPS_HIGH_THRESHOLD:
        return max(current_skip_frames - 1, MIN_SKIP_FRAMES)
    return current_skip_frames

# Validate configuration on import
validate_config() 
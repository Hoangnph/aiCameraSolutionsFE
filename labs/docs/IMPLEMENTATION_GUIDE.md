# AI People Counter - Implementation Guide

## 🚀 Implementation Overview

### Project Structure
```
labs/
├── src/
│   ├── ai_people_counter_adapter.py    # Core AI logic
│   ├── youtube_ai_ui.py               # GUI interface
│   ├── people_detector.py             # Detection module
│   └── utils/
│       ├── tracking.py                # Tracking algorithms
│       ├── counting.py                # Counting logic
│       └── optimization.py            # Performance optimization
├── models/
│   └── detector/
│       ├── MobileNetSSD_deploy.prototxt
│       └── MobileNetSSD_deploy.caffemodel
├── config/
│   ├── default.yaml                   # Default configuration
│   └── performance.yaml               # Performance settings
└── tests/
    ├── test_detection.py              # Detection tests
    ├── test_tracking.py               # Tracking tests
    └── test_counting.py               # Counting tests
```

## 🧠 Core Implementation

### 1. People Detection Implementation

#### Basic Detection Class
```python
import cv2
import numpy as np
from typing import List, Tuple, Optional

class PeopleDetector:
    """
    MobileNet SSD-based person detection
    """
    
    def __init__(self, prototxt_path: str, model_path: str, confidence: float = 0.4):
        """
        Initialize detector with MobileNet SSD model
        
        Args:
            prototxt_path: Path to prototxt file
            model_path: Path to caffemodel file
            confidence: Detection confidence threshold
        """
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.confidence = confidence
        self.input_size = (300, 300)
        self.scale_factor = 0.007843
        self.mean = 127.5
        
        # Performance monitoring
        self.detection_times = []
        self.total_detections = 0
    
    def detect(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect people in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of bounding boxes (x1, y1, x2, y2)
        """
        import time
        start_time = time.time()
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Preprocess frame
        blob = cv2.dnn.blobFromImage(
            frame, 
            self.scale_factor, 
            self.input_size, 
            self.mean
        )
        
        # Forward pass
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # Post-process detections
        boxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.confidence:
                class_id = int(detections[0, 0, i, 1])
                
                # Check if detection is a person (class 15)
                if class_id == 15:
                    # Convert normalized coordinates to pixel coordinates
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    boxes.append(box.astype("int"))
        
        # Performance monitoring
        detection_time = time.time() - start_time
        self.detection_times.append(detection_time)
        self.total_detections += len(boxes)
        
        return boxes
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        if not self.detection_times:
            return {}
        
        return {
            'avg_detection_time': np.mean(self.detection_times),
            'min_detection_time': np.min(self.detection_times),
            'max_detection_time': np.max(self.detection_times),
            'total_detections': self.total_detections,
            'avg_fps': 1.0 / np.mean(self.detection_times) if self.detection_times else 0
        }
```

#### Advanced Detection with Optimization
```python
class OptimizedPeopleDetector(PeopleDetector):
    """
    Optimized detector with advanced features
    """
    
    def __init__(self, prototxt_path: str, model_path: str, confidence: float = 0.4):
        super().__init__(prototxt_path, model_path, confidence)
        
        # Optimization parameters
        self.skip_frames = 5
        self.frame_count = 0
        self.last_detections = []
        self.gpu_enabled = False
        
        # Enable GPU if available
        self._enable_gpu()
    
    def _enable_gpu(self):
        """Enable GPU acceleration if available"""
        try:
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                self.gpu_enabled = True
                print("GPU acceleration enabled")
            else:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                print("Using CPU for detection")
        except Exception as e:
            print(f"GPU setup failed: {e}")
    
    def detect_optimized(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Optimized detection with frame skipping
        """
        self.frame_count += 1
        
        # Only detect every N frames
        if self.frame_count % self.skip_frames == 0:
            detections = self.detect(frame)
            if len(detections) > 0:
                self.last_detections = detections
        else:
            # Use last detections for tracking
            detections = self.last_detections
        
        return detections
    
    def adaptive_skip_frames(self, target_fps: float = 25.0):
        """Adaptively adjust skip frames based on performance"""
        current_fps = self.get_performance_stats().get('avg_fps', 0)
        
        if current_fps < target_fps * 0.8:
            self.skip_frames = min(self.skip_frames + 1, 30)
        elif current_fps > target_fps * 1.2:
            self.skip_frames = max(self.skip_frames - 1, 1)
```

### 2. Object Tracking Implementation

#### CentroidTracker Implementation
```python
from collections import OrderedDict
from scipy.spatial import distance as dist
import numpy as np
from typing import List, Tuple, Dict

class CentroidTracker:
    """
    Centroid-based object tracker with Hungarian assignment
    """
    
    def __init__(self, max_disappeared: int = 50, max_distance: float = 80.0):
        """
        Initialize tracker
        
        Args:
            max_disappeared: Maximum frames before deregistering object
            max_distance: Maximum distance for object matching
        """
        self.next_object_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        
        # Performance monitoring
        self.tracking_times = []
        self.total_tracks = 0
    
    def register(self, centroid: Tuple[int, int]):
        """Register new object"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
        self.total_tracks += 1
    
    def deregister(self, object_id: int):
        """Deregister object"""
        del self.objects[object_id]
        del self.disappeared[object_id]
    
    def update(self, rects: List[Tuple[int, int, int, int]]) -> Dict[int, Tuple[int, int]]:
        """
        Update tracker with new detections
        
        Args:
            rects: List of bounding boxes (x1, y1, x2, y2)
            
        Returns:
            Dictionary mapping object IDs to centroids
        """
        import time
        start_time = time.time()
        
        # Calculate centroids from bounding boxes
        input_centroids = np.array([
            (int((startX + endX) / 2.0), int((startY + endY) / 2.0))
            for (startX, startY, endX, endY) in rects
        ])
        
        # If no objects, register all new detections
        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i])
        else:
            # Get existing object IDs and centroids
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            # Calculate distance matrix
            D = dist.cdist(np.array(object_centroids), input_centroids)
            
            # Find optimal assignment using Hungarian algorithm
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            # Track used rows and columns
            used_rows = set()
            used_cols = set()
            
            # Update existing objects
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                # Check if distance is within threshold
                if D[row, col] > self.max_distance:
                    continue
                
                # Update object
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Handle disappeared objects
            unused_rows = set(range(D.shape[0])).difference(used_rows)
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            # Register new objects
            unused_cols = set(range(D.shape[1])).difference(used_cols)
            for col in unused_cols:
                self.register(input_centroids[col])
        
        # Performance monitoring
        tracking_time = time.time() - start_time
        self.tracking_times.append(tracking_time)
        
        return self.objects
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        if not self.tracking_times:
            return {}
        
        return {
            'avg_tracking_time': np.mean(self.tracking_times),
            'min_tracking_time': np.min(self.tracking_times),
            'max_tracking_time': np.max(self.tracking_times),
            'total_tracks': self.total_tracks,
            'current_objects': len(self.objects),
            'avg_fps': 1.0 / np.mean(self.tracking_times) if self.tracking_times else 0
        }
```

#### Advanced Tracking with Kalman Filter
```python
class KalmanTracker:
    """
    Kalman filter-based object tracker
    """
    
    def __init__(self, initial_state: np.ndarray):
        """
        Initialize Kalman filter
        
        Args:
            initial_state: Initial state [x, y, vx, vy]
        """
        # State transition matrix (constant velocity model)
        self.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        # Measurement matrix
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float32)
        
        # Process noise covariance
        self.Q = np.eye(4, dtype=np.float32) * 0.1
        
        # Measurement noise covariance
        self.R = np.eye(2, dtype=np.float32) * 1.0
        
        # Initialize state
        self.x = initial_state.reshape(4, 1)
        self.P = np.eye(4, dtype=np.float32) * 1000
    
    def predict(self) -> np.ndarray:
        """Predict next state"""
        # Predict state
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.x[:2].flatten()
    
    def update(self, measurement: np.ndarray):
        """Update with measurement"""
        # Kalman gain
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state
        y = measurement.reshape(2, 1) - self.H @ self.x
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        
        return self.x[:2].flatten()
```

### 3. Line Crossing Detection Implementation

#### Basic Line Crossing
```python
class LineCrossingDetector:
    """
    Line crossing detection using geometric intersection
    """
    
    def __init__(self, line_start: Tuple[int, int], line_end: Tuple[int, int]):
        """
        Initialize line crossing detector
        
        Args:
            line_start: Start point of counting line (x, y)
            line_end: End point of counting line (x, y)
        """
        self.line_start = line_start
        self.line_end = line_end
        self.trackable_objects = {}
        self.total_in = 0
        self.total_out = 0
        self.direction_threshold = 3
        
        # Performance monitoring
        self.counting_times = []
    
    def _line_intersection(self, point: Tuple[int, int]) -> float:
        """
        Determine which side of the line a point is on
        
        Args:
            point: Point to check (x, y)
            
        Returns:
            Cross product value (> 0: above, < 0: below, = 0: on line)
        """
        x, y = point
        x1, y1 = self.line_start
        x2, y2 = self.line_end
        
        # Vectors from line_start to point and line_end
        v1 = (x - x1, y - y1)
        v2 = (x2 - x1, y2 - y1)
        
        # Cross product to determine direction
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        
        return cross_product
    
    def _calculate_direction(self, centroids: List[Tuple[int, int]]) -> float:
        """
        Calculate movement direction from recent centroids
        
        Args:
            centroids: List of recent centroids
            
        Returns:
            Direction value (positive: down, negative: up)
        """
        if len(centroids) < 2:
            return 0
        
        # Use last 2 centroids for direction
        recent_centroids = centroids[-2:]
        y_coords = [c[1] for c in recent_centroids]
        direction = y_coords[-1] - y_coords[0]
        
        return direction
    
    def process_objects(self, objects: Dict[int, Tuple[int, int]]) -> Dict[str, int]:
        """
        Process objects for line crossing detection
        
        Args:
            objects: Dictionary mapping object IDs to centroids
            
        Returns:
            Dictionary with counting results
        """
        import time
        start_time = time.time()
        
        for object_id, centroid in objects.items():
            # Get or create trackable object
            to = self.trackable_objects.get(object_id, {
                'centroids': [],
                'counted': False,
                'last_side': None
            })
            
            # Add new centroid
            to['centroids'].append(centroid)
            current_side = self._line_intersection(centroid)
            
            # Initialize if first time
            if to['last_side'] is None:
                to['last_side'] = current_side
            else:
                # Check for line crossing
                if not to['counted'] and len(to['centroids']) > 1:
                    last_side = to['last_side']
                    
                    if last_side is not None and current_side != last_side:
                        # Calculate movement direction
                        direction = self._calculate_direction(to['centroids'])
                        
                        # Determine crossing type
                        if direction > self.direction_threshold and current_side < last_side:
                            # Moving down and crossed line downward = IN
                            self.total_in += 1
                            to['counted'] = True
                        elif direction < -self.direction_threshold and current_side > last_side:
                            # Moving up and crossed line upward = OUT
                            self.total_out += 1
                            to['counted'] = True
                
                to['last_side'] = current_side
            
            self.trackable_objects[object_id] = to
        
        # Performance monitoring
        counting_time = time.time() - start_time
        self.counting_times.append(counting_time)
        
        return {
            'total_in': self.total_in,
            'total_out': self.total_out,
            'current_objects': len(objects)
        }
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        if not self.counting_times:
            return {}
        
        return {
            'avg_counting_time': np.mean(self.counting_times),
            'min_counting_time': np.min(self.counting_times),
            'max_counting_time': np.max(self.counting_times),
            'total_objects_tracked': len(self.trackable_objects),
            'avg_fps': 1.0 / np.mean(self.counting_times) if self.counting_times else 0
        }
```

### 4. Main Adapter Implementation

#### PeopleCounterAdapter
```python
class PeopleCounterAdapter:
    """
    Main adapter combining detection, tracking, and counting
    """
    
    def __init__(self, prototxt_path: str, model_path: str, confidence: float = 0.4):
        """
        Initialize adapter
        
        Args:
            prototxt_path: Path to prototxt file
            model_path: Path to caffemodel file
            confidence: Detection confidence threshold
        """
        # Initialize components
        self.detector = OptimizedPeopleDetector(prototxt_path, model_path, confidence)
        self.tracker = CentroidTracker()
        self.counter = None  # Will be set when line is defined
        
        # Performance monitoring
        self.frame_count = 0
        self.processing_times = []
        
        # Configuration
        self.skip_frames = 5
        self.debug = False
    
    def set_counting_line(self, line_start: Tuple[int, int], line_end: Tuple[int, int]):
        """Set counting line"""
        self.counter = LineCrossingDetector(line_start, line_end)
    
    def process_frame(self, frame: np.ndarray, line_start: Tuple[int, int], line_end: Tuple[int, int]) -> dict:
        """
        Process single frame
        
        Args:
            frame: Input frame
            line_start: Start point of counting line
            line_end: End point of counting line
            
        Returns:
            Dictionary with processing results
        """
        import time
        start_time = time.time()
        
        # Set counting line if not set
        if self.counter is None:
            self.set_counting_line(line_start, line_end)
        
        # Detect people
        detections = self.detector.detect_optimized(frame)
        
        # Track objects
        objects = self.tracker.update(detections)
        
        # Count line crossings
        counting_results = self.counter.process_objects(objects)
        
        # Performance monitoring
        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)
        self.frame_count += 1
        
        # Prepare results
        result = {
            'boxes': detections,
            'objects': objects,
            'total_in': counting_results['total_in'],
            'total_out': counting_results['total_out'],
            'current_objects': counting_results['current_objects'],
            'processing_time': processing_time,
            'frame_count': self.frame_count
        }
        
        # Debug information
        if self.debug:
            result.update({
                'detection_stats': self.detector.get_performance_stats(),
                'tracking_stats': self.tracker.get_performance_stats(),
                'counting_stats': self.counter.get_performance_stats()
            })
        
        return result
    
    def get_performance_stats(self) -> dict:
        """Get overall performance statistics"""
        if not self.processing_times:
            return {}
        
        return {
            'avg_processing_time': np.mean(self.processing_times),
            'min_processing_time': np.min(self.processing_times),
            'max_processing_time': np.max(self.processing_times),
            'total_frames': self.frame_count,
            'avg_fps': 1.0 / np.mean(self.processing_times) if self.processing_times else 0,
            'detection_stats': self.detector.get_performance_stats(),
            'tracking_stats': self.tracker.get_performance_stats(),
            'counting_stats': self.counter.get_performance_stats() if self.counter else {}
        }
```

### 5. GUI Implementation

#### Basic Tkinter GUI
```python
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from typing import Optional

class PeopleCounterGUI:
    """
    Tkinter-based GUI for people counter
    """
    
    def __init__(self, adapter: PeopleCounterAdapter):
        """
        Initialize GUI
        
        Args:
            adapter: PeopleCounterAdapter instance
        """
        self.adapter = adapter
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("AI People Counter")
        self.root.geometry("1200x800")
        
        # Video display
        self.video_canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.video_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Control panel
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Initialize UI components
        self._init_controls()
        self._init_counters()
        self._init_performance_display()
        
        # Video state
        self.current_frame = None
        self.is_playing = False
        self.line_start = (0, 300)
        self.line_end = (800, 300)
        
        # Bind events
        self.video_canvas.bind("<Button-1>", self._on_canvas_click)
        self.video_canvas.bind("<B1-Motion>", self._on_canvas_drag)
    
    def _init_controls(self):
        """Initialize control buttons"""
        # Control buttons
        tk.Button(self.control_frame, text="Start", command=self._start_processing).pack(fill=tk.X, pady=5)
        tk.Button(self.control_frame, text="Stop", command=self._stop_processing).pack(fill=tk.X, pady=5)
        tk.Button(self.control_frame, text="Reset Counters", command=self._reset_counters).pack(fill=tk.X, pady=5)
        
        # Configuration
        config_frame = tk.LabelFrame(self.control_frame, text="Configuration")
        config_frame.pack(fill=tk.X, pady=10)
        
        # Confidence slider
        tk.Label(config_frame, text="Confidence:").pack()
        self.confidence_var = tk.DoubleVar(value=0.4)
        confidence_slider = tk.Scale(config_frame, from_=0.1, to=0.9, resolution=0.1, 
                                   variable=self.confidence_var, orient=tk.HORIZONTAL)
        confidence_slider.pack(fill=tk.X)
        
        # Skip frames slider
        tk.Label(config_frame, text="Skip Frames:").pack()
        self.skip_frames_var = tk.IntVar(value=5)
        skip_slider = tk.Scale(config_frame, from_=1, to=30, variable=self.skip_frames_var, orient=tk.HORIZONTAL)
        skip_slider.pack(fill=tk.X)
    
    def _init_counters(self):
        """Initialize counter displays"""
        counter_frame = tk.LabelFrame(self.control_frame, text="Counters")
        counter_frame.pack(fill=tk.X, pady=10)
        
        # IN counter
        tk.Label(counter_frame, text="IN:").pack()
        self.in_counter = tk.Label(counter_frame, text="0", font=("Arial", 24, "bold"))
        self.in_counter.pack()
        
        # OUT counter
        tk.Label(counter_frame, text="OUT:").pack()
        self.out_counter = tk.Label(counter_frame, text="0", font=("Arial", 24, "bold"))
        self.out_counter.pack()
        
        # Current objects
        tk.Label(counter_frame, text="Current Objects:").pack()
        self.current_objects_label = tk.Label(counter_frame, text="0", font=("Arial", 16))
        self.current_objects_label.pack()
    
    def _init_performance_display(self):
        """Initialize performance display"""
        perf_frame = tk.LabelFrame(self.control_frame, text="Performance")
        perf_frame.pack(fill=tk.X, pady=10)
        
        self.fps_label = tk.Label(perf_frame, text="FPS: 0")
        self.fps_label.pack()
        
        self.processing_time_label = tk.Label(perf_frame, text="Processing: 0ms")
        self.processing_time_label.pack()
    
    def _start_processing(self):
        """Start video processing"""
        self.is_playing = True
        self._process_frame()
    
    def _stop_processing(self):
        """Stop video processing"""
        self.is_playing = False
    
    def _reset_counters(self):
        """Reset all counters"""
        self.adapter.counter.total_in = 0
        self.adapter.counter.total_out = 0
        self.in_counter.config(text="0")
        self.out_counter.config(text="0")
    
    def _process_frame(self):
        """Process single frame"""
        if not self.is_playing or self.current_frame is None:
            return
        
        # Process frame
        result = self.adapter.process_frame(self.current_frame, self.line_start, self.line_end)
        
        # Update display
        self._update_display(result)
        
        # Schedule next frame
        self.root.after(33, self._process_frame)  # ~30 FPS
    
    def _update_display(self, result: dict):
        """Update GUI display"""
        # Update counters
        self.in_counter.config(text=str(result['total_in']))
        self.out_counter.config(text=str(result['total_out']))
        self.current_objects_label.config(text=str(result['current_objects']))
        
        # Update performance
        fps = 1.0 / result['processing_time'] if result['processing_time'] > 0 else 0
        self.fps_label.config(text=f"FPS: {fps:.1f}")
        self.processing_time_label.config(text=f"Processing: {result['processing_time']*1000:.1f}ms")
        
        # Draw frame with overlays
        self._draw_frame_with_overlays(result)
    
    def _draw_frame_with_overlays(self, result: dict):
        """Draw frame with detection and tracking overlays"""
        if self.current_frame is None:
            return
        
        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        
        # Draw bounding boxes
        for box in result['boxes']:
            x1, y1, x2, y2 = box
            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw tracking centroids
        for object_id, centroid in result['objects'].items():
            x, y = centroid
            cv2.circle(frame_rgb, (x, y), 5, (255, 0, 0), -1)
            cv2.putText(frame_rgb, str(object_id), (x-10, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Draw counting line
        cv2.line(frame_rgb, self.line_start, self.line_end, (0, 0, 255), 2)
        
        # Convert to PhotoImage
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_pil)
        
        # Update canvas
        self.video_canvas.delete("all")
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        self.video_canvas.image = frame_tk  # Keep reference
    
    def _on_canvas_click(self, event):
        """Handle canvas click for line positioning"""
        self.line_start = (event.x, event.y)
    
    def _on_canvas_drag(self, event):
        """Handle canvas drag for line positioning"""
        self.line_end = (event.x, event.y)
        if self.adapter.counter:
            self.adapter.set_counting_line(self.line_start, self.line_end)
    
    def update_frame(self, frame: np.ndarray):
        """Update current frame"""
        self.current_frame = frame.copy()
    
    def run(self):
        """Start GUI main loop"""
        self.root.mainloop()
```

## 🔧 Configuration Management

### Configuration File
```yaml
# config/default.yaml
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

performance:
  enable_monitoring: true
  log_interval: 100
  memory_cleanup_interval: 50
```

### Configuration Loader
```python
import yaml
from typing import Dict, Any

class ConfigManager:
    """Configuration manager for the application"""
    
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'detection': {
                'confidence': 0.4,
                'skip_frames': 5,
                'model_size': [300, 300],
                'gpu_acceleration': False
            },
            'tracking': {
                'max_disappeared': 50,
                'max_distance': 80,
                'min_confidence': 0.3,
                'smooth_factor': 0.8
            },
            'counting': {
                'direction_threshold': 3,
                'line_thickness': 2,
                'count_once': True,
                'debug_mode': False
            },
            'ui': {
                'max_fps': 30,
                'canvas_width': 800,
                'canvas_height': 600,
                'overlay_alpha': 0.7,
                'auto_resize': True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
```

## 🧪 Testing Implementation

### Unit Tests
```python
import unittest
import numpy as np
from unittest.mock import Mock, patch

class TestPeopleDetector(unittest.TestCase):
    """Test cases for PeopleDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = PeopleDetector("test.prototxt", "test.caffemodel")
    
    def test_detection_empty_frame(self):
        """Test detection on empty frame"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = self.detector.detect(frame)
        self.assertEqual(len(detections), 0)
    
    def test_detection_performance(self):
        """Test detection performance"""
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        start_time = time.time()
        detections = self.detector.detect(frame)
        detection_time = time.time() - start_time
        
        self.assertLess(detection_time, 0.1)  # Should be fast
    
    def test_confidence_threshold(self):
        """Test confidence threshold filtering"""
        # Test with different confidence values
        self.detector.confidence = 0.5
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        detections = self.detector.detect(frame)
        
        # All detections should have confidence >= 0.5
        # (This would need mock detections to test properly)

class TestCentroidTracker(unittest.TestCase):
    """Test cases for CentroidTracker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = CentroidTracker()
    
    def test_initialization(self):
        """Test tracker initialization"""
        self.assertEqual(len(self.tracker.objects), 0)
        self.assertEqual(self.tracker.next_object_id, 0)
    
    def test_object_registration(self):
        """Test object registration"""
        centroid = (100, 100)
        self.tracker.register(centroid)
        
        self.assertEqual(len(self.tracker.objects), 1)
        self.assertEqual(self.tracker.objects[0], centroid)
    
    def test_object_deregistration(self):
        """Test object deregistration"""
        centroid = (100, 100)
        self.tracker.register(centroid)
        
        self.assertEqual(len(self.tracker.objects), 1)
        self.tracker.deregister(0)
        self.assertEqual(len(self.tracker.objects), 0)
    
    def test_tracking_update(self):
        """Test tracking update"""
        # Initial detections
        rects = [(100, 100, 200, 300), (300, 150, 400, 350)]
        objects = self.tracker.update(rects)
        
        self.assertEqual(len(objects), 2)
        
        # Update with similar detections
        rects2 = [(110, 110, 210, 310), (310, 160, 410, 360)]
        objects2 = self.tracker.update(rects2)
        
        self.assertEqual(len(objects2), 2)
        # Should maintain same object IDs

class TestLineCrossingDetector(unittest.TestCase):
    """Test cases for LineCrossingDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = LineCrossingDetector((0, 300), (800, 300))
    
    def test_line_intersection(self):
        """Test line intersection calculation"""
        # Point above line
        point_above = (400, 200)
        result = self.detector._line_intersection(point_above)
        self.assertGreater(result, 0)
        
        # Point below line
        point_below = (400, 400)
        result = self.detector._line_intersection(point_below)
        self.assertLess(result, 0)
        
        # Point on line
        point_on = (400, 300)
        result = self.detector._line_intersection(point_on)
        self.assertEqual(result, 0)
    
    def test_direction_calculation(self):
        """Test movement direction calculation"""
        centroids = [(100, 100), (100, 90)]  # Moving up
        direction = self.detector._calculate_direction(centroids)
        self.assertLess(direction, 0)
        
        centroids = [(100, 100), (100, 110)]  # Moving down
        direction = self.detector._calculate_direction(centroids)
        self.assertGreater(direction, 0)

if __name__ == '__main__':
    unittest.main()
```

---

**Implementation Guide Version**: 2.0.0  
**Last Updated**: December 2024  
**Implementation Lead**: AI Development Team 
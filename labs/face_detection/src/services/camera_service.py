"""
Camera service for managing camera/webcam operations
"""
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Generator
import threading
import time
from loguru import logger

from config import settings

class CameraService:
    """Service for managing camera operations"""
    
    def __init__(self):
        """Initialize camera service"""
        self.device_id = settings.camera_device_id
        self.resolution = (settings.camera_resolution_width, settings.camera_resolution_height)
        self.fps = settings.camera_fps
        self.cameras = {}
        self.active_streams = {}
        
        logger.info("Camera service initialized")
    
    async def initialize(self):
        """Initialize the camera service"""
        try:
            # Test camera availability
            available_cameras = self.get_available_cameras()
            if not available_cameras:
                logger.warning("No cameras found during initialization")
            else:
                logger.info(f"Found {len(available_cameras)} cameras during initialization")
            logger.info("Camera service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize camera service: {str(e)}")
            raise
    
    def is_healthy(self) -> bool:
        """Check if the camera service is healthy"""
        try:
            # Simple health check
            return True
        except Exception as e:
            logger.error(f"Camera service health check failed: {str(e)}")
            return False
    
    def get_available_cameras(self) -> List[Dict[str, Any]]:
        """
        Get list of available cameras
        
        Returns:
            List of available camera information
        """
        try:
            available_cameras = []
            
            # Check first 10 camera indices
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    # Get camera properties
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    
                    camera_info = {
                        "id": i,
                        "name": f"Camera {i}",
                        "resolution": [width, height],
                        "fps": fps,
                        "status": "available"
                    }
                    available_cameras.append(camera_info)
                    
                    cap.release()
            
            logger.info(f"Found {len(available_cameras)} available cameras")
            return available_cameras
            
        except Exception as e:
            logger.error(f"Failed to get available cameras: {str(e)}")
            return []
    
    def open_camera(self, device_id: int = None) -> Optional[cv2.VideoCapture]:
        """
        Open camera with specified device ID
        
        Args:
            device_id: Camera device ID (defaults to configured device)
        
        Returns:
            OpenCV VideoCapture object or None
        """
        try:
            if device_id is None:
                device_id = self.device_id
            
            cap = cv2.VideoCapture(device_id)
            
            if not cap.isOpened():
                logger.error(f"Failed to open camera {device_id}")
                return None
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            logger.info(f"Opened camera {device_id} with resolution {self.resolution}")
            return cap
            
        except Exception as e:
            logger.error(f"Failed to open camera {device_id}: {str(e)}")
            return None
    
    def capture_frame(self, device_id: int = None) -> Optional[np.ndarray]:
        """
        Capture single frame from camera
        
        Args:
            device_id: Camera device ID
        
        Returns:
            Captured frame as numpy array or None
        """
        try:
            cap = self.open_camera(device_id)
            if cap is None:
                return None
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                logger.info(f"Captured frame from camera {device_id or self.device_id}")
                return frame
            else:
                logger.warning(f"Failed to capture frame from camera {device_id or self.device_id}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to capture frame: {str(e)}")
            return None
    
    def start_video_stream(
        self, 
        device_id: int = None,
        callback=None
    ) -> bool:
        """
        Start continuous video stream
        
        Args:
            device_id: Camera device ID
            callback: Callback function for frame processing
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if device_id is None:
                device_id = self.device_id
            
            # Check if stream already active
            if device_id in self.active_streams:
                logger.warning(f"Video stream already active for camera {device_id}")
                return False
            
            # Open camera
            cap = self.open_camera(device_id)
            if cap is None:
                return False
            
            # Store camera object
            self.active_streams[device_id] = {
                "cap": cap,
                "callback": callback,
                "running": True,
                "thread": None
            }
            
            # Start streaming thread
            thread = threading.Thread(
                target=self._stream_frames,
                args=(device_id,),
                daemon=True
            )
            thread.start()
            
            self.active_streams[device_id]["thread"] = thread
            
            logger.info(f"Started video stream for camera {device_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start video stream: {str(e)}")
            return False
    
    def stop_video_stream(self, device_id: int = None) -> bool:
        """
        Stop video stream
        
        Args:
            device_id: Camera device ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if device_id is None:
                device_id = self.device_id
            
            if device_id not in self.active_streams:
                logger.warning(f"No active stream for camera {device_id}")
                return False
            
            # Stop streaming
            self.active_streams[device_id]["running"] = False
            
            # Wait for thread to finish
            thread = self.active_streams[device_id]["thread"]
            if thread and thread.is_alive():
                thread.join(timeout=2.0)
            
            # Release camera
            cap = self.active_streams[device_id]["cap"]
            cap.release()
            
            # Remove from active streams
            del self.active_streams[device_id]
            
            logger.info(f"Stopped video stream for camera {device_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop video stream: {str(e)}")
            return False
    
    def _stream_frames(self, device_id: int):
        """
        Internal method for streaming frames
        
        Args:
            device_id: Camera device ID
        """
        try:
            stream_info = self.active_streams[device_id]
            cap = stream_info["cap"]
            callback = stream_info["callback"]
            
            frame_interval = 1.0 / self.fps
            
            while stream_info["running"]:
                start_time = time.time()
                
                ret, frame = cap.read()
                if ret:
                    # Process frame if callback provided
                    if callback:
                        try:
                            callback(frame, device_id)
                        except Exception as e:
                            logger.error(f"Callback error: {str(e)}")
                    
                    # Control frame rate
                    elapsed = time.time() - start_time
                    if elapsed < frame_interval:
                        time.sleep(frame_interval - elapsed)
                else:
                    logger.warning(f"Failed to read frame from camera {device_id}")
                    time.sleep(0.1)
            
            logger.info(f"Stream ended for camera {device_id}")
            
        except Exception as e:
            logger.error(f"Stream error for camera {device_id}: {str(e)}")
    
    def get_frame_generator(
        self, 
        device_id: int = None,
        max_frames: int = None
    ) -> Generator[np.ndarray, None, None]:
        """
        Get frame generator for processing
        
        Args:
            device_id: Camera device ID
            max_frames: Maximum number of frames to generate
        
        Yields:
            Frames as numpy arrays
        """
        try:
            cap = self.open_camera(device_id)
            if cap is None:
                return
            
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if ret:
                    yield frame
                    frame_count += 1
                    
                    if max_frames and frame_count >= max_frames:
                        break
                else:
                    logger.warning("Failed to read frame")
                    break
            
            cap.release()
            
        except Exception as e:
            logger.error(f"Frame generator error: {str(e)}")
    
    def save_frame(
        self, 
        frame: np.ndarray, 
        filepath: str,
        quality: int = 95
    ) -> bool:
        """
        Save frame to file
        
        Args:
            frame: Frame to save
            filepath: Output file path
            quality: JPEG quality (1-100)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert BGR to RGB if needed
            if len(frame.shape) == 3:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = frame
            
            # Save using PIL for better quality control
            from PIL import Image
            pil_image = Image.fromarray(frame_rgb)
            pil_image.save(filepath, "JPEG", quality=quality)
            
            logger.info(f"Saved frame to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save frame: {str(e)}")
            return False
    
    def resize_frame(
        self, 
        frame: np.ndarray, 
        width: int = None, 
        height: int = None
    ) -> np.ndarray:
        """
        Resize frame
        
        Args:
            frame: Input frame
            width: Target width
            height: Target height
        
        Returns:
            Resized frame
        """
        try:
            if width is None and height is None:
                return frame
            
            h, w = frame.shape[:2]
            
            if width and height:
                target_size = (width, height)
            elif width:
                aspect_ratio = w / h
                target_size = (width, int(width / aspect_ratio))
            else:
                aspect_ratio = w / h
                target_size = (int(height * aspect_ratio), height)
            
            resized = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)
            return resized
            
        except Exception as e:
            logger.error(f"Failed to resize frame: {str(e)}")
            return frame
    
    def apply_filters(
        self, 
        frame: np.ndarray, 
        filters: List[str] = None
    ) -> np.ndarray:
        """
        Apply image filters to frame
        
        Args:
            frame: Input frame
            filters: List of filters to apply
        
        Returns:
            Filtered frame
        """
        try:
            if not filters:
                return frame
            
            processed_frame = frame.copy()
            
            for filter_name in filters:
                if filter_name == "grayscale":
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
                
                elif filter_name == "blur":
                    processed_frame = cv2.GaussianBlur(processed_frame, (15, 15), 0)
                
                elif filter_name == "sharpen":
                    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    processed_frame = cv2.filter2D(processed_frame, -1, kernel)
                
                elif filter_name == "brightness":
                    hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
                    hsv[:,:,2] = cv2.add(hsv[:,:,2], 30)
                    processed_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                
                elif filter_name == "contrast":
                    processed_frame = cv2.convertScaleAbs(processed_frame, alpha=1.2, beta=0)
            
            return processed_frame
            
        except Exception as e:
            logger.error(f"Failed to apply filters: {str(e)}")
            return frame
    
    def get_camera_status(self, device_id: int = None) -> Dict[str, Any]:
        """
        Get camera status
        
        Args:
            device_id: Camera device ID
        
        Returns:
            Camera status information
        """
        try:
            if device_id is None:
                device_id = self.device_id
            
            status = {
                "device_id": device_id,
                "active": device_id in self.active_streams,
                "resolution": self.resolution,
                "fps": self.fps
            }
            
            if device_id in self.active_streams:
                status["stream_info"] = {
                    "running": self.active_streams[device_id]["running"],
                    "has_callback": self.active_streams[device_id]["callback"] is not None
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get camera status: {str(e)}")
            return {}
    
    def cleanup(self):
        """Cleanup all camera resources"""
        try:
            # Stop all active streams
            for device_id in list(self.active_streams.keys()):
                self.stop_video_stream(device_id)
            
            logger.info("Camera service cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")

# Global instance
camera_service = CameraService() 
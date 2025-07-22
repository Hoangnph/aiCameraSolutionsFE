#!/usr/bin/env python3
"""
RTSP Service for Camera Stream Processing
Handles RTSP stream connections, frame processing, and stream management
"""

import cv2
import numpy as np
import logging
import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime
import asyncio
from dataclasses import dataclass
from enum import Enum

from beCamera.src.services.worker_pool_service import (
    get_worker_pool_service, TaskPriority
)

# Configure logging
logger = logging.getLogger(__name__)

class StreamStatus(Enum):
    """RTSP stream status enumeration"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    PROCESSING = "processing"
    ERROR = "error"
    DISCONNECTED = "disconnected"
    MAINTENANCE = "maintenance"

@dataclass
class StreamMetrics:
    """RTSP stream performance metrics"""
    fps: float
    frame_count: int
    processing_time: float
    error_count: int
    last_frame_time: datetime
    connection_uptime: float
    quality_score: float

@dataclass
class StreamConfig:
    """RTSP stream configuration"""
    camera_id: str
    rtsp_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    frame_rate: int = 30
    resolution: tuple = (640, 480)
    timeout: int = 10
    retry_attempts: int = 3
    retry_delay: int = 5

class RTSPStreamHandler:
    """Handles individual RTSP stream connections"""
    
    def __init__(self, config: StreamConfig):
        self.config = config
        self.cap = None
        self.status = StreamStatus.DISCONNECTED
        self.metrics = StreamMetrics(
            fps=0.0,
            frame_count=0,
            processing_time=0.0,
            error_count=0,
            last_frame_time=datetime.now(),
            connection_uptime=0.0,
            quality_score=0.0
        )
        self.is_running = False
        self.lock = threading.Lock()
        self.frame_callbacks: List[Callable] = []
        self.error_callbacks: List[Callable] = []
        self.status_callbacks: List[Callable] = []
        self.connection_start_time = None
        
        # Worker pool integration
        self.worker_pool_service = get_worker_pool_service()
        self.use_worker_pool = True  # Enable worker pool processing
        self.processing_pool = None

    def add_frame_callback(self, callback: Callable):
        """Add callback for frame processing"""
        self.frame_callbacks.append(callback)

    def add_error_callback(self, callback: Callable):
        """Add callback for error handling"""
        self.error_callbacks.append(callback)

    def add_status_callback(self, callback: Callable):
        """Add callback for status updates"""
        self.status_callbacks.append(callback)

    def _notify_status_change(self, new_status: StreamStatus):
        """Notify status change to callbacks"""
        old_status = self.status
        self.status = new_status
        
        for callback in self.status_callbacks:
            try:
                callback(self.config.camera_id, old_status, new_status)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")

    def _notify_error(self, error: Exception):
        """Notify error to callbacks"""
        self.metrics.error_count += 1
        
        for callback in self.error_callbacks:
            try:
                callback(self.config.camera_id, error)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")

    def connect(self) -> bool:
        """Connect to RTSP stream"""
        try:
            self._notify_status_change(StreamStatus.CONNECTING)
            
            # Build RTSP URL with credentials if provided
            rtsp_url = self.config.rtsp_url
            if self.config.username and self.config.password:
                # Insert credentials into RTSP URL
                if rtsp_url.startswith('rtsp://'):
                    rtsp_url = rtsp_url.replace('rtsp://', f'rtsp://{self.config.username}:{self.config.password}@', 1)
            
            # Open RTSP stream
            self.cap = cv2.VideoCapture(rtsp_url)
            
            # Set stream properties
            self.cap.set(cv2.CAP_PROP_FPS, self.config.frame_rate)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.resolution[1])
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize latency
            
            # Test connection
            if not self.cap.isOpened():
                raise Exception(f"Failed to open RTSP stream: {rtsp_url}")
            
            # Read first frame to verify connection
            ret, frame = self.cap.read()
            if not ret or frame is None:
                raise Exception("Failed to read first frame from RTSP stream")
            
            self.connection_start_time = time.time()
            self._notify_status_change(StreamStatus.CONNECTED)
            
            logger.info(f"Successfully connected to RTSP stream: {self.config.camera_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to RTSP stream {self.config.camera_id}: {e}")
            self._notify_error(e)
            self._notify_status_change(StreamStatus.ERROR)
            return False

    def disconnect(self):
        """Disconnect from RTSP stream"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self._notify_status_change(StreamStatus.DISCONNECTED)
        logger.info(f"Disconnected from RTSP stream: {self.config.camera_id}")

    def start_processing(self):
        """Start frame processing loop"""
        if not self.cap or not self.cap.isOpened():
            if not self.connect():
                return False
        
        self.is_running = True
        self._notify_status_change(StreamStatus.PROCESSING)
        
        # Get or create worker pool for this stream
        if self.use_worker_pool:
            pool_name = f"rtsp_pool_{self.config.camera_id}"
            self.processing_pool = self.worker_pool_service.get_pool(pool_name)
            if not self.processing_pool:
                self.processing_pool = self.worker_pool_service.create_pool(pool_name, pool_size=2)
                self.worker_pool_service.start_pool(pool_name)
        
        # Start processing thread
        thread = threading.Thread(target=self._processing_loop, daemon=True)
        thread.start()
        
        logger.info(f"Started processing RTSP stream: {self.config.camera_id}")
        return True

    def stop_processing(self):
        """Stop frame processing loop"""
        self.is_running = False
        
        # Stop worker pool if used
        if self.processing_pool:
            pool_name = f"rtsp_pool_{self.config.camera_id}"
            self.worker_pool_service.stop_pool(pool_name)
            self.processing_pool = None
        
        logger.info(f"Stopped processing RTSP stream: {self.config.camera_id}")

    def _processing_loop(self):
        """Main processing loop for RTSP frames"""
        frame_times = []
        
        while self.is_running:
            try:
                if not self.cap or not self.cap.isOpened():
                    logger.warning(f"RTSP stream disconnected: {self.config.camera_id}")
                    self._notify_status_change(StreamStatus.ERROR)
                    break
                
                # Read frame
                start_time = time.time()
                ret, frame = self.cap.read()
                processing_time = time.time() - start_time
                
                if not ret or frame is None:
                    logger.warning(f"Failed to read frame from RTSP stream: {self.config.camera_id}")
                    self.metrics.error_count += 1
                    time.sleep(0.1)  # Brief pause before retry
                    continue
                
                # Update metrics
                with self.lock:
                    self.metrics.frame_count += 1
                    self.metrics.processing_time = processing_time
                    self.metrics.last_frame_time = datetime.now()
                    
                    # Calculate FPS
                    frame_times.append(time.time())
                    if len(frame_times) > 30:  # Keep last 30 frames for FPS calculation
                        frame_times.pop(0)
                    
                    if len(frame_times) > 1:
                        time_diff = frame_times[-1] - frame_times[0]
                        if time_diff > 0:
                            self.metrics.fps = len(frame_times) / time_diff
                    
                    # Calculate connection uptime
                    if self.connection_start_time:
                        self.metrics.connection_uptime = time.time() - self.connection_start_time
                    
                    # Calculate quality score (simplified)
                    self.metrics.quality_score = min(1.0, 1.0 - (self.metrics.error_count / max(self.metrics.frame_count, 1)))
                
                # Process frame with worker pool or direct callbacks
                if self.use_worker_pool and self.processing_pool:
                    # Submit to worker pool
                    asyncio.create_task(self._submit_to_worker_pool(frame, self.metrics.__dict__))
                else:
                    # Direct callback processing
                    for callback in self.frame_callbacks:
                        try:
                            callback(self.config.camera_id, frame, self.metrics)
                        except Exception as e:
                            logger.error(f"Error in frame callback: {e}")
                
                # Control frame rate
                target_frame_time = 1.0 / self.config.frame_rate
                if processing_time < target_frame_time:
                    time.sleep(target_frame_time - processing_time)
                
            except Exception as e:
                logger.error(f"Error in RTSP processing loop for {self.config.camera_id}: {e}")
                self._notify_error(e)
                self.metrics.error_count += 1
                time.sleep(1)  # Wait before retry
        
        self._notify_status_change(StreamStatus.DISCONNECTED)

    async def _submit_to_worker_pool(self, frame: np.ndarray, metrics: Dict):
        """Submit frame to worker pool for processing"""
        try:
            # Create callback for worker pool results
            async def worker_callback(result):
                # Notify frame callbacks with worker pool result
                for callback in self.frame_callbacks:
                    try:
                        callback(self.config.camera_id, frame, metrics, result)
                    except Exception as e:
                        logger.error(f"Error in worker callback: {e}")
            
            # Submit task to worker pool
            await self.processing_pool.submit_task(
                camera_id=self.config.camera_id,
                frame_data=frame,
                priority=TaskPriority.NORMAL,
                callback=worker_callback,
                metadata=metrics
            )
            
        except Exception as e:
            logger.error(f"Error submitting to worker pool: {e}")
            # Fallback to direct processing
            for callback in self.frame_callbacks:
                try:
                    callback(self.config.camera_id, frame, metrics)
                except Exception as callback_error:
                    logger.error(f"Error in fallback callback: {callback_error}")

    def get_metrics(self) -> StreamMetrics:
        """Get current stream metrics"""
        with self.lock:
            return self.metrics

    def get_status(self) -> StreamStatus:
        """Get current stream status"""
        return self.status

    def is_healthy(self) -> bool:
        """Check if stream is healthy"""
        with self.lock:
            # Stream is healthy if:
            # 1. Status is CONNECTED or PROCESSING
            # 2. Error rate is low (< 10%)
            # 3. FPS is reasonable (> 5)
            if self.status not in [StreamStatus.CONNECTED, StreamStatus.PROCESSING]:
                return False
            
            error_rate = self.metrics.error_count / max(self.metrics.frame_count, 1)
            return error_rate < 0.1 and self.metrics.fps > 5.0

class RTSPService:
    """Main RTSP service for managing multiple streams"""
    
    def __init__(self):
        self.streams: Dict[str, RTSPStreamHandler] = {}
        self.lock = threading.Lock()
        self.global_callbacks = {
            'frame': [],
            'error': [],
            'status': []
        }
        
        # Worker pool service integration
        self.worker_pool_service = get_worker_pool_service()

    def add_stream(self, config: StreamConfig) -> bool:
        """Add a new RTSP stream"""
        try:
            with self.lock:
                if config.camera_id in self.streams:
                    logger.warning(f"Stream already exists: {config.camera_id}")
                    return False
                
                handler = RTSPStreamHandler(config)
                
                # Add global callbacks
                for callback in self.global_callbacks['frame']:
                    handler.add_frame_callback(callback)
                for callback in self.global_callbacks['error']:
                    handler.add_error_callback(callback)
                for callback in self.global_callbacks['status']:
                    handler.add_status_callback(callback)
                
                self.streams[config.camera_id] = handler
                
                logger.info(f"Added RTSP stream: {config.camera_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to add RTSP stream {config.camera_id}: {e}")
            return False

    def remove_stream(self, camera_id: str) -> bool:
        """Remove an RTSP stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    logger.warning(f"Stream not found: {camera_id}")
                    return False
                
                handler = self.streams[camera_id]
                handler.stop_processing()
                handler.disconnect()
                
                del self.streams[camera_id]
                
                logger.info(f"Removed RTSP stream: {camera_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to remove RTSP stream {camera_id}: {e}")
            return False

    def start_stream(self, camera_id: str) -> bool:
        """Start processing an RTSP stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    logger.error(f"Stream not found: {camera_id}")
                    return False
                
                handler = self.streams[camera_id]
                return handler.start_processing()
                
        except Exception as e:
            logger.error(f"Failed to start RTSP stream {camera_id}: {e}")
            return False

    def stop_stream(self, camera_id: str) -> bool:
        """Stop processing an RTSP stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    logger.error(f"Stream not found: {camera_id}")
                    return False
                
                handler = self.streams[camera_id]
                handler.stop_processing()
                return True
                
        except Exception as e:
            logger.error(f"Failed to stop RTSP stream {camera_id}: {e}")
            return False

    def get_stream_status(self, camera_id: str) -> Optional[StreamStatus]:
        """Get status of an RTSP stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    return None
                
                return self.streams[camera_id].get_status()
                
        except Exception as e:
            logger.error(f"Failed to get stream status for {camera_id}: {e}")
            return None

    def get_stream_metrics(self, camera_id: str) -> Optional[StreamMetrics]:
        """Get metrics of an RTSP stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    return None
                
                return self.streams[camera_id].get_metrics()
                
        except Exception as e:
            logger.error(f"Failed to get stream metrics for {camera_id}: {e}")
            return None

    def get_all_streams(self) -> Dict[str, Dict]:
        """Get information about all streams"""
        try:
            with self.lock:
                result = {}
                for camera_id, handler in self.streams.items():
                    result[camera_id] = {
                        'status': handler.get_status().value,
                        'metrics': handler.get_metrics().__dict__,
                        'config': handler.config.__dict__,
                        'healthy': handler.is_healthy()
                    }
                return result
                
        except Exception as e:
            logger.error(f"Failed to get all streams: {e}")
            return {}

    def add_global_callback(self, callback_type: str, callback: Callable):
        """Add global callback for all streams"""
        if callback_type in self.global_callbacks:
            self.global_callbacks[callback_type].append(callback)
            
            # Add to existing streams
            with self.lock:
                for handler in self.streams.values():
                    if callback_type == 'frame':
                        handler.add_frame_callback(callback)
                    elif callback_type == 'error':
                        handler.add_error_callback(callback)
                    elif callback_type == 'status':
                        handler.add_status_callback(callback)

    def get_service_status(self) -> Dict:
        """Get overall service status"""
        try:
            with self.lock:
                total_streams = len(self.streams)
                active_streams = sum(1 for h in self.streams.values() 
                                   if h.get_status() in [StreamStatus.CONNECTED, StreamStatus.PROCESSING])
                healthy_streams = sum(1 for h in self.streams.values() if h.is_healthy())
                
                return {
                    'total_streams': total_streams,
                    'active_streams': active_streams,
                    'healthy_streams': healthy_streams,
                    'service_status': 'healthy' if healthy_streams == total_streams else 'degraded'
                }
                
        except Exception as e:
            logger.error(f"Failed to get service status: {e}")
            return {'error': str(e)}

    def enable_worker_pool_processing(self, camera_id: str, enabled: bool = True):
        """Enable or disable worker pool processing for a stream"""
        try:
            with self.lock:
                if camera_id not in self.streams:
                    logger.error(f"Stream not found: {camera_id}")
                    return False
                
                handler = self.streams[camera_id]
                handler.use_worker_pool = enabled
                
                logger.info(f"Worker pool processing {'enabled' if enabled else 'disabled'} for camera {camera_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to configure worker pool for camera {camera_id}: {e}")
            return False

    def get_worker_pool_status(self, camera_id: str) -> Optional[Dict]:
        """Get worker pool status for a camera"""
        try:
            pool_name = f"rtsp_pool_{camera_id}"
            pool = self.worker_pool_service.get_pool(pool_name)
            if pool:
                return pool.get_pool_status()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get worker pool status for camera {camera_id}: {e}")
            return None

    def get_all_worker_pools_status(self) -> Dict:
        """Get status of all worker pools"""
        try:
            return self.worker_pool_service.get_all_pools_status()
        except Exception as e:
            logger.error(f"Failed to get all worker pools status: {e}")
            return {}

    def set_ai_service_for_worker_pools(self, ai_service):
        """Set AI service for all worker pools"""
        try:
            self.worker_pool_service.set_ai_service(ai_service)
            logger.info("AI service set for all worker pools")
        except Exception as e:
            logger.error(f"Failed to set AI service for worker pools: {e}")

# Global RTSP service instance
rtsp_service = RTSPService()

def get_rtsp_service() -> RTSPService:
    """Get the global RTSP service instance"""
    return rtsp_service 
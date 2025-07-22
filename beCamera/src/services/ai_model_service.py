#!/usr/bin/env python3
"""
AI Model Service for People Counting
Based on People-Counting-in-Real-Time reference implementation
"""

import cv2
import numpy as np
import logging
import time
import json
import os
import asyncio
import aiohttp
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import threading
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class DetectionResult:
    """Result of people detection and counting"""
    people_in: int
    people_out: int
    current_count: int
    confidence: float
    frame_count: int
    processing_time: float
    timestamp: datetime

class CentroidTracker:
    """Simple centroid tracker for people counting"""
    
    def __init__(self, max_disappeared: int = 40, max_distance: int = 50):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    def register(self, centroid):
        """Register a new object"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        """Deregister an object"""
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        """Update tracked objects"""
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        input_centroids = np.array([self._get_centroid(rect) for rect in rects])
        
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            distances = self._calculate_distances(object_centroids, input_centroids)
            
            rows = distances.min(axis=1).argsort()
            cols = distances.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                    
                if distances[row, col] > self.max_distance:
                    continue
                    
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            unused_rows = set(range(0, distances.shape[0])).difference(used_rows)
            unused_cols = set(range(0, distances.shape[1])).difference(used_cols)
            
            if distances.shape[0] >= distances.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])
                    
        return self.objects

    def _get_centroid(self, rect):
        """Calculate centroid from rectangle"""
        x, y, w, h = rect
        return (int(x + w/2), int(y + h/2))

    def _calculate_distances(self, centroids1, centroids2):
        """Calculate Euclidean distances between centroids"""
        return np.linalg.norm(centroids1[:, np.newaxis] - centroids2, axis=2)

class AIModelService:
    """AI Model Service for people counting"""
    
    def __init__(self):
        self.model_loaded = False
        self.net = None
        self.classes = [
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"
        ]
        self.confidence_threshold = 0.4
        self.skip_frames = 30
        self.tracker = CentroidTracker()
        self.total_frames = 0
        self.total_down = 0
        self.total_up = 0
        self.lock = threading.Lock()
        self.websocket_url = "http://localhost:3003/api/v1/broadcast"
        self.notification_enabled = True
        
    def load_model(self, prototxt_path: str, model_path: str) -> bool:
        """Load the AI model"""
        try:
            if not os.path.exists(prototxt_path) or not os.path.exists(model_path):
                logger.error(f"Model files not found: {prototxt_path}, {model_path}")
                return False
                
            self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
            self.model_loaded = True
            logger.info("AI model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            return False

    def process_frame(self, frame: np.ndarray) -> DetectionResult:
        """Process a single frame for people detection and counting"""
        if not self.model_loaded:
            raise RuntimeError("AI model not loaded")
            
        start_time = time.time()
        
        # Resize frame for faster processing
        frame = cv2.resize(frame, (500, int(500 * frame.shape[0] / frame.shape[1])))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        H, W = frame.shape[:2]
        rects = []
        
        # Run object detection every skip_frames
        if self.total_frames % self.skip_frames == 0:
            # Convert frame to blob and run detection
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            self.net.setInput(blob)
            detections = self.net.forward()
            
            # Process detections
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                
                if confidence > self.confidence_threshold:
                    idx = int(detections[0, 0, i, 1])
                    
                    # Only detect people
                    if self.classes[idx] == "person":
                        box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        (startX, startY, endX, endY) = box.astype("int")
                        rects.append((startX, startY, endX - startX, endY - startY))
        
        # Update tracker
        objects = self.tracker.update(rects)
        
        # Count people movement (simplified logic)
        current_count = len(objects)
        
        # Calculate confidence based on detection quality
        confidence = min(1.0, len(rects) / max(current_count, 1))
        
        processing_time = time.time() - start_time
        
        with self.lock:
            self.total_frames += 1
            
        return DetectionResult(
            people_in=self.total_up,
            people_out=self.total_down,
            current_count=current_count,
            confidence=confidence,
            frame_count=self.total_frames,
            processing_time=processing_time,
            timestamp=datetime.now()
        )

    def process_rtsp_stream(self, rtsp_url: str, max_frames: int = 100) -> List[DetectionResult]:
        """Process RTSP stream for people counting"""
        results = []
        
        try:
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                logger.error(f"Failed to open RTSP stream: {rtsp_url}")
                return results
                
            frame_count = 0
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Failed to read frame from RTSP stream")
                    break
                    
                try:
                    result = self.process_frame(frame)
                    results.append(result)
                    frame_count += 1
                    
                    # Log progress
                    if frame_count % 10 == 0:
                        logger.info(f"Processed {frame_count} frames, current count: {result.current_count}")
                        
                except Exception as e:
                    logger.error(f"Error processing frame {frame_count}: {e}")
                    continue
                    
            cap.release()
            logger.info(f"Completed processing {len(results)} frames")
            
        except Exception as e:
            logger.error(f"Error processing RTSP stream: {e}")
            
        return results

    def get_model_status(self) -> Dict:
        """Get AI model status"""
        return {
            "model_loaded": self.model_loaded,
            "total_frames_processed": self.total_frames,
            "total_people_in": self.total_up,
            "total_people_out": self.total_down,
            "confidence_threshold": self.confidence_threshold,
            "skip_frames": self.skip_frames
        }

    def reset_counters(self):
        """Reset counting counters"""
        with self.lock:
            self.total_frames = 0
            self.total_up = 0
            self.total_down = 0
        logger.info("Counters reset")

    async def send_websocket_notification(self, camera_id: str, detection_result: DetectionResult):
        """Send WebSocket notification for detection result"""
        if not self.notification_enabled:
            return
            
        try:
            notification_data = {
                "camera_id": camera_id,
                "people_in": detection_result.people_in,
                "people_out": detection_result.people_out,
                "current_count": detection_result.current_count,
                "confidence": detection_result.confidence,
                "status": "active",
                "processing_time": detection_result.processing_time,
                "frame_count": detection_result.frame_count
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.websocket_url}/camera-update",
                    json={"camera_id": camera_id, "data": notification_data}
                ) as response:
                    if response.status == 200:
                        logger.debug(f"WebSocket notification sent for camera {camera_id}")
                    else:
                        logger.warning(f"Failed to send WebSocket notification: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")

    def process_frame_with_notification(self, frame: np.ndarray, camera_id: str) -> DetectionResult:
        """Process frame and send WebSocket notification"""
        result = self.process_frame(frame)
        
        # Send notification asynchronously
        if self.notification_enabled:
            asyncio.create_task(self.send_websocket_notification(camera_id, result))
        
        return result

    async def process_rtsp_frame(self, camera_id: str, frame: np.ndarray, metrics: Dict = None) -> Dict:
        """
        Process RTSP frame with AI detection and WebSocket notifications
        
        Args:
            camera_id: Camera identifier
            frame: Video frame as numpy array
            metrics: Optional stream metrics
            
        Returns:
            Detection results dictionary
        """
        try:
            start_time = time.time()
            
            # Process frame with AI detection
            detection_results = await self.process_frame_async(frame)
            
            # Add camera and timing information
            detection_results.update({
                'camera_id': camera_id,
                'timestamp': datetime.now().isoformat(),
                'processing_time': time.time() - start_time,
                'stream_metrics': metrics
            })
            
            # Send WebSocket notification
            await self.send_websocket_notification('rtsp_detection', detection_results)
            
            # Update camera analytics
            await self.update_camera_analytics(camera_id, detection_results)
            
            logger.info(f"RTSP frame processed for camera {camera_id}: {detection_results.get('count', 0)} people detected")
            return detection_results
            
        except Exception as e:
            logger.error(f"Error processing RTSP frame for camera {camera_id}: {e}")
            await self.send_websocket_notification('rtsp_error', {
                'camera_id': camera_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {'error': str(e)}

    async def update_camera_analytics(self, camera_id: str, detection_results: Dict):
        """
        Update camera analytics with detection results
        
        Args:
            camera_id: Camera identifier
            detection_results: AI detection results
        """
        try:
            # Extract relevant data
            count = detection_results.get('count', 0)
            confidence = detection_results.get('confidence', 0.0)
            processing_time = detection_results.get('processing_time', 0.0)
            
            # Update analytics in database (placeholder for now)
            # In a real implementation, this would update the database
            analytics_data = {
                'camera_id': camera_id,
                'people_count': count,
                'confidence': confidence,
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
            
            # Send analytics update via WebSocket
            await self.send_websocket_notification('analytics_update', analytics_data)
            
        except Exception as e:
            logger.error(f"Error updating camera analytics for {camera_id}: {e}")

    def setup_rtsp_integration(self, rtsp_service):
        """
        Setup RTSP integration with AI processing
        
        Args:
            rtsp_service: RTSP service instance
        """
        try:
            # Add frame processing callback to RTSP service
            rtsp_service.add_global_callback('frame', self._rtsp_frame_callback)
            
            # Add error handling callback
            rtsp_service.add_global_callback('error', self._rtsp_error_callback)
            
            # Add status change callback
            rtsp_service.add_global_callback('status', self._rtsp_status_callback)
            
            logger.info("RTSP integration setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up RTSP integration: {e}")

    def _rtsp_frame_callback(self, camera_id: str, frame: np.ndarray, metrics):
        """
        Callback for RTSP frame processing
        
        Args:
            camera_id: Camera identifier
            frame: Video frame
            metrics: Stream metrics
        """
        try:
            # Run async processing in event loop
            asyncio.create_task(self.process_rtsp_frame(camera_id, frame, metrics.__dict__))
            
        except Exception as e:
            logger.error(f"Error in RTSP frame callback for camera {camera_id}: {e}")

    def _rtsp_error_callback(self, camera_id: str, error: Exception):
        """
        Callback for RTSP error handling
        
        Args:
            camera_id: Camera identifier
            error: Error exception
        """
        try:
            # Send error notification via WebSocket
            asyncio.create_task(self.send_websocket_notification('rtsp_error', {
                'camera_id': camera_id,
                'error': str(error),
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error in RTSP error callback for camera {camera_id}: {e}")

    def _rtsp_status_callback(self, camera_id: str, old_status, new_status):
        """
        Callback for RTSP status changes
        
        Args:
            camera_id: Camera identifier
            old_status: Previous status
            new_status: New status
        """
        try:
            # Send status change notification via WebSocket
            asyncio.create_task(self.send_websocket_notification('rtsp_status', {
                'camera_id': camera_id,
                'old_status': old_status.value if hasattr(old_status, 'value') else str(old_status),
                'new_status': new_status.value if hasattr(new_status, 'value') else str(new_status),
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error in RTSP status callback for camera {camera_id}: {e}")

# Global AI model service instance
ai_model_service = AIModelService()

def get_ai_model_service() -> AIModelService:
    """Get the global AI model service instance"""
    return ai_model_service 
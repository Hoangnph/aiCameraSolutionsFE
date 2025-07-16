"""
Worker Pool for Camera Stream Processing
Handles concurrent processing of multiple camera streams
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
import time

logger = logging.getLogger(__name__)

@dataclass
class CameraTask:
    """Camera processing task"""
    camera_id: int
    rtsp_url: str
    status: str = "pending"
    worker_id: Optional[str] = None
    start_time: Optional[datetime] = None
    error_count: int = 0
    last_error: Optional[str] = None

@dataclass
class Worker:
    """Worker instance"""
    worker_id: str
    status: str = "idle"
    current_task: Optional[CameraTask] = None
    start_time: Optional[datetime] = None
    processed_frames: int = 0
    error_count: int = 0

class CameraWorkerPool:
    """Worker pool for camera stream processing"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.workers: Dict[str, Worker] = {}
        self.tasks: Dict[int, CameraTask] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = False
        self.lock = threading.Lock()
        
        # Initialize workers
        for i in range(max_workers):
            worker_id = f"worker_{i+1}"
            self.workers[worker_id] = Worker(worker_id=worker_id)
    
    async def start(self):
        """Start the worker pool"""
        self.running = True
        logger.info(f"Worker pool started with {self.max_workers} workers")
        
        # Start monitoring loop
        asyncio.create_task(self._monitor_workers())
    
    async def stop(self):
        """Stop the worker pool"""
        self.running = False
        self.executor.shutdown(wait=True)
        logger.info("Worker pool stopped")
    
    def add_camera_task(self, camera_id: int, rtsp_url: str) -> bool:
        """Add a new camera task to the pool"""
        with self.lock:
            if camera_id in self.tasks:
                logger.warning(f"Camera {camera_id} already has a task")
                return False
            
            task = CameraTask(camera_id=camera_id, rtsp_url=rtsp_url)
            self.tasks[camera_id] = task
            
            # Try to assign to available worker
            self._assign_task_to_worker(task)
            return True
    
    def remove_camera_task(self, camera_id: int) -> bool:
        """Remove a camera task"""
        with self.lock:
            if camera_id not in self.tasks:
                return False
            
            task = self.tasks[camera_id]
            if task.worker_id:
                # Stop worker if it's processing this task
                worker = self.workers.get(task.worker_id)
                if worker and worker.current_task and worker.current_task.camera_id == camera_id:
                    worker.status = "idle"
                    worker.current_task = None
            
            del self.tasks[camera_id]
            return True
    
    def get_task_status(self, camera_id: int) -> Optional[Dict]:
        """Get task status"""
        with self.lock:
            if camera_id not in self.tasks:
                return None
            
            task = self.tasks[camera_id]
            return {
                "camera_id": task.camera_id,
                "status": task.status,
                "worker_id": task.worker_id,
                "start_time": task.start_time.isoformat() if task.start_time else None,
                "error_count": task.error_count,
                "last_error": task.last_error
            }
    
    def get_worker_status(self) -> List[Dict]:
        """Get all worker statuses"""
        with self.lock:
            return [
                {
                    "worker_id": worker.worker_id,
                    "status": worker.status,
                    "current_task": worker.current_task.camera_id if worker.current_task else None,
                    "start_time": worker.start_time.isoformat() if worker.start_time else None,
                    "processed_frames": worker.processed_frames,
                    "error_count": worker.error_count
                }
                for worker in self.workers.values()
            ]
    
    def _assign_task_to_worker(self, task: CameraTask):
        """Assign task to available worker"""
        for worker_id, worker in self.workers.items():
            if worker.status == "idle":
                worker.status = "busy"
                worker.current_task = task
                worker.start_time = datetime.now()
                task.worker_id = worker_id
                task.status = "running"
                task.start_time = datetime.now()
                
                # Start processing in background
                asyncio.create_task(self._process_camera_stream(task))
                logger.info(f"Assigned camera {task.camera_id} to worker {worker_id}")
                return
        
        logger.warning(f"No available workers for camera {task.camera_id}")
    
    async def _process_camera_stream(self, task: CameraTask):
        """Process camera stream"""
        worker = self.workers[task.worker_id]
        
        try:
            logger.info(f"Starting processing for camera {task.camera_id}")
            
            # Open camera stream
            cap = cv2.VideoCapture(task.rtsp_url)
            if not cap.isOpened():
                raise Exception(f"Failed to open stream: {task.rtsp_url}")
            
            frame_count = 0
            while self.running and task.camera_id in self.tasks:
                ret, frame = cap.read()
                if not ret:
                    logger.warning(f"Failed to read frame from camera {task.camera_id}")
                    break
                
                # Process frame (simulate AI processing)
                processed_frame = await self._process_frame(frame, task.camera_id)
                frame_count += 1
                worker.processed_frames += 1
                
                # Simulate processing time
                await asyncio.sleep(0.1)
                
                # Update every 100 frames
                if frame_count % 100 == 0:
                    logger.info(f"Camera {task.camera_id}: processed {frame_count} frames")
            
            cap.release()
            logger.info(f"Finished processing camera {task.camera_id}")
            
        except Exception as e:
            logger.error(f"Error processing camera {task.camera_id}: {e}")
            task.error_count += 1
            task.last_error = str(e)
            worker.error_count += 1
        
        finally:
            # Clean up worker
            with self.lock:
                worker.status = "idle"
                worker.current_task = None
                if task.camera_id in self.tasks:
                    self.tasks[task.camera_id].status = "completed"
    
    async def _process_frame(self, frame: np.ndarray, camera_id: int) -> np.ndarray:
        """Process a single frame (simulate AI processing)"""
        # Simulate AI processing
        # In real implementation, this would run YOLO or other AI models
        
        # Convert to grayscale for simple processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Simulate people detection (just count non-zero pixels as example)
        # In real implementation, this would be actual AI inference
        people_count = np.count_nonzero(gray > 128) // 1000  # Simplified
        
        # Log detection results
        if people_count > 0:
            logger.debug(f"Camera {camera_id}: detected {people_count} people")
        
        return frame
    
    async def _monitor_workers(self):
        """Monitor worker health and status"""
        while self.running:
            try:
                with self.lock:
                    for worker_id, worker in self.workers.items():
                        # Check for stuck workers
                        if worker.status == "busy" and worker.start_time:
                            elapsed = (datetime.now() - worker.start_time).total_seconds()
                            if elapsed > 300:  # 5 minutes timeout
                                logger.warning(f"Worker {worker_id} stuck for {elapsed}s, resetting")
                                worker.status = "idle"
                                worker.current_task = None
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in worker monitoring: {e}")
                await asyncio.sleep(30)

# Global worker pool instance
worker_pool = CameraWorkerPool(max_workers=4) 
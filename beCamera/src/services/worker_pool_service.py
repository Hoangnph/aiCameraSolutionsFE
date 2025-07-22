#!/usr/bin/env python3
"""
Worker Pool Service for RTSP Stream Processing
Handles distributed processing of RTSP streams across multiple workers
"""

import asyncio
import threading
import time
import logging
import queue
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

class WorkerStatus(Enum):
    """Worker status enumeration"""
    IDLE = "idle"
    BUSY = "busy"
    PROCESSING = "processing"
    ERROR = "error"
    OFFLINE = "offline"

class TaskPriority(Enum):
    """Task priority enumeration"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class WorkerMetrics:
    """Worker performance metrics"""
    worker_id: str
    status: WorkerStatus
    tasks_processed: int
    tasks_failed: int
    total_processing_time: float
    average_processing_time: float
    last_task_time: datetime
    cpu_usage: float
    memory_usage: float
    uptime: float

@dataclass
class ProcessingTask:
    """RTSP processing task"""
    task_id: str
    camera_id: str
    frame_data: np.ndarray
    priority: TaskPriority
    created_at: datetime
    timeout: float
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = None

class Worker:
    """Individual worker for processing RTSP frames"""
    
    def __init__(self, worker_id: str, ai_service=None):
        self.worker_id = worker_id
        self.ai_service = ai_service
        self.status = WorkerStatus.IDLE
        self.metrics = WorkerMetrics(
            worker_id=worker_id,
            status=WorkerStatus.IDLE,
            tasks_processed=0,
            tasks_failed=0,
            total_processing_time=0.0,
            average_processing_time=0.0,
            last_task_time=datetime.now(),
            cpu_usage=0.0,
            memory_usage=0.0,
            uptime=0.0
        )
        self.current_task = None
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.is_running = True
        
    def update_metrics(self):
        """Update worker metrics"""
        with self.lock:
            self.metrics.uptime = time.time() - self.start_time
            self.metrics.status = self.status
            self.metrics.last_task_time = datetime.now()
            
            # Calculate average processing time
            if self.metrics.tasks_processed > 0:
                self.metrics.average_processing_time = (
                    self.metrics.total_processing_time / self.metrics.tasks_processed
                )
    
    async def process_task(self, task: ProcessingTask) -> Dict:
        """Process a single task"""
        try:
            with self.lock:
                self.status = WorkerStatus.PROCESSING
                self.current_task = task
                self.update_metrics()
            
            start_time = time.time()
            
            # Process frame with AI
            if self.ai_service:
                result = await self.ai_service.process_rtsp_frame(
                    task.camera_id, 
                    task.frame_data, 
                    task.metadata
                )
            else:
                # Mock processing for testing
                result = {
                    'camera_id': task.camera_id,
                    'count': np.random.randint(0, 10),
                    'confidence': np.random.uniform(0.7, 0.95),
                    'processing_time': time.time() - start_time,
                    'worker_id': self.worker_id,
                    'timestamp': datetime.now().isoformat()
                }
            
            processing_time = time.time() - start_time
            
            # Update metrics
            with self.lock:
                self.metrics.tasks_processed += 1
                self.metrics.total_processing_time += processing_time
                self.status = WorkerStatus.IDLE
                self.current_task = None
                self.update_metrics()
            
            # Execute callback if provided
            if task.callback:
                try:
                    await task.callback(result)
                except Exception as e:
                    logger.error(f"Error in task callback: {e}")
            
            logger.info(f"Worker {self.worker_id} processed task {task.task_id} in {processing_time:.3f}s")
            return result
            
        except Exception as e:
            with self.lock:
                self.metrics.tasks_failed += 1
                self.status = WorkerStatus.ERROR
                self.current_task = None
                self.update_metrics()
            
            logger.error(f"Worker {self.worker_id} failed to process task {task.task_id}: {e}")
            raise
    
    def get_metrics(self) -> WorkerMetrics:
        """Get current worker metrics"""
        with self.lock:
            self.update_metrics()
            return self.metrics
    
    def is_available(self) -> bool:
        """Check if worker is available for new tasks"""
        with self.lock:
            return self.status in [WorkerStatus.IDLE] and self.is_running
    
    def stop(self):
        """Stop the worker"""
        with self.lock:
            self.is_running = False
            self.status = WorkerStatus.OFFLINE

class WorkerPool:
    """Pool of workers for distributed RTSP processing"""
    
    def __init__(self, pool_size: int = 4, ai_service=None):
        self.pool_size = pool_size
        self.ai_service = ai_service
        self.workers: Dict[str, Worker] = {}
        self.task_queue = queue.PriorityQueue()
        self.completed_tasks = queue.Queue()
        self.is_running = False
        self.lock = threading.Lock()
        self.task_counter = 0
        
        # Initialize workers
        self._initialize_workers()
    
    def _initialize_workers(self):
        """Initialize worker pool"""
        for i in range(self.pool_size):
            worker_id = f"worker_{i+1}"
            worker = Worker(worker_id, self.ai_service)
            self.workers[worker_id] = worker
        
        logger.info(f"Initialized worker pool with {self.pool_size} workers")
    
    def start(self):
        """Start the worker pool"""
        self.is_running = True
        
        # Start worker threads
        for worker in self.workers.values():
            thread = threading.Thread(target=self._worker_loop, args=(worker,), daemon=True)
            thread.start()
        
        logger.info("Worker pool started")
    
    def stop(self):
        """Stop the worker pool"""
        self.is_running = False
        
        # Stop all workers
        for worker in self.workers.values():
            worker.stop()
        
        logger.info("Worker pool stopped")
    
    def _worker_loop(self, worker: Worker):
        """Main worker loop"""
        while self.is_running and worker.is_running:
            try:
                # Get task from queue with timeout
                try:
                    priority, task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process task
                asyncio.run(worker.process_task(task))
                
                # Mark task as done
                self.task_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in worker loop for {worker.worker_id}: {e}")
                time.sleep(1)  # Brief pause before retry
    
    async def submit_task(self, camera_id: str, frame_data: np.ndarray, 
                         priority: TaskPriority = TaskPriority.NORMAL,
                         callback: Optional[Callable] = None,
                         metadata: Dict[str, Any] = None) -> str:
        """Submit a task to the worker pool"""
        if not self.is_running:
            raise RuntimeError("Worker pool is not running")
        
        # Create task
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        task = ProcessingTask(
            task_id=task_id,
            camera_id=camera_id,
            frame_data=frame_data,
            priority=priority,
            created_at=datetime.now(),
            timeout=30.0,  # 30 second timeout
            callback=callback,
            metadata=metadata
        )
        
        # Add to queue with priority
        self.task_queue.put((priority.value, task))
        
        logger.info(f"Submitted task {task_id} for camera {camera_id} with priority {priority.name}")
        return task_id
    
    def get_available_worker(self) -> Optional[Worker]:
        """Get an available worker"""
        for worker in self.workers.values():
            if worker.is_available():
                return worker
        return None
    
    def get_pool_status(self) -> Dict:
        """Get overall pool status"""
        with self.lock:
            total_workers = len(self.workers)
            available_workers = sum(1 for w in self.workers.values() if w.is_available())
            busy_workers = sum(1 for w in self.workers.values() if w.status == WorkerStatus.PROCESSING)
            error_workers = sum(1 for w in self.workers.values() if w.status == WorkerStatus.ERROR)
            
            total_tasks = self.task_counter
            queued_tasks = self.task_queue.qsize()
            
            return {
                'total_workers': total_workers,
                'available_workers': available_workers,
                'busy_workers': busy_workers,
                'error_workers': error_workers,
                'total_tasks': total_tasks,
                'queued_tasks': queued_tasks,
                'pool_status': 'healthy' if error_workers == 0 else 'degraded'
            }
    
    def get_worker_metrics(self, worker_id: str) -> Optional[WorkerMetrics]:
        """Get metrics for a specific worker"""
        worker = self.workers.get(worker_id)
        if worker:
            return worker.get_metrics()
        return None
    
    def get_all_worker_metrics(self) -> Dict[str, WorkerMetrics]:
        """Get metrics for all workers"""
        return {worker_id: worker.get_metrics() 
                for worker_id, worker in self.workers.items()}
    
    def reset_worker(self, worker_id: str) -> bool:
        """Reset a worker to idle state"""
        worker = self.workers.get(worker_id)
        if worker:
            with worker.lock:
                worker.status = WorkerStatus.IDLE
                worker.current_task = None
                worker.update_metrics()
            logger.info(f"Reset worker {worker_id}")
            return True
        return False

class WorkerPoolService:
    """Service for managing worker pools"""
    
    def __init__(self):
        self.pools: Dict[str, WorkerPool] = {}
        self.default_pool_size = 4
        self.ai_service = None
    
    def create_pool(self, pool_name: str, pool_size: int = None) -> WorkerPool:
        """Create a new worker pool"""
        if pool_name in self.pools:
            raise ValueError(f"Pool {pool_name} already exists")
        
        size = pool_size or self.default_pool_size
        pool = WorkerPool(size, self.ai_service)
        self.pools[pool_name] = pool
        
        logger.info(f"Created worker pool '{pool_name}' with {size} workers")
        return pool
    
    def get_pool(self, pool_name: str) -> Optional[WorkerPool]:
        """Get a worker pool by name"""
        return self.pools.get(pool_name)
    
    def remove_pool(self, pool_name: str) -> bool:
        """Remove a worker pool"""
        pool = self.pools.get(pool_name)
        if pool:
            pool.stop()
            del self.pools[pool_name]
            logger.info(f"Removed worker pool '{pool_name}'")
            return True
        return False
    
    def start_pool(self, pool_name: str) -> bool:
        """Start a worker pool"""
        pool = self.pools.get(pool_name)
        if pool:
            pool.start()
            return True
        return False
    
    def stop_pool(self, pool_name: str) -> bool:
        """Stop a worker pool"""
        pool = self.pools.get(pool_name)
        if pool:
            pool.stop()
            return True
        return False
    
    def get_all_pools_status(self) -> Dict:
        """Get status of all pools"""
        return {
            pool_name: pool.get_pool_status()
            for pool_name, pool in self.pools.items()
        }
    
    def set_ai_service(self, ai_service):
        """Set AI service for all pools"""
        self.ai_service = ai_service
        for pool in self.pools.values():
            for worker in pool.workers.values():
                worker.ai_service = ai_service
    
    def get_service_status(self) -> Dict:
        """Get overall service status"""
        total_pools = len(self.pools)
        active_pools = sum(1 for pool in self.pools.values() if pool.is_running)
        
        total_workers = sum(len(pool.workers) for pool in self.pools.values())
        available_workers = sum(
            sum(1 for w in pool.workers.values() if w.is_available())
            for pool in self.pools.values()
        )
        
        return {
            'total_pools': total_pools,
            'active_pools': active_pools,
            'total_workers': total_workers,
            'available_workers': available_workers,
            'service_status': 'healthy' if active_pools == total_pools else 'degraded'
        }

# Global worker pool service instance
worker_pool_service = WorkerPoolService()

def get_worker_pool_service() -> WorkerPoolService:
    """Get the global worker pool service instance"""
    return worker_pool_service 
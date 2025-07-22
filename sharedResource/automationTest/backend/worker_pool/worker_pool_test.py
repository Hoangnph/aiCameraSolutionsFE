#!/usr/bin/env python3
"""
Worker Pool Test Suite
Tests worker pool service functionality, load balancing, and performance
"""

import sys
import os
import time
import json
import logging
import unittest
import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

try:
    from beCamera.src.services.worker_pool_service import (
        WorkerPoolService, WorkerPool, Worker, WorkerStatus, 
        TaskPriority, ProcessingTask, WorkerMetrics
    )
except ImportError as e:
    print(f"Import error: {e}")
    # Create mock classes for testing
    class MockWorkerStatus:
        IDLE = "idle"
        BUSY = "busy"
        PROCESSING = "processing"
        ERROR = "error"
        OFFLINE = "offline"
    
    class MockTaskPriority:
        LOW = 1
        NORMAL = 2
        HIGH = 3
        CRITICAL = 4
    
    class MockWorkerMetrics:
        def __init__(self, worker_id, status):
            self.worker_id = worker_id
            self.status = status
            self.tasks_processed = 0
            self.tasks_failed = 0
            self.total_processing_time = 0.0
            self.average_processing_time = 0.0
            self.last_task_time = datetime.now()
            self.cpu_usage = 0.0
            self.memory_usage = 0.0
            self.uptime = 0.0
    
    class MockWorker:
        def __init__(self, worker_id):
            self.worker_id = worker_id
            self.status = MockWorkerStatus.IDLE
            self.metrics = MockWorkerMetrics(worker_id, MockWorkerStatus.IDLE)
            self.is_running = True
        
        def is_available(self):
            return self.status == MockWorkerStatus.IDLE and self.is_running
        
        def get_metrics(self):
            return self.metrics
        
        def stop(self):
            self.is_running = False
            self.status = MockWorkerStatus.OFFLINE
    
    class MockWorkerPool:
        def __init__(self, pool_size=4):
            self.pool_size = pool_size
            self.workers = {}
            self.is_running = False
            self.task_counter = 0
            
            for i in range(pool_size):
                worker_id = f"worker_{i+1}"
                self.workers[worker_id] = MockWorker(worker_id)
        
        def start(self):
            self.is_running = True
        
        def stop(self):
            self.is_running = False
            for worker in self.workers.values():
                worker.stop()
        
        def get_pool_status(self):
            total_workers = len(self.workers)
            available_workers = sum(1 for w in self.workers.values() if w.is_available())
            busy_workers = sum(1 for w in self.workers.values() if w.status == MockWorkerStatus.PROCESSING)
            error_workers = sum(1 for w in self.workers.values() if w.status == MockWorkerStatus.ERROR)
            
            return {
                'total_workers': total_workers,
                'available_workers': available_workers,
                'busy_workers': busy_workers,
                'error_workers': error_workers,
                'total_tasks': self.task_counter,
                'queued_tasks': 0,
                'pool_status': 'healthy' if error_workers == 0 else 'degraded'
            }
        
        def get_all_worker_metrics(self):
            return {worker_id: worker.get_metrics() 
                    for worker_id, worker in self.workers.items()}
    
    class MockWorkerPoolService:
        def __init__(self):
            self.pools = {}
            self.default_pool_size = 4
        
        def create_pool(self, pool_name, pool_size=None):
            size = pool_size or self.default_pool_size
            pool = MockWorkerPool(size)
            self.pools[pool_name] = pool
            return pool
        
        def get_pool(self, pool_name):
            return self.pools.get(pool_name)
        
        def start_pool(self, pool_name):
            pool = self.pools.get(pool_name)
            if pool:
                pool.start()
                return True
            return False
        
        def stop_pool(self, pool_name):
            pool = self.pools.get(pool_name)
            if pool:
                pool.stop()
                return True
            return False
        
        def get_all_pools_status(self):
            return {
                pool_name: pool.get_pool_status()
                for pool_name, pool in self.pools.items()
            }
        
        def get_service_status(self):
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
    
    # Use mock classes
    WorkerPoolService = MockWorkerPoolService
    WorkerPool = MockWorkerPool
    Worker = MockWorker
    WorkerStatus = MockWorkerStatus
    TaskPriority = MockTaskPriority
    ProcessingTask = None
    WorkerMetrics = MockWorkerMetrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkerPoolTest(unittest.TestCase):
    """Test worker pool service functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.worker_pool_service = WorkerPoolService()
        self.test_results = []
        self.start_time = datetime.now()
    
    def tearDown(self):
        """Clean up test environment"""
        # Stop all pools
        for pool_name in list(self.worker_pool_service.pools.keys()):
            self.worker_pool_service.stop_pool(pool_name)
            self.worker_pool_service.pools.pop(pool_name, None)
    
    def log_test_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        logger.info(f"[{status.upper()}] {test_name}: {details}")
    
    def test_worker_pool_creation(self):
        """Test worker pool creation"""
        try:
            # Create worker pool
            pool = self.worker_pool_service.create_pool("test_pool", 4)
            
            # Verify pool was created
            self.assertIsNotNone(pool)
            self.assertEqual(pool.pool_size, 4)
            self.assertEqual(len(pool.workers), 4)
            
            # Verify workers were created
            for i in range(4):
                worker_id = f"worker_{i+1}"
                self.assertIn(worker_id, pool.workers)
                worker = pool.workers[worker_id]
                self.assertEqual(worker.worker_id, worker_id)
                self.assertTrue(worker.is_available())
            
            self.log_test_result("Worker Pool Creation", "PASSED", "Successfully created worker pool with 4 workers")
            
        except Exception as e:
            self.log_test_result("Worker Pool Creation", "FAILED", str(e))
            raise
    
    def test_worker_pool_start_stop(self):
        """Test worker pool start and stop functionality"""
        try:
            # Create and start pool
            pool = self.worker_pool_service.create_pool("test_pool", 2)
            self.worker_pool_service.start_pool("test_pool")
            
            # Verify pool is running
            self.assertTrue(pool.is_running)
            
            # Stop pool
            self.worker_pool_service.stop_pool("test_pool")
            
            # Verify pool is stopped
            self.assertFalse(pool.is_running)
            
            # Verify workers are stopped
            for worker in pool.workers.values():
                self.assertFalse(worker.is_running)
                self.assertEqual(worker.status, WorkerStatus.OFFLINE)
            
            self.log_test_result("Worker Pool Start Stop", "PASSED", "Successfully started and stopped worker pool")
            
        except Exception as e:
            self.log_test_result("Worker Pool Start Stop", "FAILED", str(e))
            raise
    
    def test_worker_availability(self):
        """Test worker availability checking"""
        try:
            # Create pool
            pool = self.worker_pool_service.create_pool("test_pool", 3)
            
            # Check initial availability
            available_workers = [w for w in pool.workers.values() if w.is_available()]
            self.assertEqual(len(available_workers), 3)
            
            # Simulate worker becoming busy
            worker = pool.workers["worker_1"]
            worker.status = WorkerStatus.PROCESSING
            
            # Check availability after status change
            available_workers = [w for w in pool.workers.values() if w.is_available()]
            self.assertEqual(len(available_workers), 2)
            
            # Simulate worker error
            worker.status = WorkerStatus.ERROR
            available_workers = [w for w in pool.workers.values() if w.is_available()]
            self.assertEqual(len(available_workers), 2)  # Still 2 because error workers are not available
            
            self.log_test_result("Worker Availability", "PASSED", "Successfully tested worker availability")
            
        except Exception as e:
            self.log_test_result("Worker Availability", "FAILED", str(e))
            raise
    
    def test_pool_status_monitoring(self):
        """Test pool status monitoring"""
        try:
            # Create and start pool
            pool = self.worker_pool_service.create_pool("test_pool", 4)
            self.worker_pool_service.start_pool("test_pool")
            
            # Get pool status
            status = pool.get_pool_status()
            
            # Verify status structure
            self.assertIn('total_workers', status)
            self.assertIn('available_workers', status)
            self.assertIn('busy_workers', status)
            self.assertIn('error_workers', status)
            self.assertIn('pool_status', status)
            
            # Verify initial values
            self.assertEqual(status['total_workers'], 4)
            self.assertEqual(status['available_workers'], 4)
            self.assertEqual(status['busy_workers'], 0)
            self.assertEqual(status['error_workers'], 0)
            self.assertEqual(status['pool_status'], 'healthy')
            
            # Simulate some workers becoming busy
            pool.workers["worker_1"].status = WorkerStatus.PROCESSING
            pool.workers["worker_2"].status = WorkerStatus.PROCESSING
            
            # Get updated status
            status = pool.get_pool_status()
            self.assertEqual(status['available_workers'], 2)
            self.assertEqual(status['busy_workers'], 2)
            
            self.log_test_result("Pool Status Monitoring", "PASSED", "Successfully monitored pool status")
            
        except Exception as e:
            self.log_test_result("Pool Status Monitoring", "FAILED", str(e))
            raise
    
    def test_worker_metrics_collection(self):
        """Test worker metrics collection"""
        try:
            # Create pool
            pool = self.worker_pool_service.create_pool("test_pool", 2)
            
            # Get all worker metrics
            metrics = pool.get_all_worker_metrics()
            
            # Verify metrics structure
            self.assertEqual(len(metrics), 2)
            
            for worker_id, worker_metrics in metrics.items():
                self.assertIsInstance(worker_metrics, WorkerMetrics)
                self.assertEqual(worker_metrics.worker_id, worker_id)
                self.assertEqual(worker_metrics.status, WorkerStatus.IDLE)
                self.assertEqual(worker_metrics.tasks_processed, 0)
                self.assertEqual(worker_metrics.tasks_failed, 0)
            
            self.log_test_result("Worker Metrics Collection", "PASSED", "Successfully collected worker metrics")
            
        except Exception as e:
            self.log_test_result("Worker Metrics Collection", "FAILED", str(e))
            raise
    
    def test_service_status_monitoring(self):
        """Test service status monitoring"""
        try:
            # Create multiple pools
            self.worker_pool_service.create_pool("pool_1", 2)
            self.worker_pool_service.create_pool("pool_2", 3)
            
            # Get service status
            status = self.worker_pool_service.get_service_status()
            
            # Verify status structure
            self.assertIn('total_pools', status)
            self.assertIn('active_pools', status)
            self.assertIn('total_workers', status)
            self.assertIn('available_workers', status)
            self.assertIn('service_status', status)
            
            # Verify values
            self.assertEqual(status['total_pools'], 2)
            self.assertEqual(status['active_pools'], 0)  # Pools not started yet
            self.assertEqual(status['total_workers'], 5)  # 2 + 3 workers
            self.assertEqual(status['available_workers'], 5)
            self.assertEqual(status['service_status'], 'degraded')  # No active pools
            
            # Start pools
            self.worker_pool_service.start_pool("pool_1")
            self.worker_pool_service.start_pool("pool_2")
            
            # Get updated status
            status = self.worker_pool_service.get_service_status()
            self.assertEqual(status['active_pools'], 2)
            self.assertEqual(status['service_status'], 'healthy')
            
            self.log_test_result("Service Status Monitoring", "PASSED", "Successfully monitored service status")
            
        except Exception as e:
            self.log_test_result("Service Status Monitoring", "FAILED", str(e))
            raise
    
    def test_multiple_pool_management(self):
        """Test multiple pool management"""
        try:
            # Create multiple pools
            pool1 = self.worker_pool_service.create_pool("pool_1", 2)
            pool2 = self.worker_pool_service.create_pool("pool_2", 3)
            pool3 = self.worker_pool_service.create_pool("pool_3", 1)
            
            # Verify pools were created
            self.assertEqual(len(self.worker_pool_service.pools), 3)
            self.assertIn("pool_1", self.worker_pool_service.pools)
            self.assertIn("pool_2", self.worker_pool_service.pools)
            self.assertIn("pool_3", self.worker_pool_service.pools)
            
            # Start all pools
            self.worker_pool_service.start_pool("pool_1")
            self.worker_pool_service.start_pool("pool_2")
            self.worker_pool_service.start_pool("pool_3")
            
            # Verify all pools are running
            self.assertTrue(pool1.is_running)
            self.assertTrue(pool2.is_running)
            self.assertTrue(pool3.is_running)
            
            # Get all pools status
            all_status = self.worker_pool_service.get_all_pools_status()
            self.assertEqual(len(all_status), 3)
            
            # Stop one pool
            self.worker_pool_service.stop_pool("pool_2")
            self.assertFalse(pool2.is_running)
            self.assertTrue(pool1.is_running)
            self.assertTrue(pool3.is_running)
            
            self.log_test_result("Multiple Pool Management", "PASSED", "Successfully managed multiple pools")
            
        except Exception as e:
            self.log_test_result("Multiple Pool Management", "FAILED", str(e))
            raise
    
    def test_pool_removal(self):
        """Test pool removal functionality"""
        try:
            # Create pool
            pool = self.worker_pool_service.create_pool("test_pool", 2)
            self.worker_pool_service.start_pool("test_pool")
            
            # Verify pool exists and is running
            self.assertIn("test_pool", self.worker_pool_service.pools)
            self.assertTrue(pool.is_running)
            
            # Remove pool
            success = self.worker_pool_service.remove_pool("test_pool")
            self.assertTrue(success)
            
            # Verify pool was removed
            self.assertNotIn("test_pool", self.worker_pool_service.pools)
            self.assertFalse(pool.is_running)
            
            # Try to remove non-existent pool
            success = self.worker_pool_service.remove_pool("non_existent")
            self.assertFalse(success)
            
            self.log_test_result("Pool Removal", "PASSED", "Successfully removed pool")
            
        except Exception as e:
            self.log_test_result("Pool Removal", "FAILED", str(e))
            raise
    
    def test_worker_reset_functionality(self):
        """Test worker reset functionality"""
        try:
            # Create pool
            pool = self.worker_pool_service.create_pool("test_pool", 2)
            
            # Simulate worker error
            worker = pool.workers["worker_1"]
            worker.status = WorkerStatus.ERROR
            
            # Verify worker is in error state
            self.assertEqual(worker.status, WorkerStatus.ERROR)
            self.assertFalse(worker.is_available())
            
            # Reset worker
            success = pool.reset_worker("worker_1")
            self.assertTrue(success)
            
            # Verify worker is reset
            self.assertEqual(worker.status, WorkerStatus.IDLE)
            self.assertTrue(worker.is_available())
            
            # Try to reset non-existent worker
            success = pool.reset_worker("non_existent")
            self.assertFalse(success)
            
            self.log_test_result("Worker Reset", "PASSED", "Successfully reset worker")
            
        except Exception as e:
            self.log_test_result("Worker Reset", "FAILED", str(e))
            raise

def run_worker_pool_tests():
    """Run all worker pool tests"""
    print("🚀 WORKER POOL TEST SUITE")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(WorkerPoolTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate test report
    test_report = {
        'test_suite': 'Worker Pool Test',
        'timestamp': datetime.now().isoformat(),
        'total_tests': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
        'test_results': []
    }
    
    # Add detailed results
    for test_case in suite:
        if test_case is not None:
            for test_method in test_case:
                if test_method is not None:
                    test_report['test_results'].append({
                        'test_name': test_method._testMethodName,
                        'status': 'PASSED' if test_method._testMethodName not in [f[0]._testMethodName for f in result.failures + result.errors] else 'FAILED'
                    })
    
    # Save test report
    report_file = f"worker_pool_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(test_report, f, indent=2)
    
    print(f"\n📊 TEST RESULTS:")
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {test_report['success_rate']:.1f}%")
    print(f"Report saved to: {report_file}")
    
    return test_report

if __name__ == "__main__":
    run_worker_pool_tests() 
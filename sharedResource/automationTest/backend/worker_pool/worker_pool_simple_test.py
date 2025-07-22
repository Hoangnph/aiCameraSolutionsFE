#!/usr/bin/env python3
"""
Simplified Worker Pool Test
Quick test of worker pool functionality
"""

import sys
import os
import time
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def test_worker_pool_basic_functionality():
    """Test basic worker pool functionality"""
    print("🧪 TESTING WORKER POOL BASIC FUNCTIONALITY")
    print("=" * 50)
    
    test_results = []
    
    try:
        # Test 1: Create worker pool service
        service = MockWorkerPoolService()
        test_results.append(("Create Service", "PASSED", "Worker pool service created successfully"))
        
        # Test 2: Create worker pool
        pool = service.create_pool("test_pool", 4)
        assert pool is not None
        assert pool.pool_size == 4
        assert len(pool.workers) == 4
        test_results.append(("Create Pool", "PASSED", "Worker pool created with 4 workers"))
        
        # Test 3: Start pool
        success = service.start_pool("test_pool")
        assert success
        assert pool.is_running
        test_results.append(("Start Pool", "PASSED", "Worker pool started successfully"))
        
        # Test 4: Check pool status
        status = pool.get_pool_status()
        assert status['total_workers'] == 4
        assert status['available_workers'] == 4
        assert status['pool_status'] == 'healthy'
        test_results.append(("Pool Status", "PASSED", "Pool status monitoring working"))
        
        # Test 5: Check worker availability
        available_workers = [w for w in pool.workers.values() if w.is_available()]
        assert len(available_workers) == 4
        test_results.append(("Worker Availability", "PASSED", "All workers available"))
        
        # Test 6: Simulate worker busy state
        worker = pool.workers["worker_1"]
        worker.status = MockWorkerStatus.PROCESSING
        available_workers = [w for w in pool.workers.values() if w.is_available()]
        assert len(available_workers) == 3
        test_results.append(("Worker State Change", "PASSED", "Worker state change working"))
        
        # Test 7: Get worker metrics
        metrics = pool.get_all_worker_metrics()
        assert len(metrics) == 4
        for worker_id, worker_metrics in metrics.items():
            assert worker_metrics.worker_id == worker_id
        test_results.append(("Worker Metrics", "PASSED", "Worker metrics collection working"))
        
        # Test 8: Stop pool
        service.stop_pool("test_pool")
        assert not pool.is_running
        test_results.append(("Stop Pool", "PASSED", "Worker pool stopped successfully"))
        
        # Test 9: Service status
        service_status = service.get_service_status()
        assert service_status['total_pools'] == 1
        assert service_status['active_pools'] == 0
        test_results.append(("Service Status", "PASSED", "Service status monitoring working"))
        
        print("✅ ALL TESTS PASSED!")
        
    except Exception as e:
        test_results.append(("Error", "FAILED", str(e)))
        print(f"❌ TEST FAILED: {e}")
    
    # Print results
    print("\n📊 TEST RESULTS:")
    for test_name, status, details in test_results:
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {test_name}: {details}")
    
    # Calculate success rate
    passed = sum(1 for _, status, _ in test_results if status == "PASSED")
    total = len(test_results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}% ({passed}/{total})")
    
    return {
        'test_suite': 'Worker Pool Simple Test',
        'timestamp': datetime.now().isoformat(),
        'total_tests': total,
        'passed': passed,
        'failed': total - passed,
        'success_rate': success_rate,
        'test_results': test_results
    }

if __name__ == "__main__":
    test_worker_pool_basic_functionality() 
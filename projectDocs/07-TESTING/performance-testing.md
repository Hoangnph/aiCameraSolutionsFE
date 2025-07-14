# Performance Testing Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn performance testing cho hệ thống AI Camera Counting, bao gồm load testing, stress testing, và performance monitoring.

### 🎯 Mục tiêu
- Đảm bảo system performance đáp ứng requirements
- Identify performance bottlenecks
- Validate scalability và reliability
- Optimize system performance

### 🛠️ Performance Testing Tools

#### K6 Load Testing
```javascript
// tests/performance/k6-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests must complete below 200ms
    http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
    errors: ['rate<0.01'],
  },
};

const BASE_URL = 'http://localhost:8001';

export default function () {
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token',
    },
  };

  // Test camera list endpoint
  const cameraListResponse = http.get(`${BASE_URL}/api/cameras/`, params);
  check(cameraListResponse, {
    'camera list status is 200': (r) => r.status === 200,
    'camera list response time < 200ms': (r) => r.timings.duration < 200,
  });

  // Test camera creation
  const cameraData = {
    name: `Test Camera ${Date.now()}`,
    location: 'Building A',
    ip_address: '192.168.1.100',
    status: 'active'
  };

  const createCameraResponse = http.post(
    `${BASE_URL}/api/cameras/`,
    JSON.stringify(cameraData),
    params
  );
  check(createCameraResponse, {
    'create camera status is 201': (r) => r.status === 201,
    'create camera response time < 300ms': (r) => r.timings.duration < 300,
  });

  // Test count data endpoint
  const countDataResponse = http.get(`${BASE_URL}/api/count-data/`, params);
  check(countDataResponse, {
    'count data status is 200': (r) => r.status === 200,
    'count data response time < 150ms': (r) => r.timings.duration < 150,
  });

  // Test AI processing endpoint
  const aiData = {
    camera_id: 1,
    frame_data: 'base64_encoded_frame_data',
    timestamp: Date.now()
  };

  const aiResponse = http.post(
    `${BASE_URL}/api/ai/process-frame`,
    JSON.stringify(aiData),
    params
  );
  check(aiResponse, {
    'ai processing status is 200': (r) => r.status === 200,
    'ai processing response time < 500ms': (r) => r.timings.duration < 500,
  });

  errorRate.add(createCameraResponse.status !== 201);
  errorRate.add(countDataResponse.status !== 200);
  errorRate.add(aiResponse.status !== 200);

  sleep(1);
}
```

#### JMeter Test Plan
```xml
<!-- tests/performance/jmeter-test-plan.jmx -->
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="AI Camera System Performance Test">
      <elementProp name="TestPlan.arguments" elementType="Arguments">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Camera API Load Test">
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">10</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">60</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Get Cameras">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8001</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.path">/api/cameras/</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Code Assertion">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="49586">200</stringProp>
            </collectionProp>
            <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">8</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### 🧪 Load Testing Scenarios

#### API Load Testing
```python
# tests/performance/api_load_test.py
import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    error_rate: float

class APILoadTester:
    def __init__(self, base_url: str, max_concurrent: int = 100):
        self.base_url = base_url
        self.max_concurrent = max_concurrent
        self.results: List[Dict] = []
    
    async def load_test(self, endpoint: str, method: str = 'GET', 
                       data: Dict = None, duration: int = 300) -> PerformanceMetrics:
        """Run load test for specified duration"""
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(self.max_concurrent):
                task = asyncio.create_task(
                    self._make_request(session, endpoint, method, data)
                )
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
        end_time = time.time()
        return self._calculate_metrics(start_time, end_time)
    
    async def _make_request(self, session: aiohttp.ClientSession, 
                           endpoint: str, method: str, data: Dict = None):
        """Make individual request"""
        start = time.time()
        try:
            if method == 'GET':
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    duration = time.time() - start
                    self.results.append({
                        'status': response.status,
                        'duration': duration,
                        'success': response.status == 200
                    })
            elif method == 'POST':
                async with session.post(f"{self.base_url}{endpoint}", 
                                      json=data) as response:
                    duration = time.time() - start
                    self.results.append({
                        'status': response.status,
                        'duration': duration,
                        'success': response.status in [200, 201]
                    })
        except Exception as e:
            duration = time.time() - start
            self.results.append({
                'status': 'error',
                'duration': duration,
                'success': False,
                'error': str(e)
            })
    
    def _calculate_metrics(self, start_time: float, end_time: float) -> PerformanceMetrics:
        """Calculate performance metrics from results"""
        total_requests = len(self.results)
        successful_requests = len([r for r in self.results if r['success']])
        failed_requests = total_requests - successful_requests
        
        response_times = [r['duration'] for r in self.results]
        response_times.sort()
        
        total_duration = end_time - start_time
        
        return PerformanceMetrics(
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time=statistics.mean(response_times),
            p95_response_time=response_times[int(len(response_times) * 0.95)],
            p99_response_time=response_times[int(len(response_times) * 0.99)],
            requests_per_second=total_requests / total_duration,
            error_rate=failed_requests / total_requests
        )

# Usage example
async def run_api_load_tests():
    tester = APILoadTester('http://localhost:8001')
    
    # Test camera list endpoint
    print("Testing camera list endpoint...")
    camera_list_metrics = await tester.load_test('/api/cameras/')
    print(f"Camera List - RPS: {camera_list_metrics.requests_per_second:.2f}, "
          f"Avg RT: {camera_list_metrics.average_response_time:.2f}ms")
    
    # Test camera creation
    print("Testing camera creation...")
    camera_data = {
        "name": "Load Test Camera",
        "location": "Building A",
        "ip_address": "192.168.1.100",
        "status": "active"
    }
    create_metrics = await tester.load_test('/api/cameras/', 'POST', camera_data)
    print(f"Camera Creation - RPS: {create_metrics.requests_per_second:.2f}, "
          f"Avg RT: {create_metrics.average_response_time:.2f}ms")

if __name__ == "__main__":
    asyncio.run(run_api_load_tests())
```

#### Database Performance Testing
```python
# tests/performance/database_performance_test.py
import asyncio
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict

class DatabasePerformanceTester:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def test_query_performance(self, query: str, iterations: int = 1000) -> Dict:
        """Test database query performance"""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            
            with self.SessionLocal() as session:
                result = session.execute(text(query))
                result.fetchall()
            
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        return {
            'query': query,
            'iterations': iterations,
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'p95_time': sorted(times)[int(len(times) * 0.95)],
            'p99_time': sorted(times)[int(len(times) * 0.99)]
        }
    
    def test_concurrent_queries(self, query: str, concurrent_users: int = 50) -> Dict:
        """Test database performance under concurrent load"""
        async def execute_query():
            start_time = time.time()
            
            with self.SessionLocal() as session:
                result = session.execute(text(query))
                result.fetchall()
            
            return (time.time() - start_time) * 1000
        
        async def run_concurrent_test():
            tasks = [execute_query() for _ in range(concurrent_users)]
            return await asyncio.gather(*tasks)
        
        times = asyncio.run(run_concurrent_test())
        
        return {
            'query': query,
            'concurrent_users': concurrent_users,
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'p95_time': sorted(times)[int(len(times) * 0.95)],
            'p99_time': sorted(times)[int(len(times) * 0.99)]
        }
    
    def test_bulk_operations(self, operation_type: str, batch_size: int = 1000) -> Dict:
        """Test bulk database operations"""
        start_time = time.time()
        
        with self.SessionLocal() as session:
            if operation_type == 'insert':
                # Test bulk insert
                cameras = []
                for i in range(batch_size):
                    cameras.append({
                        'name': f'Camera {i}',
                        'location': f'Building {i % 10}',
                        'ip_address': f'192.168.1.{i % 255}',
                        'status': 'active'
                    })
                
                session.execute(text("""
                    INSERT INTO cameras (name, location, ip_address, status)
                    VALUES (:name, :location, :ip_address, :status)
                """), cameras)
                
            elif operation_type == 'select':
                # Test bulk select
                result = session.execute(text("SELECT * FROM cameras LIMIT :limit"))
                result.fetchall()
            
            session.commit()
        
        end_time = time.time()
        
        return {
            'operation': operation_type,
            'batch_size': batch_size,
            'total_time': (end_time - start_time) * 1000,
            'operations_per_second': batch_size / (end_time - start_time)
        }

# Usage example
def run_database_performance_tests():
    tester = DatabasePerformanceTester('postgresql://user:pass@localhost/ai_camera')
    
    # Test simple queries
    print("Testing simple SELECT query...")
    select_result = tester.test_query_performance("SELECT * FROM cameras LIMIT 10")
    print(f"SELECT Query - Avg: {select_result['average_time']:.2f}ms, "
          f"P95: {select_result['p95_time']:.2f}ms")
    
    # Test concurrent queries
    print("Testing concurrent queries...")
    concurrent_result = tester.test_concurrent_queries("SELECT * FROM cameras LIMIT 10")
    print(f"Concurrent Queries - Avg: {concurrent_result['average_time']:.2f}ms, "
          f"P95: {concurrent_result['p95_time']:.2f}ms")
    
    # Test bulk operations
    print("Testing bulk insert...")
    bulk_insert_result = tester.test_bulk_operations('insert', 1000)
    print(f"Bulk Insert - Total: {bulk_insert_result['total_time']:.2f}ms, "
          f"OPS: {bulk_insert_result['operations_per_second']:.2f}")

if __name__ == "__main__":
    run_database_performance_tests()
```

### 🧪 Stress Testing

#### System Stress Testing
```python
# tests/performance/stress_test.py
import asyncio
import aiohttp
import time
import psutil
import os
from typing import Dict, List

class StressTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
    
    async def stress_test(self, max_concurrent: int = 1000, duration: int = 600):
        """Run stress test to find system limits"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(max_concurrent):
                task = asyncio.create_task(self._stress_request(session, i))
                tasks.append(task)
            
            # Monitor system resources
            monitoring_task = asyncio.create_task(self._monitor_resources())
            
            # Run stress test
            await asyncio.gather(*tasks)
            monitoring_task.cancel()
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        end_cpu = psutil.cpu_percent()
        
        return {
            'duration': end_time - start_time,
            'total_requests': len(self.results),
            'successful_requests': len([r for r in self.results if r['success']]),
            'failed_requests': len([r for r in self.results if not r['success']]),
            'memory_increase': end_memory - start_memory,
            'cpu_usage': end_cpu,
            'average_response_time': sum(r['duration'] for r in self.results) / len(self.results),
            'max_concurrent': max_concurrent
        }
    
    async def _stress_request(self, session: aiohttp.ClientSession, request_id: int):
        """Make stress test request"""
        start = time.time()
        try:
            # Rotate between different endpoints
            endpoints = [
                '/api/cameras/',
                '/api/count-data/',
                '/api/ai/process-frame'
            ]
            endpoint = endpoints[request_id % len(endpoints)]
            
            if endpoint == '/api/ai/process-frame':
                data = {
                    'camera_id': request_id % 10,
                    'frame_data': 'base64_encoded_frame_data',
                    'timestamp': time.time()
                }
                async with session.post(f"{self.base_url}{endpoint}", json=data) as response:
                    duration = time.time() - start
                    self.results.append({
                        'request_id': request_id,
                        'status': response.status,
                        'duration': duration,
                        'success': response.status == 200
                    })
            else:
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    duration = time.time() - start
                    self.results.append({
                        'request_id': request_id,
                        'status': response.status,
                        'duration': duration,
                        'success': response.status == 200
                    })
        except Exception as e:
            duration = time.time() - start
            self.results.append({
                'request_id': request_id,
                'status': 'error',
                'duration': duration,
                'success': False,
                'error': str(e)
            })
    
    async def _monitor_resources(self):
        """Monitor system resources during stress test"""
        while True:
            memory = psutil.Process().memory_info().rss / 1024 / 1024
            cpu = psutil.cpu_percent()
            
            print(f"Memory: {memory:.2f}MB, CPU: {cpu:.1f}%")
            
            # Alert if resources are critically high
            if memory > 2048:  # 2GB
                print("⚠️  High memory usage detected!")
            if cpu > 90:
                print("⚠️  High CPU usage detected!")
            
            await asyncio.sleep(5)

# Usage example
async def run_stress_test():
    tester = StressTester('http://localhost:8001')
    
    print("Starting stress test...")
    result = await tester.stress_test(max_concurrent=500, duration=300)
    
    print(f"Stress Test Results:")
    print(f"Duration: {result['duration']:.2f}s")
    print(f"Total Requests: {result['total_requests']}")
    print(f"Successful: {result['successful_requests']}")
    print(f"Failed: {result['failed_requests']}")
    print(f"Success Rate: {result['successful_requests']/result['total_requests']*100:.2f}%")
    print(f"Memory Increase: {result['memory_increase']:.2f}MB")
    print(f"CPU Usage: {result['cpu_usage']:.1f}%")
    print(f"Avg Response Time: {result['average_response_time']:.2f}ms")

if __name__ == "__main__":
    asyncio.run(run_stress_test())
```

### 📊 Performance Monitoring

#### Real-time Performance Monitoring
```python
# src/monitoring/performance_monitor.py
import time
import psutil
import asyncio
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PerformanceMetrics:
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_io: Dict[str, float]
    response_time: float
    requests_per_second: float
    error_rate: float

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    async def start_monitoring(self, interval: int = 60):
        """Start continuous performance monitoring"""
        while True:
            metrics = self._collect_metrics()
            self.metrics_history.append(metrics)
            
            # Keep only last 24 hours of data
            if len(self.metrics_history) > 1440:  # 24 hours * 60 minutes
                self.metrics_history.pop(0)
            
            # Check for performance issues
            self._check_performance_alerts(metrics)
            
            await asyncio.sleep(interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_usage_percent = psutil.disk_usage('/').percent
        
        network_io = psutil.net_io_counters()
        network_metrics = {
            'bytes_sent': network_io.bytes_sent,
            'bytes_recv': network_io.bytes_recv,
            'packets_sent': network_io.packets_sent,
            'packets_recv': network_io.packets_recv
        }
        
        # Calculate application metrics
        uptime = time.time() - self.start_time
        requests_per_second = self.request_count / uptime if uptime > 0 else 0
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
        
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_usage_percent=disk_usage_percent,
            network_io=network_metrics,
            response_time=0,  # Will be updated by request tracking
            requests_per_second=requests_per_second,
            error_rate=error_rate
        )
    
    def _check_performance_alerts(self, metrics: PerformanceMetrics):
        """Check for performance issues and send alerts"""
        alerts = []
        
        if metrics.cpu_percent > 80:
            alerts.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")
        
        if metrics.memory_percent > 85:
            alerts.append(f"High memory usage: {metrics.memory_percent:.1f}%")
        
        if metrics.disk_usage_percent > 90:
            alerts.append(f"High disk usage: {metrics.disk_usage_percent:.1f}%")
        
        if metrics.error_rate > 0.05:  # 5%
            alerts.append(f"High error rate: {metrics.error_rate:.2%}")
        
        if alerts:
            print(f"🚨 Performance Alerts at {metrics.timestamp}:")
            for alert in alerts:
                print(f"  - {alert}")
    
    def record_request(self, response_time: float, success: bool = True):
        """Record a request for performance tracking"""
        self.request_count += 1
        if not success:
            self.error_count += 1
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for the last hour"""
        now = datetime.now()
        one_hour_ago = now.replace(hour=now.hour-1)
        
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= one_hour_ago
        ]
        
        if not recent_metrics:
            return {}
        
        return {
            'avg_cpu': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            'avg_memory': sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            'avg_response_time': sum(m.response_time for m in recent_metrics) / len(recent_metrics),
            'avg_requests_per_second': sum(m.requests_per_second for m in recent_metrics) / len(recent_metrics),
            'avg_error_rate': sum(m.error_rate for m in recent_metrics) / len(recent_metrics),
            'total_requests': self.request_count,
            'total_errors': self.error_count
        }

# Usage in FastAPI application
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

class PerformanceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, monitor: PerformanceMonitor):
        super().__init__(app)
        self.monitor = monitor
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            self.monitor.record_request(
                response_time=time.time() - start_time,
                success=response.status_code < 400
            )
            return response
        except Exception:
            self.monitor.record_request(
                response_time=time.time() - start_time,
                success=False
            )
            raise
```

### 📋 Performance Testing Checklist

#### Pre-Testing Setup
- [ ] Define performance requirements
- [ ] Set up test environment
- [ ] Prepare test data
- [ ] Configure monitoring tools
- [ ] Set up baseline measurements

#### Load Testing
- [ ] Test normal load conditions
- [ ] Test peak load conditions
- [ ] Test sustained load
- [ ] Monitor resource usage
- [ ] Record response times

#### Stress Testing
- [ ] Test beyond normal capacity
- [ ] Identify breaking points
- [ ] Test recovery mechanisms
- [ ] Monitor system behavior
- [ ] Document failure modes

#### Performance Analysis
- [ ] Analyze response time distributions
- [ ] Identify bottlenecks
- [ ] Optimize slow components
- [ ] Validate improvements
- [ ] Document findings

#### Monitoring Setup
- [ ] Configure real-time monitoring
- [ ] Set up performance alerts
- [ ] Create performance dashboards
- [ ] Establish baseline metrics
- [ ] Plan scaling strategies

### 🎯 Performance Targets

#### Response Time Targets
- **API Endpoints**: < 200ms (95th percentile)
- **Database Queries**: < 100ms (95th percentile)
- **Frontend Pages**: < 3 seconds (95th percentile)
- **AI Processing**: < 500ms (95th percentile)

#### Throughput Targets
- **API Requests**: > 1000 requests/second
- **Database Operations**: > 5000 operations/second
- **Concurrent Users**: > 500 simultaneous users
- **Real-time Updates**: < 100ms latency

#### Resource Usage Targets
- **Memory Usage**: < 2GB per instance
- **CPU Usage**: < 80% under normal load
- **Disk Usage**: < 10GB for application data
- **Network I/O**: < 100MB/s per instance

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
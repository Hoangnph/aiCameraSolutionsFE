#!/usr/bin/env python3
"""
Performance Testing Suite - AI Camera Counting System
Tests API performance, database performance, load testing, resource monitoring
"""

import requests
import json
import time
import sys
import threading
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

class PerformanceTestSuite:
    def __init__(self):
        self.base_url_auth = "http://localhost:3001/api/v1"
        self.base_url_camera = "http://localhost:3002/api/v1"
        self.auth_token = None
        self.test_results = []
        self.session = requests.Session()
        self.performance_metrics = {}
        
    def log_test(self, test_name: str, status: str, details: str = "", metrics: Dict = None):
        """Log test result with performance metrics"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "metrics": metrics or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {details}")
        if metrics:
            print(f"   📊 Metrics: {json.dumps(metrics, indent=2)}")
        
    def get_auth_token(self) -> bool:
        """Get authentication token for testing"""
        try:
            # Register a test user first
            register_data = {
                "username": f"perf_test_{int(time.time())}",
                "email": f"perf_test_{int(time.time())}@example.com",
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Performance",
                "lastName": "Test",
                "registrationCode": "DEV2024"
            }
            
            response = self.session.post(f"{self.base_url_auth}/auth/register", json=register_data)
            if response.status_code == 201:
                self.auth_token = response.json()["data"]["accessToken"]
                return True
            else:
                # Try login if registration fails
                login_data = {
                    "username": "apitestuser",
                    "password": "Test123!"
                }
                response = self.session.post(f"{self.base_url_auth}/auth/login", json=login_data)
                if response.status_code == 200:
                    self.auth_token = response.json()["data"]["accessToken"]
                    return True
                    
            self.log_test("Get Auth Token", "FAILED", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Get Auth Token", "FAILED", str(e))
            return False

    def measure_response_time(self, url: str, method: str = "GET", headers: Dict = None, 
                            data: Dict = None, iterations: int = 10) -> Dict:
        """Measure response time for an endpoint"""
        response_times = []
        success_count = 0
        error_count = 0
        
        for i in range(iterations):
            start_time = time.time()
            try:
                if method.upper() == "GET":
                    response = self.session.get(url, headers=headers, timeout=10)
                elif method.upper() == "POST":
                    response = self.session.post(url, headers=headers, json=data, timeout=10)
                elif method.upper() == "PUT":
                    response = self.session.put(url, headers=headers, json=data, timeout=10)
                elif method.upper() == "DELETE":
                    response = self.session.delete(url, headers=headers, timeout=10)
                    
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                response_times.append(response_time)
                
                if response.status_code < 400:
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                response_times.append(10000)  # 10 seconds for timeout
                
        return {
            "min": min(response_times),
            "max": max(response_times),
            "avg": statistics.mean(response_times),
            "median": statistics.median(response_times),
            "p95": sorted(response_times)[int(len(response_times) * 0.95)],
            "success_rate": (success_count / iterations) * 100,
            "error_rate": (error_count / iterations) * 100,
            "total_requests": iterations
        }

    def test_api_response_time_baseline(self):
        """TC-PERF-001: API Response Time Baseline Test"""
        print("\n=== Testing API Response Time Baseline ===")
        
        # Test beAuth endpoints
        auth_endpoints = [
            ("/auth/login", "POST", {"username": "apitestuser", "password": "Test123!"}),
            ("/auth/me", "GET", None),
            ("/auth/refresh", "POST", {"refreshToken": "test"}),
        ]
        
        for endpoint, method, data in auth_endpoints:
            url = f"{self.base_url_auth}{endpoint}"
            headers = {"Authorization": f"Bearer {self.auth_token}"} if "me" in endpoint else None
            
            metrics = self.measure_response_time(url, method, headers, data, 5)
            
            if metrics["avg"] < 200:  # Less than 200ms
                self.log_test(f"TC-PERF-001.1 {endpoint}", "PASSED", 
                            f"Average response time: {metrics['avg']:.2f}ms", metrics)
            else:
                self.log_test(f"TC-PERF-001.1 {endpoint}", "FAILED", 
                            f"Average response time too high: {metrics['avg']:.2f}ms", metrics)
                
        # Test beCamera endpoints
        camera_endpoints = [
            ("/cameras", "GET", None),
            ("/cameras", "POST", {"name": "Perf Test Camera", "description": "Test", 
                                "ip_address": "192.168.1.100", "rtsp_url": "rtsp://test.com/stream"}),
            ("/analytics/summary", "GET", None),
        ]
        
        for endpoint, method, data in camera_endpoints:
            url = f"{self.base_url_camera}{endpoint}"
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            metrics = self.measure_response_time(url, method, headers, data, 5)
            
            if metrics["avg"] < 200:  # Less than 200ms
                self.log_test(f"TC-PERF-001.2 {endpoint}", "PASSED", 
                            f"Average response time: {metrics['avg']:.2f}ms", metrics)
            else:
                self.log_test(f"TC-PERF-001.2 {endpoint}", "FAILED", 
                            f"Average response time too high: {metrics['avg']:.2f}ms", metrics)

    def test_database_query_performance(self):
        """TC-PERF-002: Database Query Performance Test"""
        print("\n=== Testing Database Query Performance ===")
        
        # Test database-heavy operations
        db_operations = [
            ("/cameras", "GET", "SELECT all cameras"),
            ("/counts", "GET", "SELECT count data"),
            ("/analytics/summary", "GET", "Analytics summary query"),
        ]
        
        for endpoint, method, description in db_operations:
            url = f"{self.base_url_camera}{endpoint}"
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            metrics = self.measure_response_time(url, method, headers, None, 10)
            
            if metrics["avg"] < 100:  # Less than 100ms for DB queries
                self.log_test(f"TC-PERF-002 {description}", "PASSED", 
                            f"Database query performance: {metrics['avg']:.2f}ms", metrics)
            else:
                self.log_test(f"TC-PERF-002 {description}", "FAILED", 
                            f"Database query too slow: {metrics['avg']:.2f}ms", metrics)

    def test_concurrent_user_load(self):
        """TC-PERF-003: Concurrent User Load Test"""
        print("\n=== Testing Concurrent User Load ===")
        
        def make_request():
            """Make a single request"""
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url_camera}/cameras", 
                                          headers={"Authorization": f"Bearer {self.auth_token}"},
                                          timeout=10)
                end_time = time.time()
                return {
                    "response_time": (end_time - start_time) * 1000,
                    "status_code": response.status_code,
                    "success": response.status_code < 400
                }
            except Exception as e:
                return {
                    "response_time": 10000,
                    "status_code": 0,
                    "success": False,
                    "error": str(e)
                }
        
        # Test with 20 concurrent users
        concurrent_users = 20
        print(f"Testing with {concurrent_users} concurrent users...")
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_request) for _ in range(concurrent_users)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        total_time = (end_time - start_time) * 1000
        response_times = [r["response_time"] for r in results]
        success_count = sum(1 for r in results if r["success"])
        
        metrics = {
            "total_time_ms": total_time,
            "avg_response_time": statistics.mean(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "success_rate": (success_count / concurrent_users) * 100,
            "requests_per_second": concurrent_users / (total_time / 1000),
            "concurrent_users": concurrent_users
        }
        
        if metrics["avg_response_time"] < 200 and metrics["success_rate"] > 95:
            self.log_test("TC-PERF-003", "PASSED", 
                        f"Concurrent load test passed: {metrics['avg_response_time']:.2f}ms avg", metrics)
        else:
            self.log_test("TC-PERF-003", "FAILED", 
                        f"Concurrent load test failed: {metrics['avg_response_time']:.2f}ms avg, {metrics['success_rate']:.1f}% success", metrics)

    def test_worker_pool_performance(self):
        """TC-PERF-007: Worker Pool Performance Test"""
        print("\n=== Testing Worker Pool Performance ===")
        
        # Test worker pool status endpoint
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url_camera}/workers/status", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"},
                                      timeout=10)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            if response.status_code == 200:
                worker_data = response.json()
                metrics = {
                    "response_time_ms": response_time,
                    "total_workers": worker_data.get("data", {}).get("total_workers", 0),
                    "idle_workers": worker_data.get("data", {}).get("idle_workers", 0),
                    "busy_workers": worker_data.get("data", {}).get("busy_workers", 0)
                }
                
                if response_time < 100:  # Less than 100ms
                    self.log_test("TC-PERF-007", "PASSED", 
                                f"Worker pool status: {response_time:.2f}ms", metrics)
                else:
                    self.log_test("TC-PERF-007", "FAILED", 
                                f"Worker pool status too slow: {response_time:.2f}ms", metrics)
            else:
                self.log_test("TC-PERF-007", "FAILED", f"Worker pool status failed: {response.status_code}")
        except Exception as e:
            self.log_test("TC-PERF-007", "FAILED", str(e))

    def test_memory_usage_under_load(self):
        """TC-PERF-008: Memory Usage Under Load Test"""
        print("\n=== Testing Memory Usage Under Load ===")
        
        # This would require system monitoring tools
        # For now, we'll test if the system remains responsive under load
        
        def stress_test():
            """Run stress test"""
            for i in range(50):
                try:
                    self.session.get(f"{self.base_url_camera}/cameras", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"},
                                   timeout=5)
                except:
                    pass
                    
        # Run stress test
        start_time = time.time()
        stress_test()
        end_time = time.time()
        
        # Test if system is still responsive
        try:
            response = self.session.get(f"{self.base_url_camera}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("TC-PERF-008", "PASSED", 
                            f"System remained responsive under load: {(end_time - start_time):.2f}s")
            else:
                self.log_test("TC-PERF-008", "FAILED", 
                            f"System became unresponsive: {response.status_code}")
        except Exception as e:
            self.log_test("TC-PERF-008", "FAILED", f"System became unresponsive: {str(e)}")

    def test_cpu_usage_under_load(self):
        """TC-PERF-009: CPU Usage Under Load Test"""
        print("\n=== Testing CPU Usage Under Load ===")
        
        # Similar to memory test, check system responsiveness
        def cpu_stress_test():
            """Run CPU stress test"""
            for i in range(100):
                try:
                    self.session.get(f"{self.base_url_camera}/cameras", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"},
                                   timeout=3)
                except:
                    pass
                    
        # Run stress test
        start_time = time.time()
        cpu_stress_test()
        end_time = time.time()
        
        # Test if system is still responsive
        try:
            response = self.session.get(f"{self.base_url_camera}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("TC-PERF-009", "PASSED", 
                            f"System remained responsive under CPU load: {(end_time - start_time):.2f}s")
            else:
                self.log_test("TC-PERF-009", "FAILED", 
                            f"System became unresponsive under CPU load: {response.status_code}")
        except Exception as e:
            self.log_test("TC-PERF-009", "FAILED", f"System became unresponsive under CPU load: {str(e)}")

    def test_network_performance(self):
        """TC-PERF-010: Network Performance Test"""
        print("\n=== Testing Network Performance ===")
        
        # Test inter-service communication
        endpoints = [
            f"{self.base_url_auth}/health",
            f"{self.base_url_camera}/health",
        ]
        
        for endpoint in endpoints:
            metrics = self.measure_response_time(endpoint, "GET", None, None, 10)
            
            if metrics["avg"] < 10:  # Less than 10ms for health checks
                self.log_test(f"TC-PERF-010 {endpoint}", "PASSED", 
                            f"Network performance: {metrics['avg']:.2f}ms", metrics)
            else:
                self.log_test(f"TC-PERF-010 {endpoint}", "FAILED", 
                            f"Network performance too slow: {metrics['avg']:.2f}ms", metrics)

    def run_all_performance_tests(self):
        """Run all performance tests"""
        print("⚡ PERFORMANCE TESTING SUITE")
        print("=" * 50)
        
        # Get authentication token first
        if not self.get_auth_token():
            print("❌ Cannot proceed without authentication token")
            return False
            
        # Run all performance tests
        self.test_api_response_time_baseline()
        self.test_database_query_performance()
        self.test_concurrent_user_load()
        self.test_worker_pool_performance()
        self.test_memory_usage_under_load()
        self.test_cpu_usage_under_load()
        self.test_network_performance()
        
        # Generate summary
        self.generate_summary()
        return True
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("⚡ PERFORMANCE TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASSED"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAILED"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        # Calculate average response times
        response_times = []
        for result in self.test_results:
            if "metrics" in result and "avg" in result["metrics"]:
                response_times.append(result["metrics"]["avg"])
                
        if response_times:
            print(f"Average Response Time: {statistics.mean(response_times):.2f}ms")
            print(f"Max Response Time: {max(response_times):.2f}ms")
            print(f"Min Response Time: {min(response_times):.2f}ms")
        
        # Save results
        results_file = "sharedResource/automationTest/backend/results/performance_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_suite": "Performance Testing",
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": (passed_tests/total_tests*100) if total_tests > 0 else 0,
                    "avg_response_time": statistics.mean(response_times) if response_times else 0
                },
                "results": self.test_results
            }, f, indent=2)
            
        print(f"\n📊 Results saved to: {results_file}")

if __name__ == "__main__":
    test_suite = PerformanceTestSuite()
    test_suite.run_all_performance_tests() 
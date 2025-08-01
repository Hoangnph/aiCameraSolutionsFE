#!/usr/bin/env python3
"""
Load Testing Script for Face Detection System
Tests system performance under high concurrent load
"""

import requests
import time
import statistics
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import concurrent.futures
import threading
import random
import string

class LoadTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.test_images_dir = "automation_test/test_images"
        self.load_scenarios = {
            "light": {"users": 10, "requests_per_user": 20, "duration": 60},
            "medium": {"users": 25, "requests_per_user": 30, "duration": 120},
            "heavy": {"users": 50, "requests_per_user": 40, "duration": 180},
            "extreme": {"users": 100, "requests_per_user": 50, "duration": 300}
        }
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        return success
    
    def generate_random_data(self) -> Dict[str, str]:
        """Generate random test data"""
        return {
            "name": f"Load Test User {random.randint(1000, 9999)}",
            "email": f"loadtest{random.randint(1000, 9999)}@example.com",
            "phone": f"123456{random.randint(1000, 9999)}"
        }
    
    def make_request(self, endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None) -> Dict[str, Any]:
        """Make a single request and measure performance"""
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
            elif method.upper() == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", data=data, files=files, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            return {
                "success": response.status_code == 200,
                "response_time_ms": response_time,
                "status_code": response.status_code,
                "response_size_bytes": len(response.content) if response.content else 0,
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "method": method
            }
            
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            return {
                "success": False,
                "response_time_ms": response_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "method": method
            }
    
    def worker_function(self, user_id: int, requests_count: int, endpoints: List[str]) -> List[Dict[str, Any]]:
        """Worker function for concurrent load testing"""
        results = []
        
        for i in range(requests_count):
            # Randomly select endpoint
            endpoint = random.choice(endpoints)
            
            if endpoint == "/api/v1/faces/upload":
                # Test face upload with random data
                test_data = self.generate_random_data()
                test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
                
                if os.path.exists(test_image_path):
                    with open(test_image_path, 'rb') as f:
                        files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                        result = self.make_request(endpoint, "POST", data=test_data, files=files)
                else:
                    result = self.make_request(endpoint, "POST", data=test_data)
            elif endpoint == "/api/v1/faces/recognize":
                # Test face recognition
                test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
                
                if os.path.exists(test_image_path):
                    with open(test_image_path, 'rb') as f:
                        files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                        data = {'threshold': '0.6'}
                        result = self.make_request(endpoint, "POST", data=data, files=files)
                else:
                    result = self.make_request(endpoint, "POST", data={'threshold': '0.6'})
            else:
                # Simple GET request
                result = self.make_request(endpoint, "GET")
            
            result["user_id"] = user_id
            result["request_id"] = i
            results.append(result)
            
            # Small delay between requests
            time.sleep(random.uniform(0.1, 0.5))
        
        return results
    
    def run_load_test(self, scenario: str, duration: int = None) -> Dict[str, Any]:
        """Run load test with specified scenario"""
        if scenario not in self.load_scenarios:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        config = self.load_scenarios[scenario]
        users = config["users"]
        requests_per_user = config["requests_per_user"]
        test_duration = duration or config["duration"]
        
        print(f"🚀 Starting {scenario.upper()} load test...")
        print(f"   Users: {users}")
        print(f"   Requests per user: {requests_per_user}")
        print(f"   Duration: {test_duration}s")
        print(f"   Total requests: {users * requests_per_user}")
        
        # Define endpoints to test
        endpoints = [
            "/health",
            "/",
            "/api/v1/camera/status",
            "/api/v1/faces/list",
            "/api/v1/faces/upload",
            "/api/v1/faces/recognize"
        ]
        
        all_results = []
        start_time = time.time()
        
        # Run concurrent load test
        with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
            futures = [executor.submit(self.worker_function, user_id, requests_per_user, endpoints) 
                      for user_id in range(users)]
            
            for future in concurrent.futures.as_completed(futures):
                all_results.extend(future.result())
                
                # Check if we've exceeded duration
                if time.time() - start_time > test_duration:
                    break
        
        # Calculate statistics
        successful_requests = [r for r in all_results if r["success"]]
        failed_requests = [r for r in all_results if not r["success"]]
        
        if successful_requests:
            response_times = [r["response_time_ms"] for r in successful_requests]
            
            stats = {
                "scenario": scenario,
                "total_requests": len(all_results),
                "successful_requests": len(successful_requests),
                "failed_requests": len(failed_requests),
                "success_rate": (len(successful_requests) / len(all_results)) * 100,
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times),
                "avg_response_time_ms": statistics.mean(response_times),
                "median_response_time_ms": statistics.median(response_times),
                "std_deviation_ms": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "throughput_rps": len(all_results) / (test_duration),
                "duration_seconds": test_duration,
                "concurrent_users": users,
                "requests_per_user": requests_per_user,
                "all_results": all_results
            }
        else:
            stats = {
                "scenario": scenario,
                "total_requests": len(all_results),
                "successful_requests": 0,
                "failed_requests": len(all_results),
                "success_rate": 0,
                "error": "No successful requests",
                "duration_seconds": test_duration,
                "concurrent_users": users,
                "requests_per_user": requests_per_user,
                "all_results": all_results
            }
        
        return stats
    
    def test_endpoint_specific_load(self, endpoint: str, method: str = "GET", 
                                   concurrent_users: int = 10, requests_per_user: int = 20) -> Dict[str, Any]:
        """Test specific endpoint under load"""
        print(f"🎯 Testing {method} {endpoint} under load...")
        print(f"   Concurrent users: {concurrent_users}")
        print(f"   Requests per user: {requests_per_user}")
        
        all_results = []
        
        def endpoint_worker(user_id: int):
            user_results = []
            for i in range(requests_per_user):
                if endpoint == "/api/v1/faces/upload":
                    test_data = self.generate_random_data()
                    test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
                    
                    if os.path.exists(test_image_path):
                        with open(test_image_path, 'rb') as f:
                            files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                            result = self.make_request(endpoint, method, data=test_data, files=files)
                    else:
                        result = self.make_request(endpoint, method, data=test_data)
                elif endpoint == "/api/v1/faces/recognize":
                    test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
                    
                    if os.path.exists(test_image_path):
                        with open(test_image_path, 'rb') as f:
                            files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                            data = {'threshold': '0.6'}
                            result = self.make_request(endpoint, method, data=data, files=files)
                    else:
                        result = self.make_request(endpoint, method, data={'threshold': '0.6'})
                else:
                    result = self.make_request(endpoint, method)
                
                result["user_id"] = user_id
                result["request_id"] = i
                user_results.append(result)
                time.sleep(random.uniform(0.1, 0.3))
            
            return user_results
        
        # Run concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(endpoint_worker, user_id) for user_id in range(concurrent_users)]
            for future in concurrent.futures.as_completed(futures):
                all_results.extend(future.result())
        
        # Calculate statistics
        successful_requests = [r for r in all_results if r["success"]]
        failed_requests = [r for r in all_results if not r["success"]]
        
        if successful_requests:
            response_times = [r["response_time_ms"] for r in successful_requests]
            
            stats = {
                "endpoint": endpoint,
                "method": method,
                "total_requests": len(all_results),
                "successful_requests": len(successful_requests),
                "failed_requests": len(failed_requests),
                "success_rate": (len(successful_requests) / len(all_results)) * 100,
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times),
                "avg_response_time_ms": statistics.mean(response_times),
                "median_response_time_ms": statistics.median(response_times),
                "std_deviation_ms": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "concurrent_users": concurrent_users,
                "requests_per_user": requests_per_user,
                "all_results": all_results
            }
        else:
            stats = {
                "endpoint": endpoint,
                "method": method,
                "total_requests": len(all_results),
                "successful_requests": 0,
                "failed_requests": len(all_results),
                "success_rate": 0,
                "error": "No successful requests",
                "concurrent_users": concurrent_users,
                "requests_per_user": requests_per_user,
                "all_results": all_results
            }
        
        return stats
    
    def run_comprehensive_load_test(self) -> Dict[str, Any]:
        """Run comprehensive load test suite"""
        print("🚀 Starting Comprehensive Load Test Suite")
        print("=" * 60)
        
        test_results = {}
        
        # Test 1: Light load
        print("\n1️⃣ Testing Light Load...")
        test_results["light_load"] = self.run_load_test("light")
        
        # Test 2: Medium load
        print("\n2️⃣ Testing Medium Load...")
        test_results["medium_load"] = self.run_load_test("medium")
        
        # Test 3: Heavy load
        print("\n3️⃣ Testing Heavy Load...")
        test_results["heavy_load"] = self.run_load_test("heavy")
        
        # Test 4: Endpoint-specific tests
        print("\n4️⃣ Testing Endpoint-Specific Load...")
        test_results["health_endpoint"] = self.test_endpoint_specific_load("/health", "GET", 20, 30)
        test_results["face_list_endpoint"] = self.test_endpoint_specific_load("/api/v1/faces/list", "GET", 15, 25)
        
        # Generate summary
        summary = self.generate_load_summary(test_results)
        test_results["summary"] = summary
        
        # Display results
        self.display_load_results(summary)
        
        return test_results
    
    def generate_load_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate load test summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_scenarios": len(test_results),
            "scenarios_tested": [],
            "performance_metrics": {},
            "recommendations": []
        }
        
        for scenario_name, result in test_results.items():
            if isinstance(result, dict) and "success_rate" in result:
                summary["scenarios_tested"].append(scenario_name)
                summary["performance_metrics"][scenario_name] = {
                    "success_rate": result["success_rate"],
                    "avg_response_time_ms": result.get("avg_response_time_ms", 0),
                    "throughput_rps": result.get("throughput_rps", 0)
                }
        
        # Generate recommendations
        for scenario_name, metrics in summary["performance_metrics"].items():
            success_rate = metrics["success_rate"]
            avg_response_time = metrics["avg_response_time_ms"]
            throughput = metrics["throughput_rps"]
            
            if success_rate < 95:
                summary["recommendations"].append(f"Improve reliability for {scenario_name}: {success_rate:.1f}% success rate")
            
            if avg_response_time > 1000:
                summary["recommendations"].append(f"Optimize performance for {scenario_name}: {avg_response_time:.1f}ms response time")
            
            if throughput < 10:
                summary["recommendations"].append(f"Increase throughput for {scenario_name}: {throughput:.1f} RPS")
        
        if not summary["recommendations"]:
            summary["recommendations"].append("All load tests passed! System is ready for production.")
        
        return summary
    
    def display_load_results(self, summary: Dict[str, Any]):
        """Display load test results"""
        print("\n" + "=" * 60)
        print("📊 LOAD TEST RESULTS")
        print("=" * 60)
        
        print(f"Total Scenarios: {summary['total_scenarios']}")
        print(f"Scenarios Tested: {', '.join(summary['scenarios_tested'])}")
        print(f"Timestamp: {summary['timestamp']}")
        
        print("\n📈 Performance Metrics:")
        for scenario_name, metrics in summary["performance_metrics"].items():
            success_rate = metrics["success_rate"]
            avg_response_time = metrics["avg_response_time_ms"]
            throughput = metrics["throughput_rps"]
            
            status = "🟢" if success_rate >= 95 and avg_response_time < 1000 else "🟡" if success_rate >= 80 else "🔴"
            print(f"   {status} {scenario_name}:")
            print(f"      Success Rate: {success_rate:.1f}%")
            print(f"      Avg Response Time: {avg_response_time:.1f}ms")
            print(f"      Throughput: {throughput:.1f} RPS")
        
        print("\n💡 Recommendations:")
        for rec in summary["recommendations"]:
            print(f"   • {rec}")
    
    def save_load_report(self, test_results: Dict[str, Any], filename: str = None):
        """Save load test report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"load_report_{timestamp}.json"
        
        report_path = os.path.join("automation_test", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n📊 Load test report saved to: {report_path}")
        return report_path

def main():
    """Main function"""
    print("🎯 Face Detection System - Load Testing")
    print("=" * 60)
    
    # Create test instance
    tester = LoadTest()
    
    # Run comprehensive load test
    results = tester.run_comprehensive_load_test()
    
    # Save report
    tester.save_load_report(results)
    
    print("\n✅ Load testing completed!")

if __name__ == "__main__":
    main() 
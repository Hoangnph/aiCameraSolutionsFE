#!/usr/bin/env python3
"""
Performance Testing Script for Face Detection System
Tests response times, throughput, and system performance under load
"""

import requests
import time
import statistics
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import concurrent.futures
import threading

class PerformanceTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {}
        self.test_images_dir = "automation_test/test_images"
        
    def measure_response_time(self, endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None) -> Dict[str, Any]:
        """Measure response time for a single request"""
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
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            return {
                "success": False,
                "response_time_ms": response_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def test_endpoint_performance(self, endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None, iterations: int = 10) -> Dict[str, Any]:
        """Test performance of a specific endpoint"""
        print(f"🔍 Testing {method} {endpoint} ({iterations} iterations)...")
        
        response_times = []
        success_count = 0
        total_size = 0
        
        for i in range(iterations):
            result = self.measure_response_time(endpoint, method, data, files)
            response_times.append(result["response_time_ms"])
            
            if result["success"]:
                success_count += 1
                total_size += result.get("response_size_bytes", 0)
            
            # Small delay between requests
            time.sleep(0.1)
        
        # Calculate statistics
        if response_times:
            stats = {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "success_count": success_count,
                "success_rate": (success_count / iterations) * 100,
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times),
                "avg_response_time_ms": statistics.mean(response_times),
                "median_response_time_ms": statistics.median(response_times),
                "std_deviation_ms": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "total_size_bytes": total_size,
                "avg_size_bytes": total_size / success_count if success_count > 0 else 0,
                "response_times": response_times
            }
        else:
            stats = {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "success_count": 0,
                "success_rate": 0,
                "error": "No successful responses"
            }
        
        # Print summary
        if stats.get("success_rate", 0) > 0:
            print(f"✅ {endpoint}: {success_count}/{iterations} successful")
            print(f"   Avg: {stats['avg_response_time_ms']:.1f}ms, Min: {stats['min_response_time_ms']:.1f}ms, Max: {stats['max_response_time_ms']:.1f}ms")
        else:
            print(f"❌ {endpoint}: 0/{iterations} successful")
        
        return stats
    
    def test_concurrent_requests(self, endpoint: str, method: str = "GET", concurrent_users: int = 5, requests_per_user: int = 10) -> Dict[str, Any]:
        """Test performance under concurrent load"""
        print(f"🚀 Testing concurrent load: {concurrent_users} users, {requests_per_user} requests each...")
        
        all_results = []
        
        def worker(user_id: int):
            user_results = []
            for i in range(requests_per_user):
                result = self.measure_response_time(endpoint, method)
                result["user_id"] = user_id
                result["request_id"] = i
                user_results.append(result)
                time.sleep(0.1)  # Small delay
            return user_results
        
        # Run concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker, user_id) for user_id in range(concurrent_users)]
            for future in concurrent.futures.as_completed(futures):
                all_results.extend(future.result())
        
        # Calculate concurrent statistics
        response_times = [r["response_time_ms"] for r in all_results if r["success"]]
        success_count = sum(1 for r in all_results if r["success"])
        total_requests = len(all_results)
        
        if response_times:
            concurrent_stats = {
                "endpoint": endpoint,
                "method": method,
                "concurrent_users": concurrent_users,
                "requests_per_user": requests_per_user,
                "total_requests": total_requests,
                "success_count": success_count,
                "success_rate": (success_count / total_requests) * 100,
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times),
                "avg_response_time_ms": statistics.mean(response_times),
                "median_response_time_ms": statistics.median(response_times),
                "std_deviation_ms": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "throughput_rps": total_requests / (max(response_times) / 1000) if response_times else 0,
                "all_results": all_results
            }
        else:
            concurrent_stats = {
                "endpoint": endpoint,
                "method": method,
                "concurrent_users": concurrent_users,
                "requests_per_user": requests_per_user,
                "total_requests": total_requests,
                "success_count": 0,
                "success_rate": 0,
                "error": "No successful responses"
            }
        
        # Print summary
        if concurrent_stats.get("success_rate", 0) > 0:
            print(f"✅ Concurrent test: {success_count}/{total_requests} successful")
            print(f"   Avg: {concurrent_stats['avg_response_time_ms']:.1f}ms, Throughput: {concurrent_stats['throughput_rps']:.1f} RPS")
        else:
            print(f"❌ Concurrent test: 0/{total_requests} successful")
        
        return concurrent_stats
    
    def test_face_recognition_performance(self) -> Dict[str, Any]:
        """Test face recognition performance with test image"""
        test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
        
        if not os.path.exists(test_image_path):
            return {"error": f"Test image not found: {test_image_path}"}
        
        print("🎯 Testing Face Recognition Performance...")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_face.jpg', f, 'image/jpeg')}
            data = {'threshold': '0.6'}
            
            return self.test_endpoint_performance(
                "/api/v1/faces/recognize",
                "POST",
                data=data,
                files=files,
                iterations=5
            )
    
    def test_face_registration_performance(self) -> Dict[str, Any]:
        """Test face registration performance"""
        test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
        
        if not os.path.exists(test_image_path):
            return {"error": f"Test image not found: {test_image_path}"}
        
        print("📝 Testing Face Registration Performance...")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_face.jpg', f, 'image/jpeg')}
            data = {
                'name': f'Performance Test User {int(time.time())}',
                'email': f'perf{int(time.time())}@example.com',
                'phone': '1234567890',
                'notes': 'Performance test user'
            }
            
            return self.test_endpoint_performance(
                "/api/v1/faces/upload",
                "POST",
                data=data,
                files=files,
                iterations=3
            )
    
    def run_comprehensive_performance_test(self) -> Dict[str, Any]:
        """Run comprehensive performance test suite"""
        print("🚀 Starting Comprehensive Performance Test Suite")
        print("=" * 60)
        
        test_results = {}
        
        # Test 1: Basic API endpoints
        print("\n1️⃣ Testing Basic API Endpoints...")
        test_results["health_check"] = self.test_endpoint_performance("/health", iterations=20)
        test_results["root_endpoint"] = self.test_endpoint_performance("/", iterations=20)
        test_results["camera_status"] = self.test_endpoint_performance("/api/v1/camera/status", iterations=20)
        test_results["face_list"] = self.test_endpoint_performance("/api/v1/faces/list", iterations=20)
        
        # Test 2: Face recognition performance
        print("\n2️⃣ Testing Face Recognition Performance...")
        test_results["face_recognition"] = self.test_face_recognition_performance()
        
        # Test 3: Face registration performance
        print("\n3️⃣ Testing Face Registration Performance...")
        test_results["face_registration"] = self.test_face_registration_performance()
        
        # Test 4: Concurrent load testing
        print("\n4️⃣ Testing Concurrent Load...")
        test_results["concurrent_health"] = self.test_concurrent_requests("/health", concurrent_users=3, requests_per_user=5)
        test_results["concurrent_face_list"] = self.test_concurrent_requests("/api/v1/faces/list", concurrent_users=3, requests_per_user=5)
        
        # Generate summary
        summary = self.generate_performance_summary(test_results)
        test_results["summary"] = summary
        
        # Display results
        self.display_performance_results(summary)
        
        return test_results
    
    def generate_performance_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(test_results),
            "successful_tests": 0,
            "average_response_times": {},
            "recommendations": []
        }
        
        for test_name, result in test_results.items():
            if isinstance(result, dict) and "avg_response_time_ms" in result:
                summary["successful_tests"] += 1
                summary["average_response_times"][test_name] = result["avg_response_time_ms"]
        
        # Generate recommendations
        for test_name, avg_time in summary["average_response_times"].items():
            if avg_time > 1000:  # More than 1 second
                summary["recommendations"].append(f"Optimize {test_name}: {avg_time:.1f}ms is too slow")
            elif avg_time > 500:  # More than 500ms
                summary["recommendations"].append(f"Consider optimizing {test_name}: {avg_time:.1f}ms")
        
        if not summary["recommendations"]:
            summary["recommendations"].append("All endpoints performing well!")
        
        return summary
    
    def display_performance_results(self, summary: Dict[str, Any]):
        """Display performance test results"""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE TEST RESULTS")
        print("=" * 60)
        
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful Tests: {summary['successful_tests']}")
        print(f"Timestamp: {summary['timestamp']}")
        
        print("\n📈 Average Response Times:")
        for test_name, avg_time in summary["average_response_times"].items():
            status = "🟢" if avg_time < 500 else "🟡" if avg_time < 1000 else "🔴"
            print(f"   {status} {test_name}: {avg_time:.1f}ms")
        
        print("\n💡 Recommendations:")
        for rec in summary["recommendations"]:
            print(f"   • {rec}")
    
    def save_performance_report(self, test_results: Dict[str, Any], filename: str = None):
        """Save performance test report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        report_path = os.path.join("automation_test", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n📊 Performance report saved to: {report_path}")
        return report_path

def main():
    """Main function"""
    print("🎯 Face Detection System - Performance Testing")
    print("=" * 60)
    
    # Create test instance
    tester = PerformanceTest()
    
    # Run comprehensive performance test
    results = tester.run_comprehensive_performance_test()
    
    # Save report
    tester.save_performance_report(results)
    
    print("\n✅ Performance testing completed!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🚀 Auto Test Runner
Tự động chạy tất cả tests và báo cáo kết quả
"""

import subprocess
import time
import json
import os
from datetime import datetime

class AutoTestRunner:
    def __init__(self):
        self.test_results = []
        self.server_running = False
        
    def run_test(self, test_name, command, timeout=60):
        """Run a test and capture results"""
        print(f"\n🔍 Running Test: {test_name}")
        print("=" * 50)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            output = result.stdout
            error = result.stderr
            
            test_result = {
                "test_name": test_name,
                "success": success,
                "returncode": result.returncode,
                "output": output,
                "error": error,
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(test_result)
            
            if success:
                print(f"✅ {test_name}: PASS")
            else:
                print(f"❌ {test_name}: FAIL")
                if error:
                    print(f"Error: {error}")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name}: TIMEOUT")
            test_result = {
                "test_name": test_name,
                "success": False,
                "returncode": -1,
                "output": "",
                "error": "Timeout",
                "timestamp": datetime.now().isoformat()
            }
            self.test_results.append(test_result)
            return False
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            test_result = {
                "test_name": test_name,
                "success": False,
                "returncode": -1,
                "output": "",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.test_results.append(test_result)
            return False
    
    def start_server(self):
        """Start the auto server"""
        print("🚀 Starting Auto Server...")
        return self.run_test("Auto Server", "python auto_server.py", timeout=30)
    
    def test_server_health(self):
        """Test server health"""
        print("🔍 Testing Server Health...")
        return self.run_test("Server Health", "curl -s http://localhost:8000/health", timeout=10)
    
    def test_real_face(self):
        """Test with real face images"""
        print("🔍 Testing Real Face Images...")
        return self.run_test("Real Face Test", "python test_real_face.py", timeout=120)
    
    def test_content_type(self):
        """Test content type handling"""
        print("🔍 Testing Content Type...")
        return self.run_test("Content Type Test", "python test_with_content_type.py", timeout=60)
    
    def test_debug_logging(self):
        """Test debug logging"""
        print("🔍 Testing Debug Logging...")
        return self.run_test("Debug Logging Test", "python debug_logging.py", timeout=60)
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Auto Test Runner")
        print("=" * 60)
        
        # Step 1: Start server
        server_success = self.start_server()
        
        if server_success:
            # Step 2: Test server health
            health_success = self.test_server_health()
            
            if health_success:
                # Step 3: Run all tests
                real_face_success = self.test_real_face()
                content_type_success = self.test_content_type()
                debug_logging_success = self.test_debug_logging()
                
                # Summary
                self.print_summary()
                self.save_results()
                
                return all([
                    server_success,
                    health_success,
                    real_face_success,
                    content_type_success,
                    debug_logging_success
                ])
            else:
                print("❌ Server health check failed")
                return False
        else:
            print("❌ Failed to start server")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        
        passed = sum(1 for r in self.test_results if r["success"])
        failed = len(self.test_results) - passed
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Total: {len(self.test_results)}")
        
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"  {status}: {result['test_name']}")
    
    def save_results(self):
        """Save test results to file"""
        results_file = f"auto_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")

def main():
    """Run auto test runner"""
    runner = AutoTestRunner()
    success = runner.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Face Embedding System is working correctly")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("🔧 Please check the logs and fix issues")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
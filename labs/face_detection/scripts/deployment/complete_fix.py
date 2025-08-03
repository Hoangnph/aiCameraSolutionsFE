#!/usr/bin/env python3
"""
🔧 Complete Fix Script - Face Detection System
Fix tất cả lỗi và hiển thị log khởi động chi tiết
"""

import subprocess
import time
import os
import sys
import signal
import requests
from datetime import datetime

class CompleteFix:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.log_file = f"startup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    def log_message(self, message):
        """Log message với timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        # Save to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def kill_all_processes(self):
        """Kill tất cả processes liên quan"""
        self.log_message("🔧 Killing all existing processes...")
        
        try:
            # Kill uvicorn processes
            subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True)
            # Kill http.server processes
            subprocess.run(['pkill', '-f', 'http.server'], capture_output=True)
            # Kill any processes on ports 8000 and 3000
            subprocess.run(['lsof', '-ti:8000', '|', 'xargs', 'kill', '-9'], shell=True, capture_output=True)
            subprocess.run(['lsof', '-ti:3000', '|', 'xargs', 'kill', '-9'], shell=True, capture_output=True)
            
            time.sleep(3)
            self.log_message("✅ All processes killed successfully")
        except Exception as e:
            self.log_message(f"⚠️ Warning: {e}")
    
    def check_directory(self):
        """Kiểm tra và chuyển đến đúng directory"""
        current_dir = os.getcwd()
        self.log_message(f"📁 Current directory: {current_dir}")
        
        # Check if we're in the right directory
        if not os.path.exists('src/api/main.py'):
            self.log_message("❌ Not in correct directory, changing to labs/face_detection")
            os.chdir('/Users/macintoshhd/Project/Project/AI_OCR/feMain/labs/face_detection')
            new_dir = os.getcwd()
            self.log_message(f"📁 New directory: {new_dir}")
            
            if not os.path.exists('src/api/main.py'):
                self.log_message("❌ ERROR: Cannot find src/api/main.py")
                return False
            else:
                self.log_message("✅ Found src/api/main.py")
                return True
        else:
            self.log_message("✅ Already in correct directory")
            return True
    
    def start_api_server(self):
        """Khởi động API server với log chi tiết"""
        self.log_message("🚀 Starting API Server...")
        
        try:
            # Start API server
            self.api_process = subprocess.Popen([
                'python', '-m', 'uvicorn', 'src.api.main:app',
                '--host', '0.0.0.0', '--port', '8000', '--reload'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.log_message("⏳ Waiting for API server to start...")
            time.sleep(10)
            
            # Check if process is running
            if self.api_process.poll() is None:
                self.log_message("✅ API server process started")
                
                # Test health check
                if self.test_api_health():
                    self.log_message("✅ API server is healthy and responding")
                    return True
                else:
                    self.log_message("❌ API server not responding to health check")
                    return False
            else:
                stdout, stderr = self.api_process.communicate()
                self.log_message(f"❌ API server failed to start:")
                self.log_message(f"STDOUT: {stdout}")
                self.log_message(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Error starting API server: {e}")
            return False
    
    def test_api_health(self):
        """Test API health check"""
        try:
            response = requests.get('http://localhost:8000/health', timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_message(f"✅ Health check response: {data}")
                return True
            else:
                self.log_message(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_message(f"❌ Health check error: {e}")
            return False
    
    def start_frontend_server(self):
        """Khởi động frontend server"""
        self.log_message("🚀 Starting Frontend Server...")
        
        try:
            # Change to frontend directory
            frontend_dir = os.path.join(os.getcwd(), 'fe')
            if not os.path.exists(frontend_dir):
                self.log_message(f"❌ Frontend directory not found: {frontend_dir}")
                return False
            
            os.chdir(frontend_dir)
            self.log_message(f"📁 Frontend directory: {os.getcwd()}")
            
            # Start frontend server
            self.frontend_process = subprocess.Popen([
                'python', '-m', 'http.server', '3000'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            
            if self.frontend_process.poll() is None:
                self.log_message("✅ Frontend server started")
                
                # Test frontend
                if self.test_frontend():
                    self.log_message("✅ Frontend server is accessible")
                    return True
                else:
                    self.log_message("❌ Frontend server not accessible")
                    return False
            else:
                stdout, stderr = self.frontend_process.communicate()
                self.log_message(f"❌ Frontend server failed to start:")
                self.log_message(f"STDOUT: {stdout}")
                self.log_message(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Error starting frontend server: {e}")
            return False
    
    def test_frontend(self):
        """Test frontend accessibility"""
        try:
            response = requests.get('http://localhost:3000', timeout=10)
            if response.status_code == 200:
                self.log_message("✅ Frontend is accessible")
                return True
            else:
                self.log_message(f"❌ Frontend not accessible: {response.status_code}")
                return False
        except Exception as e:
            self.log_message(f"❌ Frontend test error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Chạy comprehensive test"""
        self.log_message("🔍 Running comprehensive system test...")
        
        tests = [
            ("API Health", self.test_api_health),
            ("Frontend Access", self.test_frontend),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            self.log_message(f"🔍 Testing: {test_name}")
            if test_func():
                self.log_message(f"✅ {test_name}: PASS")
                passed += 1
            else:
                self.log_message(f"❌ {test_name}: FAIL")
            time.sleep(2)
        
        self.log_message(f"📊 Test Results: {passed}/{total} passed")
        return passed == total
    
    def monitor_servers(self):
        """Monitor servers và hiển thị status"""
        self.log_message("🔄 Starting server monitoring...")
        
        try:
            while True:
                api_status = "✅ RUNNING" if self.test_api_health() else "❌ DOWN"
                frontend_status = "✅ RUNNING" if self.test_frontend() else "❌ DOWN"
                
                self.log_message(f"📊 Status - API: {api_status}, Frontend: {frontend_status}")
                
                # Check if processes are still running
                if self.api_process and self.api_process.poll() is not None:
                    self.log_message("⚠️ API server stopped, restarting...")
                    self.start_api_server()
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    self.log_message("⚠️ Frontend server stopped, restarting...")
                    self.start_frontend_server()
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            self.log_message("🛑 Monitoring stopped by user")
            self.cleanup()
    
    def cleanup(self):
        """Cleanup processes"""
        self.log_message("🧹 Cleaning up processes...")
        
        if self.api_process:
            self.api_process.terminate()
            self.api_process.wait()
            self.log_message("✅ API server stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            self.log_message("✅ Frontend server stopped")
    
    def run(self):
        """Run complete fix process"""
        self.log_message("🚀 Starting Complete Fix Process")
        self.log_message("=" * 60)
        
        # Step 1: Kill existing processes
        self.kill_all_processes()
        
        # Step 2: Check directory
        if not self.check_directory():
            self.log_message("❌ Cannot proceed due to directory issues")
            return False
        
        # Step 3: Start API server
        if not self.start_api_server():
            self.log_message("❌ Failed to start API server")
            return False
        
        # Step 4: Start frontend server
        if not self.start_frontend_server():
            self.log_message("❌ Failed to start frontend server")
            return False
        
        # Step 5: Run comprehensive test
        if not self.run_comprehensive_test():
            self.log_message("❌ System test failed")
            return False
        
        # Step 6: Start monitoring
        self.log_message("🎉 All systems are running! Starting monitoring...")
        self.log_message(f"📝 Log file: {self.log_file}")
        self.log_message("🌐 Access URLs:")
        self.log_message("   - API: http://localhost:8000")
        self.log_message("   - Frontend: http://localhost:3000")
        self.log_message("   - Health Check: http://localhost:8000/health")
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, lambda sig, frame: self.cleanup())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.cleanup())
        
        # Start monitoring
        self.monitor_servers()

def main():
    """Main function"""
    fixer = CompleteFix()
    try:
        fixer.run()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        fixer.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        fixer.cleanup()

if __name__ == "__main__":
    main() 
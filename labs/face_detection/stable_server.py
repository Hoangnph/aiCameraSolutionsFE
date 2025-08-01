#!/usr/bin/env python3
"""
🚀 Stable API Server
Khởi động và giữ API server chạy ổn định
"""

import subprocess
import time
import requests
import sys
import signal
import os

class StableServer:
    def __init__(self):
        self.process = None
        self.running = False
        
    def start_server(self):
        """Start API server"""
        print("🚀 Starting Stable API Server...")
        print("=" * 50)
        
        try:
            # Kill any existing processes
            self.kill_existing_processes()
            
            # Start server
            self.process = subprocess.Popen([
                'python', '-m', 'uvicorn', 'src.api.main:app',
                '--host', '0.0.0.0', '--port', '8000', '--reload'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            print("⏳ Waiting for server to start...")
            time.sleep(5)
            
            # Check if process is still running
            if self.process.poll() is None:
                print("✅ API server started successfully")
                
                # Test health check
                if self.test_health():
                    print("✅ Health check passed")
                    self.running = True
                    return True
                else:
                    print("❌ Health check failed")
                    return False
            else:
                stdout, stderr = self.process.communicate()
                print(f"❌ API server failed to start:")
                print(f"STDOUT: {stdout.decode()}")
                print(f"STDERR: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting API server: {e}")
            return False
    
    def kill_existing_processes(self):
        """Kill existing uvicorn processes"""
        try:
            result = subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True, text=True)
            print("🔧 Killed existing uvicorn processes")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error killing processes: {e}")
    
    def test_health(self):
        """Test server health"""
        try:
            response = requests.get('http://localhost:8000/health', timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def monitor_server(self):
        """Monitor and maintain server"""
        print("\n🔄 Monitoring API server...")
        print("Press Ctrl+C to stop")
        
        try:
            while self.running:
                # Check if process is still running
                if self.process.poll() is not None:
                    print("❌ API server stopped unexpectedly")
                    break
                
                # Test health check every 30 seconds
                if self.test_health():
                    print("✅ Server is healthy")
                else:
                    print("⚠️ Server health check failed")
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping API server...")
            self.stop_server()
    
    def stop_server(self):
        """Stop API server"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✅ API server stopped")
        self.running = False
    
    def run(self):
        """Run stable server"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_server())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_server())
        
        if self.start_server():
            self.monitor_server()
        else:
            print("❌ Failed to start API server")
            sys.exit(1)

if __name__ == "__main__":
    server = StableServer()
    server.run() 
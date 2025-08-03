#!/usr/bin/env python3
"""
🚀 Start API Server
Khởi động và giữ API server chạy
"""

import subprocess
import time
import requests
import sys

def start_api_server():
    """Start API server and keep it running"""
    print("🚀 Starting API Server...")
    print("=" * 50)
    
    try:
        # Start API server in background
        process = subprocess.Popen([
            'python', '-m', 'uvicorn', 'src.api.main:app',
            '--host', '0.0.0.0', '--port', '8000', '--reload'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ API server started successfully")
            
            # Test health check
            try:
                response = requests.get('http://localhost:8000/health', timeout=10)
                if response.status_code == 200:
                    print("✅ Health check passed")
                    return process
                else:
                    print(f"❌ Health check failed: {response.status_code}")
                    return None
            except Exception as e:
                print(f"❌ Health check error: {e}")
                return None
        else:
            stdout, stderr = process.communicate()
            print(f"❌ API server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def keep_server_running(process):
    """Keep the server running and monitor it"""
    print("\n🔄 Keeping API server running...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Check if process is still running
            if process.poll() is not None:
                print("❌ API server stopped unexpectedly")
                break
                
            # Test health check every 30 seconds
            try:
                response = requests.get('http://localhost:8000/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Server is healthy")
                else:
                    print(f"⚠️ Server health check failed: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Health check error: {e}")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping API server...")
        process.terminate()
        process.wait()
        print("✅ API server stopped")

if __name__ == "__main__":
    process = start_api_server()
    if process:
        keep_server_running(process)
    else:
        print("❌ Failed to start API server")
        sys.exit(1) 
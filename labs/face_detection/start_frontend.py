#!/usr/bin/env python3
"""
🌐 Frontend Startup Script
Khởi động frontend server cho Face Detection System
"""

import os
import sys
import subprocess
import signal
import time
import requests
import webbrowser
from pathlib import Path

class FrontendServer:
    def __init__(self):
        self.process = None
        self.port = 3000
        self.host = "0.0.0.0"
        self.project_dir = Path(__file__).parent
        self.frontend_dir = self.project_dir / "fe"
        
    def kill_existing_processes(self):
        """Kill existing processes on port 3000"""
        print("🔪 Killing existing processes...")
        
        try:
            # Kill processes on port 3000
            subprocess.run(["lsof", "-ti", f":{self.port}"], check=True, capture_output=True)
            subprocess.run(["kill", "-9", "$(lsof -ti :3000)"], shell=True)
            print(f"✅ Killed processes on port {self.port}")
        except subprocess.CalledProcessError:
            print(f"ℹ️  No existing processes on port {self.port}")
        except Exception as e:
            print(f"⚠️  Error killing processes: {e}")
    
    def check_frontend_files(self):
        """Check if frontend files exist"""
        print("🔍 Checking frontend files...")
        
        required_files = [
            "index.html"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = self.frontend_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
                print(f"❌ {file_name}")
            else:
                print(f"✅ {file_name}")
        
        if missing_files:
            print(f"\n❌ Missing files: {', '.join(missing_files)}")
            return False
        
        print("✅ All frontend files exist")
        print("ℹ️  CSS and JS are inline in index.html")
        return True
    
    def check_backend_health(self):
        """Check if backend is running"""
        print("🔍 Checking backend health...")
        
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend is healthy")
                print(f"📊 Status: {data.get('data', {}).get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend is not running: {e}")
            print("💡 Please start the backend first: python start_backend.py")
            return False
    
    def start_server(self):
        """Start the frontend server"""
        print("🚀 Starting frontend server...")
        
        # Change to frontend directory
        os.chdir(self.frontend_dir)
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Start Python HTTP server
        cmd = [
            "python", "-m", "http.server",
            str(self.port),
            "--bind", self.host
        ]
        
        print(f"🔧 Command: {' '.join(cmd)}")
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print(f"✅ Frontend server started on http://{self.host}:{self.port}")
            print("📝 Press Ctrl+C to stop the server")
            
            # Monitor output
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    print(line.rstrip())
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            self.stop_server()
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
        
        return True
    
    def health_check(self):
        """Check if frontend server is running"""
        print("🏥 Performing frontend health check...")
        
        try:
            response = requests.get(f"http://localhost:{self.port}", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend server is running")
                return True
            else:
                print(f"❌ Frontend health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend health check failed: {e}")
            return False
    
    def open_browser(self):
        """Open browser to frontend"""
        print("🌐 Opening browser...")
        
        try:
            webbrowser.open(f"http://localhost:{self.port}")
            print("✅ Browser opened")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"💡 Please open manually: http://localhost:{self.port}")
    
    def stop_server(self):
        """Stop the server"""
        if self.process:
            print("🛑 Stopping server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                print("✅ Server stopped")
            except subprocess.TimeoutExpired:
                print("⚠️  Force killing server...")
                self.process.kill()
                self.process.wait()
                print("✅ Server force stopped")
    
    def run(self):
        """Main run method"""
        print("🌐 Frontend Startup Script")
        print("=" * 50)
        
        # Check frontend files
        if not self.check_frontend_files():
            return False
        
        # Check backend health
        if not self.check_backend_health():
            return False
        
        # Kill existing processes
        self.kill_existing_processes()
        
        # Start server
        if self.start_server():
            # Wait a bit for server to start
            time.sleep(2)
            
            # Health check
            if self.health_check():
                print("\n🎉 Frontend server is running successfully!")
                print(f"🌐 Frontend URL: http://localhost:{self.port}")
                print(f"🔗 Backend API: http://localhost:8000")
                
                # Open browser
                self.open_browser()
                
                return True
            else:
                print("\n❌ Frontend server failed health check")
                return False
        else:
            print("\n❌ Failed to start frontend server")
            return False

def main():
    """Main function"""
    server = FrontendServer()
    
    try:
        success = server.run()
        if success:
            print("\n✅ Frontend startup completed successfully!")
        else:
            print("\n❌ Frontend startup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Frontend startup interrupted")
        server.stop_server()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        server.stop_server()
        sys.exit(1)

if __name__ == "__main__":
    main() 
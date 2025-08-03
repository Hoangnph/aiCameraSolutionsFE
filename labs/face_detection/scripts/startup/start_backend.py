#!/usr/bin/env python3
"""
🚀 Backend Startup Script
Khởi động API server cho Face Detection System
"""

import os
import sys
import subprocess
import signal
import time
import requests
from pathlib import Path

class BackendServer:
    def __init__(self):
        self.process = None
        self.port = 8000
        self.host = "0.0.0.0"
        self.project_dir = Path(__file__).parent.parent.parent
        self.api_dir = self.project_dir / "src" / "api"
        
    def kill_existing_processes(self):
        """Kill existing uvicorn processes"""
        print("🔪 Killing existing processes...")
        
        try:
            # Kill processes on port 8000
            subprocess.run(["lsof", "-ti", f":{self.port}"], check=True, capture_output=True)
            subprocess.run(["kill", "-9", "$(lsof -ti :8000)"], shell=True)
            print(f"✅ Killed processes on port {self.port}")
        except subprocess.CalledProcessError:
            print(f"ℹ️  No existing processes on port {self.port}")
        except Exception as e:
            print(f"⚠️  Error killing processes: {e}")
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            ("fastapi", "fastapi"),
            ("uvicorn", "uvicorn"),
            ("opencv-python", "cv2"),
            ("face-recognition", "face_recognition"),
            ("pillow", "PIL"),
            ("numpy", "numpy"),
            ("sqlite3", "sqlite3"),
            ("loguru", "loguru")
        ]
        
        missing_packages = []
        for package_name, import_name in required_packages:
            try:
                __import__(import_name)
                print(f"✅ {package_name}")
            except ImportError:
                missing_packages.append(package_name)
                print(f"❌ {package_name}")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Please install missing packages:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ All dependencies are installed")
        return True
    
    def check_project_structure(self):
        """Check if project structure is correct"""
        print("🔍 Checking project structure...")
        
        required_files = [
            "src/api/main.py",
            "src/services/face_processing.py",
            "src/services/camera_service.py",
            "src/services/simple_vector_db.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                print(f"❌ {file_path}")
            else:
                print(f"✅ {file_path}")
        
        if missing_files:
            print(f"\n❌ Missing files: {', '.join(missing_files)}")
            return False
        
        print("✅ Project structure is correct")
        return True
    
    def start_server(self):
        """Start the FastAPI server"""
        print("🚀 Starting FastAPI server...")
        
        # Change to project directory
        os.chdir(self.project_dir)
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Start uvicorn
        cmd = [
            "python", "-m", "uvicorn",
            "src.api.main:app",
            "--host", self.host,
            "--port", str(self.port),
            "--reload"
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
            
            print(f"✅ Server started on http://{self.host}:{self.port}")
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
        """Check if server is healthy"""
        print("🏥 Performing health check...")
        
        try:
            response = requests.get(f"http://localhost:{self.port}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed")
                print(f"📊 Status: {data.get('data', {}).get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Health check failed: {e}")
            return False
    
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
        print("🚀 Backend Startup Script")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Check project structure
        if not self.check_project_structure():
            return False
        
        # Kill existing processes
        self.kill_existing_processes()
        
        # Start server
        if self.start_server():
            # Wait a bit for server to start
            time.sleep(3)
            
            # Health check
            if self.health_check():
                print("\n🎉 Backend server is running successfully!")
                print(f"🌐 API URL: http://localhost:{self.port}")
                print(f"📚 API Docs: http://localhost:{self.port}/docs")
                return True
            else:
                print("\n❌ Backend server failed health check")
                return False
        else:
            print("\n❌ Failed to start backend server")
            return False

def main():
    """Main function"""
    server = BackendServer()
    
    try:
        success = server.run()
        if success:
            print("\n✅ Backend startup completed successfully!")
        else:
            print("\n❌ Backend startup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Backend startup interrupted")
        server.stop_server()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        server.stop_server()
        sys.exit(1)

if __name__ == "__main__":
    main() 
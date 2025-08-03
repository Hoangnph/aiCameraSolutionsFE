#!/usr/bin/env python3
"""
🚀 Complete System Startup Script
Khởi động cả backend và frontend cho Face Detection System
"""

import os
import sys
import subprocess
import signal
import time
import requests
import threading
from pathlib import Path

class CompleteSystem:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = 8000
        self.frontend_port = 3000
        self.project_dir = Path(__file__).parent
        
    def kill_all_processes(self):
        """Kill all existing processes"""
        print("🔪 Killing all existing processes...")
        
        ports = [self.backend_port, self.frontend_port]
        for port in ports:
            try:
                subprocess.run(["lsof", "-ti", f":{port}"], check=True, capture_output=True)
                subprocess.run(["kill", "-9", f"$(lsof -ti :{port})"], shell=True)
                print(f"✅ Killed processes on port {port}")
            except subprocess.CalledProcessError:
                print(f"ℹ️  No existing processes on port {port}")
            except Exception as e:
                print(f"⚠️  Error killing processes on port {port}: {e}")
    
    def check_dependencies(self):
        """Check system dependencies"""
        print("🔍 Checking system dependencies...")
        
        # Check Python
        try:
            python_version = subprocess.run(["python", "--version"], capture_output=True, text=True)
            print(f"✅ Python: {python_version.stdout.strip()}")
        except Exception as e:
            print(f"❌ Python not found: {e}")
            return False
        
        # Check required packages
        required_packages = [
            "fastapi",
            "uvicorn", 
            "opencv-python",
            "face-recognition",
            "pillow",
            "numpy",
            "requests"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Please install missing packages:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ All dependencies are installed")
        return True
    
    def check_project_structure(self):
        """Check project structure"""
        print("🔍 Checking project structure...")
        
        required_dirs = [
            "src/api",
            "src/services", 
            "fe"
        ]
        
        required_files = [
            "src/api/main.py",
            "src/services/face_processing.py",
            "src/services/camera_service.py",
            "src/services/simple_vector_db.py",
            "fe/index.html"
        ]
        
        # Check directories
        for dir_path in required_dirs:
            full_path = self.project_dir / dir_path
            if not full_path.exists():
                print(f"❌ Missing directory: {dir_path}")
                return False
            else:
                print(f"✅ Directory: {dir_path}")
        
        # Check files
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                print(f"❌ Missing file: {file_path}")
                return False
            else:
                print(f"✅ File: {file_path}")
        
        print("✅ Project structure is correct")
        return True
    
    def start_backend(self):
        """Start backend server"""
        print("🚀 Starting backend server...")
        
        # Change to project directory
        os.chdir(self.project_dir)
        
        cmd = [
            "python", "-m", "uvicorn",
            "src.api.main:app",
            "--host", "0.0.0.0",
            "--port", str(self.backend_port),
            "--reload"
        ]
        
        try:
            self.backend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print(f"✅ Backend server started on http://localhost:{self.backend_port}")
            return True
            
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start frontend server"""
        print("🌐 Starting frontend server...")
        
        # Change to frontend directory
        frontend_dir = self.project_dir / "fe"
        os.chdir(frontend_dir)
        
        cmd = [
            "python", "-m", "http.server",
            str(self.frontend_port),
            "--bind", "0.0.0.0"
        ]
        
        try:
            self.frontend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print(f"✅ Frontend server started on http://localhost:{self.frontend_port}")
            return True
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
    
    def monitor_backend(self):
        """Monitor backend output"""
        if self.backend_process:
            for line in iter(self.backend_process.stdout.readline, ''):
                if line:
                    print(f"[BACKEND] {line.rstrip()}")
    
    def monitor_frontend(self):
        """Monitor frontend output"""
        if self.frontend_process:
            for line in iter(self.frontend_process.stdout.readline, ''):
                if line:
                    print(f"[FRONTEND] {line.rstrip()}")
    
    def health_check(self):
        """Check health of both services"""
        print("🏥 Performing health checks...")
        
        # Check backend
        try:
            response = requests.get(f"http://localhost:{self.backend_port}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is healthy")
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend health check failed: {e}")
            return False
        
        # Check frontend
        try:
            response = requests.get(f"http://localhost:{self.frontend_port}", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend is healthy")
            else:
                print(f"❌ Frontend health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend health check failed: {e}")
            return False
        
        return True
    
    def stop_all(self):
        """Stop all servers"""
        print("🛑 Stopping all servers...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("✅ Backend force stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("✅ Frontend force stopped")
    
    def run(self):
        """Main run method"""
        print("🚀 Complete System Startup Script")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Check project structure
        if not self.check_project_structure():
            return False
        
        # Kill existing processes
        self.kill_all_processes()
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Wait for backend to start
        time.sleep(3)
        
        # Start frontend
        if not self.start_frontend():
            self.stop_all()
            return False
        
        # Wait for frontend to start
        time.sleep(2)
        
        # Health check
        if self.health_check():
            print("\n🎉 Complete system is running successfully!")
            print(f"🌐 Frontend URL: http://localhost:{self.frontend_port}")
            print(f"🔗 Backend API: http://localhost:{self.backend_port}")
            print(f"📚 API Docs: http://localhost:{self.backend_port}/docs")
            print("\n📝 Press Ctrl+C to stop all servers")
            
            # Start monitoring threads
            backend_thread = threading.Thread(target=self.monitor_backend, daemon=True)
            frontend_thread = threading.Thread(target=self.monitor_frontend, daemon=True)
            
            backend_thread.start()
            frontend_thread.start()
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                self.stop_all()
            
            return True
        else:
            print("\n❌ System health check failed")
            self.stop_all()
            return False

def main():
    """Main function"""
    system = CompleteSystem()
    
    try:
        success = system.run()
        if success:
            print("\n✅ Complete system startup completed successfully!")
        else:
            print("\n❌ Complete system startup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 System startup interrupted")
        system.stop_all()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        system.stop_all()
        sys.exit(1)

if __name__ == "__main__":
    main() 
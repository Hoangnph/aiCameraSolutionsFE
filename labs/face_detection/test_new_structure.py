#!/usr/bin/env python3
"""
🧪 Test New Directory Structure
Script để test cấu trúc thư mục mới
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_directory_structure():
    """Test cấu trúc thư mục mới"""
    print("🧪 Testing New Directory Structure")
    print("=" * 40)
    
    # Check if new directories exist
    required_dirs = [
        "scripts/startup",
        "scripts/management", 
        "scripts/debugging",
        "scripts/testing",
        "scripts/tools",
        "scripts/deployment",
        "docs/architecture",
        "docs/summaries",
        "docs/guides",
        "docs/plans",
        "assets/images",
        "assets/data",
        "config"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
    
    print()

def test_startup_scripts():
    """Test các startup scripts"""
    print("🚀 Testing Startup Scripts")
    print("=" * 30)
    
    startup_scripts = [
        "scripts/startup/quick_start_fe.py",
        "scripts/startup/start_backend.py",
        "scripts/startup/start_frontend.py"
    ]
    
    for script in startup_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script}")
    
    print()

def test_management_scripts():
    """Test các management scripts"""
    print("🎛️ Testing Management Scripts")
    print("=" * 30)
    
    management_scripts = [
        "scripts/management/manage_frontend.py",
        "scripts/management/stop_frontend.py",
        "scripts/management/stop_all.py"
    ]
    
    for script in management_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script}")
    
    print()

def test_backend_startup():
    """Test backend startup"""
    print("🔧 Testing Backend Startup")
    print("=" * 30)
    
    try:
        # Start backend
        print("🚀 Starting backend...")
        process = subprocess.Popen([
            sys.executable, "scripts/startup/start_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        time.sleep(10)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and healthy")
                print(f"📊 Response: {response.json()}")
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend is not responding: {e}")
        
        # Stop backend
        process.terminate()
        process.wait(timeout=5)
        print("🛑 Backend stopped")
        
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
    
    print()

def test_frontend_startup():
    """Test frontend startup"""
    print("🌐 Testing Frontend Startup")
    print("=" * 30)
    
    try:
        # Start frontend
        print("🚀 Starting frontend...")
        process = subprocess.Popen([
            sys.executable, "scripts/startup/quick_start_fe.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        time.sleep(5)
        
        # Test frontend
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend is running")
                print("📄 Serving HTML content")
            else:
                print(f"❌ Frontend check failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend is not responding: {e}")
        
        # Stop frontend
        process.terminate()
        process.wait(timeout=5)
        print("🛑 Frontend stopped")
        
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
    
    print()

def main():
    """Main test function"""
    print("🧪 Face Detection System - New Structure Test")
    print("=" * 50)
    
    # Test directory structure
    test_directory_structure()
    
    # Test startup scripts
    test_startup_scripts()
    
    # Test management scripts
    test_management_scripts()
    
    # Test backend startup
    test_backend_startup()
    
    # Test frontend startup
    test_frontend_startup()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 
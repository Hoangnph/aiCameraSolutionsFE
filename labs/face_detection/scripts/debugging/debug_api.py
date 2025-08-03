#!/usr/bin/env python3
"""
🔧 API Server Debug Script
Kiểm tra và debug API server issues
"""

import subprocess
import time
import requests
import os
import sys

def check_port_usage():
    """Check if port 8000 is in use"""
    try:
        result = subprocess.run(['lsof', '-i', ':8000'], capture_output=True, text=True)
        if result.returncode == 0:
            print("🔍 Port 8000 is in use:")
            print(result.stdout)
            return True
        else:
            print("✅ Port 8000 is free")
            return False
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False

def kill_existing_processes():
    """Kill existing uvicorn processes"""
    try:
        result = subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True, text=True)
        print("🔧 Killed existing uvicorn processes")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Error killing processes: {e}")

def start_api_server():
    """Start API server"""
    try:
        print("🚀 Starting API server...")
        process = subprocess.Popen([
            'python', '-m', 'uvicorn', 'src.api.main:app',
            '--host', '0.0.0.0', '--port', '8000', '--reload'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ API server started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ API server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def test_api_health():
    """Test API health endpoint"""
    try:
        print("🔍 Testing API health...")
        response = requests.get('http://localhost:8000/health', timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ API health test failed: {e}")
        return False

def test_api_endpoints():
    """Test basic API endpoints"""
    endpoints = [
        '/health',
        '/api/v1/faces/list',
    ]
    
    for endpoint in endpoints:
        try:
            print(f"🔍 Testing {endpoint}...")
            response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Response: {data}")
            else:
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

def main():
    """Main debug function"""
    print("🔧 API Server Debug Tool")
    print("=" * 50)
    
    # Step 1: Check port usage
    print("\n📋 Step 1: Check Port Usage")
    port_in_use = check_port_usage()
    
    # Step 2: Kill existing processes if needed
    if port_in_use:
        print("\n📋 Step 2: Kill Existing Processes")
        kill_existing_processes()
    
    # Step 3: Start API server
    print("\n📋 Step 3: Start API Server")
    process = start_api_server()
    
    if process:
        # Step 4: Test API health
        print("\n📋 Step 4: Test API Health")
        health_ok = test_api_health()
        
        if health_ok:
            # Step 5: Test endpoints
            print("\n📋 Step 5: Test API Endpoints")
            test_api_endpoints()
        else:
            print("❌ API health check failed")
    
    print("\n" + "=" * 50)
    print("🔧 Debug completed")

if __name__ == "__main__":
    main() 
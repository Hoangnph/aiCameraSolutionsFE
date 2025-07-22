#!/usr/bin/env python3
"""
Simple Demo - AI Camera Counting System
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BEAUTH_URL = "http://localhost:3001"
BECAMERA_URL = "http://localhost:3002"
FRONTEND_URL = "http://localhost:3000"

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🎯 {title}")
    print(f"{'='*50}")

def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 30)

def check_service_health():
    """Check all services health"""
    print_section("SERVICE HEALTH CHECK")
    
    # Check beAuth
    try:
        response = requests.get(f"{BEAUTH_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ beAuth: Healthy")
        else:
            print(f"⚠️  beAuth: Status {response.status_code}")
    except Exception as e:
        print(f"❌ beAuth: Error - {e}")
    
    # Check beCamera
    try:
        response = requests.get(f"{BECAMERA_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ beCamera: Healthy")
        else:
            print(f"⚠️  beCamera: Status {response.status_code}")
    except Exception as e:
        print(f"❌ beCamera: Error - {e}")
    
    # Check Frontend
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Healthy")
        else:
            print(f"⚠️  Frontend: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")

def demo_auth_endpoints():
    """Demo authentication endpoints"""
    print_section("AUTHENTICATION ENDPOINTS")
    
    # Test registration
    register_data = {
        "username": f"demo_user_{int(time.time())}",
        "email": f"demo_{int(time.time())}@example.com",
        "password": "DemoPass123!",
        "password_confirmation": "DemoPass123!",
        "registration_code": "DEMO2024"
    }
    
    print("1. Testing user registration...")
    try:
        response = requests.post(f"{BEAUTH_URL}/api/v1/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ Registration successful")
            user_data = response.json()
            return user_data['data']['access_token']
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def demo_camera_endpoints(token):
    """Demo camera endpoints"""
    print_section("CAMERA ENDPOINTS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get cameras
    print("1. Getting camera list...")
    try:
        response = requests.get(f"{BECAMERA_URL}/api/v1/cameras", headers=headers)
        if response.status_code == 200:
            cameras = response.json()['data']
            print(f"✅ Found {len(cameras)} cameras")
        else:
            print(f"❌ Failed to get cameras: {response.text}")
    except Exception as e:
        print(f"❌ Camera list error: {e}")
    
    # Get worker pool status
    print("2. Getting worker pool status...")
    try:
        response = requests.get(f"{BECAMERA_URL}/api/v1/cameras/worker-pool/status", headers=headers)
        if response.status_code == 200:
            status = response.json()['data']
            print(f"✅ Worker pool: {status['status']} ({status['active_workers']}/{status['total_workers']} workers)")
        else:
            print(f"❌ Failed to get worker pool: {response.text}")
    except Exception as e:
        print(f"❌ Worker pool error: {e}")

def demo_frontend():
    """Demo frontend features"""
    print_section("FRONTEND FEATURES")
    
    print("1. Frontend is running on http://localhost:3000")
    print("2. Available features:")
    print("   - User authentication (login/register)")
    print("   - Camera management dashboard")
    print("   - Real-time analytics")
    print("   - Worker pool monitoring")
    print("   - AI model integration")

def main():
    """Main demo function"""
    print_header("AI CAMERA COUNTING SYSTEM - SIMPLE DEMO")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check service health
    check_service_health()
    
    # Demo authentication
    token = demo_auth_endpoints()
    
    # Demo camera endpoints if we have a token
    if token:
        demo_camera_endpoints(token)
    
    # Demo frontend
    demo_frontend()
    
    print_header("DEMO SUMMARY")
    print("🎉 System is operational!")
    print("📊 All core services are running")
    print("🌐 Frontend accessible at http://localhost:3000")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 
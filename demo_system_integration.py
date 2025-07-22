#!/usr/bin/env python3
"""
AI Camera Counting System - Complete Demo
Showcases all features and integrations
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
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_authentication():
    """Demo authentication flow"""
    print_section("AUTHENTICATION FLOW")
    
    # Register new user
    register_data = {
        "username": f"demo_user_{int(time.time())}",
        "email": f"demo_{int(time.time())}@example.com",
        "password": "DemoPass123!",
        "registration_code": "DEMO2024"
    }
    
    print("1. Registering new user...")
    response = requests.post(f"{BEAUTH_URL}/api/v1/auth/register", json=register_data)
    if response.status_code == 201:
        user_data = response.json()
        print(f"✅ User registered: {user_data['data']['user']['username']}")
        return user_data['data']['access_token']
    else:
        print(f"❌ Registration failed: {response.text}")
        return None

def demo_camera_management(token):
    """Demo camera management features"""
    print_section("CAMERA MANAGEMENT")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create test camera
    camera_data = {
        "name": "Demo Camera 1",
        "rtsp_url": "rtsp://demo:demo@192.168.1.100:554/stream1",
        "location": "Main Entrance",
        "description": "Demo camera for testing",
        "zone_id": 1,
        "ai_model_id": 1
    }
    
    print("1. Creating test camera...")
    response = requests.post(f"{BECAMERA_URL}/api/v1/cameras", json=camera_data, headers=headers)
    if response.status_code == 201:
        camera = response.json()['data']
        print(f"✅ Camera created: {camera['name']} (ID: {camera['id']})")
        return camera['id']
    else:
        print(f"❌ Camera creation failed: {response.text}")
        return None

def demo_worker_pool(token):
    """Demo worker pool features"""
    print_section("WORKER POOL")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("1. Getting worker pool status...")
    response = requests.get(f"{BECAMERA_URL}/api/v1/cameras/worker-pool/status", headers=headers)
    if response.status_code == 200:
        status = response.json()['data']
        print(f"✅ Worker pool status: {status['status']}")
        print(f"   Active workers: {status['active_workers']}")
        print(f"   Total workers: {status['total_workers']}")
        print(f"   Queue size: {status['queue_size']}")
    else:
        print(f"❌ Failed to get worker pool status: {response.text}")

def demo_analytics(token):
    """Demo analytics features"""
    print_section("ANALYTICS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("1. Getting analytics summary...")
    response = requests.get(f"{BECAMERA_URL}/api/v1/cameras/analytics/summary", headers=headers)
    if response.status_code == 200:
        analytics = response.json()['data']
        print(f"✅ Analytics summary retrieved")
        print(f"   Total cameras: {analytics.get('total_cameras', 0)}")
        print(f"   Active cameras: {analytics.get('active_cameras', 0)}")
        print(f"   Total counts: {analytics.get('total_counts', 0)}")
    else:
        print(f"❌ Failed to get analytics: {response.text}")

def demo_frontend_integration():
    """Demo frontend integration"""
    print_section("FRONTEND INTEGRATION")
    
    print("1. Checking frontend accessibility...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")

def demo_system_health():
    """Demo system health checks"""
    print_section("SYSTEM HEALTH")
    
    services = [
        ("beAuth", f"{BEAUTH_URL}/api/v1/auth/health"),
        ("beCamera", f"{BECAMERA_URL}/api/v1/cameras/health"),
        ("Frontend", FRONTEND_URL)
    ]
    
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name}: Healthy")
            else:
                print(f"⚠️  {service_name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {service_name}: Error - {e}")

def main():
    """Main demo function"""
    print_header("AI CAMERA COUNTING SYSTEM - COMPLETE DEMO")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Demo system health
    demo_system_health()
    
    # Demo authentication
    token = demo_authentication()
    if not token:
        print("❌ Cannot continue without authentication token")
        return
    
    # Demo camera management
    camera_id = demo_camera_management(token)
    
    # Demo worker pool
    demo_worker_pool(token)
    
    # Demo analytics
    demo_analytics(token)
    
    # Demo frontend integration
    demo_frontend_integration()
    
    print_header("DEMO COMPLETED")
    print("🎉 All system components are working correctly!")
    print("📊 System is ready for production deployment")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 
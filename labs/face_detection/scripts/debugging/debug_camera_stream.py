#!/usr/bin/env python3
"""
🔍 Debug Camera Stream
Kiểm tra camera stream functionality
"""

import requests
import json
import time
import cv2
import numpy as np

def test_camera_availability():
    """Test camera availability"""
    print("🎥 Testing Camera Availability")
    print("=" * 40)
    
    try:
        # Test OpenCV camera access
        print("1. Testing OpenCV camera access...")
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"   ✅ Camera {i} is available and working")
                    print(f"      - Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
                    print(f"      - FPS: {cap.get(cv2.CAP_PROP_FPS)}")
                else:
                    print(f"   ⚠️ Camera {i} is available but can't read frames")
                cap.release()
            else:
                print(f"   ❌ Camera {i} is not available")
                
    except Exception as e:
        print(f"   ❌ Error testing camera availability: {e}")

def test_camera_api_endpoints():
    """Test camera API endpoints"""
    print("\n🌐 Testing Camera API Endpoints")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Camera status
        print("1. Testing camera status...")
        status_response = requests.get(f"{base_url}/api/v1/camera/status")
        print(f"   Status: {status_response.status_code}")
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   Response: {status_data}")
            
            if status_data.get('success'):
                camera_data = status_data.get('data', {})
                print(f"   📊 Camera Status:")
                print(f"      - Device ID: {camera_data.get('device_id')}")
                print(f"      - Active: {camera_data.get('active')}")
                print(f"      - Resolution: {camera_data.get('resolution')}")
                print(f"      - FPS: {camera_data.get('fps')}")
            else:
                print(f"   ❌ Camera status failed: {status_data.get('message')}")
        else:
            print(f"   ❌ Camera status failed with status: {status_response.status_code}")
            
        # Test 2: Start camera
        print("\n2. Testing camera start...")
        start_response = requests.post(
            f"{base_url}/api/v1/camera/start",
            headers={'Content-Type': 'application/json'},
            json={'camera_id': 0}
        )
        print(f"   Status: {start_response.status_code}")
        
        if start_response.status_code == 200:
            start_data = start_response.json()
            print(f"   Response: {start_data}")
            
            if start_data.get('success'):
                print("   ✅ Camera started successfully")
                
                # Test 3: Camera stream
                print("\n3. Testing camera stream...")
                test_camera_stream()
                
                # Test 4: Stop camera
                print("\n4. Testing camera stop...")
                stop_response = requests.post(f"{base_url}/api/v1/camera/stop")
                print(f"   Status: {stop_response.status_code}")
                
                if stop_response.status_code == 200:
                    stop_data = stop_response.json()
                    print(f"   Response: {stop_data}")
                    
                    if stop_data.get('success'):
                        print("   ✅ Camera stopped successfully")
                    else:
                        print(f"   ❌ Camera stop failed: {stop_data.get('message')}")
                else:
                    print(f"   ❌ Camera stop failed with status: {stop_response.status_code}")
            else:
                print(f"   ❌ Camera start failed: {start_data.get('message')}")
        else:
            print(f"   ❌ Camera start failed with status: {start_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing camera API endpoints: {e}")

def test_camera_stream():
    """Test camera stream endpoint"""
    print("   📹 Testing camera stream...")
    
    try:
        base_url = "http://localhost:8000"
        
        # Test stream endpoint
        stream_response = requests.get(
            f"{base_url}/api/v1/camera/stream",
            stream=True,
            timeout=10
        )
        
        print(f"   Stream Status: {stream_response.status_code}")
        print(f"   Content-Type: {stream_response.headers.get('content-type')}")
        
        if stream_response.status_code == 200:
            print("   ✅ Stream endpoint responding")
            
            # Try to read some data
            data_received = False
            for chunk in stream_response.iter_content(chunk_size=1024):
                if chunk:
                    data_received = True
                    print(f"   📊 Received {len(chunk)} bytes of stream data")
                    break
                    
            if data_received:
                print("   ✅ Stream data received successfully")
            else:
                print("   ⚠️ Stream endpoint responding but no data received")
        else:
            print(f"   ❌ Stream endpoint failed: {stream_response.status_code}")
            
    except requests.exceptions.Timeout:
        print("   ⏰ Stream request timed out")
    except Exception as e:
        print(f"   ❌ Error testing camera stream: {e}")

def test_camera_service_integration():
    """Test camera service integration"""
    print("\n🔧 Testing Camera Service Integration")
    print("=" * 45)
    
    try:
        # Import camera service
        import sys
        import os
        sys.path.append(os.path.join(os.getcwd(), 'src'))
        
        from services.camera_service import CameraService
        
        # Initialize camera service
        print("1. Initializing camera service...")
        camera_service = CameraService()
        
        # Test available cameras
        print("\n2. Testing available cameras...")
        available_cameras = camera_service.get_available_cameras()
        print(f"   Found {len(available_cameras)} available cameras")
        
        for camera in available_cameras:
            print(f"   📷 Camera {camera['id']}: {camera['name']}")
            print(f"      - Resolution: {camera['resolution']}")
            print(f"      - FPS: {camera['fps']}")
            print(f"      - Status: {camera['status']}")
        
        # Test frame generator
        if available_cameras:
            print("\n3. Testing frame generator...")
            frame_count = 0
            max_frames = 5
            
            for frame in camera_service.get_frame_generator(device_id=0, max_frames=max_frames):
                if frame is not None:
                    frame_count += 1
                    print(f"   📊 Frame {frame_count}: shape={frame.shape}")
                    
                    if frame_count >= max_frames:
                        break
                else:
                    print("   ❌ No frame received")
                    break
            
            print(f"   ✅ Generated {frame_count} frames")
        else:
            print("   ⚠️ No cameras available for testing")
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
    except Exception as e:
        print(f"   ❌ Error testing camera service: {e}")

def test_frontend_camera_integration():
    """Test frontend camera integration"""
    print("\n🎨 Testing Frontend Camera Integration")
    print("=" * 45)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for camera control elements
            camera_elements = [
                'camera-select',
                'camera-info',
                'camera-stream',
                'camera-placeholder',
                'startCamera()',
                'stopCamera()',
                'startVideoStream()',
                'stopVideoStream()'
            ]
            
            for element in camera_elements:
                if element in html_content:
                    print(f"✅ {element} found in HTML")
                else:
                    print(f"❌ {element} missing from HTML")
                    
            # Check for camera stream URL
            if '/api/v1/camera/stream' in html_content:
                print("✅ Camera stream URL found in JavaScript")
            else:
                print("❌ Camera stream URL missing from JavaScript")
                
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend camera integration: {e}")

def provide_debug_recommendations():
    """Provide debug recommendations"""
    print("\n💡 Debug Recommendations")
    print("=" * 30)
    
    recommendations = [
        "1. Check if camera is connected and working",
        "2. Verify camera permissions in system",
        "3. Test camera with other applications",
        "4. Check backend logs for camera errors",
        "5. Verify camera device ID in config",
        "6. Test with different camera indices",
        "7. Check OpenCV installation",
        "8. Verify camera drivers are installed"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    print("🔍 Camera Stream Debug")
    print("=" * 60)
    
    # Test camera availability
    test_camera_availability()
    
    # Test camera API endpoints
    test_camera_api_endpoints()
    
    # Test camera service integration
    test_camera_service_integration()
    
    # Test frontend integration
    test_frontend_camera_integration()
    
    # Provide recommendations
    provide_debug_recommendations()
    
    print("\n✅ Camera stream debug completed!")
    print("\n💡 Common Issues:")
    print("   - Camera not connected or recognized")
    print("   - Camera permissions denied")
    print("   - OpenCV camera access issues")
    print("   - Backend camera service not working")
    print("   - Frontend stream URL incorrect")
    print("   - Network connectivity issues") 
#!/usr/bin/env python3
"""
🔍 Check Available Cameras
Kiểm tra các camera có sẵn trên hệ thống
"""

import cv2
import sys

def check_available_cameras():
    """Check which cameras are available"""
    print("🔍 Checking Available Cameras")
    print("=" * 40)
    
    available_cameras = []
    
    # Check first 10 camera indices
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Try to read a frame
                ret, frame = cap.read()
                if ret:
                    # Get camera properties
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    
                    camera_info = {
                        'id': i,
                        'width': width,
                        'height': height,
                        'fps': fps,
                        'status': 'Available'
                    }
                    available_cameras.append(camera_info)
                    
                    print(f"✅ Camera {i}: Available")
                    print(f"   - Resolution: {width}x{height}")
                    print(f"   - FPS: {fps}")
                else:
                    print(f"⚠️ Camera {i}: Opened but can't read frames")
            else:
                print(f"❌ Camera {i}: Not available")
                
            cap.release()
            
        except Exception as e:
            print(f"❌ Camera {i}: Error - {e}")
    
    print(f"\n📊 Summary: Found {len(available_cameras)} available cameras")
    
    if available_cameras:
        print("\n🎯 Recommended Configuration:")
        for camera in available_cameras:
            print(f"   - Use Camera {camera['id']} as primary")
            print(f"   - Resolution: {camera['width']}x{camera['height']}")
            print(f"   - FPS: {camera['fps']}")
    else:
        print("\n⚠️ No cameras found! Check:")
        print("   - Camera is connected")
        print("   - Camera drivers are installed")
        print("   - Camera permissions are granted")
        print("   - No other app is using camera")
    
    return available_cameras

def test_camera_api():
    """Test camera API endpoints"""
    print("\n🌐 Testing Camera API")
    print("=" * 25)
    
    import requests
    
    try:
        base_url = "http://localhost:8000"
        
        # Test health check
        print("1. Testing health check...")
        health_response = requests.get(f"{base_url}/health")
        print(f"   Status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            print("   ✅ Backend is running")
            
            # Test camera status
            print("\n2. Testing camera status...")
            status_response = requests.get(f"{base_url}/api/v1/camera/status")
            print(f"   Status: {status_response.status_code}")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Response: {status_data}")
            else:
                print(f"   ❌ Camera status failed: {status_response.status_code}")
                
            # Test camera start with different IDs
            print("\n3. Testing camera start...")
            for camera_id in [0, 1]:
                print(f"   Testing Camera {camera_id}...")
                start_response = requests.post(
                    f"{base_url}/api/v1/camera/start",
                    headers={'Content-Type': 'application/json'},
                    json={'camera_id': camera_id}
                )
                print(f"   Status: {start_response.status_code}")
                
                if start_response.status_code == 200:
                    start_data = start_response.json()
                    print(f"   Success: {start_data.get('success')}")
                    print(f"   Message: {start_data.get('message')}")
                else:
                    print(f"   Error: {start_response.text}")
                
                # Stop camera
                stop_response = requests.post(f"{base_url}/api/v1/camera/stop")
                print(f"   Stop Status: {stop_response.status_code}")
                
        else:
            print("   ❌ Backend not running")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing camera API: {e}")

if __name__ == "__main__":
    print("🔍 Camera Configuration Check")
    print("=" * 60)
    
    # Check available cameras
    cameras = check_available_cameras()
    
    # Test camera API
    test_camera_api()
    
    print("\n✅ Camera check completed!")
    
    if cameras:
        print(f"\n💡 Configuration Recommendation:")
        print(f"   - Primary Camera: Camera {cameras[0]['id']}")
        print(f"   - Resolution: {cameras[0]['width']}x{cameras[0]['height']}")
        print(f"   - FPS: {cameras[0]['fps']}")
    else:
        print("\n⚠️ No cameras found! Please check camera connection and permissions.") 
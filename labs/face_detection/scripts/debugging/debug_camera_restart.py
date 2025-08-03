#!/usr/bin/env python3
"""
🔍 Debug Camera Restart Issues
Kiểm tra vấn đề camera restart và switch
"""

import requests
import json
import time
import cv2
import numpy as np

def test_camera_restart_cycle():
    """Test camera restart cycle"""
    print("🔄 Testing Camera Restart Cycle")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        for cycle in range(3):
            print(f"\n--- Cycle {cycle + 1} ---")
            
            # Step 1: Check initial status
            print("1. Checking camera status...")
            status_response = requests.get(f"{base_url}/api/v1/camera/status")
            print(f"   Status: {status_response.status_code}")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Active: {status_data.get('data', {}).get('active', False)}")
            
            # Step 2: Start camera
            print("2. Starting camera...")
            start_response = requests.post(
                f"{base_url}/api/v1/camera/start",
                headers={'Content-Type': 'application/json'},
                json={'camera_id': 0}
            )
            print(f"   Status: {start_response.status_code}")
            
            if start_response.status_code == 200:
                start_data = start_response.json()
                print(f"   Success: {start_data.get('success', False)}")
                
                # Step 3: Test stream briefly
                print("3. Testing stream...")
                test_stream_briefly()
                
                # Step 4: Stop camera
                print("4. Stopping camera...")
                stop_response = requests.post(f"{base_url}/api/v1/camera/stop")
                print(f"   Status: {stop_response.status_code}")
                
                if stop_response.status_code == 200:
                    stop_data = stop_response.json()
                    print(f"   Success: {stop_data.get('success', False)}")
                
                # Step 5: Wait before next cycle
                print("5. Waiting 2 seconds...")
                time.sleep(2)
            else:
                print("   ❌ Failed to start camera")
                
    except Exception as e:
        print(f"❌ Error in camera restart cycle: {e}")

def test_camera_switch():
    """Test switching between different cameras"""
    print("\n📷 Testing Camera Switch")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test with different camera IDs
        for camera_id in [0, 1, 0]:  # Test 0 -> 1 -> 0
            print(f"\n--- Testing Camera {camera_id} ---")
            
            # Start camera
            print(f"1. Starting camera {camera_id}...")
            start_response = requests.post(
                f"{base_url}/api/v1/camera/start",
                headers={'Content-Type': 'application/json'},
                json={'camera_id': camera_id}
            )
            print(f"   Status: {start_response.status_code}")
            
            if start_response.status_code == 200:
                start_data = start_response.json()
                print(f"   Success: {start_data.get('success', False)}")
                
                # Test stream
                print("2. Testing stream...")
                test_stream_briefly()
                
                # Stop camera
                print("3. Stopping camera...")
                stop_response = requests.post(f"{base_url}/api/v1/camera/stop")
                print(f"   Status: {stop_response.status_code}")
                
                # Wait before next camera
                print("4. Waiting 1 second...")
                time.sleep(1)
            else:
                print(f"   ❌ Failed to start camera {camera_id}")
                
    except Exception as e:
        print(f"❌ Error in camera switch test: {e}")

def test_stream_briefly():
    """Test stream briefly to see if it's working"""
    try:
        base_url = "http://localhost:8000"
        
        # Test stream for 3 seconds
        stream_response = requests.get(
            f"{base_url}/api/v1/camera/stream",
            stream=True,
            timeout=3
        )
        
        print(f"   Stream Status: {stream_response.status_code}")
        
        if stream_response.status_code == 200:
            # Try to read some data
            data_received = False
            chunk_count = 0
            
            for chunk in stream_response.iter_content(chunk_size=1024):
                if chunk:
                    data_received = True
                    chunk_count += 1
                    print(f"   📊 Received chunk {chunk_count}: {len(chunk)} bytes")
                    
                    if chunk_count >= 3:  # Only read 3 chunks
                        break
                        
            if data_received:
                print("   ✅ Stream data received successfully")
            else:
                print("   ⚠️ Stream responding but no data received")
        else:
            print(f"   ❌ Stream failed: {stream_response.status_code}")
            
    except requests.exceptions.Timeout:
        print("   ⏰ Stream request timed out")
    except Exception as e:
        print(f"   ❌ Error testing stream: {e}")

def test_camera_service_cleanup():
    """Test camera service cleanup"""
    print("\n🧹 Testing Camera Service Cleanup")
    print("=" * 35)
    
    try:
        # Import camera service
        import sys
        import os
        sys.path.append(os.path.join(os.getcwd(), 'src'))
        
        from services.camera_service import CameraService
        
        # Initialize camera service
        print("1. Initializing camera service...")
        camera_service = CameraService()
        
        # Test camera operations
        print("2. Testing camera operations...")
        
        # Open camera
        cap = camera_service.open_camera(0)
        if cap:
            print("   ✅ Camera opened successfully")
            
            # Read a few frames
            frame_count = 0
            for i in range(5):
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
                    print(f"   📊 Frame {frame_count}: shape={frame.shape}")
                else:
                    print(f"   ❌ Failed to read frame {i}")
                    break
            
            # Release camera
            cap.release()
            print("   ✅ Camera released successfully")
            
            # Test cleanup
            print("3. Testing cleanup...")
            camera_service.cleanup()
            print("   ✅ Camera service cleaned up")
            
        else:
            print("   ❌ Failed to open camera")
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
    except Exception as e:
        print(f"   ❌ Error testing camera service: {e}")

def test_frontend_camera_restart():
    """Test frontend camera restart handling"""
    print("\n🎨 Testing Frontend Camera Restart")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for restart handling
            restart_elements = [
                'stopVideoStream()',
                'streamImg.src = \'\'',
                'cameraServiceActive = false',
                'clearInterval',
                'getTracks().forEach(track => track.stop())',
                'startVideoStream()',
                'streamImg.src = `${API_BASE}/api/v1/camera/stream`'
            ]
            
            for element in restart_elements:
                if element in html_content:
                    print(f"✅ {element} found in JavaScript")
                else:
                    print(f"❌ {element} missing from JavaScript")
                    
            # Check for error handling
            error_handling = [
                'streamImg.onerror',
                'console.error',
                'status-error',
                'stopVideoStream()'
            ]
            
            for element in error_handling:
                if element in html_content:
                    print(f"✅ {element} found in error handling")
                else:
                    print(f"❌ {element} missing from error handling")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend restart: {e}")

def provide_restart_debug_recommendations():
    """Provide debug recommendations for restart issues"""
    print("\n💡 Debug Recommendations for Camera Restart")
    print("=" * 50)
    
    recommendations = [
        "1. Check if camera is properly released after stop",
        "2. Verify stream connection is closed correctly",
        "3. Test camera service cleanup methods",
        "4. Check frontend error handling for stream failures",
        "5. Verify camera device is not locked by other processes",
        "6. Test with different camera indices",
        "7. Check browser console for JavaScript errors",
        "8. Monitor backend logs for camera service errors",
        "9. Test camera permissions after restart",
        "10. Verify OpenCV camera release is working"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    print("🔍 Camera Restart Debug")
    print("=" * 60)
    
    # Test camera restart cycle
    test_camera_restart_cycle()
    
    # Test camera switch
    test_camera_switch()
    
    # Test camera service cleanup
    test_camera_service_cleanup()
    
    # Test frontend restart handling
    test_frontend_camera_restart()
    
    # Provide recommendations
    provide_restart_debug_recommendations()
    
    print("\n✅ Camera restart debug completed!")
    print("\n💡 Common Restart Issues:")
    print("   - Camera not properly released after stop")
    print("   - Stream connection not closed correctly")
    print("   - Frontend not handling stream errors")
    print("   - Camera device locked by other processes")
    print("   - Browser not refreshing stream source")
    print("   - Backend camera service not cleaning up") 
#!/usr/bin/env python3
"""
🔍 Debug Camera Permissions
Kiểm tra camera permissions và availability
"""

import cv2
import subprocess
import sys
import os

def check_camera_permissions():
    """Check camera permissions on macOS"""
    print("🔍 Checking Camera Permissions")
    print("=" * 40)
    
    try:
        # Check if we're on macOS
        if sys.platform == "darwin":
            print("🖥️ macOS detected")
            
            # Check camera permissions using tccutil
            result = subprocess.run([
                'tccutil', 'reset', 'Camera'
            ], capture_output=True, text=True)
            
            print("📋 Camera permissions reset (if needed)")
            
            # Check if camera is being used by other apps
            print("\n🔍 Checking for camera usage by other apps:")
            
            # Common apps that might use camera
            camera_apps = [
                'FaceTime',
                'Photo Booth',
                'Zoom',
                'Teams',
                'Skype',
                'Chrome',
                'Safari',
                'Firefox'
            ]
            
            for app in camera_apps:
                result = subprocess.run([
                    'pgrep', '-f', app
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ⚠️ {app} is running (might be using camera)")
                else:
                    print(f"   ✅ {app} is not running")
                    
        else:
            print("🖥️ Non-macOS system detected")
            
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")

def force_release_camera():
    """Force release camera from any processes"""
    print("\n🔧 Force Releasing Camera")
    print("=" * 30)
    
    try:
        # Try to open and immediately release camera
        print("1. Attempting to open camera...")
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("   ✅ Camera opened successfully")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret:
                print("   ✅ Camera can read frames")
                print(f"   📊 Frame shape: {frame.shape}")
            else:
                print("   ⚠️ Camera opened but can't read frames")
            
            # Release camera
            cap.release()
            print("   ✅ Camera released")
            
        else:
            print("   ❌ Camera cannot be opened")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_camera_with_different_methods():
    """Test camera with different methods"""
    print("\n🧪 Testing Camera with Different Methods")
    print("=" * 45)
    
    methods = [
        ("OpenCV VideoCapture", lambda: cv2.VideoCapture(0)),
        ("OpenCV VideoCapture with backend", lambda: cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)),
        ("OpenCV VideoCapture with V4L2", lambda: cv2.VideoCapture(0, cv2.CAP_V4L2)),
    ]
    
    for method_name, method_func in methods:
        print(f"\nTesting: {method_name}")
        try:
            cap = method_func()
            if cap.isOpened():
                print(f"   ✅ {method_name} - Camera opened")
                
                # Try to read frame
                ret, frame = cap.read()
                if ret:
                    print(f"   ✅ {method_name} - Frame read successfully")
                    print(f"   📊 Frame shape: {frame.shape}")
                else:
                    print(f"   ⚠️ {method_name} - Camera opened but can't read frames")
                
                cap.release()
                print(f"   ✅ {method_name} - Camera released")
            else:
                print(f"   ❌ {method_name} - Camera cannot be opened")
                
        except Exception as e:
            print(f"   ❌ {method_name} - Error: {e}")

def check_system_camera_info():
    """Check system camera information"""
    print("\n📋 System Camera Information")
    print("=" * 35)
    
    try:
        # Check if we're on macOS
        if sys.platform == "darwin":
            print("🖥️ macOS Camera Info:")
            
            # Check camera devices
            result = subprocess.run([
                'system_profiler', 'SPCameraDataType'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   📷 Camera devices found:")
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Camera' in line or 'Webcam' in line or 'FaceTime' in line:
                        print(f"      {line.strip()}")
            else:
                print("   ❌ Could not get camera device info")
                
        else:
            print("🖥️ Non-macOS system - checking /dev/video*")
            
            # Check for video devices
            result = subprocess.run([
                'ls', '/dev/video*'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   📷 Video devices found:")
                for device in result.stdout.strip().split('\n'):
                    if device:
                        print(f"      {device}")
            else:
                print("   ❌ No video devices found")
                
    except Exception as e:
        print(f"❌ Error getting system camera info: {e}")

def provide_camera_fix_recommendations():
    """Provide recommendations to fix camera issues"""
    print("\n💡 Camera Fix Recommendations")
    print("=" * 35)
    
    recommendations = [
        "1. Close all apps that might be using camera:",
        "   - FaceTime, Photo Booth, Zoom, Teams, Skype",
        "   - Chrome, Safari, Firefox (if using camera)",
        "   - Any video conferencing apps",
        "",
        "2. Check camera permissions:",
        "   - Go to System Preferences > Security & Privacy > Privacy > Camera",
        "   - Make sure your terminal/IDE has camera access",
        "   - Reset camera permissions if needed",
        "",
        "3. Restart camera services:",
        "   - Restart your computer",
        "   - Or restart camera-related services",
        "",
        "4. Check camera hardware:",
        "   - Ensure camera is not physically covered",
        "   - Check if camera works in other apps",
        "   - Test camera in FaceTime or Photo Booth",
        "",
        "5. Update camera drivers:",
        "   - Check for system updates",
        "   - Update camera drivers if available",
        "",
        "6. Test with different camera index:",
        "   - Try camera index 1, 2, etc.",
        "   - Some systems use different indices",
        "",
        "7. Check for camera conflicts:",
        "   - External cameras might conflict with built-in",
        "   - USB cameras might need different drivers"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    print("🔍 Camera Permissions Debug")
    print("=" * 60)
    
    # Check camera permissions
    check_camera_permissions()
    
    # Force release camera
    force_release_camera()
    
    # Test with different methods
    test_camera_with_different_methods()
    
    # Check system camera info
    check_system_camera_info()
    
    # Provide recommendations
    provide_camera_fix_recommendations()
    
    print("\n✅ Camera permissions debug completed!")
    print("\n💡 If camera still doesn't work:")
    print("   1. Close all apps using camera")
    print("   2. Check camera permissions in System Preferences")
    print("   3. Restart your computer")
    print("   4. Test camera in FaceTime or Photo Booth first") 
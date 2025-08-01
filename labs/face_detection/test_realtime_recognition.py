#!/usr/bin/env python3
"""
Real-time Face Recognition Test Script
Tests the camera stream with face recognition capabilities
"""

import cv2
import requests
import json
import time
import numpy as np
from PIL import Image
import io
import base64

class RealTimeFaceRecognitionTest:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.camera = None
        self.face_recognition_active = False
        
    def test_api_health(self):
        """Test if the API is running"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ API Health Check:", data.get('message', 'Unknown'))
                return True
            else:
                print("❌ API Health Check Failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ API Health Check Error: {e}")
            return False
    
    def test_camera_status(self):
        """Test camera status"""
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/camera/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                camera_data = data.get('data', {})
                print(f"✅ Camera Status: Device {camera_data.get('device_id')}, Active: {camera_data.get('active')}")
                return camera_data.get('active', False)
            else:
                print("❌ Camera Status Failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ Camera Status Error: {e}")
            return False
    
    def start_camera(self):
        """Start the camera"""
        try:
            response = requests.post(f"{self.api_base_url}/api/v1/camera/start", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Camera Started:", data.get('message', 'Unknown'))
                return True
            else:
                print("❌ Camera Start Failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ Camera Start Error: {e}")
            return False
    
    def stop_camera(self):
        """Stop the camera"""
        try:
            response = requests.post(f"{self.api_base_url}/api/v1/camera/stop", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Camera Stopped:", data.get('message', 'Unknown'))
                return True
            else:
                print("❌ Camera Stop Failed:", response.status_code)
                return False
        except Exception as e:
            print(f"❌ Camera Stop Error: {e}")
            return False
    
    def test_face_recognition_with_frame(self, frame):
        """Test face recognition with a single frame"""
        try:
            # Convert frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()
            
            # Prepare multipart form data
            files = {'file': ('frame.jpg', image_bytes, 'image/jpeg')}
            data = {'threshold': '0.6'}
            
            response = requests.post(
                f"{self.api_base_url}/api/v1/faces/recognize",
                files=files,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    recognition_data = result.get('data', {})
                    if recognition_data.get('recognized'):
                        person = recognition_data.get('person', {})
                        confidence = recognition_data.get('confidence', 0)
                        print(f"✅ Face Recognized: {person.get('name', 'Unknown')} (Confidence: {confidence:.2f})")
                        return True
                    else:
                        print("ℹ️ No face recognized in frame")
                        return False
                else:
                    print("❌ Face recognition failed:", result.get('message', 'Unknown error'))
                    return False
            else:
                print(f"❌ Face recognition request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Face recognition error: {e}")
            return False
    
    def test_local_camera_recognition(self):
        """Test face recognition using local camera"""
        print("\n🎥 Testing Real-time Face Recognition with Local Camera...")
        
        # Initialize local camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot open local camera")
            return False
        
        print("✅ Local camera opened successfully")
        print("Press 'q' to quit, 'r' to test recognition on current frame")
        
        frame_count = 0
        recognition_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Failed to grab frame")
                    break
                
                # Display frame
                cv2.imshow('Real-time Face Recognition Test', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    print(f"\n🔄 Testing recognition on frame {frame_count}...")
                    if self.test_face_recognition_with_frame(frame):
                        recognition_count += 1
                    frame_count += 1
                
                # Auto-test every 30 frames (about 1 second at 30fps)
                if frame_count % 30 == 0 and frame_count > 0:
                    print(f"\n🔄 Auto-testing recognition on frame {frame_count}...")
                    if self.test_face_recognition_with_frame(frame):
                        recognition_count += 1
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n⏹️ Test interrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
        print(f"\n📊 Test Summary:")
        print(f"   Total frames processed: {frame_count}")
        print(f"   Recognition attempts: {recognition_count}")
        print(f"   Recognition rate: {(recognition_count/frame_count*100):.1f}%" if frame_count > 0 else "N/A")
        
        return True
    
    def test_registered_faces(self):
        """Test listing registered faces"""
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/faces/list", timeout=5)
            if response.status_code == 200:
                data = response.json()
                faces = data.get('data', {}).get('faces', [])
                print(f"✅ Found {len(faces)} registered faces:")
                for i, face in enumerate(faces, 1):
                    metadata = face.get('metadata', {})
                    name = metadata.get('name', 'Unknown')
                    person_id = metadata.get('person_id', 'Unknown')
                    print(f"   {i}. {name} (ID: {person_id})")
                return len(faces)
            else:
                print("❌ Failed to get registered faces:", response.status_code)
                return 0
        except Exception as e:
            print(f"❌ Error getting registered faces: {e}")
            return 0
    
    def run_comprehensive_test(self):
        """Run comprehensive real-time face recognition test"""
        print("🚀 Starting Real-time Face Recognition Test")
        print("=" * 50)
        
        # Test 1: API Health
        print("\n1️⃣ Testing API Health...")
        if not self.test_api_health():
            print("❌ API is not running. Please start the server first.")
            return False
        
        # Test 2: Camera Status
        print("\n2️⃣ Testing Camera Status...")
        camera_active = self.test_camera_status()
        
        # Test 3: Start Camera if needed
        if not camera_active:
            print("\n3️⃣ Starting Camera...")
            if not self.start_camera():
                print("❌ Failed to start camera")
                return False
        
        # Test 4: List Registered Faces
        print("\n4️⃣ Checking Registered Faces...")
        face_count = self.test_registered_faces()
        if face_count == 0:
            print("⚠️ No faces registered. Please register some faces first.")
            print("   Use: curl -X POST -F 'file=@test_image.jpg' -F 'name=Test User' http://localhost:8000/api/v1/faces/upload")
        
        # Test 5: Real-time Recognition
        print("\n5️⃣ Testing Real-time Face Recognition...")
        self.test_local_camera_recognition()
        
        # Test 6: Stop Camera
        print("\n6️⃣ Stopping Camera...")
        self.stop_camera()
        
        print("\n✅ Real-time Face Recognition Test Completed!")
        return True

def main():
    """Main function"""
    print("🎯 Face Detection System - Real-time Recognition Test")
    print("=" * 60)
    
    # Create test instance
    tester = RealTimeFaceRecognitionTest()
    
    # Run comprehensive test
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the server and try again.")
    
    print("\n📝 Test Instructions:")
    print("1. Make sure the server is running: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload")
    print("2. Register some faces first using the upload endpoint")
    print("3. Run this test script to verify real-time recognition")
    print("4. Press 'r' during the test to manually trigger recognition")
    print("5. Press 'q' to quit the test")

if __name__ == "__main__":
    main() 
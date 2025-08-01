#!/usr/bin/env python3
"""
🔍 Test Real-time Face Detection
Kiểm tra tính năng real-time face detection
"""

import requests
import json
import time
from PIL import Image, ImageDraw
import io

def create_test_face_image():
    """Tạo test image với face"""
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ một face đơn giản
    # Head
    draw.ellipse([200, 150, 440, 350], outline='black', width=3)
    # Eyes
    draw.ellipse([250, 200, 290, 240], fill='black')  # Left eye
    draw.ellipse([350, 200, 390, 240], fill='black')  # Right eye
    # Nose
    draw.line([320, 240, 320, 280], fill='black', width=3)
    # Mouth
    draw.arc([280, 280, 360, 320], 0, 180, fill='black', width=3)
    
    return img

def create_no_face_image():
    """Tạo test image không có face"""
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Vẽ một số hình dạng ngẫu nhiên
    draw.rectangle([100, 100, 200, 200], fill='red')
    draw.ellipse([400, 300, 450, 350], fill='green')
    
    return img

def test_face_detection_api():
    """Test face detection API"""
    print("🔍 Testing Face Detection API...")
    
    # Test với face image
    print("\n📷 Testing with face image:")
    face_img = create_test_face_image()
    img_bytes = io.BytesIO()
    face_img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    try:
        files = {'file': ('face_test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/recognize', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data['success']}")
            if data['success']:
                result = data['data']
                print(f"   - Detected: {result['recognized']}")
                print(f"   - Confidence: {result.get('confidence', 0):.2%}")
            else:
                print(f"   - Error: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test với no-face image
    print("\n📷 Testing with no-face image:")
    no_face_img = create_no_face_image()
    img_bytes = io.BytesIO()
    no_face_img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    try:
        files = {'file': ('no_face_test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/recognize', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data['success']}")
            if data['success']:
                result = data['data']
                print(f"   - Detected: {result['recognized']}")
                print(f"   - Confidence: {result.get('confidence', 0):.2%}")
            else:
                print(f"   - Error: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_health():
    """Test API health"""
    print("🏥 Testing API Health...")
    
    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy")
            print(f"   - Services: {data['data']['services']}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API health check error: {e}")

def test_frontend_access():
    """Test frontend access"""
    print("\n🌐 Testing Frontend Access...")
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            if 'face-detection-overlay' in response.text:
                print("✅ Real-time face detection UI elements found")
            else:
                print("⚠️ Real-time face detection UI elements not found")
        else:
            print(f"❌ Frontend access failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend access error: {e}")

def main():
    """Main function"""
    print("🚀 Real-time Face Detection Test")
    print("=" * 50)
    
    # Test API health
    test_api_health()
    
    # Test face detection API
    test_face_detection_api()
    
    # Test frontend access
    test_frontend_access()
    
    print("\n✅ Real-time face detection test completed!")
    print("\n📋 Instructions for manual testing:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Go to 'Register New Face' tab")
    print("3. Select 'Use Webcam' option")
    print("4. Click 'Start Webcam'")
    print("5. Look at the camera - you should see face detection status")
    print("6. Capture button should only be enabled when face is detected")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🔍 Test Face Detection with Bounding Boxes
Kiểm tra endpoint detect faces với bounding boxes
"""

import requests
import json
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

def test_face_detection_api():
    """Test face detection API với bounding boxes"""
    print("🔍 Testing Face Detection API with Bounding Boxes...")
    
    # Tạo test image
    face_img = create_test_face_image()
    img_bytes = io.BytesIO()
    face_img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    try:
        files = {'file': ('face_test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Face Detection Response:")
            print(json.dumps(data, indent=2))
            
            if data['success']:
                faces = data['data']['faces']
                print(f"\n📊 Detection Results:")
                print(f"   - Total faces detected: {len(faces)}")
                
                for i, face in enumerate(faces):
                    box = face['bounding_box']
                    print(f"   - Face {i+1}:")
                    print(f"     * Position: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
                    print(f"     * Size: {box['width']} x {box['height']} pixels")
                    print(f"     * Confidence: {face['confidence']:.2%}")
                    print(f"     * Quality: {face['quality_score']:.2%}")
            else:
                print(f"❌ Detection failed: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
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

def main():
    """Main function"""
    print("🚀 Face Detection with Bounding Boxes Test")
    print("=" * 50)
    
    # Test API health
    test_api_health()
    
    # Test face detection API
    test_face_detection_api()
    
    print("\n✅ Face detection test completed!")
    print("\n📋 Instructions for manual testing:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Go to 'Register New Face' tab")
    print("3. Select 'Use Webcam' option")
    print("4. Click 'Start Webcam'")
    print("5. Look at the camera - you should see green bounding boxes around faces")
    print("6. Capture button should only be enabled when face is detected")
    print("7. When capturing, only the face region will be cropped")

if __name__ == "__main__":
    main() 
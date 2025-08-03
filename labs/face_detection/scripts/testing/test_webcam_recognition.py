#!/usr/bin/env python3
"""
📷 Test Webcam Recognition Script
Debug vấn đề "undefined" trong webcam recognition
"""

import requests
import json
import base64
from PIL import Image, ImageDraw
import io

def create_test_webcam_image():
    """Tạo test image giống webcam capture"""
    # Tạo một image đơn giản để test
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
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_webcam_recognition():
    """Test webcam recognition với test image"""
    print("📷 Testing Webcam Recognition...")
    
    try:
        # Tạo test image
        image_data = create_test_webcam_image()
        
        # Test recognition
        files = {'file': ('webcam_test.jpg', io.BytesIO(image_data), 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/recognize', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Webcam Recognition Response:")
            print(json.dumps(data, indent=2))
            
            if data['success']:
                result = data['data']
                print(f"\n📊 Webcam Recognition Results:")
                print(f"   - Recognized: {result['recognized']}")
                if result['recognized']:
                    print(f"   - Person Name: {result['person']['name']}")
                    print(f"   - Person ID: {result['person']['id']}")
                    print(f"   - Confidence: {result['confidence']:.2%}")
                else:
                    print(f"   - No face detected or no match found")
            else:
                print(f"❌ Recognition failed: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_with_real_face():
    """Test với real face image"""
    print("\n🔍 Testing with Real Face Image...")
    
    try:
        # Sử dụng face image của "hoang"
        with open('uploads/face_20250731_222544.jpg', 'rb') as f:
            files = {'file': ('hoang_face.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/recognize', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Real Face Recognition Response:")
            print(json.dumps(data, indent=2))
            
            if data['success']:
                result = data['data']
                print(f"\n📊 Real Face Recognition Results:")
                print(f"   - Recognized: {result['recognized']}")
                print(f"   - Person Name: {result['person']['name']}")
                print(f"   - Person ID: {result['person']['id']}")
                print(f"   - Confidence: {result['confidence']:.2%}")
            else:
                print(f"❌ Recognition failed: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 Webcam Recognition Debug Test")
    print("=" * 50)
    
    # Test với real face trước
    test_with_real_face()
    
    # Test với webcam-like image
    test_webcam_recognition()
    
    print("\n✅ Webcam recognition test completed!")

if __name__ == "__main__":
    main() 
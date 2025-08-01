#!/usr/bin/env python3
"""
🧪 Test Bounding Box with Original Coordinates
Kiểm tra bounding box sử dụng original coordinates
"""

import requests
import json
from PIL import Image, ImageDraw
import io
import base64

def create_test_face_image():
    """Create a simple test image with a face-like shape"""
    # Create a 640x480 image
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face-like shape in the center
    center_x, center_y = 320, 240
    face_width, face_height = 200, 250
    
    # Face outline
    draw.ellipse([
        center_x - face_width//2, 
        center_y - face_height//2,
        center_x + face_width//2, 
        center_y + face_height//2
    ], outline='black', width=3)
    
    # Eyes
    eye_size = 20
    draw.ellipse([
        center_x - 60 - eye_size//2, 
        center_y - 30 - eye_size//2,
        center_x - 60 + eye_size//2, 
        center_y - 30 + eye_size//2
    ], fill='black')
    draw.ellipse([
        center_x + 60 - eye_size//2, 
        center_y - 30 - eye_size//2,
        center_x + 60 + eye_size//2, 
        center_y - 30 + eye_size//2
    ], fill='black')
    
    # Nose
    draw.rectangle([
        center_x - 5, center_y - 10,
        center_x + 5, center_y + 20
    ], fill='black')
    
    # Mouth
    draw.arc([
        center_x - 30, center_y + 20,
        center_x + 30, center_y + 60
    ], start=0, end=180, fill='black', width=3)
    
    return img

def test_bounding_box_api():
    """Test the bounding box API with original coordinates"""
    print("🧪 Testing Bounding Box with Original Coordinates")
    print("=" * 60)
    
    # Create test image
    print("📸 Creating test face image...")
    test_image = create_test_face_image()
    
    # Convert to bytes
    img_buffer = io.BytesIO()
    test_image.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    # Test API
    print("🔗 Testing /api/v1/faces/detect endpoint...")
    
    try:
        files = {'file': ('test_face.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response:")
            print(json.dumps(data, indent=2))
            
            if data.get('success') and data.get('data', {}).get('faces'):
                faces = data['data']['faces']
                print(f"\n📊 Found {len(faces)} face(s)")
                
                for i, face in enumerate(faces):
                    box = face.get('bounding_box', {})
                    print(f"\n🎯 Face {i+1}:")
                    print(f"   Original coordinates:")
                    print(f"   - Left: {box.get('left', 'N/A')}")
                    print(f"   - Top: {box.get('top', 'N/A')}")
                    print(f"   - Width: {box.get('width', 'N/A')}")
                    print(f"   - Height: {box.get('height', 'N/A')}")
                    print(f"   - Right: {box.get('right', 'N/A')}")
                    print(f"   - Bottom: {box.get('bottom', 'N/A')}")
                    print(f"   Confidence: {face.get('confidence', 'N/A'):.3f}")
                    print(f"   Quality: {face.get('quality_score', 'N/A'):.3f}")
                    
                    # Verify coordinates are reasonable
                    left = box.get('left', 0)
                    top = box.get('top', 0)
                    width = box.get('width', 0)
                    height = box.get('height', 0)
                    
                    if 0 <= left <= 640 and 0 <= top <= 480 and width > 0 and height > 0:
                        print("   ✅ Coordinates are within valid range")
                    else:
                        print("   ⚠️  Coordinates may be outside valid range")
                        
            else:
                print("❌ No faces detected in test image")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure backend is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_frontend_coordinates():
    """Test how frontend should handle original coordinates"""
    print("\n🌐 Frontend Coordinate Handling Test")
    print("=" * 60)
    
    # Simulate what the frontend receives
    sample_response = {
        "success": True,
        "message": "Detected 1 faces",
        "data": {
            "faces": [
                {
                    "bounding_box": {
                        "left": 220,
                        "top": 115,
                        "width": 200,
                        "height": 250,
                        "right": 420,
                        "bottom": 365
                    },
                    "confidence": 0.95,
                    "quality_score": 0.87
                }
            ],
            "total_faces": 1,
            "image_size": {"width": 640, "height": 480}
        }
    }
    
    print("📋 Sample API Response:")
    print(json.dumps(sample_response, indent=2))
    
    print("\n🎯 Frontend should use:")
    print("   - x = box.left (220)")
    print("   - y = box.top (115)")
    print("   - width = box.width (200)")
    print("   - height = box.height (250)")
    
    print("\n📐 Canvas drawing:")
    print("   ctx.strokeRect(220, 115, 200, 250)")
    
    print("\n✂️  Face cropping:")
    print("   ctx.drawImage(video, 220, 115, 200, 250, 0, 0, 200, 250)")

if __name__ == "__main__":
    print("🚀 Bounding Box Original Coordinates Test")
    print("=" * 60)
    
    # Test API
    test_bounding_box_api()
    
    # Test frontend handling
    test_frontend_coordinates()
    
    print("\n✅ Test completed!")
    print("\n💡 To test in browser:")
    print("   1. Open http://localhost:3000")
    print("   2. Go to 'Register Face' tab")
    print("   3. Click 'Use Webcam'")
    print("   4. Check console for debug logs")
    print("   5. Verify bounding box alignment") 
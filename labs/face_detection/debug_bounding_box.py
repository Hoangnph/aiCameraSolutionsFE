#!/usr/bin/env python3
"""
🔍 Debug Bounding Box Accuracy
Kiểm tra độ chính xác của bounding box với real images
"""

import requests
import json
import os
from PIL import Image, ImageDraw
import io

def test_with_uploaded_image():
    """Test với image đã upload"""
    print("🔍 Testing with uploaded image...")
    
    # Kiểm tra xem có file nào trong uploads không
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            test_file = os.path.join(uploads_dir, files[0])
            print(f"📷 Using uploaded image: {test_file}")
            
            try:
                with open(test_file, 'rb') as f:
                    files = {'file': (files[0], f, 'image/jpeg')}
                    response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Detection Response:")
                    print(json.dumps(data, indent=2))
                    
                    if data['success'] and data['data']['faces']:
                        faces = data['data']['faces']
                        print(f"\n📊 Bounding Box Analysis:")
                        for i, face in enumerate(faces):
                            box = face['bounding_box']
                            print(f"   - Face {i+1}:")
                            print(f"     * Box: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
                            print(f"     * Size: {box['width']} x {box['height']} pixels")
                            print(f"     * Image size: {data['data']['image_size']['width']} x {data['data']['image_size']['height']}")
                            print(f"     * Confidence: {face['confidence']:.2%}")
                            print(f"     * Quality: {face['quality_score']:.2%}")
                    else:
                        print("❌ No faces detected in uploaded image")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ No image files found in uploads directory")
    else:
        print("❌ Uploads directory not found")

def create_debug_image():
    """Tạo debug image với face rõ ràng hơn"""
    print("🎨 Creating debug image...")
    
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ face rõ ràng hơn
    # Head - lớn hơn
    draw.ellipse([150, 100, 490, 400], outline='black', width=5)
    
    # Eyes - rõ ràng hơn
    draw.ellipse([200, 180, 250, 230], fill='black')  # Left eye
    draw.ellipse([390, 180, 440, 230], fill='black')  # Right eye
    
    # Nose
    draw.line([320, 230, 320, 280], fill='black', width=5)
    
    # Mouth - rõ ràng hơn
    draw.arc([250, 280, 390, 330], 0, 180, fill='black', width=5)
    
    # Lưu image
    debug_file = "debug_face.jpg"
    img.save(debug_file)
    print(f"✅ Debug image saved: {debug_file}")
    
    return debug_file

def test_debug_image():
    """Test với debug image"""
    print("\n🔍 Testing with debug image...")
    
    debug_file = create_debug_image()
    
    try:
        with open(debug_file, 'rb') as f:
            files = {'file': ('debug_face.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Debug Detection Response:")
            print(json.dumps(data, indent=2))
            
            if data['success'] and data['data']['faces']:
                faces = data['data']['faces']
                print(f"\n📊 Debug Bounding Box Analysis:")
                for i, face in enumerate(faces):
                    box = face['bounding_box']
                    print(f"   - Face {i+1}:")
                    print(f"     * Box: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
                    print(f"     * Size: {box['width']} x {box['height']} pixels")
                    print(f"     * Image size: {data['data']['image_size']['width']} x {data['data']['image_size']['height']}")
                    print(f"     * Confidence: {face['confidence']:.2%}")
                    print(f"     * Quality: {face['quality_score']:.2%}")
                    
                    # Tính toán tỷ lệ
                    img_width = data['data']['image_size']['width']
                    img_height = data['data']['image_size']['height']
                    box_ratio = box['width'] / box['height']
                    img_ratio = img_width / img_height
                    
                    print(f"     * Box ratio: {box_ratio:.2f}")
                    print(f"     * Image ratio: {img_ratio:.2f}")
            else:
                print("❌ No faces detected in debug image")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 Debug Bounding Box Accuracy")
    print("=" * 50)
    
    # Test với uploaded image
    test_with_uploaded_image()
    
    # Test với debug image
    test_debug_image()
    
    print("\n✅ Bounding box debug completed!")

if __name__ == "__main__":
    main() 
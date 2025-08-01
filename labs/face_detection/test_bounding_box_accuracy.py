#!/usr/bin/env python3
"""
🎯 Test Bounding Box Accuracy
Kiểm tra độ chính xác của bounding box và đưa ra khuyến nghị
"""

import requests
import json
import os
from PIL import Image, ImageDraw
import io

def analyze_bounding_box(box, image_size):
    """Phân tích bounding box"""
    print(f"📊 Bounding Box Analysis:")
    print(f"   - Box coordinates: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
    print(f"   - Box size: {box['width']} x {box['height']} pixels")
    print(f"   - Image size: {image_size['width']} x {image_size['height']} pixels")
    
    # Tính toán tỷ lệ
    box_ratio = box['width'] / box['height']
    image_ratio = image_size['width'] / image_size['height']
    
    print(f"   - Box ratio: {box_ratio:.2f}")
    print(f"   - Image ratio: {image_ratio:.2f}")
    
    # Kiểm tra vị trí
    center_x = box['left'] + box['width'] / 2
    center_y = box['top'] + box['height'] / 2
    
    print(f"   - Box center: ({center_x:.1f}, {center_y:.1f})")
    print(f"   - Image center: ({image_size['width']/2:.1f}, {image_size['height']/2:.1f})")
    
    # Kiểm tra kích thước hợp lý
    box_area = box['width'] * box['height']
    image_area = image_size['width'] * image_size['height']
    coverage = box_area / image_area * 100
    
    print(f"   - Box coverage: {coverage:.1f}% of image")
    
    # Đánh giá
    if coverage < 5:
        print("   ⚠️  Box too small - might be inaccurate")
    elif coverage > 80:
        print("   ⚠️  Box too large - might include background")
    else:
        print("   ✅ Box size looks reasonable")
    
    if box_ratio < 0.5 or box_ratio > 2.0:
        print("   ⚠️  Box ratio unusual - might be distorted")
    else:
        print("   ✅ Box ratio looks reasonable")

def test_with_real_image():
    """Test với real image"""
    print("🔍 Testing with real uploaded image...")
    
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            test_file = os.path.join(uploads_dir, files[0])
            print(f"📷 Using: {test_file}")
            
            try:
                with open(test_file, 'rb') as f:
                    files = {'file': (files[0], f, 'image/jpeg')}
                    response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['success'] and data['data']['faces']:
                        faces = data['data']['faces']
                        image_size = data['data']['image_size']
                        
                        print(f"✅ Detected {len(faces)} faces")
                        
                        for i, face in enumerate(faces):
                            print(f"\n🎯 Face {i+1}:")
                            analyze_bounding_box(face['bounding_box'], image_size)
                            print(f"   - Confidence: {face['confidence']:.2%}")
                            print(f"   - Quality: {face['quality_score']:.2%}")
                    else:
                        print("❌ No faces detected")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ No image files found")
    else:
        print("❌ Uploads directory not found")

def create_ideal_face_image():
    """Tạo image với face lý tưởng"""
    print("\n🎨 Creating ideal face image...")
    
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ face với tỷ lệ chuẩn (1:1.2)
    face_width = 200
    face_height = 240
    face_x = (640 - face_width) // 2
    face_y = (480 - face_height) // 2
    
    # Head
    draw.ellipse([face_x, face_y, face_x + face_width, face_y + face_height], outline='black', width=3)
    
    # Eyes
    eye_y = face_y + face_height * 0.3
    left_eye_x = face_x + face_width * 0.25
    right_eye_x = face_x + face_width * 0.75
    eye_size = 20
    
    draw.ellipse([left_eye_x - eye_size//2, eye_y - eye_size//2, left_eye_x + eye_size//2, eye_y + eye_size//2], fill='black')
    draw.ellipse([right_eye_x - eye_size//2, eye_y - eye_size//2, right_eye_x + eye_size//2, eye_y + eye_size//2], fill='black')
    
    # Nose
    nose_x = face_x + face_width // 2
    nose_y = eye_y + eye_size
    draw.line([nose_x, nose_y, nose_x, nose_y + 30], fill='black', width=3)
    
    # Mouth
    mouth_y = nose_y + 40
    mouth_width = 60
    draw.arc([nose_x - mouth_width//2, mouth_y, nose_x + mouth_width//2, mouth_y + 30], 0, 180, fill='black', width=3)
    
    # Lưu image
    ideal_file = "ideal_face.jpg"
    img.save(ideal_file)
    print(f"✅ Ideal face image saved: {ideal_file}")
    
    return ideal_file

def test_ideal_face():
    """Test với ideal face"""
    print("\n🔍 Testing with ideal face image...")
    
    ideal_file = create_ideal_face_image()
    
    try:
        with open(ideal_file, 'rb') as f:
            files = {'file': ('ideal_face.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success'] and data['data']['faces']:
                faces = data['data']['faces']
                image_size = data['data']['image_size']
                
                print(f"✅ Detected {len(faces)} faces in ideal image")
                
                for i, face in enumerate(faces):
                    print(f"\n🎯 Ideal Face {i+1}:")
                    analyze_bounding_box(face['bounding_box'], image_size)
                    print(f"   - Confidence: {face['confidence']:.2%}")
                    print(f"   - Quality: {face['quality_score']:.2%}")
            else:
                print("❌ No faces detected in ideal image")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 Bounding Box Accuracy Test")
    print("=" * 50)
    
    # Test với real image
    test_with_real_image()
    
    # Test với ideal face
    test_ideal_face()
    
    print("\n📋 Frontend Recommendations:")
    print("1. ✅ Line width reduced to 1px")
    print("2. ✅ Added corner indicators for better visibility")
    print("3. ✅ Smaller font size (12px)")
    print("4. ✅ Better text positioning")
    print("5. ✅ Debug logging added")
    print("6. ✅ Improved crop accuracy")
    
    print("\n✅ Bounding box accuracy test completed!")

if __name__ == "__main__":
    main() 
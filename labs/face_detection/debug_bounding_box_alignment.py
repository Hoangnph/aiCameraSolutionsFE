#!/usr/bin/env python3
"""
🎯 Debug Bounding Box Alignment
Kiểm tra vấn đề bounding box bị lệch so với face
"""

import requests
import json
import os
from PIL import Image, ImageDraw
import io

def analyze_bounding_box_alignment(box, image_size):
    """Phân tích alignment của bounding box"""
    print(f"📊 Bounding Box Alignment Analysis:")
    print(f"   - Box coordinates: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
    print(f"   - Box size: {box['width']} x {box['height']} pixels")
    print(f"   - Image size: {image_size['width']} x {image_size['height']} pixels")
    
    # Tính toán center points
    box_center_x = box['left'] + box['width'] / 2
    box_center_y = box['top'] + box['height'] / 2
    image_center_x = image_size['width'] / 2
    image_center_y = image_size['height'] / 2
    
    print(f"   - Box center: ({box_center_x:.1f}, {box_center_y:.1f})")
    print(f"   - Image center: ({image_center_x:.1f}, {image_center_y:.1f})")
    
    # Tính toán offset
    offset_x = box_center_x - image_center_x
    offset_y = box_center_y - image_center_y
    
    print(f"   - Offset from center: ({offset_x:.1f}, {offset_y:.1f})")
    
    # Kiểm tra vị trí hợp lý
    if abs(offset_x) > image_size['width'] * 0.3:
        print(f"   ⚠️  Box too far from center horizontally: {abs(offset_x):.1f}px")
    else:
        print(f"   ✅ Horizontal position reasonable")
        
    if abs(offset_y) > image_size['height'] * 0.3:
        print(f"   ⚠️  Box too far from center vertically: {abs(offset_y):.1f}px")
    else:
        print(f"   ✅ Vertical position reasonable")
    
    # Kiểm tra kích thước
    box_area = box['width'] * box['height']
    image_area = image_size['width'] * image_size['height']
    coverage = box_area / image_area * 100
    
    print(f"   - Box coverage: {coverage:.1f}% of image")
    
    if coverage < 5:
        print("   ⚠️  Box too small - might be inaccurate")
    elif coverage > 80:
        print("   ⚠️  Box too large - might include background")
    else:
        print("   ✅ Box size looks reasonable")

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
                            print(f"\n🎯 Face {i+1} Alignment:")
                            analyze_bounding_box_alignment(face['bounding_box'], image_size)
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

def create_test_image_with_face():
    """Tạo test image với face ở center"""
    print("\n🎨 Creating test image with centered face...")
    
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ face ở center
    face_width = 200
    face_height = 240
    face_x = (640 - face_width) // 2  # Center horizontally
    face_y = (480 - face_height) // 2  # Center vertically
    
    print(f"   - Face position: ({face_x}, {face_y}) to ({face_x + face_width}, {face_y + face_height})")
    print(f"   - Face center: ({face_x + face_width//2}, {face_y + face_height//2})")
    print(f"   - Image center: (320, 240)")
    
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
    test_file = "test_centered_face.jpg"
    img.save(test_file)
    print(f"✅ Test image saved: {test_file}")
    
    return test_file

def test_centered_face():
    """Test với centered face"""
    print("\n🔍 Testing with centered face image...")
    
    test_file = create_test_image_with_face()
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': ('test_centered_face.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success'] and data['data']['faces']:
                faces = data['data']['faces']
                image_size = data['data']['image_size']
                
                print(f"✅ Detected {len(faces)} faces in centered image")
                
                for i, face in enumerate(faces):
                    print(f"\n🎯 Centered Face {i+1} Alignment:")
                    analyze_bounding_box_alignment(face['bounding_box'], image_size)
                    print(f"   - Confidence: {face['confidence']:.2%}")
                    print(f"   - Quality: {face['quality_score']:.2%}")
            else:
                print("❌ No faces detected in centered image")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_frontend_scaling():
    """Phân tích frontend scaling issues"""
    print("\n🔧 Frontend Scaling Analysis:")
    print("   - Video dimensions vs Canvas dimensions")
    print("   - Scaling factors calculation")
    print("   - Coordinate transformation")
    
    print("\n📋 Potential Issues:")
    print("   1. Video.videoWidth vs Video.offsetWidth mismatch")
    print("   2. Canvas scaling not matching video display")
    print("   3. Coordinate system differences")
    print("   4. Browser zoom affecting calculations")
    
    print("\n🔧 Recommended Fixes:")
    print("   1. Use video.videoWidth/video.videoHeight for scaling")
    print("   2. Ensure canvas size matches video display size")
    print("   3. Add debug logging for coordinate calculations")
    print("   4. Test with different browser zoom levels")

def main():
    """Main function"""
    print("🚀 Debug Bounding Box Alignment")
    print("=" * 50)
    
    # Test với real image
    test_with_real_image()
    
    # Test với centered face
    test_centered_face()
    
    # Phân tích frontend scaling
    analyze_frontend_scaling()
    
    print("\n📋 Frontend Debug Steps:")
    print("1. Open browser console (F12)")
    print("2. Go to Register New Face tab")
    print("3. Start webcam")
    print("4. Check console logs for coordinate data")
    print("5. Compare video.videoWidth vs video.offsetWidth")
    print("6. Verify canvas scaling calculations")
    
    print("\n✅ Bounding box alignment debug completed!")

if __name__ == "__main__":
    main() 
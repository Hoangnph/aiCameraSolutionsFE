#!/usr/bin/env python3
"""
🎯 Test Frontend Bounding Box Alignment
Kiểm tra alignment của bounding box trên frontend
"""

import requests
import json
import os
from PIL import Image, ImageDraw
import io

def create_test_image_with_known_face():
    """Tạo test image với face ở vị trí biết trước"""
    print("🎨 Creating test image with known face position...")
    
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ face ở vị trí cụ thể (giống như real image)
    face_left = 349
    face_top = 82
    face_width = 268
    face_height = 268
    
    print(f"   - Expected face position: ({face_left}, {face_top}) to ({face_left + face_width}, {face_top + face_height})")
    print(f"   - Expected face center: ({face_left + face_width//2}, {face_top + face_height//2})")
    
    # Head
    draw.ellipse([face_left, face_top, face_left + face_width, face_top + face_height], outline='black', width=3)
    
    # Eyes
    eye_y = face_top + face_height * 0.3
    left_eye_x = face_left + face_width * 0.25
    right_eye_x = face_left + face_width * 0.75
    eye_size = 20
    
    draw.ellipse([left_eye_x - eye_size//2, eye_y - eye_size//2, left_eye_x + eye_size//2, eye_y + eye_size//2], fill='black')
    draw.ellipse([right_eye_x - eye_size//2, eye_y - eye_size//2, right_eye_x + eye_size//2, eye_y + eye_size//2], fill='black')
    
    # Nose
    nose_x = face_left + face_width // 2
    nose_y = eye_y + eye_size
    draw.line([nose_x, nose_y, nose_x, nose_y + 30], fill='black', width=3)
    
    # Mouth
    mouth_y = nose_y + 40
    mouth_width = 60
    draw.arc([nose_x - mouth_width//2, mouth_y, nose_x + mouth_width//2, mouth_y + 30], 0, 180, fill='black', width=3)
    
    # Lưu image
    test_file = "test_known_face.jpg"
    img.save(test_file)
    print(f"✅ Test image saved: {test_file}")
    
    return test_file

def test_known_face_position():
    """Test với face ở vị trí biết trước"""
    print("\n🔍 Testing with known face position...")
    
    test_file = create_test_image_with_known_face()
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': ('test_known_face.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success'] and data['data']['faces']:
                faces = data['data']['faces']
                image_size = data['data']['image_size']
                
                print(f"✅ Detected {len(faces)} faces")
                
                for i, face in enumerate(faces):
                    box = face['bounding_box']
                    print(f"\n🎯 Detected Face {i+1}:")
                    print(f"   - Box: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
                    print(f"   - Expected: (349, 82) to (617, 350)")
                    
                    # Kiểm tra độ chính xác
                    left_diff = abs(box['left'] - 349)
                    top_diff = abs(box['top'] - 82)
                    width_diff = abs(box['width'] - 268)
                    height_diff = abs(box['height'] - 268)
                    
                    print(f"   - Left difference: {left_diff}px")
                    print(f"   - Top difference: {top_diff}px")
                    print(f"   - Width difference: {width_diff}px")
                    print(f"   - Height difference: {height_diff}px")
                    
                    if left_diff < 10 and top_diff < 10 and width_diff < 10 and height_diff < 10:
                        print("   ✅ Bounding box position is accurate")
                    else:
                        print("   ⚠️  Bounding box position has significant deviation")
                        
                    print(f"   - Confidence: {face['confidence']:.2%}")
                    print(f"   - Quality: {face['quality_score']:.2%}")
            else:
                print("❌ No faces detected")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_scaling_issues():
    """Phân tích scaling issues"""
    print("\n🔧 Scaling Issues Analysis:")
    print("   - Video.videoWidth vs Video.offsetWidth")
    print("   - Canvas scaling vs Video display")
    print("   - Coordinate transformation")
    
    print("\n📋 Common Issues:")
    print("   1. Video.videoWidth ≠ Video.offsetWidth (browser scaling)")
    print("   2. Canvas size ≠ Video display size")
    print("   3. Incorrect scaling factors")
    print("   4. Browser zoom affecting calculations")
    
    print("\n🔧 Frontend Fixes Applied:")
    print("   1. ✅ Use video.offsetWidth/offsetHeight for display scaling")
    print("   2. ✅ Use video.videoWidth/videoHeight for crop scaling")
    print("   3. ✅ Added debug logging for coordinate calculations")
    print("   4. ✅ Improved scaling factor calculations")

def test_frontend_accessibility():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend Accessibility:")
    
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible at http://localhost:3000")
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")

def main():
    """Main function"""
    print("🚀 Test Frontend Bounding Box Alignment")
    print("=" * 50)
    
    # Test với known face position
    test_known_face_position()
    
    # Phân tích scaling issues
    analyze_scaling_issues()
    
    # Test frontend accessibility
    test_frontend_accessibility()
    
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Go to Register New Face tab")
    print("3. Start webcam")
    print("4. Open browser console (F12)")
    print("5. Look for debug logs:")
    print("   - 'Face detection:' - coordinate data")
    print("   - 'Scaling factors:' - scaling calculations")
    print("   - 'Scaled coordinates:' - final positions")
    print("6. Verify bounding box aligns with face")
    print("7. Test capture functionality")
    
    print("\n🔧 Expected Debug Output:")
    print("   - videoSize: { width: 640, height: 480 }")
    print("   - videoDisplay: { width: 640, height: 480 } (or different if scaled)")
    print("   - canvasSize: { width: 640, height: 480 }")
    print("   - box: { left: 349, top: 82, width: 268, height: 268 }")
    print("   - Scaling factors: { scaleX: 1.0, scaleY: 1.0 } (or different)")
    print("   - Scaled coordinates: { x: 349, y: 82, width: 268, height: 268 }")
    
    print("\n✅ Frontend alignment test completed!")

if __name__ == "__main__":
    main() 
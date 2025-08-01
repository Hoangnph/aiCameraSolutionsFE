#!/usr/bin/env python3
"""
🔍 Comprehensive Bounding Box Analysis
Phân tích kỹ vấn đề bounding box và tỷ lệ khung hình
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import numpy as np
import cv2

def create_test_image_with_face():
    """Create a test image with a clear face for analysis"""
    # Create a 640x480 image (standard webcam resolution)
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw a more realistic face-like structure
    center_x, center_y = 320, 240
    
    # Face outline (oval)
    face_width, face_height = 180, 220
    draw.ellipse([
        center_x - face_width//2, 
        center_y - face_height//2,
        center_x + face_width//2, 
        center_y + face_height//2
    ], outline='black', width=3, fill='peachpuff')
    
    # Hair
    draw.ellipse([
        center_x - face_width//2 - 10, 
        center_y - face_height//2 - 30,
        center_x + face_width//2 + 10, 
        center_y - face_height//2 + 10
    ], fill='brown')
    
    # Eyes
    eye_size = 25
    draw.ellipse([
        center_x - 50 - eye_size//2, 
        center_y - 20 - eye_size//2,
        center_x - 50 + eye_size//2, 
        center_y - 20 + eye_size//2
    ], fill='white')
    draw.ellipse([
        center_x - 50 - 8, 
        center_y - 20 - 8,
        center_x - 50 + 8, 
        center_y - 20 + 8
    ], fill='black')
    
    draw.ellipse([
        center_x + 50 - eye_size//2, 
        center_y - 20 - eye_size//2,
        center_x + 50 + eye_size//2, 
        center_y - 20 + eye_size//2
    ], fill='white')
    draw.ellipse([
        center_x + 50 - 8, 
        center_y - 20 - 8,
        center_x + 50 + 8, 
        center_y - 20 + 8
    ], fill='black')
    
    # Nose
    draw.polygon([
        (center_x, center_y - 10),
        (center_x - 8, center_y + 15),
        (center_x + 8, center_y + 15)
    ], fill='peachpuff', outline='black')
    
    # Mouth
    draw.arc([
        center_x - 25, center_y + 20,
        center_x + 25, center_y + 50
    ], start=0, end=180, fill='red', width=3)
    
    # Add some text for reference
    draw.text((10, 10), "Test Face Image", fill='black')
    draw.text((10, 30), "640x480 pixels", fill='black')
    draw.text((10, 50), "Center: (320, 240)", fill='black')
    
    return img

def analyze_api_response(response_data):
    """Analyze the API response for bounding box data"""
    print("🔍 API Response Analysis:")
    print("=" * 50)
    
    if response_data.get('success'):
        faces = response_data.get('data', {}).get('faces', [])
        image_size = response_data.get('data', {}).get('image_size', {})
        
        print(f"📊 Image Size: {image_size.get('width', 'N/A')} x {image_size.get('height', 'N/A')}")
        print(f"👥 Detected Faces: {len(faces)}")
        
        for i, face in enumerate(faces):
            box = face.get('bounding_box', {})
            print(f"\n🎯 Face {i+1} Analysis:")
            print(f"   Original Coordinates:")
            print(f"   - Left: {box.get('left', 'N/A')}")
            print(f"   - Top: {box.get('top', 'N/A')}")
            print(f"   - Width: {box.get('width', 'N/A')}")
            print(f"   - Height: {box.get('height', 'N/A')}")
            print(f"   - Right: {box.get('right', 'N/A')}")
            print(f"   - Bottom: {box.get('bottom', 'N/A')}")
            print(f"   Confidence: {face.get('confidence', 'N/A'):.3f}")
            print(f"   Quality: {face.get('quality_score', 'N/A'):.3f}")
            
            # Calculate center point
            left = box.get('left', 0)
            top = box.get('top', 0)
            width = box.get('width', 0)
            height = box.get('height', 0)
            center_x = left + width // 2
            center_y = top + height // 2
            
            print(f"   Calculated Center: ({center_x}, {center_y})")
            
            # Check if coordinates are reasonable
            img_width = image_size.get('width', 640)
            img_height = image_size.get('height', 480)
            
            if (0 <= left <= img_width and 0 <= top <= img_height and 
                width > 0 and height > 0 and 
                left + width <= img_width and top + height <= img_height):
                print("   ✅ Coordinates are within valid range")
            else:
                print("   ⚠️  Coordinates may be outside valid range")
                
    else:
        print("❌ API returned error or no faces detected")

def test_different_resolutions():
    """Test with different image resolutions"""
    print("\n📐 Testing Different Resolutions:")
    print("=" * 50)
    
    resolutions = [
        (320, 240),   # Low resolution
        (640, 480),   # Standard webcam
        (1280, 720),  # HD
        (1920, 1080), # Full HD
    ]
    
    for width, height in resolutions:
        print(f"\n🔍 Testing {width}x{height}:")
        
        # Create test image with this resolution
        img = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple face in the center
        center_x, center_y = width // 2, height // 2
        face_size = min(width, height) // 4
        
        # Face circle
        draw.ellipse([
            center_x - face_size, center_y - face_size,
            center_x + face_size, center_y + face_size
        ], fill='peachpuff', outline='black', width=2)
        
        # Eyes
        eye_size = face_size // 4
        draw.ellipse([
            center_x - face_size//2 - eye_size, center_y - eye_size,
            center_x - face_size//2 + eye_size, center_y + eye_size
        ], fill='black')
        draw.ellipse([
            center_x + face_size//2 - eye_size, center_y - eye_size,
            center_x + face_size//2 + eye_size, center_y + eye_size
        ], fill='black')
        
        # Test API
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        try:
            files = {'file': (f'test_{width}x{height}.jpg', img_buffer, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
            
            if response.status_code == 200:
                data = response.json()
                faces = data.get('data', {}).get('faces', [])
                print(f"   ✅ API Response: {len(faces)} face(s) detected")
                
                for face in faces:
                    box = face.get('bounding_box', {})
                    print(f"   📦 Box: ({box.get('left', 0)}, {box.get('top', 0)}) "
                          f"{box.get('width', 0)}x{box.get('height', 0)}")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def analyze_frontend_coordinate_system():
    """Analyze frontend coordinate system issues"""
    print("\n🌐 Frontend Coordinate System Analysis:")
    print("=" * 50)
    
    print("📋 Common Issues:")
    print("1. Video element vs Canvas size mismatch")
    print("2. Browser zoom affecting getBoundingClientRect()")
    print("3. CSS transforms scaling video")
    print("4. Device pixel ratio differences")
    print("5. Video aspect ratio vs display aspect ratio")
    
    print("\n🔧 Recommended Solutions:")
    print("1. Ensure canvas.width = video.videoWidth")
    print("2. Ensure canvas.height = video.videoHeight")
    print("3. Use video.videoWidth/video.videoHeight for scaling")
    print("4. Account for device pixel ratio")
    print("5. Handle browser zoom properly")
    
    print("\n📐 Coordinate System Rules:")
    print("- API returns coordinates in video pixel space")
    print("- Canvas should match video dimensions exactly")
    print("- No browser display scaling should be applied")
    print("- Coordinates are absolute pixels, not relative")

def create_coordinate_test_image():
    """Create an image with coordinate markers for testing"""
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw coordinate grid
    for x in range(0, 641, 50):
        draw.line([(x, 0), (x, 480)], fill='lightgray')
        draw.text((x, 10), str(x), fill='black')
    
    for y in range(0, 481, 50):
        draw.line([(0, y), (640, y)], fill='lightgray')
        draw.text((10, y), str(y), fill='black')
    
    # Draw a face in the center
    center_x, center_y = 320, 240
    face_size = 100
    
    # Face outline
    draw.ellipse([
        center_x - face_size, center_y - face_size,
        center_x + face_size, center_y + face_size
    ], outline='red', width=3)
    
    # Mark center
    draw.ellipse([center_x-5, center_y-5, center_x+5, center_y+5], fill='red')
    draw.text((center_x+10, center_y-10), f"({center_x},{center_y})", fill='red')
    
    # Expected bounding box
    expected_left = center_x - face_size
    expected_top = center_y - face_size
    expected_width = face_size * 2
    expected_height = face_size * 2
    
    draw.rectangle([
        expected_left, expected_top,
        expected_left + expected_width, expected_top + expected_height
    ], outline='green', width=2)
    
    draw.text((10, 450), f"Expected: ({expected_left},{expected_top}) {expected_width}x{expected_height}", fill='green')
    
    return img

def test_coordinate_accuracy():
    """Test coordinate accuracy with marked image"""
    print("\n🎯 Testing Coordinate Accuracy:")
    print("=" * 50)
    
    # Create test image with coordinate markers
    test_img = create_coordinate_test_image()
    
    # Save for reference
    test_img.save('coordinate_test_image.jpg')
    print("📸 Saved coordinate test image as 'coordinate_test_image.jpg'")
    
    # Test API
    img_buffer = io.BytesIO()
    test_img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    try:
        files = {'file': ('coordinate_test.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response received")
            analyze_api_response(data)
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Comprehensive Bounding Box Analysis")
    print("=" * 60)
    
    # Test 1: Basic API functionality
    print("\n1️⃣ Testing Basic API Functionality")
    test_img = create_test_image_with_face()
    
    img_buffer = io.BytesIO()
    test_img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    try:
        files = {'file': ('test_face.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            analyze_api_response(data)
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Different resolutions
    test_different_resolutions()
    
    # Test 3: Coordinate accuracy
    test_coordinate_accuracy()
    
    # Test 4: Analysis
    analyze_frontend_coordinate_system()
    
    print("\n✅ Analysis completed!")
    print("\n💡 Next steps:")
    print("1. Check the generated 'coordinate_test_image.jpg'")
    print("2. Compare API coordinates with expected values")
    print("3. Verify frontend canvas setup matches video dimensions")
    print("4. Test with real webcam feed") 
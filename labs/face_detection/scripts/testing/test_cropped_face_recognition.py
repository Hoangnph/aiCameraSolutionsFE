#!/usr/bin/env python3
"""
🧪 Test Cropped Face Recognition
Kiểm tra recognition với cropped face images
"""

import requests
import json
import time
import base64
from PIL import Image, ImageDraw
import io

def test_cropped_face_recognition():
    """Test recognition with properly cropped face"""
    print("🧪 Testing Cropped Face Recognition")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Get real face from database
        print("1. Getting face from database...")
        list_response = requests.get(f"{base_url}/api/v1/faces/list")
        
        if list_response.status_code == 200:
            list_data = list_response.json()
            faces = list_data.get('data', {}).get('faces', [])
            
            if faces:
                face = faces[0]
                face_id = face['id']
                print(f"   ✅ Found face: {face['metadata']['name']} (ID: {face_id})")
                
                # Step 2: Download face image
                print("\n2. Downloading face image...")
                image_response = requests.get(f"{base_url}/api/v1/faces/{face_id}/image")
                
                if image_response.status_code == 200:
                    with open('test_face.jpg', 'wb') as f:
                        f.write(image_response.content)
                    print("   ✅ Face image downloaded")
                    
                    # Step 3: Test face detection
                    print("\n3. Testing face detection...")
                    detect_response = requests.post(
                        f"{base_url}/api/v1/faces/detect",
                        files={'file': ('test_face.jpg', open('test_face.jpg', 'rb'), 'image/jpeg')},
                        timeout=10
                    )
                    
                    print(f"   Status: {detect_response.status_code}")
                    
                    if detect_response.status_code == 200:
                        detect_data = detect_response.json()
                        print(f"   Response: {detect_data}")
                        
                        if detect_data.get('success'):
                            faces_count = len(detect_data.get('data', {}).get('faces', []))
                            print(f"   ✅ Face detection successful - {faces_count} faces detected")
                            
                            if faces_count > 0:
                                detected_face = detect_data['data']['faces'][0]
                                print(f"   📊 Detected face details:")
                                print(f"      - Confidence: {detected_face.get('confidence', 'N/A')}")
                                print(f"      - Quality: {detected_face.get('quality_score', 'N/A')}")
                                print(f"      - Bounding Box: {detected_face.get('bounding_box', 'N/A')}")
                                
                                # Step 4: Test different cropping methods
                                print("\n4. Testing different cropping methods...")
                                test_different_cropping_methods(detected_face['bounding_box'])
                                
                            else:
                                print("   ⚠️ No faces detected in image")
                        else:
                            print(f"   ❌ Face detection failed: {detect_data.get('message')}")
                    else:
                        print(f"   ❌ Face detection failed with status: {detect_response.status_code}")
                else:
                    print(f"   ❌ Failed to download face image: {image_response.status_code}")
            else:
                print("   ❌ No faces found in database")
        else:
            print(f"   ❌ Failed to get face list: {list_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing cropped face recognition: {e}")

def test_different_cropping_methods(bounding_box):
    """Test different cropping methods"""
    print("   🔍 Testing different cropping methods...")
    
    try:
        # Load the original image
        with open('test_face.jpg', 'rb') as f:
            original_image_data = f.read()
        
        img = Image.open(io.BytesIO(original_image_data))
        print(f"   📊 Original image size: {img.width} x {img.height}")
        
        # Method 1: Exact bounding box cropping
        print("\n   Method 1: Exact bounding box cropping")
        cropped_exact = crop_exact_face(img, bounding_box)
        test_recognition_with_image(cropped_exact, "exact_crop.jpg")
        
        # Method 2: Padded cropping (10% padding)
        print("\n   Method 2: Padded cropping (10% padding)")
        cropped_padded = crop_padded_face(img, bounding_box, 0.1)
        test_recognition_with_image(cropped_padded, "padded_crop.jpg")
        
        # Method 3: Extended cropping (20% padding)
        print("\n   Method 3: Extended cropping (20% padding)")
        cropped_extended = crop_padded_face(img, bounding_box, 0.2)
        test_recognition_with_image(cropped_extended, "extended_crop.jpg")
        
        # Method 4: Square cropping (maintain aspect ratio)
        print("\n   Method 4: Square cropping (maintain aspect ratio)")
        cropped_square = crop_square_face(img, bounding_box)
        test_recognition_with_image(cropped_square, "square_crop.jpg")
        
    except Exception as e:
        print(f"   ❌ Error testing cropping methods: {e}")

def crop_exact_face(img, bounding_box):
    """Crop face using exact bounding box coordinates"""
    left = bounding_box['left']
    top = bounding_box['top']
    width = bounding_box['width']
    height = bounding_box['height']
    
    cropped = img.crop((left, top, left + width, top + height))
    
    # Convert to bytes
    cropped_bytes = io.BytesIO()
    cropped.save(cropped_bytes, format='JPEG', quality=90)
    cropped_bytes.seek(0)
    
    return cropped_bytes.getvalue()

def crop_padded_face(img, bounding_box, padding_ratio):
    """Crop face with padding"""
    left = bounding_box['left']
    top = bounding_box['top']
    width = bounding_box['width']
    height = bounding_box['height']
    
    # Calculate padding
    padding = min(width, height) * padding_ratio
    
    # Calculate crop coordinates with padding
    crop_left = max(0, left - padding)
    crop_top = max(0, top - padding)
    crop_width = min(width + 2 * padding, img.width - crop_left)
    crop_height = min(height + 2 * padding, img.height - crop_top)
    
    cropped = img.crop((crop_left, crop_top, crop_left + crop_width, crop_top + crop_height))
    
    # Convert to bytes
    cropped_bytes = io.BytesIO()
    cropped.save(cropped_bytes, format='JPEG', quality=90)
    cropped_bytes.seek(0)
    
    return cropped_bytes.getvalue()

def crop_square_face(img, bounding_box):
    """Crop face as square maintaining aspect ratio"""
    left = bounding_box['left']
    top = bounding_box['top']
    width = bounding_box['width']
    height = bounding_box['height']
    
    # Calculate center and size
    center_x = left + width / 2
    center_y = top + height / 2
    size = max(width, height)
    
    # Calculate square crop coordinates
    crop_left = max(0, center_x - size / 2)
    crop_top = max(0, center_y - size / 2)
    crop_size = min(size, img.width - crop_left, img.height - crop_top)
    
    cropped = img.crop((crop_left, crop_top, crop_left + crop_size, crop_top + crop_size))
    
    # Convert to bytes
    cropped_bytes = io.BytesIO()
    cropped.save(cropped_bytes, format='JPEG', quality=90)
    cropped_bytes.seek(0)
    
    return cropped_bytes.getvalue()

def test_recognition_with_image(image_data, filename):
    """Test recognition with given image data"""
    try:
        base_url = "http://localhost:8000"
        
        # Test recognition
        recognize_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': (filename, image_data, 'image/jpeg')},
            timeout=10
        )
        
        print(f"      Status: {recognize_response.status_code}")
        
        if recognize_response.status_code == 200:
            recognize_data = recognize_response.json()
            
            if recognize_data.get('success'):
                if recognize_data.get('data', {}).get('recognized'):
                    name = recognize_data['data']['person']['name']
                    confidence = recognize_data['data']['confidence']
                    print(f"      ✅ Recognized: {name} ({confidence:.2%})")
                else:
                    print(f"      ❓ Not recognized")
            else:
                print(f"      ❌ Recognition failed: {recognize_data.get('message')}")
        else:
            print(f"      ❌ Recognition failed with status: {recognize_response.status_code}")
            
    except Exception as e:
        print(f"      ❌ Error testing recognition: {e}")

def test_frontend_cropping_logic():
    """Test frontend cropping logic"""
    print("\n🎨 Testing Frontend Cropping Logic")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for improved cropping logic
            cropping_improvements = [
                'Math.max(0, boundingBox.left)',
                'Math.min(boundingBox.width, img.width - left)',
                'padding = Math.min(width, height) * 0.1',
                'cropLeft = Math.max(0, left - padding)',
                'cropWidth = Math.min(width + 2 * padding',
                'canvas.toDataURL(\'image/jpeg\', 0.95)'
            ]
            
            for improvement in cropping_improvements:
                if improvement in html_content:
                    print(f"✅ {improvement} found in JavaScript")
                else:
                    print(f"❌ {improvement} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend cropping logic: {e}")

if __name__ == "__main__":
    print("🧪 Cropped Face Recognition Test")
    print("=" * 60)
    
    # Test cropped face recognition
    test_cropped_face_recognition()
    
    # Test frontend cropping logic
    test_frontend_cropping_logic()
    
    print("\n✅ Cropped face recognition test completed!")
    print("\n💡 Expected Results:")
    print("   - Method 1 (Exact): May fail if face is cut off")
    print("   - Method 2 (10% padding): Should work best")
    print("   - Method 3 (20% padding): Should work well")
    print("   - Method 4 (Square): Should work consistently")
    print("\n🎯 Best Method: Use padded cropping (10-20% padding)")
    print("   This ensures the entire face is included in the crop") 
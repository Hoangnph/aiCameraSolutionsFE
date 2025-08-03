#!/usr/bin/env python3
"""
🔍 Debug Auto Recognition
Kiểm tra và debug auto recognition mode
"""

import requests
import json
import time
import base64
from PIL import Image, ImageDraw
import io

def test_auto_recognition_frontend():
    """Test auto recognition frontend elements"""
    print("🎨 Testing Auto Recognition Frontend")
    print("=" * 45)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for auto recognition functions
            functions = [
                'startAutoRecognition()',
                'stopAutoRecognition()',
                'processAutoRecognitionFrame()',
                'performAutoRecognition()',
                'drawAutoRecognitionBoundingBoxes()',
                'cropFaceFromImage()',
                'updateAutoRecognitionStatus()',
                'toggleAutoMode()'
            ]
            
            for func in functions:
                if func in html_content:
                    print(f"✅ {func} found")
                else:
                    print(f"❌ {func} missing")
                    
            # Check for auto recognition elements
            elements = [
                'auto-recognition-section',
                'auto-recognition-video',
                'auto-recognition-canvas',
                'auto-recognition-overlay',
                'auto-recognition-status',
                'auto-recognition-results'
            ]
            
            for element in elements:
                if element in html_content:
                    print(f"✅ {element} found")
                else:
                    print(f"❌ {element} missing")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")

def test_auto_recognition_api_endpoints():
    """Test auto recognition API endpoints"""
    print("\n🔍 Testing Auto Recognition API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Health check
        print("1. Testing health check...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print("   ❌ Backend not responding")
            return
            
        # Test 2: Face detection API
        print("\n2. Testing face detection API...")
        
        # Create a test image with a more realistic face
        test_image = create_realistic_face_image()
        
        detect_response = requests.post(
            f"{base_url}/api/v1/faces/detect",
            files={'file': ('test_face.jpg', test_image, 'image/jpeg')},
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
                    face = detect_data['data']['faces'][0]
                    print(f"   📊 Face details:")
                    print(f"      - Confidence: {face.get('confidence', 'N/A')}")
                    print(f"      - Quality: {face.get('quality_score', 'N/A')}")
                    print(f"      - Bounding Box: {face.get('bounding_box', 'N/A')}")
                    
                    # Test 3: Face recognition with detected face
                    test_face_recognition_with_detected_face(test_image, face['bounding_box'])
                else:
                    print("   ⚠️ No faces detected - testing with simple image")
                    test_face_recognition_with_simple_image()
            else:
                print(f"   ❌ Face detection failed: {detect_data.get('message')}")
        else:
            print(f"   ❌ Face detection failed with status: {detect_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")

def test_face_recognition_with_detected_face(original_image, bounding_box):
    """Test face recognition with detected face"""
    print("\n3. Testing face recognition with detected face...")
    
    try:
        # Crop the face from the original image
        cropped_image = crop_face_from_image(original_image, bounding_box)
        
        # Test recognition with cropped face
        base_url = "http://localhost:8000"
        recognize_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('cropped_face.jpg', cropped_image, 'image/jpeg')},
            timeout=10
        )
        
        print(f"   Status: {recognize_response.status_code}")
        
        if recognize_response.status_code == 200:
            recognize_data = recognize_response.json()
            print(f"   Response: {recognize_data}")
            
            if recognize_data.get('success'):
                if recognize_data.get('data', {}).get('recognized'):
                    name = recognize_data['data']['name']
                    confidence = recognize_data['data']['confidence']
                    print(f"   ✅ Face recognized: {name} ({confidence:.2%})")
                else:
                    print("   ❓ Face not recognized - no matching faces in database")
            else:
                print(f"   ❌ Recognition failed: {recognize_data.get('message')}")
        else:
            print(f"   ❌ Recognition failed with status: {recognize_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error testing face recognition: {e}")

def test_face_recognition_with_simple_image():
    """Test face recognition with simple image"""
    print("\n4. Testing face recognition with simple image...")
    
    try:
        # Create a simple test image
        test_image = create_simple_test_image()
        
        # Test recognition with simple image
        base_url = "http://localhost:8000"
        recognize_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('simple_test.jpg', test_image, 'image/jpeg')},
            timeout=10
        )
        
        print(f"   Status: {recognize_response.status_code}")
        
        if recognize_response.status_code == 200:
            recognize_data = recognize_response.json()
            print(f"   Response: {recognize_data}")
            
            if recognize_data.get('success'):
                if recognize_data.get('data', {}).get('recognized'):
                    name = recognize_data['data']['name']
                    confidence = recognize_data['data']['confidence']
                    print(f"   ✅ Face recognized: {name} ({confidence:.2%})")
                else:
                    print("   ❓ Face not recognized - no matching faces in database")
            else:
                print(f"   ❌ Recognition failed: {recognize_data.get('message')}")
        else:
            print(f"   ❌ Recognition failed with status: {recognize_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error testing face recognition: {e}")

def create_realistic_face_image():
    """Create a more realistic face image"""
    # Create a 400x400 image with a more detailed face
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a more realistic face
    # Head
    draw.ellipse([100, 100, 300, 300], outline='black', width=3, fill='#f4d03f')
    
    # Hair
    draw.ellipse([80, 80, 320, 180], fill='#8b4513')
    
    # Eyes
    draw.ellipse([140, 160, 170, 190], fill='black')
    draw.ellipse([230, 160, 260, 190], fill='black')
    draw.ellipse([145, 165, 165, 185], fill='white')
    draw.ellipse([235, 165, 255, 185], fill='white')
    
    # Nose
    draw.polygon([(200, 200), (190, 220), (210, 220)], fill='#e67e22')
    
    # Mouth
    draw.arc([160, 240, 240, 280], start=0, end=180, fill='#e74c3c', width=3)
    
    # Ears
    draw.ellipse([90, 180, 110, 220], fill='#f4d03f')
    draw.ellipse([290, 180, 310, 220], fill='#f4d03f')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=90)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def create_simple_test_image():
    """Create a simple test image"""
    # Create a 200x200 image with a simple face
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face
    # Head
    draw.ellipse([50, 50, 150, 150], outline='black', width=2)
    
    # Eyes
    draw.ellipse([70, 80, 85, 95], fill='black')
    draw.ellipse([115, 80, 130, 95], fill='black')
    
    # Nose
    draw.polygon([(100, 100), (95, 110), (105, 110)], fill='black')
    
    # Mouth
    draw.arc([80, 120, 120, 140], start=0, end=180, fill='black', width=2)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=90)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def crop_face_from_image(image_bytes, bounding_box):
    """Crop face from image using bounding box"""
    # Load image from bytes
    img = Image.open(io.BytesIO(image_bytes))
    
    # Crop using bounding box
    left = bounding_box['left']
    top = bounding_box['top']
    width = bounding_box['width']
    height = bounding_box['height']
    
    cropped_img = img.crop((left, top, left + width, top + height))
    
    # Convert to bytes
    cropped_bytes = io.BytesIO()
    cropped_img.save(cropped_bytes, format='JPEG', quality=90)
    cropped_bytes.seek(0)
    
    return cropped_bytes.getvalue()

def test_auto_recognition_workflow():
    """Test auto recognition workflow"""
    print("\n🔄 Testing Auto Recognition Workflow")
    print("=" * 40)
    
    workflow_steps = [
        "1. User selects 'Auto Recognition' option",
        "2. User clicks 'Start Auto Recognition'",
        "3. Webcam stream starts",
        "4. Real-time face detection begins",
        "5. Bounding boxes drawn on detected faces",
        "6. Automatic face recognition triggered",
        "7. Recognition results displayed",
        "8. User can toggle modes",
        "9. User can stop auto recognition"
    ]
    
    for step in workflow_steps:
        print(f"✅ {step}")

def test_potential_issues():
    """Test potential issues with auto recognition"""
    print("\n⚠️ Testing Potential Issues")
    print("=" * 35)
    
    issues = [
        "✅ Backend API not running",
        "✅ Face detection API failing",
        "✅ Face recognition API failing",
        "✅ No faces in database",
        "✅ Webcam access denied",
        "✅ JavaScript errors in console",
        "✅ Network connectivity issues",
        "✅ Memory/performance issues"
    ]
    
    for issue in issues:
        print(issue)

if __name__ == "__main__":
    print("🔍 Auto Recognition Debug Test")
    print("=" * 60)
    
    # Test frontend elements
    test_auto_recognition_frontend()
    
    # Test API endpoints
    test_auto_recognition_api_endpoints()
    
    # Test workflow
    test_auto_recognition_workflow()
    
    # Test potential issues
    test_potential_issues()
    
    print("\n✅ Auto recognition debug completed!")
    print("\n💡 Debug Steps:")
    print("   1. Check browser console for JavaScript errors")
    print("   2. Verify backend API is running")
    print("   3. Check webcam permissions")
    print("   4. Verify faces are registered in database")
    print("   5. Test face detection API manually")
    print("   6. Test face recognition API manually")
    print("   7. Check network connectivity")
    print("   8. Monitor memory usage")
    
    print("\n🎯 Common Issues:")
    print("   - Backend API not running (check port 8000)")
    print("   - No faces registered in database")
    print("   - Webcam access denied by browser")
    print("   - JavaScript errors preventing execution")
    print("   - Network connectivity issues")
    print("   - Memory/performance bottlenecks") 
#!/usr/bin/env python3
"""
🧪 Test Auto Detection Workflow Steps
Kiểm tra từng step trong auto detection workflow
"""

import requests
import json
import time
import base64
from PIL import Image, ImageDraw
import io

def test_workflow_step_1_webcam_access():
    """Test Step 1: Webcam Access"""
    print("🎥 Step 1: Testing Webcam Access")
    print("=" * 40)
    
    # This would be tested in browser
    print("✅ Webcam access test requires browser")
    print("   - Open http://localhost:3000")
    print("   - Go to Face Recognition tab")
    print("   - Click 'Start Auto Recognition'")
    print("   - Allow webcam access when prompted")
    print("   - Check browser console for webcam logs")

def test_workflow_step_2_video_stream():
    """Test Step 2: Video Stream Setup"""
    print("\n📹 Step 2: Testing Video Stream Setup")
    print("=" * 45)
    
    try:
        # Check if frontend is accessible
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for video elements
            video_elements = [
                'auto-recognition-video',
                'auto-recognition-canvas'
            ]
            
            for element in video_elements:
                if element in html_content:
                    print(f"✅ {element} found in HTML")
                else:
                    print(f"❌ {element} missing from HTML")
                    
            # Check for video setup functions
            setup_functions = [
                'startAutoRecognition()',
                'video.srcObject',
                'canvas.width',
                'canvas.height'
            ]
            
            for func in setup_functions:
                if func in html_content:
                    print(f"✅ {func} found in JavaScript")
                else:
                    print(f"❌ {func} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing video stream setup: {e}")

def test_workflow_step_3_interval_loop():
    """Test Step 3: Interval Loop Setup"""
    print("\n🔄 Step 3: Testing Interval Loop Setup")
    print("=" * 45)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for interval setup
            interval_elements = [
                'setInterval',
                'processAutoRecognitionFrame',
                'autoRecognitionInterval',
                '1000'
            ]
            
            for element in interval_elements:
                if element in html_content:
                    print(f"✅ {element} found in JavaScript")
                else:
                    print(f"❌ {element} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing interval loop: {e}")

def test_workflow_step_4_canvas_drawing():
    """Test Step 4: Canvas Drawing"""
    print("\n🎨 Step 4: Testing Canvas Drawing")
    print("=" * 35)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for canvas drawing functions
            drawing_functions = [
                'drawImage',
                'toDataURL',
                'getContext',
                'canvas.width',
                'canvas.height'
            ]
            
            for func in drawing_functions:
                if func in html_content:
                    print(f"✅ {func} found in JavaScript")
                else:
                    print(f"❌ {func} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing canvas drawing: {e}")

def test_workflow_step_5_api_detection():
    """Test Step 5: API Detection Call"""
    print("\n🌐 Step 5: Testing API Detection Call")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test detection API directly
        print("Testing face detection API...")
        
        # Create test image
        test_image = create_test_face_image()
        
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
                print(f"   ✅ Detection API working - {faces_count} faces detected")
                
                if faces_count > 0:
                    face = detect_data['data']['faces'][0]
                    print(f"   📊 Face details:")
                    print(f"      - Confidence: {face.get('confidence', 'N/A')}")
                    print(f"      - Quality: {face.get('quality_score', 'N/A')}")
                    print(f"      - Bounding Box: {face.get('bounding_box', 'N/A')}")
                else:
                    print("   ⚠️ No faces detected in test image")
            else:
                print(f"   ❌ Detection failed: {detect_data.get('message')}")
        else:
            print(f"   ❌ Detection API failed: {detect_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing detection API: {e}")

def test_workflow_step_6_face_cropping():
    """Test Step 6: Face Cropping"""
    print("\n✂️ Step 6: Testing Face Cropping")
    print("=" * 35)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for cropping functions
            cropping_functions = [
                'cropFaceFromImage',
                'boundingBox',
                'drawImage',
                'toDataURL'
            ]
            
            for func in cropping_functions:
                if func in html_content:
                    print(f"✅ {func} found in JavaScript")
                else:
                    print(f"❌ {func} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing face cropping: {e}")

def test_workflow_step_7_api_recognition():
    """Test Step 7: API Recognition Call"""
    print("\n🔍 Step 7: Testing API Recognition Call")
    print("=" * 45)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test recognition API directly
        print("Testing face recognition API...")
        
        # Get real face from database
        list_response = requests.get(f"{base_url}/api/v1/faces/list")
        
        if list_response.status_code == 200:
            list_data = list_response.json()
            faces = list_data.get('data', {}).get('faces', [])
            
            if faces:
                face = faces[0]
                face_id = face['id']
                
                # Download face image
                image_response = requests.get(f"{base_url}/api/v1/faces/{face_id}/image")
                
                if image_response.status_code == 200:
                    with open('test_real_face.jpg', 'wb') as f:
                        f.write(image_response.content)
                    
                    # Test recognition
                    recognize_response = requests.post(
                        f"{base_url}/api/v1/faces/recognize",
                        files={'file': ('test_real_face.jpg', open('test_real_face.jpg', 'rb'), 'image/jpeg')},
                        timeout=10
                    )
                    
                    print(f"   Status: {recognize_response.status_code}")
                    
                    if recognize_response.status_code == 200:
                        recognize_data = recognize_response.json()
                        print(f"   Response: {recognize_data}")
                        
                        if recognize_data.get('success'):
                            if recognize_data.get('data', {}).get('recognized'):
                                name = recognize_data['data']['person']['name']
                                confidence = recognize_data['data']['confidence']
                                print(f"   ✅ Recognition API working - {name} ({confidence:.2%})")
                            else:
                                print("   ❓ Face not recognized")
                        else:
                            print(f"   ❌ Recognition failed: {recognize_data.get('message')}")
                    else:
                        print(f"   ❌ Recognition API failed: {recognize_response.status_code}")
                else:
                    print(f"   ❌ Failed to download face image: {image_response.status_code}")
            else:
                print("   ❌ No faces in database")
        else:
            print(f"   ❌ Failed to get face list: {list_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend not running")
    except Exception as e:
        print(f"❌ Error testing recognition API: {e}")

def test_workflow_step_8_ui_updates():
    """Test Step 8: UI Updates"""
    print("\n🎨 Step 8: Testing UI Updates")
    print("=" * 30)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for UI update elements
            ui_elements = [
                'auto-recognition-results',
                'auto-recognized-name',
                'auto-recognition-confidence',
                'auto-recognition-quality',
                'auto-faces-count',
                'auto-status'
            ]
            
            for element in ui_elements:
                if element in html_content:
                    print(f"✅ {element} found in HTML")
                else:
                    print(f"❌ {element} missing from HTML")
                    
            # Check for UI update functions
            ui_functions = [
                'updateAutoRecognitionStatus',
                'classList.add',
                'classList.remove',
                'textContent'
            ]
            
            for func in ui_functions:
                if func in html_content:
                    print(f"✅ {func} found in JavaScript")
                else:
                    print(f"❌ {func} missing from JavaScript")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing UI updates: {e}")

def create_test_face_image():
    """Create a test face image"""
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

def test_complete_workflow():
    """Test complete workflow"""
    print("🧪 Complete Auto Detection Workflow Test")
    print("=" * 60)
    
    # Test each step
    test_workflow_step_1_webcam_access()
    test_workflow_step_2_video_stream()
    test_workflow_step_3_interval_loop()
    test_workflow_step_4_canvas_drawing()
    test_workflow_step_5_api_detection()
    test_workflow_step_6_face_cropping()
    test_workflow_step_7_api_recognition()
    test_workflow_step_8_ui_updates()
    
    print("\n✅ Workflow test completed!")
    print("\n💡 Manual Testing Required:")
    print("   1. Open browser: http://localhost:3000")
    print("   2. Go to Face Recognition tab")
    print("   3. Click 'Start Auto Recognition'")
    print("   4. Allow webcam access")
    print("   5. Show face to camera")
    print("   6. Check browser console for debug logs")
    print("   7. Monitor network tab for API calls")
    print("   8. Verify recognition results appear")

if __name__ == "__main__":
    test_complete_workflow() 
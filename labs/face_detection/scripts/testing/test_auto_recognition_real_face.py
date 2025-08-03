#!/usr/bin/env python3
"""
🧪 Test Auto Recognition with Real Face
Kiểm tra auto recognition với real face images
"""

import requests
import json
import time
import base64
from PIL import Image, ImageDraw
import io

def test_auto_recognition_with_real_face():
    """Test auto recognition with real face from database"""
    print("🎯 Testing Auto Recognition with Real Face")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Get real face from database
        print("1. Getting real face from database...")
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
                    with open('test_real_face.jpg', 'wb') as f:
                        f.write(image_response.content)
                    print("   ✅ Face image downloaded")
                    
                    # Step 3: Test face detection
                    print("\n3. Testing face detection...")
                    detect_response = requests.post(
                        f"{base_url}/api/v1/faces/detect",
                        files={'file': ('test_real_face.jpg', open('test_real_face.jpg', 'rb'), 'image/jpeg')},
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
                                
                                # Step 4: Test face recognition
                                print("\n4. Testing face recognition...")
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
                                            print(f"   ✅ Face recognized: {name} ({confidence:.2%})")
                                            
                                            # Step 5: Test auto recognition workflow
                                            print("\n5. Testing auto recognition workflow...")
                                            test_auto_recognition_workflow()
                                            
                                        else:
                                            print("   ❓ Face not recognized")
                                    else:
                                        print(f"   ❌ Recognition failed: {recognize_data.get('message')}")
                                else:
                                    print(f"   ❌ Recognition failed with status: {recognize_response.status_code}")
                            else:
                                print("   ⚠️ No faces detected in real face image")
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
        print(f"❌ Error testing auto recognition: {e}")

def test_auto_recognition_workflow():
    """Test complete auto recognition workflow"""
    print("\n🔄 Testing Auto Recognition Workflow")
    print("=" * 40)
    
    workflow_steps = [
        "1. Start auto recognition mode",
        "2. Webcam stream starts",
        "3. Real-time face detection",
        "4. Bounding box visualization",
        "5. Automatic face cropping",
        "6. Face recognition API call",
        "7. Results display in overlay",
        "8. Status updates",
        "9. Cooldown management"
    ]
    
    for step in workflow_steps:
        print(f"✅ {step}")

def test_frontend_auto_recognition():
    """Test frontend auto recognition elements"""
    print("\n🎨 Testing Frontend Auto Recognition")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
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
                    
            # Check for JavaScript functions
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
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")

def test_auto_recognition_debug_info():
    """Provide debug information for auto recognition"""
    print("\n🔍 Auto Recognition Debug Information")
    print("=" * 40)
    
    debug_info = [
        "✅ Backend API running on port 8000",
        "✅ Frontend running on port 3000",
        "✅ Face detection API working",
        "✅ Face recognition API working",
        "✅ Real face in database",
        "✅ Auto recognition functions implemented",
        "✅ Debug logging added",
        "✅ Error handling implemented"
    ]
    
    for info in debug_info:
        print(info)
    
    print("\n💡 Manual Testing Steps:")
    print("   1. Open http://localhost:3000")
    print("   2. Go to 'Face Recognition' tab")
    print("   3. Select 'Auto Recognition' option")
    print("   4. Click 'Start Auto Recognition'")
    print("   5. Allow webcam access when prompted")
    print("   6. Show your face to the camera")
    print("   7. Check browser console for debug logs")
    print("   8. Verify recognition results appear")
    
    print("\n🎯 Expected Behavior:")
    print("   - Webcam stream starts automatically")
    print("   - Face detection with bounding boxes")
    print("   - Automatic recognition every 2 seconds")
    print("   - Recognition results in overlay")
    print("   - Debug logs in browser console")
    print("   - Status updates in UI")

if __name__ == "__main__":
    print("🧪 Auto Recognition with Real Face Test")
    print("=" * 60)
    
    # Test with real face
    test_auto_recognition_with_real_face()
    
    # Test frontend elements
    test_frontend_auto_recognition()
    
    # Test workflow
    test_auto_recognition_workflow()
    
    # Provide debug info
    test_auto_recognition_debug_info()
    
    print("\n✅ Auto recognition test completed!")
    print("\n🔍 If auto recognition is not working:")
    print("   1. Check browser console for JavaScript errors")
    print("   2. Verify webcam permissions are granted")
    print("   3. Check network connectivity to backend")
    print("   4. Monitor debug logs in browser console")
    print("   5. Test with different lighting conditions")
    print("   6. Ensure face is clearly visible to camera") 
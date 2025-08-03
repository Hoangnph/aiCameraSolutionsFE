#!/usr/bin/env python3
"""
🔍 Debug Face Recognition Error
Tìm hiểu nguyên nhân "Name: Error" trong auto recognition
"""

import requests
import json
import time
import base64
from PIL import Image, ImageDraw
import io

def test_recognition_error_scenario():
    """Test the exact scenario that's causing the error"""
    print("🔍 Debugging Face Recognition Error")
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
                    with open('debug_real_face.jpg', 'wb') as f:
                        f.write(image_response.content)
                    print("   ✅ Face image downloaded")
                    
                    # Step 3: Test face detection with real face
                    print("\n3. Testing face detection with real face...")
                    detect_response = requests.post(
                        f"{base_url}/api/v1/faces/detect",
                        files={'file': ('debug_real_face.jpg', open('debug_real_face.jpg', 'rb'), 'image/jpeg')},
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
                                
                                # Step 4: Test face recognition with original image
                                print("\n4. Testing face recognition with original image...")
                                recognize_response = requests.post(
                                    f"{base_url}/api/v1/faces/recognize",
                                    files={'file': ('debug_real_face.jpg', open('debug_real_face.jpg', 'rb'), 'image/jpeg')},
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
                                        else:
                                            print("   ❓ Face not recognized")
                                    else:
                                        print(f"   ❌ Recognition failed: {recognize_data.get('message')}")
                                else:
                                    print(f"   ❌ Recognition failed with status: {recognize_response.status_code}")
                                
                                # Step 5: Test face recognition with cropped face
                                print("\n5. Testing face recognition with cropped face...")
                                test_recognition_with_cropped_face(detected_face['bounding_box'])
                                
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
        print(f"❌ Error testing recognition error: {e}")

def test_recognition_with_cropped_face(bounding_box):
    """Test recognition with cropped face"""
    print("   🔍 Testing recognition with cropped face...")
    
    try:
        # Load the original image
        with open('debug_real_face.jpg', 'rb') as f:
            original_image_data = f.read()
        
        # Create cropped image using PIL
        img = Image.open(io.BytesIO(original_image_data))
        
        # Crop using bounding box
        left = bounding_box['left']
        top = bounding_box['top']
        width = bounding_box['width']
        height = bounding_box['height']
        
        cropped_img = img.crop((left, top, left + width, top + height))
        
        # Save cropped image
        cropped_bytes = io.BytesIO()
        cropped_img.save(cropped_bytes, format='JPEG', quality=90)
        cropped_bytes.seek(0)
        
        # Test recognition with cropped face
        base_url = "http://localhost:8000"
        recognize_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('cropped_face.jpg', cropped_bytes.getvalue(), 'image/jpeg')},
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
                    print(f"   ✅ Cropped face recognized: {name} ({confidence:.2%})")
                else:
                    print("   ❓ Cropped face not recognized")
            else:
                print(f"   ❌ Cropped face recognition failed: {recognize_data.get('message')}")
        else:
            print(f"   ❌ Cropped face recognition failed with status: {recognize_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error testing cropped face recognition: {e}")

def test_frontend_recognition_error():
    """Test frontend recognition error handling"""
    print("\n🎨 Testing Frontend Recognition Error Handling")
    print("=" * 55)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            html_content = response.text
            
            # Check for error handling in recognition
            error_handling = [
                'catch (error)',
                'console.error',
                'updateAutoRecognitionStatus',
                'textContent = \'Error\'',
                'classList.add(\'error\')'
            ]
            
            for element in error_handling:
                if element in html_content:
                    print(f"✅ {element} found in JavaScript")
                else:
                    print(f"❌ {element} missing from JavaScript")
                    
            # Check for specific error handling in performAutoRecognition
            recognition_error_handling = [
                'performAutoRecognition',
                'catch (error)',
                'console.error',
                'textContent = \'Error\'',
                'classList.add(\'error\')'
            ]
            
            for element in recognition_error_handling:
                if element in html_content:
                    print(f"✅ {element} found in performAutoRecognition")
                else:
                    print(f"❌ {element} missing from performAutoRecognition")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing frontend error handling: {e}")

def test_api_error_scenarios():
    """Test various API error scenarios"""
    print("\n🌐 Testing API Error Scenarios")
    print("=" * 35)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Invalid image format
    print("1. Testing invalid image format...")
    try:
        invalid_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('invalid.txt', b'invalid data', 'text/plain')},
            timeout=10
        )
        print(f"   Status: {invalid_response.status_code}")
        print(f"   Response: {invalid_response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Empty image
    print("\n2. Testing empty image...")
    try:
        empty_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('empty.jpg', b'', 'image/jpeg')},
            timeout=10
        )
        print(f"   Status: {empty_response.status_code}")
        print(f"   Response: {empty_response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Large image
    print("\n3. Testing large image...")
    try:
        # Create a large test image
        large_img = Image.new('RGB', (4000, 4000), color='white')
        large_bytes = io.BytesIO()
        large_img.save(large_bytes, format='JPEG', quality=90)
        large_bytes.seek(0)
        
        large_response = requests.post(
            f"{base_url}/api/v1/faces/recognize",
            files={'file': ('large.jpg', large_bytes.getvalue(), 'image/jpeg')},
            timeout=30
        )
        print(f"   Status: {large_response.status_code}")
        print(f"   Response: {large_response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def analyze_error_patterns():
    """Analyze common error patterns"""
    print("\n🔍 Analyzing Error Patterns")
    print("=" * 35)
    
    error_patterns = [
        "1. Network timeout - API calls taking too long",
        "2. Invalid image format - Frontend sending wrong format",
        "3. Empty image data - Canvas not drawing properly",
        "4. Large image size - Memory issues",
        "5. Backend service error - Face recognition service down",
        "6. Database connection error - Can't access face embeddings",
        "7. JavaScript error - Frontend code execution failed",
        "8. CORS error - Cross-origin request blocked"
    ]
    
    for pattern in error_patterns:
        print(f"   {pattern}")

def provide_debug_commands():
    """Provide debug commands for manual testing"""
    print("\n🛠️ Debug Commands for Manual Testing")
    print("=" * 45)
    
    commands = [
        "1. Check browser console (F12):",
        "   - Look for JavaScript errors",
        "   - Check network tab for failed API calls",
        "   - Monitor console.log outputs",
        "",
        "2. Test backend APIs manually:",
        "   curl -X POST 'http://localhost:8000/api/v1/faces/detect' \\",
        "     -F 'file=@debug_real_face.jpg'",
        "   curl -X POST 'http://localhost:8000/api/v1/faces/recognize' \\",
        "     -F 'file=@debug_real_face.jpg'",
        "",
        "3. Check backend logs:",
        "   - Monitor backend console for errors",
        "   - Check for database connection issues",
        "   - Verify face recognition service status",
        "",
        "4. Test with different images:",
        "   - Try with different face images",
        "   - Test with various image sizes",
        "   - Check different lighting conditions"
    ]
    
    for command in commands:
        print(f"   {command}")

if __name__ == "__main__":
    print("🔍 Face Recognition Error Debug")
    print("=" * 60)
    
    # Test recognition error scenario
    test_recognition_error_scenario()
    
    # Test frontend error handling
    test_frontend_recognition_error()
    
    # Test API error scenarios
    test_api_error_scenarios()
    
    # Analyze error patterns
    analyze_error_patterns()
    
    # Provide debug commands
    provide_debug_commands()
    
    print("\n✅ Error debug completed!")
    print("\n💡 Next Steps:")
    print("   1. Check browser console for JavaScript errors")
    print("   2. Monitor network tab for failed API calls")
    print("   3. Test backend APIs manually")
    print("   4. Check backend logs for service errors")
    print("   5. Verify database connectivity")
    print("   6. Test with different face images") 
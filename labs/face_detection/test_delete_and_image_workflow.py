#!/usr/bin/env python3
"""
🧪 Test Delete & Image Workflow
Kiểm tra toàn bộ workflow delete face và hiển thị hình ảnh
"""

import requests
import json
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io

def create_test_face():
    """Create a test face image"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img.fill(200)
    
    # Draw a simple face
    center_x, center_y = 320, 240
    cv2.circle(img, (center_x, center_y), 100, (255, 200, 150), -1)
    cv2.circle(img, (center_x - 40, center_y - 20), 15, (255, 255, 255), -1)
    cv2.circle(img, (center_x + 40, center_y - 20), 15, (255, 255, 255), -1)
    cv2.circle(img, (center_x, center_y + 30), 25, (0, 0, 255), 3)
    
    return img

def test_face_workflow():
    """Test complete face workflow: create → list → delete → verify"""
    print("🧪 Testing Face Delete & Image Workflow")
    print("=" * 60)
    
    # Step 1: Create a test face
    print("\n1️⃣ Creating test face...")
    test_img = create_test_face()
    
    # Convert to PIL and save
    pil_img = Image.fromarray(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    # Generate unique email
    test_email = f'test_{int(time.time())}@example.com'
    
    try:
        files = {'file': ('test_face.jpg', img_buffer, 'image/jpeg')}
        data = {
            'name': 'TestUser',
            'email': test_email,
            'phone': '1234567890',
            'notes': 'Test face for workflow'
        }
        
        response = requests.post('http://localhost:8000/api/v1/faces/upload', 
                               files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test face created successfully")
            print(f"   Response: {result}")
            face_id = result['data']['embedding_id']
        else:
            print(f"❌ Failed to create test face: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test face: {e}")
        return False
    
    # Step 2: List faces and verify image URLs
    print("\n2️⃣ Listing faces and checking image URLs...")
    try:
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            print(f"✅ Found {len(faces)} faces")
            
            # Check if our test face is in the list
            test_face = None
            for face in faces:
                if face['metadata']['name'] == 'TestUser' and face['metadata']['email'] == test_email:
                    test_face = face
                    break
            
            if test_face:
                print("✅ Test face found in list")
                print(f"   Face ID: {test_face['id']}")
                print(f"   Image URL: {test_face.get('image_url', 'N/A')}")
                
                # Test image endpoint
                if 'image_url' in test_face:
                    img_response = requests.get(f"http://localhost:8000{test_face['image_url']}")
                    if img_response.status_code == 200:
                        print("✅ Face image endpoint working")
                    else:
                        print(f"❌ Face image endpoint failed: {img_response.status_code}")
            else:
                print("❌ Test face not found in list")
                return False
        else:
            print(f"❌ Failed to list faces: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error listing faces: {e}")
        return False
    
    # Step 3: Delete the test face
    print(f"\n3️⃣ Deleting test face...")
    try:
        # Get the actual face_id from the list
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            
            # Find our test face
            test_face = None
            for face in faces:
                if face['metadata']['name'] == 'TestUser':
                    test_face = face
                    break
            
            if test_face:
                face_id = test_face['id']
                print(f"   Using face ID: {face_id}")
                
                response = requests.delete(f'http://localhost:8000/api/v1/faces/{face_id}')
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Test face deleted successfully")
                    print(f"   Deleted face ID: {result['data']['face_id']}")
                else:
                    print(f"❌ Failed to delete test face: {response.status_code}")
                    return False
            else:
                print("❌ Test face not found for deletion")
                return False
        else:
            print(f"❌ Failed to get face list for deletion: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting test face: {e}")
        return False
    
    # Step 4: Verify face is gone
    print("\n4️⃣ Verifying face is removed...")
    try:
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            
            # Check if test face is still in list
            test_face_still_exists = any(
                face['metadata']['name'] == 'TestUser' and face['metadata']['email'] == test_email
                for face in faces
            )
            
            if not test_face_still_exists:
                print("✅ Test face successfully removed from list")
                print(f"   Remaining faces: {len(faces)}")
            else:
                print("❌ Test face still exists in list")
                return False
        else:
            print(f"❌ Failed to verify face removal: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying face removal: {e}")
        return False
    
    print("\n🎉 All tests passed! Face delete and image workflow working correctly.")
    return True

def test_image_endpoints():
    """Test image serving endpoints"""
    print("\n🖼️ Testing Image Endpoints")
    print("=" * 40)
    
    try:
        # Get current faces
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            
            if faces:
                # Test first face image
                face = faces[0]
                print(f"Testing image for face: {face['metadata']['name']}")
                
                if 'image_url' in face:
                    img_response = requests.get(f"http://localhost:8000{face['image_url']}")
                    if img_response.status_code == 200:
                        print(f"✅ Image endpoint working: {len(img_response.content)} bytes")
                        print(f"   Content-Type: {img_response.headers.get('content-type', 'N/A')}")
                    else:
                        print(f"❌ Image endpoint failed: {img_response.status_code}")
                else:
                    print("❌ No image_url in face data")
            else:
                print("ℹ️  No faces to test image endpoints")
        else:
            print(f"❌ Failed to get faces: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing image endpoints: {e}")

if __name__ == "__main__":
    print("🧪 Face Delete & Image Workflow Test")
    print("=" * 60)
    
    # Test image endpoints
    test_image_endpoints()
    
    # Test complete workflow
    success = test_face_workflow()
    
    if success:
        print("\n✅ All tests passed!")
        print("\n💡 Frontend should now show:")
        print("   - Face images in the list")
        print("   - Working delete functionality")
        print("   - Proper error handling")
    else:
        print("\n❌ Some tests failed!")
        print("   Please check the logs above for issues.") 
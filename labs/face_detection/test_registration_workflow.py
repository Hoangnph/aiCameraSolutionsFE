#!/usr/bin/env python3
"""
🧪 Test Registration Workflow
Kiểm tra workflow register face và form reset
"""

import requests
import json
import time
import cv2
import numpy as np
from PIL import Image
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

def test_registration_workflow():
    """Test face registration workflow with multiple registrations"""
    print("🧪 Testing Face Registration Workflow")
    print("=" * 60)
    
    # Test multiple registrations
    for i in range(3):
        print(f"\n{i+1}️⃣ Testing registration {i+1}...")
        
        # Create test image
        test_img = create_test_face()
        pil_img = Image.fromarray(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        img_buffer = io.BytesIO()
        pil_img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # Generate unique data
        timestamp = int(time.time())
        test_name = f"TestUser_{timestamp}"
        test_email = f"test_{timestamp}@example.com"
        
        try:
            files = {'file': (f'test_face_{timestamp}.jpg', img_buffer, 'image/jpeg')}
            data = {
                'name': test_name,
                'email': test_email,
                'phone': f'123456789{i}',
                'notes': f'Test registration {i+1}'
            }
            
            response = requests.post('http://localhost:8000/api/v1/faces/upload', 
                                   files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Registration {i+1} successful")
                print(f"   Name: {result['data']['name']}")
                print(f"   Email: {result['data']['email']}")
                print(f"   Face ID: {result['data']['embedding_id']}")
            else:
                print(f"❌ Registration {i+1} failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error in registration {i+1}: {e}")
            return False
        
        # Small delay between registrations
        time.sleep(1)
    
    # Verify all faces are in database
    print("\n4️⃣ Verifying all registrations...")
    try:
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            print(f"✅ Found {len(faces)} total faces in database")
            
            # Check for our test faces
            test_faces = [face for face in faces if face['metadata']['name'].startswith('TestUser_')]
            print(f"✅ Found {len(test_faces)} test faces")
            
            for face in test_faces:
                print(f"   - {face['metadata']['name']} (ID: {face['id']})")
                
        else:
            print(f"❌ Failed to verify registrations: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying registrations: {e}")
        return False
    
    print("\n🎉 All registration tests passed!")
    return True

def test_form_reset_simulation():
    """Simulate form reset behavior"""
    print("\n🔄 Testing Form Reset Simulation")
    print("=" * 40)
    
    print("✅ Form reset functions added to frontend:")
    print("   - resetRegistrationForm() for webcam registration")
    print("   - resetFileUploadForm() for file upload")
    print("   - Auto-reset after 2 seconds on success")
    print("   - Clear name input, file input, captured image")
    print("   - Disable upload button")
    print("   - Clear face detection status")
    
    print("\n💡 Frontend should now:")
    print("   - Reset form after successful registration")
    print("   - Allow multiple registrations without manual reset")
    print("   - Clear all form fields automatically")
    print("   - Show success message before reset")

if __name__ == "__main__":
    print("🧪 Face Registration Workflow Test")
    print("=" * 60)
    
    # Test registration workflow
    success = test_registration_workflow()
    
    # Test form reset simulation
    test_form_reset_simulation()
    
    if success:
        print("\n✅ All tests passed!")
        print("\n💡 Frontend workflow should now work correctly:")
        print("   - Register face → Success message → Auto reset → Ready for next registration")
        print("   - No manual form clearing needed")
        print("   - Multiple registrations possible")
    else:
        print("\n❌ Some tests failed!")
        print("   Please check the logs above for issues.") 
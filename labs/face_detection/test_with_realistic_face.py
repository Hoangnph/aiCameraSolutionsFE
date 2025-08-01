#!/usr/bin/env python3
"""
🔍 Test with Realistic Face Image
Test với ảnh face thực tế hơn
"""

import requests
import json
import time
from PIL import Image, ImageDraw
import io
import numpy as np

def create_realistic_face_image():
    """Create a more realistic face image"""
    # Create a larger image (200x200) with more realistic face features
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Skin tone
    skin_color = (255, 220, 177)
    draw.rectangle([0, 0, 200, 200], fill=skin_color)
    
    # Hair
    hair_color = (139, 69, 19)
    draw.rectangle([0, 0, 200, 50], fill=hair_color)
    
    # Eyes (more realistic)
    eye_color = (0, 0, 0)
    # Left eye
    draw.ellipse([70, 80, 90, 100], fill=eye_color)
    # Right eye
    draw.ellipse([110, 80, 130, 100], fill=eye_color)
    
    # Nose
    nose_color = (255, 200, 150)
    draw.ellipse([95, 100, 105, 120], fill=nose_color)
    
    # Mouth
    mouth_color = (255, 150, 150)
    draw.ellipse([85, 130, 115, 140], fill=mouth_color)
    
    return img

def test_upload_with_realistic_face():
    """Test upload with realistic face image"""
    api_base = "http://localhost:8000"
    
    print("🔍 Testing Upload with Realistic Face")
    print("=" * 50)
    
    try:
        # Create realistic face image
        print("📸 Creating realistic face image...")
        img = create_realistic_face_image()
        
        # Convert to bytes with proper format
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        print("📤 Uploading realistic face image...")
        
        # Upload with proper content type
        files = {
            'file': ('realistic_face.jpg', img_bytes, 'image/jpeg')
        }
        data = {
            'name': 'RealisticTestUser',
            'email': 'realistic@test.com'
        }
        
        response = requests.post(
            f"{api_base}/api/v1/faces/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"📊 Response data: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recognition_with_realistic_face():
    """Test recognition with realistic face image"""
    api_base = "http://localhost:8000"
    
    print("\n🔍 Testing Recognition with Realistic Face")
    print("=" * 50)
    
    try:
        # Create realistic face image for recognition
        print("📸 Creating realistic face image for recognition...")
        img = create_realistic_face_image()
        
        # Convert to bytes with proper format
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        print("🔍 Sending recognition request...")
        
        # Recognition with proper content type
        files = {
            'file': ('realistic_recognition.jpg', img_bytes, 'image/jpeg')
        }
        
        response = requests.post(
            f"{api_base}/api/v1/faces/recognize",
            files=files,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recognition successful!")
            print(f"📊 Response data: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Recognition failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    api_base = "http://localhost:8000"
    
    print("\n🔄 Testing End-to-End Workflow")
    print("=" * 50)
    
    try:
        # Step 1: Upload realistic face
        print("📤 Step 1: Uploading realistic face...")
        img = create_realistic_face_image()
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95)
        img_bytes.seek(0)
        
        files = {
            'file': ('workflow_face.jpg', img_bytes, 'image/jpeg')
        }
        data = {
            'name': 'WorkflowTestUser',
            'email': 'workflow@test.com'
        }
        
        upload_response = requests.post(
            f"{api_base}/api/v1/faces/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📊 Upload Response: {upload_response.status_code}")
        if upload_response.status_code == 200:
            print("✅ Upload successful!")
            
            # Step 2: Wait a bit for processing
            time.sleep(2)
            
            # Step 3: Test recognition with same image
            print("🔍 Step 2: Testing recognition...")
            
            img_bytes.seek(0)
            recognition_files = {
                'file': ('workflow_recognition.jpg', img_bytes, 'image/jpeg')
            }
            
            recognition_response = requests.post(
                f"{api_base}/api/v1/faces/recognize",
                files=recognition_files,
                timeout=30
            )
            
            print(f"📊 Recognition Response: {recognition_response.status_code}")
            if recognition_response.status_code == 200:
                recognition_data = recognition_response.json()
                print("✅ Recognition successful!")
                print(f"📊 Recognition data: {json.dumps(recognition_data, indent=2)}")
                return True
            else:
                print(f"❌ Recognition failed: {recognition_response.text}")
                return False
        else:
            print(f"❌ Upload failed: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return False

def main():
    """Run tests with realistic face images"""
    print("🚀 Starting Realistic Face Tests")
    print("=" * 60)
    
    # Test 1: Upload with realistic face
    upload_success = test_upload_with_realistic_face()
    
    # Test 2: Recognition with realistic face
    recognition_success = test_recognition_with_realistic_face()
    
    # Test 3: End-to-end workflow
    workflow_success = test_end_to_end_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"✅ Upload: {'PASS' if upload_success else 'FAIL'}")
    print(f"✅ Recognition: {'PASS' if recognition_success else 'FAIL'}")
    print(f"✅ End-to-End Workflow: {'PASS' if workflow_success else 'FAIL'}")
    
    return upload_success and recognition_success and workflow_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
#!/usr/bin/env python3
"""
🔍 Test with Real Face Image
Test với ảnh face thực tế từ internet
"""

import requests
import json
import time
import os
from PIL import Image
import io

def download_real_face_image():
    """Download a real face image for testing"""
    try:
        # Use a real face image URL (public domain)
        url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face"
        
        print("📥 Downloading real face image...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Save the image
            image_path = "real_face_test.jpg"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded real face image: {image_path}")
            return image_path
        else:
            print(f"❌ Failed to download image: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return None

def create_synthetic_face_image():
    """Create a more realistic synthetic face image"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a larger, more realistic face image
        img = Image.new('RGB', (300, 300), color='white')
        draw = ImageDraw.Draw(img)
        
        # Skin tone background
        skin_color = (255, 220, 177)
        draw.rectangle([0, 0, 300, 300], fill=skin_color)
        
        # Hair
        hair_color = (139, 69, 19)
        draw.rectangle([0, 0, 300, 80], fill=hair_color)
        
        # Eyes (more realistic)
        eye_color = (0, 0, 0)
        # Left eye
        draw.ellipse([100, 120, 130, 150], fill=eye_color)
        # Right eye
        draw.ellipse([170, 120, 200, 150], fill=eye_color)
        
        # Nose
        nose_color = (255, 200, 150)
        draw.ellipse([140, 160, 160, 190], fill=nose_color)
        
        # Mouth
        mouth_color = (255, 150, 150)
        draw.ellipse([120, 200, 180, 220], fill=mouth_color)
        
        # Save image
        image_path = "synthetic_face_test.jpg"
        img.save(image_path, quality=95)
        
        print(f"✅ Created synthetic face image: {image_path}")
        return image_path
        
    except Exception as e:
        print(f"❌ Error creating synthetic image: {e}")
        return None

def test_upload_with_real_face(image_path):
    """Test upload with real face image"""
    api_base = "http://localhost:8000"
    
    print(f"🔍 Testing Upload with Real Face: {image_path}")
    print("=" * 50)
    
    try:
        # Upload with real face image
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path, f, 'image/jpeg')
            }
            data = {
                'name': 'RealFaceTestUser',
                'email': 'realface@test.com'
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

def test_recognition_with_real_face(image_path):
    """Test recognition with real face image"""
    api_base = "http://localhost:8000"
    
    print(f"\n🔍 Testing Recognition with Real Face: {image_path}")
    print("=" * 50)
    
    try:
        # Recognition with real face image
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path, f, 'image/jpeg')
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

def test_end_to_end_with_real_face():
    """Test complete end-to-end workflow with real face"""
    api_base = "http://localhost:8000"
    
    print("\n🔄 Testing End-to-End Workflow with Real Face")
    print("=" * 50)
    
    try:
        # Step 1: Create/Download real face image
        image_path = download_real_face_image()
        if not image_path:
            image_path = create_synthetic_face_image()
        
        if not image_path:
            print("❌ Could not create/download face image")
            return False
        
        # Step 2: Upload face
        print("📤 Step 1: Uploading real face...")
        upload_success = test_upload_with_real_face(image_path)
        
        if upload_success:
            # Step 3: Wait for processing
            time.sleep(3)
            
            # Step 4: Test recognition
            print("🔍 Step 2: Testing recognition...")
            recognition_success = test_recognition_with_real_face(image_path)
            
            if recognition_success:
                print("✅ End-to-end workflow successful!")
                return True
            else:
                print("❌ Recognition failed")
                return False
        else:
            print("❌ Upload failed")
            return False
            
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return False

def main():
    """Run tests with real face images"""
    print("🚀 Starting Real Face Tests")
    print("=" * 60)
    
    # Test 1: Upload with real face
    image_path = download_real_face_image()
    if not image_path:
        image_path = create_synthetic_face_image()
    
    if image_path:
        upload_success = test_upload_with_real_face(image_path)
        recognition_success = test_recognition_with_real_face(image_path)
        workflow_success = test_end_to_end_with_real_face()
    else:
        upload_success = recognition_success = workflow_success = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"✅ Upload: {'PASS' if upload_success else 'FAIL'}")
    print(f"✅ Recognition: {'PASS' if recognition_success else 'FAIL'}")
    print(f"✅ End-to-End Workflow: {'PASS' if workflow_success else 'FAIL'}")
    
    # Cleanup
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        print(f"🧹 Cleaned up: {image_path}")
    
    return upload_success and recognition_success and workflow_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
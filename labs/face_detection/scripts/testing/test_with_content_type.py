#!/usr/bin/env python3
"""
🔍 Test with Proper Content Type
Test với content type đúng cho image files
"""

import requests
import json
import time
from PIL import Image
import io

def test_upload_with_proper_content_type():
    """Test upload with proper content type"""
    api_base = "http://localhost:8000"
    
    print("🔍 Testing Upload with Proper Content Type")
    print("=" * 50)
    
    try:
        # Create test image
        print("📸 Creating test image...")
        img = Image.new('RGB', (100, 100), color='red')
        
        # Convert to bytes with proper format
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        print("📤 Uploading image with proper content type...")
        
        # Upload with proper content type
        files = {
            'file': ('test_image.jpg', img_bytes, 'image/jpeg')
        }
        data = {
            'name': 'TestUser',
            'email': 'test@example.com'
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

def test_recognition_with_proper_content_type():
    """Test recognition with proper content type"""
    api_base = "http://localhost:8000"
    
    print("\n🔍 Testing Recognition with Proper Content Type")
    print("=" * 50)
    
    try:
        # Create test image for recognition
        print("📸 Creating recognition test image...")
        img = Image.new('RGB', (100, 100), color='blue')
        
        # Convert to bytes with proper format
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        print("🔍 Sending recognition request...")
        
        # Recognition with proper content type
        files = {
            'file': ('recognition_test.jpg', img_bytes, 'image/jpeg')
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

def main():
    """Run tests with proper content type"""
    print("🚀 Starting Content Type Tests")
    print("=" * 60)
    
    # Test 1: Upload
    upload_success = test_upload_with_proper_content_type()
    
    # Test 2: Recognition
    recognition_success = test_recognition_with_proper_content_type()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"✅ Upload: {'PASS' if upload_success else 'FAIL'}")
    print(f"✅ Recognition: {'PASS' if recognition_success else 'FAIL'}")
    
    return upload_success and recognition_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
#!/usr/bin/env python3
"""
🔍 Simple API Test
Test API endpoints trực tiếp
"""

import requests
import json
import time

def test_api_endpoints():
    """Test basic API endpoints"""
    api_base = "http://localhost:8000"
    
    print("🔍 Testing API Endpoints...")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n📋 Test 1: Health Check")
    try:
        response = requests.get(f"{api_base}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('message')}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: List faces
    print("\n📋 Test 2: List Faces")
    try:
        response = requests.get(f"{api_base}/api/v1/faces/list", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            faces = data.get('data', {}).get('faces', [])
            print(f"✅ List faces passed: Found {len(faces)} faces")
        else:
            print(f"❌ List faces failed: {response.text}")
    except Exception as e:
        print(f"❌ List faces error: {e}")
    
    # Test 3: Upload test (with simple image)
    print("\n📋 Test 3: Upload Test")
    try:
        # Create a simple test image
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save('test_upload.jpg')
        
        with open('test_upload.jpg', 'rb') as f:
            files = {'file': f}
            data = {'name': 'TestUser'}
            response = requests.post(f"{api_base}/api/v1/faces/upload", 
                                  files=files, data=data, timeout=30)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Upload test passed")
        else:
            print("❌ Upload test failed")
            
        # Clean up
        import os
        os.remove('test_upload.jpg')
        
    except Exception as e:
        print(f"❌ Upload test error: {e}")
    
    # Test 4: Recognition test
    print("\n📋 Test 4: Recognition Test")
    try:
        # Create a simple test image for recognition
        img = Image.new('RGB', (100, 100), color='blue')
        img.save('test_recognition.jpg')
        
        with open('test_recognition.jpg', 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{api_base}/api/v1/faces/recognize", 
                                  files=files, timeout=30)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Recognition test passed")
        else:
            print("❌ Recognition test failed")
            
        # Clean up
        os.remove('test_recognition.jpg')
        
    except Exception as e:
        print(f"❌ Recognition test error: {e}")

if __name__ == "__main__":
    test_api_endpoints() 
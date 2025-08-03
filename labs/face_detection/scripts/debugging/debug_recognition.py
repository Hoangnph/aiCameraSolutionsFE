#!/usr/bin/env python3
"""
🔍 Debug Face Recognition Script
Test recognition với face images hiện có
"""

import requests
import json
import os
from datetime import datetime

def test_face_recognition():
    """Test face recognition với face images hiện có"""
    print("🔍 Testing Face Recognition...")
    
    # Test với face image của "hoang"
    image_path = "uploads/face_20250731_222544.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('face_20250731_222544.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/api/v1/faces/recognize', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recognition Response:")
            print(json.dumps(data, indent=2))
            
            if data['success']:
                result = data['data']
                print(f"\n📊 Recognition Results:")
                print(f"   - Recognized: {result['recognized']}")
                print(f"   - Person Name: {result['person']['name']}")
                print(f"   - Person ID: {result['person']['id']}")
                print(f"   - Confidence: {result['confidence']:.2%}")
                
                if 'matches' in result:
                    print(f"   - All Matches:")
                    for match in result['matches']:
                        print(f"     * {match['name']}: {match['confidence']:.2%}")
            else:
                print(f"❌ Recognition failed: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_face_list():
    """Test face list API"""
    print("\n📋 Testing Face List...")
    
    try:
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Face List Response:")
            print(json.dumps(data, indent=2))
            
            if data['success']:
                faces = data['data']['faces']
                print(f"\n📊 Registered Faces ({len(faces)}):")
                for face in faces:
                    print(f"   - {face['metadata']['name']} (ID: {face['id']}, Person ID: {face['metadata']['person_id']})")
            else:
                print(f"❌ Face list failed: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    """Test health check"""
    print("\n🏥 Testing Health Check...")
    
    try:
        response = requests.get('http://localhost:8000/health')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 Face Recognition Debug Test")
    print("=" * 50)
    
    # Test health first
    test_health()
    
    # Test face list
    test_face_list()
    
    # Test recognition
    test_face_recognition()
    
    print("\n✅ Debug test completed!")

if __name__ == "__main__":
    main() 
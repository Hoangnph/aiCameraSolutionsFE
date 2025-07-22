#!/usr/bin/env python3
"""
AI Camera Test Suite
Test camera with AI model processing
"""

import requests
import json
import time
import sys
import os
from typing import Dict, Any, Optional

# Test configuration based on the camera image
CAMERA_CONFIG = {
    "name": "AI Test Camera",
    "location": "Test Location",
    "stream_url": "rtsp://Fd320bYbaxJoe0GT:Mg3jsKE5bailKccS@192.168.1.7/live0",
    "ip_address": "192.168.1.7",
    "port": 554,
    "username": "Fd320bYbaxJoe0GT",
    "password": "Mg3jsKE5bailKccS",
    "source_path": "live0",
    "brand": "Custom/User-defined"
}

# API endpoints
BASE_URL = "http://localhost:3002/api/v1"
AUTH_URL = "http://localhost:3001/api/v1"

class AICameraTest:
    def __init__(self):
        self.auth_token = None
        self.test_camera_id = None
        self.session = requests.Session()
        
    def setup_auth(self) -> bool:
        """Setup authentication for API calls"""
        try:
            login_data = {
                "username": "testuser",
                "password": "testpass123"
            }
            
            response = self.session.post(f"{AUTH_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success") and response_data.get("data", {}).get("accessToken"):
                    self.auth_token = response_data["data"]["accessToken"]
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    print("✅ Authentication successful")
                    return True
                else:
                    print(f"❌ Authentication failed: No access token in response")
                    return False
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def test_ai_model_status(self) -> bool:
        """Test AI model status"""
        try:
            response = self.session.post(f"{BASE_URL}/test/ai-processing")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("data", {}).get("ai_model_status") == "active":
                    print("✅ AI model is active and working")
                    print(f"   Model loaded: {result['data']['model_info']['model_loaded']}")
                    print(f"   Confidence threshold: {result['data']['model_info']['confidence_threshold']}")
                    return True
                else:
                    print("❌ AI model not active")
                    return False
            else:
                print(f"❌ AI model test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ AI model test error: {e}")
            return False

    def test_camera_creation(self) -> bool:
        """Test creating camera"""
        try:
            camera_data = {
                "name": CAMERA_CONFIG["name"],
                "location": CAMERA_CONFIG["location"],
                "stream_url": CAMERA_CONFIG["stream_url"],
                "status": "active"  # Set active for AI processing
            }
            
            response = self.session.post(f"{BASE_URL}/cameras", json=camera_data)
            
            if response.status_code == 201:
                response_data = response.json()
                if response_data.get("success") and response_data.get("data"):
                    camera = response_data["data"]
                    self.test_camera_id = camera.get("id")
                    print(f"✅ Camera created successfully with ID: {self.test_camera_id}")
                    print(f"   Name: {camera.get('name')}")
                    print(f"   Status: {camera.get('status')}")
                    return True
                else:
                    print(f"❌ Camera creation failed: Invalid response format")
                    return False
            else:
                print(f"❌ Camera creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Camera creation error: {e}")
            return False

    def test_camera_ai_processing(self) -> bool:
        """Test camera AI processing"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            response = self.session.post(f"{BASE_URL}/cameras/{self.test_camera_id}/test-ai")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    ai_results = result.get("data", {}).get("ai_processing_results", {})
                    print("✅ Camera AI processing test completed")
                    print(f"   Frames processed: {ai_results.get('frames_processed')}")
                    print(f"   Average count: {ai_results.get('average_count')}")
                    print(f"   Average confidence: {ai_results.get('average_confidence')}")
                    print(f"   Processing time: {ai_results.get('processing_time')}")
                    return True
                else:
                    print("❌ Camera AI processing failed")
                    return False
            else:
                print(f"❌ Camera AI processing test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Camera AI processing error: {e}")
            return False

    def test_worker_pool_status(self) -> bool:
        """Test worker pool status"""
        try:
            response = self.session.get(f"{BASE_URL}/workers/status")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    workers = result.get("data", {}).get("workers", [])
                    print("✅ Worker pool status check successful")
                    print(f"   Total Workers: {len(workers)}")
                    
                    ai_workers = [w for w in workers if w.get("ai_model_loaded")]
                    print(f"   AI Model Workers: {len(ai_workers)}")
                    
                    active_workers = [w for w in workers if w.get("status") == "busy"]
                    print(f"   Active Workers: {len(active_workers)}")
                    
                    return True
                else:
                    print("❌ Worker pool status check failed")
                    return False
            else:
                print(f"❌ Worker pool status check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Worker pool status check error: {e}")
            return False

    def test_camera_processing_start(self) -> bool:
        """Test starting camera processing"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            response = self.session.post(f"{BASE_URL}/cameras/{self.test_camera_id}/start")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Camera processing started")
                print(f"   Status: {result.get('status')}")
                print(f"   Message: {result.get('message')}")
                return True
            else:
                print(f"❌ Camera processing start failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Camera processing start error: {e}")
            return False

    def test_camera_deletion(self) -> bool:
        """Test deleting test camera"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            response = self.session.delete(f"{BASE_URL}/cameras/{self.test_camera_id}")
            
            if response.status_code == 200:
                print("✅ Test camera deleted successfully")
                return True
            else:
                print(f"❌ Camera deletion failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Camera deletion error: {e}")
            return False

    def run_all_tests(self) -> Dict[str, bool]:
        """Run all AI camera tests"""
        print("🚀 Starting AI Camera Test Suite")
        print("=" * 50)
        
        test_results = {}
        
        # Test 1: Authentication
        print("\n1. Testing Authentication...")
        test_results['auth'] = self.setup_auth()
        
        if not test_results['auth']:
            print("❌ Authentication failed, skipping remaining tests")
            return test_results
        
        # Test 2: AI Model Status
        print("\n2. Testing AI Model Status...")
        test_results['ai_model'] = self.test_ai_model_status()
        
        # Test 3: Worker Pool Status
        print("\n3. Testing Worker Pool Status...")
        test_results['worker_pool'] = self.test_worker_pool_status()
        
        # Test 4: Camera Creation
        print("\n4. Testing Camera Creation...")
        test_results['camera_creation'] = self.test_camera_creation()
        
        # Test 5: Camera AI Processing
        print("\n5. Testing Camera AI Processing...")
        test_results['camera_ai'] = self.test_camera_ai_processing()
        
        # Test 6: Camera Processing Start
        print("\n6. Testing Camera Processing Start...")
        test_results['processing_start'] = self.test_camera_processing_start()
        
        # Test 7: Camera Deletion
        print("\n7. Testing Camera Deletion...")
        test_results['camera_deletion'] = self.test_camera_deletion()
        
        # Print results
        print("\n" + "=" * 50)
        print("📊 AI Camera Test Results")
        print("=" * 50)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        print(f"\nOverall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Some tests failed. Check the logs above.")
        
        return test_results

def main():
    """Main function"""
    test_suite = AICameraTest()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main() 
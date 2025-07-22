#!/usr/bin/env python3
"""
RTSP Camera Test Suite
Based on camera configuration from NAS(RTSP) mobile app
"""

import requests
import json
import time
import subprocess
import sys
import os
from typing import Dict, Any, Optional

# Test configuration based on the camera image
CAMERA_CONFIG = {
    "name": "Test RTSP Camera",
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

class RTSPCameraTest:
    def __init__(self):
        self.auth_token = None
        self.test_camera_id = None
        self.session = requests.Session()
        
    def setup_auth(self) -> bool:
        """Setup authentication for API calls"""
        try:
            # Login to get auth token
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

    def test_rtsp_url_parsing(self) -> bool:
        """Test RTSP URL parsing and validation"""
        try:
            # Test URL parsing
            url = CAMERA_CONFIG["stream_url"]
            expected_parts = {
                "protocol": "rtsp",
                "username": CAMERA_CONFIG["username"],
                "password": CAMERA_CONFIG["password"],
                "ip": CAMERA_CONFIG["ip_address"],
                "port": CAMERA_CONFIG["port"],
                "path": CAMERA_CONFIG["source_path"]
            }
            
            print(f"Testing RTSP URL: {url}")
            print(f"Expected IP: {expected_parts['ip']}")
            print(f"Expected Port: {expected_parts['port']}")
            print(f"Expected Path: {expected_parts['path']}")
            
            # Basic URL validation
            if not url.startswith("rtsp://"):
                print("❌ Invalid RTSP protocol")
                return False
                
            if CAMERA_CONFIG["ip_address"] not in url:
                print("❌ IP address not found in URL")
                return False
                
            print("✅ RTSP URL parsing successful")
            return True
            
        except Exception as e:
            print(f"❌ RTSP URL parsing error: {e}")
            return False

    def test_camera_creation_with_rtsp(self) -> bool:
        """Test creating camera with RTSP configuration"""
        try:
            camera_data = {
                "name": CAMERA_CONFIG["name"],
                "location": CAMERA_CONFIG["location"],
                "stream_url": CAMERA_CONFIG["stream_url"],
                "status": "offline"  # Start offline for testing
            }
            
            response = self.session.post(f"{BASE_URL}/cameras", json=camera_data)
            
            if response.status_code == 201:
                response_data = response.json()
                if response_data.get("success") and response_data.get("data"):
                    camera = response_data["data"]
                    self.test_camera_id = camera.get("id")
                    print(f"✅ Camera created successfully with ID: {self.test_camera_id}")
                    print(f"   Name: {camera.get('name')}")
                    print(f"   Location: {camera.get('location')}")
                    print(f"   Stream URL: {camera.get('stream_url')}")
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

    def test_camera_rtsp_connection(self) -> bool:
        """Test RTSP connection to camera"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            # Test camera connection endpoint
            response = self.session.post(f"{BASE_URL}/cameras/{self.test_camera_id}/test-connection")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ RTSP connection test completed")
                print(f"   Connection Status: {result.get('status')}")
                print(f"   Message: {result.get('message')}")
                return result.get('status') == 'success'
            else:
                print(f"❌ RTSP connection test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ RTSP connection test error: {e}")
            return False

    def test_camera_processing_start(self) -> bool:
        """Test starting camera processing"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            # Start camera processing
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

    def test_camera_processing_status(self) -> bool:
        """Test camera processing status"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            # Check camera status
            response = self.session.get(f"{BASE_URL}/cameras/{self.test_camera_id}")
            
            if response.status_code == 200:
                camera = response.json()
                status = camera.get('status')
                print(f"✅ Camera status: {status}")
                return status in ['active', 'processing']
            else:
                print(f"❌ Camera status check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Camera status check error: {e}")
            return False

    def test_worker_pool_status(self) -> bool:
        """Test worker pool status"""
        try:
            response = self.session.get(f"{BASE_URL}/workers/status")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Worker pool status check successful")
                print(f"   Total Workers: {result.get('total_workers')}")
                print(f"   Active Workers: {result.get('active_workers')}")
                print(f"   Status: {result.get('status')}")
                return True
            else:
                print(f"❌ Worker pool status check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Worker pool status check error: {e}")
            return False

    def test_camera_processing_stop(self) -> bool:
        """Test stopping camera processing"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            # Stop camera processing
            response = self.session.post(f"{BASE_URL}/cameras/{self.test_camera_id}/stop")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Camera processing stopped")
                print(f"   Status: {result.get('status')}")
                print(f"   Message: {result.get('message')}")
                return True
            else:
                print(f"❌ Camera processing stop failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Camera processing stop error: {e}")
            return False

    def test_camera_deletion(self) -> bool:
        """Test deleting test camera"""
        try:
            if not self.test_camera_id:
                print("❌ No test camera ID available")
                return False
                
            # Delete test camera
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
        """Run all RTSP camera tests"""
        print("🚀 Starting RTSP Camera Test Suite")
        print("=" * 50)
        
        test_results = {}
        
        # Test 1: Authentication
        print("\n1. Testing Authentication...")
        test_results['auth'] = self.setup_auth()
        
        if not test_results['auth']:
            print("❌ Authentication failed, skipping remaining tests")
            return test_results
        
        # Test 2: RTSP URL Parsing
        print("\n2. Testing RTSP URL Parsing...")
        test_results['rtsp_parsing'] = self.test_rtsp_url_parsing()
        
        # Test 3: Camera Creation
        print("\n3. Testing Camera Creation...")
        test_results['camera_creation'] = self.test_camera_creation_with_rtsp()
        
        if test_results['camera_creation']:
            # Test 4: Worker Pool Status
            print("\n4. Testing Worker Pool Status...")
            test_results['worker_pool'] = self.test_worker_pool_status()
            
            # Test 5: RTSP Connection Test
            print("\n5. Testing RTSP Connection...")
            test_results['rtsp_connection'] = self.test_camera_rtsp_connection()
            
            # Test 6: Camera Processing Start
            print("\n6. Testing Camera Processing Start...")
            test_results['processing_start'] = self.test_camera_processing_start()
            
            if test_results['processing_start']:
                # Wait a moment for processing to start
                time.sleep(2)
                
                # Test 7: Camera Processing Status
                print("\n7. Testing Camera Processing Status...")
                test_results['processing_status'] = self.test_camera_processing_status()
                
                # Test 8: Camera Processing Stop
                print("\n8. Testing Camera Processing Stop...")
                test_results['processing_stop'] = self.test_camera_processing_stop()
            
            # Test 9: Camera Deletion
            print("\n9. Testing Camera Deletion...")
            test_results['camera_deletion'] = self.test_camera_deletion()
        
        return test_results

def main():
    """Main test execution"""
    test_suite = RTSPCameraTest()
    results = test_suite.run_all_tests()
    
    print("\n" + "=" * 50)
    print("📊 RTSP Camera Test Results")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All RTSP camera tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
"""
Automation Tests for Face Detection System API
Comprehensive test suite for all API endpoints and functionality.
"""

import requests
import json
import time
import os
import sys
import pytest
from pathlib import Path
from typing import Dict, Any, Optional
import cv2
import numpy as np
from PIL import Image
import io

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from utils.logger import setup_logger

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_IMAGES_DIR = Path(__file__).parent / "test_images"
LOGS_DIR = Path(__file__).parent.parent / "logs"

# Setup logging
logger = setup_logger("face_detection_tests", log_file=str(LOGS_DIR / "test_results.log"))

class FaceDetectionAPITest:
    """Test class for Face Detection API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.test_images = {}
        self.setup_test_images()
    
    def setup_test_images(self):
        """Setup test images for testing"""
        # Create test images directory
        TEST_IMAGES_DIR.mkdir(exist_ok=True)
        
        # Generate test images if they don't exist
        self.generate_test_images()
    
    def generate_test_images(self):
        """Generate test images for face detection"""
        # Create a simple test image with a face-like pattern
        test_image = np.zeros((300, 300, 3), dtype=np.uint8)
        
        # Draw a simple face-like pattern
        # Face outline
        cv2.circle(test_image, (150, 150), 80, (255, 255, 255), -1)
        # Eyes
        cv2.circle(test_image, (130, 130), 10, (0, 0, 0), -1)
        cv2.circle(test_image, (170, 130), 10, (0, 0, 0), -1)
        # Nose
        cv2.circle(test_image, (150, 160), 5, (0, 0, 0), -1)
        # Mouth
        cv2.ellipse(test_image, (150, 180), (20, 10), 0, 0, 180, (0, 0, 0), 2)
        
        # Save test images
        test_image_path = TEST_IMAGES_DIR / "test_face.jpg"
        cv2.imwrite(str(test_image_path), test_image)
        
        # Convert to PIL Image for API testing
        pil_image = Image.fromarray(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        
        # Save as bytes for API testing
        img_bytes = io.BytesIO()
        pil_image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        self.test_images['face'] = {
            'path': test_image_path,
            'bytes': img_bytes,
            'pil': pil_image
        }
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", data: Dict[str, Any] = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "details": details,
            "data": data or {}
        }
        
        self.test_results.append(result)
        
        if success:
            logger.info(f"✅ {test_name}: PASSED - {details}")
        else:
            logger.error(f"❌ {test_name}: FAILED - {details}")
    
    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('status') == 'healthy':
                    self.log_test_result("Health Check", True, "System is healthy")
                    return True
                else:
                    self.log_test_result("Health Check", False, "Health check returned unhealthy status")
                    return False
            else:
                self.log_test_result("Health Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'endpoints' in data.get('data', {}):
                    self.log_test_result("Root Endpoint", True, "Root endpoint accessible")
                    return True
                else:
                    self.log_test_result("Root Endpoint", False, "Invalid response format")
                    return False
            else:
                self.log_test_result("Root Endpoint", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Root Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_face_registration(self) -> bool:
        """Test face registration endpoint"""
        try:
            # Prepare test data
            test_image = self.test_images['face']['bytes']
            test_data = {
                'name': 'Test Person',
                'email': 'test@example.com',
                'phone': '1234567890',
                'notes': 'Test registration'
            }
            
            files = {'file': ('test_face.jpg', test_image, 'image/jpeg')}
            
            response = self.session.post(
                f"{API_BASE_URL}/api/v1/faces/upload",
                files=files,
                data=test_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'person_id' in data.get('data', {}):
                    self.log_test_result("Face Registration", True, "Face registered successfully")
                    return True
                else:
                    self.log_test_result("Face Registration", False, "Invalid response format")
                    return False
            else:
                self.log_test_result("Face Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("Face Registration", False, f"Exception: {str(e)}")
            return False
    
    def test_face_recognition(self) -> bool:
        """Test face recognition endpoint"""
        try:
            # Prepare test data
            test_image = self.test_images['face']['bytes']
            test_data = {'threshold': 0.6}
            
            files = {'file': ('test_face.jpg', test_image, 'image/jpeg')}
            
            response = self.session.post(
                f"{API_BASE_URL}/api/v1/faces/recognize",
                files=files,
                data=test_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test_result("Face Recognition", True, "Face recognition completed")
                    return True
                else:
                    self.log_test_result("Face Recognition", False, "Recognition failed")
                    return False
            else:
                self.log_test_result("Face Recognition", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("Face Recognition", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_status(self) -> bool:
        """Test camera status endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/api/v1/camera/status")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test_result("Camera Status", True, "Camera status retrieved")
                    return True
                else:
                    self.log_test_result("Camera Status", False, "Invalid response format")
                    return False
            else:
                self.log_test_result("Camera Status", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Camera Status", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_control(self) -> bool:
        """Test camera start/stop endpoints"""
        try:
            # Test camera start
            start_response = self.session.post(f"{API_BASE_URL}/api/v1/camera/start")
            
            if start_response.status_code == 200:
                self.log_test_result("Camera Start", True, "Camera started successfully")
            else:
                self.log_test_result("Camera Start", False, f"HTTP {start_response.status_code}")
                return False
            
            # Wait a moment
            time.sleep(2)
            
            # Test camera stop
            stop_response = self.session.post(f"{API_BASE_URL}/api/v1/camera/stop")
            
            if stop_response.status_code == 200:
                self.log_test_result("Camera Stop", True, "Camera stopped successfully")
                return True
            else:
                self.log_test_result("Camera Stop", False, f"HTTP {stop_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Camera Control", False, f"Exception: {str(e)}")
            return False
    
    def test_faces_list(self) -> bool:
        """Test faces list endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/api/v1/faces/list")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test_result("Faces List", True, "Faces list retrieved successfully")
                    return True
                else:
                    self.log_test_result("Faces List", False, "Invalid response format")
                    return False
            else:
                self.log_test_result("Faces List", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Faces List", False, f"Exception: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling with invalid requests"""
        try:
            # Test with invalid file
            files = {'file': ('invalid.txt', b'invalid content', 'text/plain')}
            data = {'name': 'Test'}
            
            response = self.session.post(
                f"{API_BASE_URL}/api/v1/faces/upload",
                files=files,
                data=data
            )
            
            if response.status_code == 400:
                self.log_test_result("Error Handling", True, "Properly handled invalid file")
                return True
            else:
                self.log_test_result("Error Handling", False, f"Expected 400, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Error Handling", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        logger.info("🚀 Starting Face Detection API Tests")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("Face Registration", self.test_face_registration),
            ("Face Recognition", self.test_face_recognition),
            ("Camera Status", self.test_camera_status),
            ("Camera Control", self.test_camera_control),
            ("Faces List", self.test_faces_list),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test_result(test_name, False, f"Test exception: {str(e)}")
        
        # Generate summary
        summary = {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": (passed / total) * 100 if total > 0 else 0,
            "test_results": self.test_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"📊 Test Summary: {passed}/{total} tests passed ({summary['success_rate']:.1f}%)")
        
        return summary

def main():
    """Main test runner"""
    # Create logs directory
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Run tests
    tester = FaceDetectionAPITest()
    results = tester.run_all_tests()
    
    # Save results
    results_file = LOGS_DIR / f"test_results_{int(time.time())}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"📄 Test results saved to: {results_file}")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Face Detection API Test Results")
    print(f"{'='*50}")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"{'='*50}")
    
    # Exit with appropriate code
    if results['passed'] == results['total_tests']:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🔍 Debug Logging Script
Trace lỗi chi tiết theo từng step
"""

import requests
import json
import time
import os
import logging
from datetime import datetime

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('debug_trace.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DebugTracer:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.test_results = []
        
    def log_step(self, step_name, status, details=""):
        """Log detailed step information"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        logger.info(f"🔍 STEP: {step_name} | STATUS: {status} | TIME: {timestamp}")
        if details:
            logger.debug(f"📝 DETAILS: {details}")
        
        result = {
            "step": step_name,
            "status": status,
            "details": details,
            "timestamp": timestamp
        }
        self.test_results.append(result)
        
    def test_api_server_startup(self):
        """Test 1: API Server Startup"""
        logger.info("=" * 60)
        logger.info("🚀 TEST 1: API Server Startup")
        logger.info("=" * 60)
        
        try:
            # Step 1.1: Check if server is running
            self.log_step("1.1", "START", "Checking if API server is running")
            response = requests.get(f"{self.api_base}/health", timeout=5)
            
            if response.status_code == 200:
                self.log_step("1.1", "PASS", f"Server is running, status: {response.status_code}")
                data = response.json()
                logger.debug(f"Health response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log_step("1.1", "FAIL", f"Server returned status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError as e:
            self.log_step("1.1", "FAIL", f"Connection error: {e}")
            logger.error(f"Connection failed: {e}")
            return False
        except Exception as e:
            self.log_step("1.1", "ERROR", f"Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}")
            return False
            
    def test_face_upload_workflow(self):
        """Test 2: Face Upload Workflow"""
        logger.info("=" * 60)
        logger.info("📤 TEST 2: Face Upload Workflow")
        logger.info("=" * 60)
        
        try:
            # Step 2.1: Create test image
            self.log_step("2.1", "START", "Creating test image")
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            test_image_path = 'debug_test_image.jpg'
            img.save(test_image_path)
            self.log_step("2.1", "PASS", f"Test image created: {test_image_path}")
            
            # Step 2.2: Prepare upload data
            self.log_step("2.2", "START", "Preparing upload data")
            upload_data = {
                'name': 'DebugTestUser',
                'email': 'debug@test.com'
            }
            self.log_step("2.2", "PASS", f"Upload data prepared: {upload_data}")
            
            # Step 2.3: Upload image
            self.log_step("2.3", "START", "Uploading image to API")
            with open(test_image_path, 'rb') as f:
                files = {'file': f}
                logger.debug(f"Files: {list(files.keys())}")
                logger.debug(f"Data: {upload_data}")
                
                response = requests.post(
                    f"{self.api_base}/api/v1/faces/upload",
                    files=files,
                    data=upload_data,
                    timeout=30
                )
            
            # Step 2.4: Analyze response
            self.log_step("2.4", "START", f"Analyzing response (status: {response.status_code})")
            logger.debug(f"Response headers: {dict(response.headers)}")
            logger.debug(f"Response content: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                self.log_step("2.4", "PASS", "Upload successful")
                logger.debug(f"Response data: {json.dumps(data, indent=2)}")
            else:
                self.log_step("2.4", "FAIL", f"Upload failed with status: {response.status_code}")
                logger.error(f"Error response: {response.text}")
            
            # Cleanup
            os.remove(test_image_path)
            self.log_step("2.5", "PASS", "Test image cleaned up")
            
            return response.status_code == 200
            
        except Exception as e:
            self.log_step("2.3", "ERROR", f"Upload workflow error: {e}")
            logger.error(f"Upload workflow failed: {e}")
            return False
            
    def test_face_recognition_workflow(self):
        """Test 3: Face Recognition Workflow"""
        logger.info("=" * 60)
        logger.info("🔍 TEST 3: Face Recognition Workflow")
        logger.info("=" * 60)
        
        try:
            # Step 3.1: Create test image for recognition
            self.log_step("3.1", "START", "Creating test image for recognition")
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='blue')
            test_image_path = 'debug_recognition_image.jpg'
            img.save(test_image_path)
            self.log_step("3.1", "PASS", f"Recognition test image created: {test_image_path}")
            
            # Step 3.2: Send recognition request
            self.log_step("3.2", "START", "Sending recognition request")
            with open(test_image_path, 'rb') as f:
                files = {'file': f}
                logger.debug(f"Recognition files: {list(files.keys())}")
                
                response = requests.post(
                    f"{self.api_base}/api/v1/faces/recognize",
                    files=files,
                    timeout=30
                )
            
            # Step 3.3: Analyze recognition response
            self.log_step("3.3", "START", f"Analyzing recognition response (status: {response.status_code})")
            logger.debug(f"Recognition response headers: {dict(response.headers)}")
            logger.debug(f"Recognition response content: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                self.log_step("3.3", "PASS", "Recognition request successful")
                logger.debug(f"Recognition data: {json.dumps(data, indent=2)}")
            else:
                self.log_step("3.3", "FAIL", f"Recognition failed with status: {response.status_code}")
                logger.error(f"Recognition error response: {response.text}")
            
            # Cleanup
            os.remove(test_image_path)
            self.log_step("3.4", "PASS", "Recognition test image cleaned up")
            
            return response.status_code == 200
            
        except Exception as e:
            self.log_step("3.2", "ERROR", f"Recognition workflow error: {e}")
            logger.error(f"Recognition workflow failed: {e}")
            return False
            
    def test_database_operations(self):
        """Test 4: Database Operations"""
        logger.info("=" * 60)
        logger.info("🗄️ TEST 4: Database Operations")
        logger.info("=" * 60)
        
        try:
            # Step 4.1: List faces
            self.log_step("4.1", "START", "Testing face list endpoint")
            response = requests.get(f"{self.api_base}/api/v1/faces/list", timeout=10)
            
            self.log_step("4.1", "START", f"Analyzing list response (status: {response.status_code})")
            logger.debug(f"List response headers: {dict(response.headers)}")
            logger.debug(f"List response content: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                faces = data.get('data', {}).get('faces', [])
                self.log_step("4.1", "PASS", f"List faces successful, found {len(faces)} faces")
                logger.debug(f"Faces data: {json.dumps(data, indent=2)}")
            else:
                self.log_step("4.1", "FAIL", f"List faces failed with status: {response.status_code}")
                logger.error(f"List faces error response: {response.text}")
            
            return response.status_code == 200
            
        except Exception as e:
            self.log_step("4.1", "ERROR", f"Database operations error: {e}")
            logger.error(f"Database operations failed: {e}")
            return False
            
    def run_comprehensive_debug(self):
        """Run comprehensive debug with detailed logging"""
        logger.info("🔍 Starting Comprehensive Debug Session")
        logger.info("=" * 80)
        
        # Test 1: API Server
        server_ok = self.test_api_server_startup()
        
        if server_ok:
            # Test 2: Upload Workflow
            upload_ok = self.test_face_upload_workflow()
            
            # Test 3: Recognition Workflow
            recognition_ok = self.test_face_recognition_workflow()
            
            # Test 4: Database Operations
            db_ok = self.test_database_operations()
        else:
            logger.error("❌ API server not available, skipping other tests")
            upload_ok = recognition_ok = db_ok = False
        
        # Summary
        logger.info("=" * 80)
        logger.info("📊 DEBUG SUMMARY:")
        logger.info(f"✅ API Server: {'PASS' if server_ok else 'FAIL'}")
        logger.info(f"✅ Upload Workflow: {'PASS' if upload_ok else 'FAIL'}")
        logger.info(f"✅ Recognition Workflow: {'PASS' if recognition_ok else 'FAIL'}")
        logger.info(f"✅ Database Operations: {'PASS' if db_ok else 'FAIL'}")
        
        # Save detailed results
        with open('debug_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        logger.info("💾 Detailed results saved to: debug_results.json")
        
        return all([server_ok, upload_ok, recognition_ok, db_ok])

if __name__ == "__main__":
    tracer = DebugTracer()
    success = tracer.run_comprehensive_debug()
    exit(0 if success else 1) 
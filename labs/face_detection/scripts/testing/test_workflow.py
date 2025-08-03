#!/usr/bin/env python3
"""
🔍 Face Embedding Workflow Test Script
Test toàn bộ workflow từ Frontend → Backend → Database
"""

import requests
import json
import time
import os
import sqlite3
from pathlib import Path

class FaceEmbeddingWorkflowTest:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {message}")
        
    def test_api_health(self):
        """Test 1.1: API Server Health Check"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("API Health Check", "✅ PASS", "Server is healthy")
                    return True
                else:
                    self.log_test("API Health Check", "❌ FAIL", "Health check failed")
                    return False
            else:
                self.log_test("API Health Check", "❌ FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("API Health Check", "❌ FAIL", f"Connection error: {e}")
            return False
            
    def test_database_connection(self):
        """Test 1.3: Database Connection"""
        try:
            # Test vector database
            vector_db_path = "data/face_vectors.db"
            if os.path.exists(vector_db_path):
                conn = sqlite3.connect(vector_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM face_embeddings")
                count = cursor.fetchone()[0]
                conn.close()
                self.log_test("Database Connection", "✅ PASS", f"Vector DB: {count} faces")
                return True
            else:
                self.log_test("Database Connection", "⚠️ WARN", "Vector DB file not found")
                return True
        except Exception as e:
            self.log_test("Database Connection", "❌ FAIL", f"DB error: {e}")
            return False
            
    def test_face_upload_workflow(self):
        """Test 2.1-2.6: Face Upload Workflow"""
        try:
            # Create a simple test image (1x1 pixel)
            test_image_path = "test_image.jpg"
            with open(test_image_path, "wb") as f:
                f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
            
            # Upload test image
            with open(test_image_path, "rb") as f:
                files = {"file": f}
                data = {"name": "TestUser", "email": "test@example.com"}
                response = requests.post(f"{self.api_base}/api/v1/faces/upload", 
                                      files=files, data=data, timeout=30)
            
            # Clean up test image
            os.remove(test_image_path)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Face Upload Workflow", "✅ PASS", "Face uploaded successfully")
                    return True
                else:
                    self.log_test("Face Upload Workflow", "❌ FAIL", data.get("message", "Unknown error"))
                    return False
            else:
                self.log_test("Face Upload Workflow", "❌ FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Face Upload Workflow", "❌ FAIL", f"Upload error: {e}")
            return False
            
    def test_face_recognition_workflow(self):
        """Test 3.1-3.5: Face Recognition Workflow"""
        try:
            # Create a simple test image for recognition
            test_image_path = "test_recognition.jpg"
            with open(test_image_path, "wb") as f:
                f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
            
            # Test recognition
            with open(test_image_path, "rb") as f:
                files = {"file": f}
                response = requests.post(f"{self.api_base}/api/v1/faces/recognize", 
                                      files=files, timeout=30)
            
            # Clean up test image
            os.remove(test_image_path)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Face Recognition Workflow", "✅ PASS", "Recognition successful")
                    return True
                else:
                    self.log_test("Face Recognition Workflow", "⚠️ WARN", data.get("message", "No face found"))
                    return True  # This might be expected if no faces in DB
            else:
                self.log_test("Face Recognition Workflow", "❌ FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Face Recognition Workflow", "❌ FAIL", f"Recognition error: {e}")
            return False
            
    def test_face_list_endpoint(self):
        """Test: Face List Endpoint"""
        try:
            response = requests.get(f"{self.api_base}/api/v1/faces/list", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    faces = data.get("data", {}).get("faces", [])
                    self.log_test("Face List Endpoint", "✅ PASS", f"Found {len(faces)} faces")
                    return True
                else:
                    self.log_test("Face List Endpoint", "❌ FAIL", data.get("message", "Unknown error"))
                    return False
            else:
                self.log_test("Face List Endpoint", "❌ FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Face List Endpoint", "❌ FAIL", f"List error: {e}")
            return False
            
    def test_frontend_server(self):
        """Test 4.1: Frontend Server"""
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Server", "✅ PASS", "Frontend is accessible")
                return True
            else:
                self.log_test("Frontend Server", "❌ FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Frontend Server", "❌ FAIL", f"Frontend error: {e}")
            return False
            
    def run_all_tests(self):
        """Run all tests"""
        print("🔍 Starting Face Embedding Workflow Tests...")
        print("=" * 60)
        
        # Phase 1: Backend API Testing
        print("\n📋 Phase 1: Backend API Testing")
        self.test_api_health()
        self.test_database_connection()
        
        # Phase 2: Face Upload Workflow
        print("\n📋 Phase 2: Face Upload Workflow")
        self.test_face_upload_workflow()
        
        # Phase 3: Face Recognition Workflow
        print("\n📋 Phase 3: Face Recognition Workflow")
        self.test_face_recognition_workflow()
        
        # Phase 4: Additional API Tests
        print("\n📋 Phase 4: Additional API Tests")
        self.test_face_list_endpoint()
        self.test_frontend_server()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary:")
        passed = sum(1 for r in self.test_results if r["status"] == "✅ PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "❌ FAIL")
        warned = sum(1 for r in self.test_results if r["status"] == "⚠️ WARN")
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Warnings: {warned}")
        print(f"📈 Total: {len(self.test_results)}")
        
        # Save results
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n💾 Results saved to: test_results.json")
        
        return failed == 0

if __name__ == "__main__":
    tester = FaceEmbeddingWorkflowTest()
    success = tester.run_all_tests()
    exit(0 if success else 1) 
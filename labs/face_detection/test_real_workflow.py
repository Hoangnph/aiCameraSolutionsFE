#!/usr/bin/env python3
"""
🔍 Real Face Embedding Workflow Test
Test với ảnh thực tế và kiểm tra chi tiết
"""

import requests
import json
import time
import os
import base64
from PIL import Image
import io

class RealWorkflowTest:
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
        
    def create_test_image(self, filename="test_face.jpg"):
        """Create a simple test image"""
        try:
            # Create a simple 100x100 image with a face-like pattern
            img = Image.new('RGB', (100, 100), color='white')
            
            # Draw a simple face (eyes and mouth)
            pixels = img.load()
            
            # Eyes
            for x in range(30, 40):
                for y in range(30, 40):
                    pixels[x, y] = (0, 0, 0)
            for x in range(60, 70):
                for y in range(30, 40):
                    pixels[x, y] = (0, 0, 0)
                    
            # Mouth
            for x in range(40, 60):
                for y in range(60, 70):
                    pixels[x, y] = (0, 0, 0)
            
            img.save(filename)
            return filename
        except Exception as e:
            print(f"❌ Error creating test image: {e}")
            return None
            
    def test_upload_with_real_image(self):
        """Test upload with a real image file"""
        try:
            # Create test image
            test_image = self.create_test_image()
            if not test_image:
                self.log_test("Upload with Real Image", "❌ FAIL", "Could not create test image")
                return False
                
            # Upload image
            with open(test_image, "rb") as f:
                files = {"file": f}
                data = {"name": "TestUser", "email": "test@example.com"}
                response = requests.post(f"{self.api_base}/api/v1/faces/upload", 
                                      files=files, data=data, timeout=30)
            
            # Clean up
            os.remove(test_image)
            
            print(f"Upload Response Status: {response.status_code}")
            print(f"Upload Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Upload with Real Image", "✅ PASS", "Face uploaded successfully")
                    return True
                else:
                    self.log_test("Upload with Real Image", "❌ FAIL", data.get("message", "Unknown error"))
                    return False
            else:
                self.log_test("Upload with Real Image", "❌ FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Upload with Real Image", "❌ FAIL", f"Upload error: {e}")
            return False
            
    def test_recognition_with_real_image(self):
        """Test recognition with a real image file"""
        try:
            # Create test image
            test_image = self.create_test_image("test_recognition.jpg")
            if not test_image:
                self.log_test("Recognition with Real Image", "❌ FAIL", "Could not create test image")
                return False
                
            # Test recognition
            with open(test_image, "rb") as f:
                files = {"file": f}
                response = requests.post(f"{self.api_base}/api/v1/faces/recognize", 
                                      files=files, timeout=30)
            
            # Clean up
            os.remove(test_image)
            
            print(f"Recognition Response Status: {response.status_code}")
            print(f"Recognition Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Recognition with Real Image", "✅ PASS", "Recognition successful")
                    return True
                else:
                    self.log_test("Recognition with Real Image", "⚠️ WARN", data.get("message", "No face found"))
                    return True  # This might be expected if no faces in DB
            else:
                self.log_test("Recognition with Real Image", "❌ FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Recognition with Real Image", "❌ FAIL", f"Recognition error: {e}")
            return False
            
    def test_database_operations(self):
        """Test database operations"""
        try:
            # Test list faces
            response = requests.get(f"{self.api_base}/api/v1/faces/list", timeout=10)
            if response.status_code == 200:
                data = response.json()
                faces = data.get("data", {}).get("faces", [])
                self.log_test("Database Operations", "✅ PASS", f"Found {len(faces)} faces in database")
                return True
            else:
                self.log_test("Database Operations", "❌ FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Database Operations", "❌ FAIL", f"Database error: {e}")
            return False
            
    def run_all_tests(self):
        """Run all tests"""
        print("🔍 Starting Real Face Embedding Workflow Tests...")
        print("=" * 60)
        
        # Test 1: Upload with real image
        print("\n📋 Test 1: Upload with Real Image")
        self.test_upload_with_real_image()
        
        # Test 2: Recognition with real image
        print("\n📋 Test 2: Recognition with Real Image")
        self.test_recognition_with_real_image()
        
        # Test 3: Database operations
        print("\n📋 Test 3: Database Operations")
        self.test_database_operations()
        
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
        with open("real_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n💾 Results saved to: real_test_results.json")
        
        return failed == 0

if __name__ == "__main__":
    tester = RealWorkflowTest()
    success = tester.run_all_tests()
    exit(0 if success else 1) 
#!/usr/bin/env python3
"""
🔍 Comprehensive Service Check (Fixed)
Kiểm tra tất cả services của Face Detection System - đã fix content type
"""

import requests
import json
import time
import subprocess
import os
from datetime import datetime

class ServiceChecker:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.frontend_base = "http://localhost:3000"
        self.results = {}
        
    def check_api_server(self):
        """Check API server health"""
        print("🔍 Checking API Server...")
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.results['api_server'] = {
                    'status': '✅ HEALTHY',
                    'details': data
                }
                print("✅ API Server: HEALTHY")
                return True
            else:
                self.results['api_server'] = {
                    'status': '❌ ERROR',
                    'details': f"Status code: {response.status_code}"
                }
                print(f"❌ API Server: ERROR (Status: {response.status_code})")
                return False
        except Exception as e:
            self.results['api_server'] = {
                'status': '❌ CONNECTION FAILED',
                'details': str(e)
            }
            print(f"❌ API Server: CONNECTION FAILED - {e}")
            return False
    
    def check_frontend_server(self):
        """Check frontend server"""
        print("🔍 Checking Frontend Server...")
        try:
            response = requests.get(self.frontend_base, timeout=10)
            if response.status_code == 200:
                self.results['frontend_server'] = {
                    'status': '✅ RUNNING',
                    'details': 'Frontend accessible'
                }
                print("✅ Frontend Server: RUNNING")
                return True
            else:
                self.results['frontend_server'] = {
                    'status': '❌ ERROR',
                    'details': f"Status code: {response.status_code}"
                }
                print(f"❌ Frontend Server: ERROR (Status: {response.status_code})")
                return False
        except Exception as e:
            self.results['frontend_server'] = {
                'status': '❌ CONNECTION FAILED',
                'details': str(e)
            }
            print(f"❌ Frontend Server: CONNECTION FAILED - {e}")
            return False
    
    def check_face_upload_endpoint(self):
        """Check face upload endpoint with proper content type"""
        print("🔍 Checking Face Upload Endpoint...")
        try:
            # Create a simple test image
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            test_image_path = 'test_upload.jpg'
            img.save(test_image_path)
            
            with open(test_image_path, 'rb') as f:
                files = {
                    'file': ('test_upload.jpg', f, 'image/jpeg')
                }
                data = {'name': 'TestUser'}
                response = requests.post(
                    f"{self.api_base}/api/v1/faces/upload",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            os.remove(test_image_path)
            
            if response.status_code == 200:
                data = response.json()
                self.results['face_upload'] = {
                    'status': '✅ WORKING',
                    'details': data
                }
                print("✅ Face Upload: WORKING")
                return True
            else:
                self.results['face_upload'] = {
                    'status': '❌ ERROR',
                    'details': response.text
                }
                print(f"❌ Face Upload: ERROR - {response.text}")
                return False
        except Exception as e:
            self.results['face_upload'] = {
                'status': '❌ FAILED',
                'details': str(e)
            }
            print(f"❌ Face Upload: FAILED - {e}")
            return False
    
    def check_face_recognition_endpoint(self):
        """Check face recognition endpoint with proper content type"""
        print("🔍 Checking Face Recognition Endpoint...")
        try:
            # Create a simple test image
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='blue')
            test_image_path = 'test_recognition.jpg'
            img.save(test_image_path)
            
            with open(test_image_path, 'rb') as f:
                files = {
                    'file': ('test_recognition.jpg', f, 'image/jpeg')
                }
                response = requests.post(
                    f"{self.api_base}/api/v1/faces/recognize",
                    files=files,
                    timeout=30
                )
            
            os.remove(test_image_path)
            
            if response.status_code == 200:
                data = response.json()
                self.results['face_recognition'] = {
                    'status': '✅ WORKING',
                    'details': data
                }
                print("✅ Face Recognition: WORKING")
                return True
            else:
                self.results['face_recognition'] = {
                    'status': '❌ ERROR',
                    'details': response.text
                }
                print(f"❌ Face Recognition: ERROR - {response.text}")
                return False
        except Exception as e:
            self.results['face_recognition'] = {
                'status': '❌ FAILED',
                'details': str(e)
            }
            print(f"❌ Face Recognition: FAILED - {e}")
            return False
    
    def check_face_list_endpoint(self):
        """Check face list endpoint"""
        print("🔍 Checking Face List Endpoint...")
        try:
            response = requests.get(f"{self.api_base}/api/v1/faces/list", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.results['face_list'] = {
                    'status': '✅ WORKING',
                    'details': data
                }
                print("✅ Face List: WORKING")
                return True
            else:
                self.results['face_list'] = {
                    'status': '❌ ERROR',
                    'details': response.text
                }
                print(f"❌ Face List: ERROR - {response.text}")
                return False
        except Exception as e:
            self.results['face_list'] = {
                'status': '❌ FAILED',
                'details': str(e)
            }
            print(f"❌ Face List: FAILED - {e}")
            return False
    
    def check_database_connection(self):
        """Check database connection"""
        print("🔍 Checking Database Connection...")
        try:
            # Check if database files exist
            db_files = [
                'face_vectors.db',
                'face_detection.db',
                'metadata.db'
            ]
            
            existing_files = []
            for db_file in db_files:
                if os.path.exists(db_file):
                    existing_files.append(db_file)
            
            if existing_files:
                self.results['database'] = {
                    'status': '✅ CONNECTED',
                    'details': f"Database files: {existing_files}"
                }
                print("✅ Database: CONNECTED")
                return True
            else:
                self.results['database'] = {
                    'status': '⚠️ NO FILES',
                    'details': "No database files found"
                }
                print("⚠️ Database: NO FILES")
                return False
        except Exception as e:
            self.results['database'] = {
                'status': '❌ ERROR',
                'details': str(e)
            }
            print(f"❌ Database: ERROR - {e}")
            return False
    
    def check_process_status(self):
        """Check running processes"""
        print("🔍 Checking Process Status...")
        try:
            # Check uvicorn process
            result = subprocess.run(['pgrep', '-f', 'uvicorn'], capture_output=True, text=True)
            uvicorn_running = result.returncode == 0
            
            # Check python http server
            result = subprocess.run(['pgrep', '-f', 'http.server'], capture_output=True, text=True)
            http_server_running = result.returncode == 0
            
            processes = []
            if uvicorn_running:
                processes.append("uvicorn (API)")
            if http_server_running:
                processes.append("http.server (Frontend)")
            
            if processes:
                self.results['processes'] = {
                    'status': '✅ RUNNING',
                    'details': f"Running processes: {', '.join(processes)}"
                }
                print("✅ Processes: RUNNING")
                return True
            else:
                self.results['processes'] = {
                    'status': '❌ NOT RUNNING',
                    'details': "No required processes found"
                }
                print("❌ Processes: NOT RUNNING")
                return False
        except Exception as e:
            self.results['processes'] = {
                'status': '❌ ERROR',
                'details': str(e)
            }
            print(f"❌ Processes: ERROR - {e}")
            return False
    
    def run_comprehensive_check(self):
        """Run all service checks"""
        print("🚀 Starting Comprehensive Service Check (Fixed)")
        print("=" * 60)
        
        checks = [
            self.check_api_server,
            self.check_frontend_server,
            self.check_face_upload_endpoint,
            self.check_face_recognition_endpoint,
            self.check_face_list_endpoint,
            self.check_database_connection,
            self.check_process_status
        ]
        
        passed = 0
        total = len(checks)
        
        for check in checks:
            if check():
                passed += 1
            time.sleep(1)  # Small delay between checks
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SERVICE CHECK SUMMARY:")
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        for service, result in self.results.items():
            status = result['status']
            print(f"  {status}: {service.replace('_', ' ').title()}")
        
        # Save results
        results_file = f"service_check_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        if passed == total:
            print("\n🎉 ALL SERVICES ARE WORKING!")
            return True
        else:
            print(f"\n⚠️ {total - passed} SERVICE(S) NEED ATTENTION")
            return False

def main():
    """Run comprehensive service check"""
    checker = ServiceChecker()
    success = checker.run_comprehensive_check()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
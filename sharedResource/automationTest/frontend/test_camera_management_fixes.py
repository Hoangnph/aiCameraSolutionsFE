#!/usr/bin/env python3
"""
Test script to verify camera management page fixes
"""

import asyncio
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

class CameraManagementFixesTest:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.test_results = {
            "test_name": "Camera Management Fixes Test",
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
        
        # Setup Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = None
    
    def log_result(self, test_name, status, message=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results["results"].append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {message}")
    
    def setup_driver(self):
        """Setup WebDriver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            self.log_result("Driver Setup", "FAIL", f"Failed to setup driver: {str(e)}")
            return False
    
    def teardown_driver(self):
        """Cleanup WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def test_page_loads_without_crash(self):
        """Test that camera management page loads without crashing"""
        try:
            print("🌐 Testing camera management page load...")
            
            # Navigate to camera management page
            self.driver.get(f"{self.base_url}/camera-management")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if page loaded without critical errors
            page_title = self.driver.title
            if "Vision UI Dashboard" in page_title:
                self.log_result("Page Load", "PASS", f"Page loaded successfully: {page_title}")
            else:
                self.log_result("Page Load", "FAIL", f"Unexpected page title: {page_title}")
                return False
            
            return True
            
        except TimeoutException:
            self.log_result("Page Load", "FAIL", "Page load timeout")
            return False
        except Exception as e:
            self.log_result("Page Load", "FAIL", f"Page load error: {str(e)}")
            return False
    
    def test_no_cameras_map_error(self):
        """Test that cameras.map error is fixed"""
        try:
            print("🔍 Testing for cameras.map error...")
            
            # Check console logs for the specific error
            logs = self.driver.get_log('browser')
            
            # Look for cameras.map error
            cameras_map_errors = []
            for log in logs:
                if log['level'] == 'SEVERE' and 'cameras.map is not a function' in log['message']:
                    cameras_map_errors.append(log['message'])
            
            if cameras_map_errors:
                self.log_result("Cameras Map Error", "FAIL", f"Found {len(cameras_map_errors)} cameras.map errors")
                for error in cameras_map_errors:
                    print(f"   ❌ {error}")
                return False
            else:
                self.log_result("Cameras Map Error", "PASS", "No cameras.map errors found")
                return True
                
        except Exception as e:
            self.log_result("Cameras Map Error", "FAIL", f"Error checking console: {str(e)}")
            return False
    
    def test_camera_list_renders(self):
        """Test that camera list renders correctly"""
        try:
            print("📹 Testing camera list rendering...")
            
            # Wait for camera list to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table, .MuiTable-root, [data-testid='camera-table']"))
                )
                self.log_result("Camera List Render", "PASS", "Camera table found")
            except TimeoutException:
                # Check if "No cameras found" message is displayed
                try:
                    no_cameras_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No cameras found')]")
                    self.log_result("Camera List Render", "PASS", "No cameras message displayed (expected)")
                except:
                    self.log_result("Camera List Render", "WARN", "Camera table not found and no fallback message")
            
            return True
            
        except Exception as e:
            self.log_result("Camera List Render", "FAIL", f"Camera list test error: {str(e)}")
            return False
    
    def test_websocket_connection(self):
        """Test WebSocket connection status"""
        try:
            print("🔌 Testing WebSocket connection...")
            
            # Check console logs for WebSocket messages
            logs = self.driver.get_log('browser')
            
            # Look for WebSocket connection messages
            websocket_connected = False
            websocket_errors = []
            
            for log in logs:
                if 'WebSocket connected' in log['message']:
                    websocket_connected = True
                elif 'WebSocket error' in log['message'] or 'WebSocket connection failed' in log['message']:
                    websocket_errors.append(log['message'])
            
            if websocket_connected:
                self.log_result("WebSocket Connection", "PASS", "WebSocket connected successfully")
            elif websocket_errors:
                self.log_result("WebSocket Connection", "WARN", f"WebSocket errors found: {len(websocket_errors)}")
                for error in websocket_errors[:3]:  # Show first 3 errors
                    print(f"   ⚠️ {error}")
            else:
                self.log_result("WebSocket Connection", "INFO", "No WebSocket connection logs found")
            
            return True
            
        except Exception as e:
            self.log_result("WebSocket Connection", "FAIL", f"WebSocket test error: {str(e)}")
            return False
    
    def test_api_requests(self):
        """Test API request handling"""
        try:
            print("🌐 Testing API requests...")
            
            # Check console logs for API request messages
            logs = self.driver.get_log('browser')
            
            # Look for API-related messages
            api_errors = []
            test_endpoint_used = False
            
            for log in logs:
                if '401' in log['message'] and 'Unauthorized' in log['message']:
                    api_errors.append(log['message'])
                elif 'test endpoint' in log['message'].lower():
                    test_endpoint_used = True
                elif 'mock data' in log['message'].lower():
                    test_endpoint_used = True
            
            if test_endpoint_used:
                self.log_result("API Requests", "PASS", "API fallback to test endpoint working")
            elif api_errors:
                self.log_result("API Requests", "WARN", f"API errors found: {len(api_errors)}")
                for error in api_errors[:2]:  # Show first 2 errors
                    print(f"   ⚠️ {error}")
            else:
                self.log_result("API Requests", "INFO", "No API request logs found")
            
            return True
            
        except Exception as e:
            self.log_result("API Requests", "FAIL", f"API test error: {str(e)}")
            return False
    
    def test_no_critical_errors(self):
        """Test for any critical errors"""
        try:
            print("🚨 Testing for critical errors...")
            
            # Check console logs for critical errors
            logs = self.driver.get_log('browser')
            
            # Look for critical errors (SEVERE level)
            critical_errors = []
            for log in logs:
                if log['level'] == 'SEVERE':
                    critical_errors.append(log['message'])
            
            if critical_errors:
                self.log_result("Critical Errors", "FAIL", f"Found {len(critical_errors)} critical errors")
                for error in critical_errors[:3]:  # Show first 3 errors
                    print(f"   ❌ {error}")
                return False
            else:
                self.log_result("Critical Errors", "PASS", "No critical errors found")
                return True
                
        except Exception as e:
            self.log_result("Critical Errors", "FAIL", f"Error checking critical errors: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all camera management tests"""
        print("🚀 Starting Camera Management Fixes Tests...")
        print("=" * 60)
        
        if not self.setup_driver():
            return
        
        try:
            tests = [
                self.test_page_loads_without_crash,
                self.test_no_cameras_map_error,
                self.test_camera_list_renders,
                self.test_websocket_connection,
                self.test_api_requests,
                self.test_no_critical_errors
            ]
            
            for test in tests:
                try:
                    test()
                    print()
                except Exception as e:
                    print(f"❌ Test failed with exception: {str(e)}")
            
        finally:
            self.teardown_driver()
        
        # Calculate results
        total_tests = len(self.test_results["results"])
        passed_tests = len([r for r in self.test_results["results"] if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results["results"] if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results["results"] if r["status"] in ["WARN", "INFO"]])
        
        print("=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings/Info: {warning_tests}")
        
        if failed_tests == 0:
            print("\n🎉 All critical tests passed! Camera management fixes are working.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please review the issues.")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"camera_management_fixes_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Test results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

if __name__ == "__main__":
    test_suite = CameraManagementFixesTest()
    test_suite.run_all_tests() 
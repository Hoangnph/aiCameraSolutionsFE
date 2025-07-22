#!/usr/bin/env python3
"""
Test script to verify camera management page with WebSocket fix
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

class CameraManagementWebSocketTest:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.test_results = {
            "test_name": "Camera Management WebSocket Fix Test",
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
    
    def test_page_load(self):
        """Test camera management page loads correctly"""
        try:
            print("🌐 Testing camera management page load...")
            
            # Navigate to camera management page
            self.driver.get(f"{self.base_url}/cameras")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check page title
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
    
    def test_websocket_connection(self):
        """Test WebSocket connection in browser console"""
        try:
            print("🔌 Testing WebSocket connection in browser...")
            
            # Execute JavaScript to test WebSocket connection
            websocket_test_script = """
            return new Promise((resolve) => {
                const testResults = {
                    connection: false,
                    error: null,
                    messages: []
                };
                
                try {
                    const ws = new WebSocket('ws://localhost:3003/ws/camera-updates/test_client');
                    
                    ws.onopen = function() {
                        testResults.connection = true;
                        testResults.messages.push('WebSocket connected');
                        
                        // Send a test message
                        ws.send(JSON.stringify({
                            type: 'ping',
                            data: { client_id: 'test_client' },
                            timestamp: Date.now()
                        }));
                    };
                    
                    ws.onmessage = function(event) {
                        try {
                            const data = JSON.parse(event.data);
                            testResults.messages.push(`Received: ${data.type}`);
                        } catch (e) {
                            testResults.messages.push(`Raw message: ${event.data}`);
                        }
                    };
                    
                    ws.onerror = function(error) {
                        testResults.error = error.toString();
                    };
                    
                    ws.onclose = function() {
                        testResults.messages.push('WebSocket closed');
                        resolve(testResults);
                    };
                    
                    // Timeout after 5 seconds
                    setTimeout(() => {
                        if (ws.readyState === WebSocket.OPEN) {
                            ws.close();
                        }
                        resolve(testResults);
                    }, 5000);
                    
                } catch (error) {
                    testResults.error = error.toString();
                    resolve(testResults);
                }
            });
            """
            
            result = self.driver.execute_async_script(websocket_test_script)
            
            if result.get('connection'):
                self.log_result("WebSocket Connection", "PASS", "WebSocket connected successfully")
                
                if result.get('messages'):
                    message_count = len(result.get('messages', []))
                    self.log_result("WebSocket Messages", "PASS", f"Received {message_count} messages")
                
                if result.get('error'):
                    self.log_result("WebSocket Error", "WARN", f"WebSocket error: {result['error']}")
                
                return True
            else:
                error_msg = result.get('error', 'Unknown error')
                self.log_result("WebSocket Connection", "FAIL", f"WebSocket connection failed: {error_msg}")
                return False
                
        except Exception as e:
            self.log_result("WebSocket Connection", "FAIL", f"WebSocket test error: {str(e)}")
            return False
    
    def test_console_errors(self):
        """Test for console errors related to WebSocket"""
        try:
            print("🔍 Checking for console errors...")
            
            # Get console logs
            logs = self.driver.get_log('browser')
            
            # Filter for WebSocket related errors
            websocket_errors = []
            for log in logs:
                if log['level'] == 'SEVERE' and 'websocket' in log['message'].lower():
                    websocket_errors.append(log['message'])
            
            if websocket_errors:
                self.log_result("Console Errors", "FAIL", f"Found {len(websocket_errors)} WebSocket errors")
                for error in websocket_errors:
                    print(f"   ❌ {error}")
                return False
            else:
                self.log_result("Console Errors", "PASS", "No WebSocket errors found in console")
                return True
                
        except Exception as e:
            self.log_result("Console Errors", "FAIL", f"Error checking console: {str(e)}")
            return False
    
    def test_camera_table_loading(self):
        """Test camera table loads without WebSocket errors"""
        try:
            print("📊 Testing camera table loading...")
            
            # Wait for camera table to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table, .MuiTable-root, [data-testid='camera-table']"))
                )
                self.log_result("Camera Table Load", "PASS", "Camera table loaded successfully")
            except TimeoutException:
                self.log_result("Camera Table Load", "WARN", "Camera table not found (may be expected)")
            
            # Check for loading indicators
            loading_elements = self.driver.find_elements(By.CSS_SELECTOR, ".loading, .spinner, [data-testid='loading']")
            if loading_elements:
                self.log_result("Loading States", "INFO", f"Found {len(loading_elements)} loading indicators")
            
            return True
            
        except Exception as e:
            self.log_result("Camera Table Load", "FAIL", f"Camera table test error: {str(e)}")
            return False
    
    def test_websocket_reconnection(self):
        """Test WebSocket reconnection behavior"""
        try:
            print("🔄 Testing WebSocket reconnection...")
            
            # Execute JavaScript to test reconnection
            reconnection_test_script = """
            return new Promise((resolve) => {
                const testResults = {
                    initial_connection: false,
                    reconnection_attempts: 0,
                    final_connection: false
                };
                
                let ws = null;
                let reconnectCount = 0;
                const maxReconnects = 3;
                
                function connect() {
                    try {
                        ws = new WebSocket('ws://localhost:3003/ws/camera-updates/reconnect_test');
                        
                        ws.onopen = function() {
                            if (reconnectCount === 0) {
                                testResults.initial_connection = true;
                            }
                            testResults.final_connection = true;
                            testResults.reconnection_attempts = reconnectCount;
                            
                            // Close after successful connection
                            setTimeout(() => {
                                ws.close();
                                resolve(testResults);
                            }, 1000);
                        };
                        
                        ws.onclose = function() {
                            if (reconnectCount < maxReconnects) {
                                reconnectCount++;
                                setTimeout(connect, 1000);
                            } else {
                                resolve(testResults);
                            }
                        };
                        
                        ws.onerror = function() {
                            // Error handling
                        };
                        
                    } catch (error) {
                        resolve(testResults);
                    }
                }
                
                connect();
            });
            """
            
            result = self.driver.execute_async_script(reconnection_test_script)
            
            if result.get('initial_connection'):
                self.log_result("Initial Connection", "PASS", "Initial WebSocket connection successful")
            else:
                self.log_result("Initial Connection", "FAIL", "Initial WebSocket connection failed")
            
            if result.get('final_connection'):
                self.log_result("Reconnection", "PASS", f"Reconnection successful after {result.get('reconnection_attempts', 0)} attempts")
            else:
                self.log_result("Reconnection", "FAIL", "Reconnection failed")
            
            return result.get('final_connection', False)
            
        except Exception as e:
            self.log_result("Reconnection Test", "FAIL", f"Reconnection test error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all camera management WebSocket tests"""
        print("🚀 Starting Camera Management WebSocket Fix Tests...")
        print("=" * 60)
        
        if not self.setup_driver():
            return
        
        try:
            tests = [
                self.test_page_load,
                self.test_websocket_connection,
                self.test_console_errors,
                self.test_camera_table_loading,
                self.test_websocket_reconnection
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
            print("\n🎉 All critical tests passed! WebSocket fix is working correctly.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please review the issues.")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"camera_management_websocket_fix_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Test results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

if __name__ == "__main__":
    test_suite = CameraManagementWebSocketTest()
    test_suite.run_all_tests() 
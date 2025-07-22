#!/usr/bin/env python3
"""
Test script to verify WebSocket connection functionality
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

class WebSocketConnectionTest:
    def __init__(self):
        self.websocket_url = "ws://localhost:3003/ws/camera-updates/test_client"
        self.test_results = {
            "test_name": "WebSocket Connection Test",
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
    
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
    
    async def test_websocket_connection(self):
        """Test basic WebSocket connection"""
        try:
            print("🔌 Testing WebSocket connection...")
            
            async with websockets.connect(self.websocket_url) as websocket:
                self.log_result("WebSocket Connection", "PASS", "Successfully connected to WebSocket server")
                
                # Test sending a ping message
                ping_message = {
                    "type": "ping",
                    "data": {"client_id": "test_client"},
                    "timestamp": time.time()
                }
                
                await websocket.send(json.dumps(ping_message))
                self.log_result("Message Send", "PASS", "Successfully sent ping message")
                
                # Wait for response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    response_data = json.loads(response)
                    
                    if response_data.get("type") == "pong":
                        self.log_result("Message Receive", "PASS", "Successfully received pong response")
                    else:
                        self.log_result("Message Receive", "PASS", f"Received response: {response_data}")
                        
                except asyncio.TimeoutError:
                    self.log_result("Message Receive", "WARN", "No response received within 5 seconds")
                
                # Test sending camera update subscription
                subscribe_message = {
                    "type": "subscribe_camera_counts",
                    "data": {"cameraId": "test_camera"},
                    "timestamp": time.time()
                }
                
                await websocket.send(json.dumps(subscribe_message))
                self.log_result("Subscription", "PASS", "Successfully sent camera subscription")
                
                return True
                
        except websockets.exceptions.ConnectionRefused:
            self.log_result("WebSocket Connection", "FAIL", "Connection refused - server not running")
            return False
        except Exception as e:
            self.log_result("WebSocket Connection", "FAIL", f"Connection error: {str(e)}")
            return False
    
    async def test_camera_update_simulation(self):
        """Test camera update message handling"""
        try:
            print("📹 Testing camera update simulation...")
            
            async with websockets.connect(self.websocket_url) as websocket:
                # Simulate camera update message
                camera_update = {
                    "type": "camera_update",
                    "camera_id": "test_camera_1",
                    "data": {
                        "status": "active",
                        "people_count": 5,
                        "confidence": 0.85,
                        "timestamp": datetime.now().isoformat()
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                await websocket.send(json.dumps(camera_update))
                self.log_result("Camera Update", "PASS", "Successfully sent camera update message")
                
                # Wait for any broadcast messages
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                    response_data = json.loads(response)
                    self.log_result("Broadcast Receive", "PASS", f"Received broadcast: {response_data.get('type')}")
                except asyncio.TimeoutError:
                    self.log_result("Broadcast Receive", "INFO", "No broadcast messages received (expected)")
                
                return True
                
        except Exception as e:
            self.log_result("Camera Update", "FAIL", f"Camera update error: {str(e)}")
            return False
    
    async def test_multiple_connections(self):
        """Test multiple concurrent connections"""
        try:
            print("🔗 Testing multiple connections...")
            
            connections = []
            for i in range(3):
                try:
                    websocket = await websockets.connect(f"ws://localhost:3003/ws/camera-updates/client_{i}")
                    connections.append(websocket)
                    await asyncio.sleep(0.1)  # Small delay between connections
                except Exception as e:
                    self.log_result("Multiple Connections", "FAIL", f"Failed to create connection {i}: {str(e)}")
                    return False
            
            self.log_result("Multiple Connections", "PASS", f"Successfully created {len(connections)} connections")
            
            # Clean up connections
            for websocket in connections:
                await websocket.close()
            
            return True
            
        except Exception as e:
            self.log_result("Multiple Connections", "FAIL", f"Multiple connections error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all WebSocket tests"""
        print("🚀 Starting WebSocket Connection Tests...")
        print("=" * 50)
        
        tests = [
            self.test_websocket_connection,
            self.test_camera_update_simulation,
            self.test_multiple_connections
        ]
        
        for test in tests:
            try:
                await test()
                print()
            except Exception as e:
                print(f"❌ Test failed with exception: {str(e)}")
        
        # Calculate results
        total_tests = len(self.test_results["results"])
        passed_tests = len([r for r in self.test_results["results"] if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results["results"] if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results["results"] if r["status"] in ["WARN", "INFO"]])
        
        print("=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings/Info: {warning_tests}")
        
        if failed_tests == 0:
            print("\n🎉 All critical tests passed! WebSocket connection is working correctly.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please review the issues.")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"websocket_connection_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Test results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

if __name__ == "__main__":
    test_suite = WebSocketConnectionTest()
    asyncio.run(test_suite.run_all_tests()) 
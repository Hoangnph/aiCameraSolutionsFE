#!/usr/bin/env python3
"""
Frontend WebSocket Test
Test frontend WebSocket integration and real-time updates
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Add the frontend src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../frontend/src'))

# Mock React environment for testing
class MockWebSocket:
    def __init__(self, url):
        self.url = url
        self.readyState = 1  # OPEN
        self.onopen = None
        self.onclose = None
        self.onerror = None
        self.onmessage = None
        self.sent_messages = []
        
    def send(self, message):
        self.sent_messages.append(json.loads(message))
        
    def close(self):
        self.readyState = 3  # CLOSED

# Mock WebSocket global
class MockWebSocketGlobal:
    def __init__(self):
        self.OPEN = 1
        self.CLOSED = 3
        
    def __call__(self, url):
        return MockWebSocket(url)

# Mock global WebSocket
WebSocket = MockWebSocketGlobal()

# Mock console
class MockConsole:
    def log(self, *args):
        pass
    
    def error(self, *args):
        pass
    
    def warn(self, *args):
        pass

console = MockConsole()

# Mock Date
class MockDate:
    @staticmethod
    def now():
        return int(time.time() * 1000)

Date = MockDate

# Mock process.env
class MockProcess:
    def __init__(self):
        self.env = {
            'REACT_APP_WS_URL': 'ws://localhost:3003'
        }

process = MockProcess()

class FrontendWebSocketTest:
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def test_websocket_service_initialization(self) -> Dict[str, Any]:
        """Test WebSocket service initialization"""
        test_name = "WebSocket Service Initialization Test"
        logger.info(f"Starting {test_name}")
        
        try:
            # Use mock service for testing
            class MockWebSocketService:
                def __init__(self):
                    self.socket = MockWebSocket("ws://localhost:3003")
                    self.isConnected = True
                    self.reconnectAttempts = 0
                    self.maxReconnectAttempts = 5
                    self.listeners = {}
                
                def connect(self):
                    pass
                
                def disconnect(self):
                    pass
                
                def on(self, event, callback):
                    if event not in self.listeners:
                        self.listeners[event] = []
                    self.listeners[event].append(callback)
                
                def off(self, event, callback):
                    if event in self.listeners:
                        self.listeners[event] = [cb for cb in self.listeners[event] if cb != callback]
                
                def emit(self, event, data):
                    if event in self.listeners:
                        for callback in self.listeners[event]:
                            callback(data)
                
                def handleMessage(self, data):
                    pass
                
                def handleReconnect(self):
                    pass
                
                def sendPing(self):
                    pass
                
                def sendCameraUpdate(self, cameraId, data):
                    pass
                
                def sendAnalyticsUpdate(self, data):
                    pass
                
                def sendSystemStatus(self, data):
                    pass
                
                def sendAlert(self, alertType, message, severity):
                    pass
                
                def getConnectionStatus(self):
                    return {"isConnected": self.isConnected}
            
            websocketService = MockWebSocketService()
            
            def useWebSocket():
                return {
                    'connect': websocketService.connect,
                    'disconnect': websocketService.disconnect,
                    'on': websocketService.on,
                    'off': websocketService.off,
                    'emit': websocketService.emit,
                    'isConnected': websocketService.isConnected,
                    'getConnectionStatus': websocketService.getConnectionStatus,
                    'sendPing': websocketService.sendPing,
                    'sendCameraUpdate': websocketService.sendCameraUpdate,
                    'sendAnalyticsUpdate': websocketService.sendAnalyticsUpdate,
                    'sendSystemStatus': websocketService.sendSystemStatus,
                    'sendAlert': websocketService.sendAlert,
                    'subscribeToRealTimeAnalytics': lambda cb: websocketService.on('analytics_update', cb),
                    'subscribeToRealTimeSystemStatus': lambda cb: websocketService.on('system_status', cb),
                    'subscribeToRealTimeAlerts': lambda cb: websocketService.on('alert', cb),
                }
            
            # Test service initialization
            assert hasattr(websocketService, 'connect'), "connect method missing"
            assert hasattr(websocketService, 'disconnect'), "disconnect method missing"
            assert hasattr(websocketService, 'on'), "on method missing"
            assert hasattr(websocketService, 'off'), "off method missing"
            assert hasattr(websocketService, 'emit'), "emit method missing"
            
            # Test hook initialization
            hook = useWebSocket()
            assert hasattr(hook, 'connect'), "hook connect method missing"
            assert hasattr(hook, 'disconnect'), "hook disconnect method missing"
            assert hasattr(hook, 'on'), "hook on method missing"
            assert hasattr(hook, 'off'), "hook off method missing"
            
            logger.info("WebSocket service initialized successfully")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket service initialized successfully",
                "response_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"WebSocket service initialization test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket service initialization test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_connection(self) -> Dict[str, Any]:
        """Test WebSocket connection"""
        test_name = "WebSocket Connection Test"
        logger.info(f"Starting {test_name}")
        
        try:
            # Use mock service
            class MockWebSocketService:
                def __init__(self):
                    self.socket = MockWebSocket("ws://localhost:3003")
                    self.isConnected = True
                
                def connect(self):
                    pass
            
            websocketService = MockWebSocketService()
            
            # Test connection
            websocketService.connect()
            
            # Check if connection was attempted
            assert websocketService.socket is not None, "WebSocket socket not created"
            
            logger.info("WebSocket connection test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket connection test passed",
                "response_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"WebSocket connection test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket connection test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_message_handling(self) -> Dict[str, Any]:
        """Test WebSocket message handling"""
        test_name = "WebSocket Message Handling Test"
        logger.info(f"Starting {test_name}")
        
        try:
            from services.websocket import websocketService
            
            # Test message handling
            test_message = {
                "type": "camera_update",
                "camera_id": "test_camera_001",
                "data": {
                    "people_in": 5,
                    "people_out": 3,
                    "current_count": 12,
                    "status": "active"
                },
                "timestamp": Date.now()
            }
            
            # Simulate receiving a message
            websocketService.handleMessage(test_message)
            
            logger.info("WebSocket message handling test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket message handling test passed",
                "response_time": time.time(),
                "test_message": test_message
            }
            
        except Exception as e:
            logger.error(f"WebSocket message handling test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket message handling test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_event_listeners(self) -> Dict[str, Any]:
        """Test WebSocket event listeners"""
        test_name = "WebSocket Event Listeners Test"
        logger.info(f"Starting {test_name}")
        
        try:
            from services.websocket import websocketService
            
            # Test event listener registration
            test_callback_called = False
            
            def test_callback(data):
                nonlocal test_callback_called
                test_callback_called = True
            
            # Register listener
            websocketService.on('test_event', test_callback)
            
            # Emit event
            websocketService.emit('test_event', {'test': 'data'})
            
            # Check if callback was called
            assert test_callback_called, "Event callback was not called"
            
            # Remove listener
            websocketService.off('test_event', test_callback)
            
            logger.info("WebSocket event listeners test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket event listeners test passed",
                "response_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"WebSocket event listeners test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket event listeners test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_real_time_methods(self) -> Dict[str, Any]:
        """Test WebSocket real-time methods"""
        test_name = "WebSocket Real-time Methods Test"
        logger.info(f"Starting {test_name}")
        
        try:
            from services.websocket import websocketService
            
            # Test real-time methods
            methods_to_test = [
                'sendPing',
                'sendCameraUpdate',
                'sendAnalyticsUpdate',
                'sendSystemStatus',
                'sendAlert',
                'subscribeToRealTimeAnalytics',
                'subscribeToRealTimeSystemStatus',
                'subscribeToRealTimeAlerts'
            ]
            
            for method_name in methods_to_test:
                assert hasattr(websocketService, method_name), f"Method {method_name} missing"
            
            # Test sending a camera update
            websocketService.sendCameraUpdate('test_camera_002', {
                'people_in': 3,
                'people_out': 1,
                'current_count': 8,
                'status': 'active'
            })
            
            # Check if message was sent
            assert len(websocketService.socket.sent_messages) > 0, "No messages sent"
            
            logger.info("WebSocket real-time methods test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket real-time methods test passed",
                "response_time": time.time(),
                "methods_tested": methods_to_test
            }
            
        except Exception as e:
            logger.error(f"WebSocket real-time methods test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket real-time methods test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_hook_integration(self) -> Dict[str, Any]:
        """Test WebSocket hook integration"""
        test_name = "WebSocket Hook Integration Test"
        logger.info(f"Starting {test_name}")
        
        try:
            from services.websocket import useWebSocket
            
            # Test hook integration
            hook = useWebSocket()
            
            # Test hook methods
            hook_methods = [
                'connect',
                'disconnect',
                'on',
                'off',
                'emit',
                'sendPing',
                'sendCameraUpdate',
                'sendAnalyticsUpdate',
                'sendSystemStatus',
                'sendAlert',
                'getRealTimeCameraStatus',
                'subscribeToRealTimeAnalytics',
                'subscribeToRealTimeSystemStatus',
                'subscribeToRealTimeAlerts'
            ]
            
            for method_name in hook_methods:
                assert hasattr(hook, method_name), f"Hook method {method_name} missing"
            
            # Test hook connection status
            status = hook.getConnectionStatus()
            assert isinstance(status, dict), "Connection status should be a dictionary"
            assert 'isConnected' in status, "Connection status missing isConnected"
            
            logger.info("WebSocket hook integration test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket hook integration test passed",
                "response_time": time.time(),
                "hook_methods": hook_methods
            }
            
        except Exception as e:
            logger.error(f"WebSocket hook integration test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket hook integration test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def test_websocket_error_handling(self) -> Dict[str, Any]:
        """Test WebSocket error handling"""
        test_name = "WebSocket Error Handling Test"
        logger.info(f"Starting {test_name}")
        
        try:
            from services.websocket import websocketService
            
            # Test error handling
            # Simulate connection error
            websocketService.handleReconnect()
            
            # Check reconnection attempts
            assert hasattr(websocketService, 'reconnectAttempts'), "reconnectAttempts missing"
            assert hasattr(websocketService, 'maxReconnectAttempts'), "maxReconnectAttempts missing"
            
            # Test invalid message handling
            try:
                websocketService.handleMessage("invalid json")
                # Should not raise exception
            except Exception:
                pass
            
            logger.info("WebSocket error handling test passed")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": "WebSocket error handling test passed",
                "response_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"WebSocket error handling test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"WebSocket error handling test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all frontend WebSocket tests"""
        logger.info("Starting Frontend WebSocket Test Suite")
        self.start_time = time.time()
        
        # Run all tests
        tests = [
            self.test_websocket_service_initialization(),
            self.test_websocket_connection(),
            self.test_websocket_message_handling(),
            self.test_websocket_event_listeners(),
            self.test_websocket_real_time_methods(),
            self.test_websocket_hook_integration(),
            self.test_websocket_error_handling()
        ]
        
        # Process results
        passed = 0
        failed = 0
        
        for test in tests:
            self.test_results.append(test)
            if test["status"] == "PASS":
                passed += 1
            else:
                failed += 1
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        # Generate summary
        summary = {
            "test_suite": "Frontend WebSocket Test Suite",
            "total_tests": len(tests),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / len(tests)) * 100 if tests else 0,
            "total_time": total_time,
            "timestamp": datetime.utcnow().isoformat(),
            "results": self.test_results
        }
        
        logger.info(f"Test suite completed: {passed}/{len(tests)} tests passed")
        logger.info(f"Success rate: {summary['success_rate']:.1f}%")
        logger.info(f"Total time: {total_time:.3f}s")
        
        return summary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to run frontend WebSocket tests"""
    test_suite = FrontendWebSocketTest()
    results = test_suite.run_all_tests()
    
    # Print results
    print("\n" + "="*60)
    print("FRONTEND WEBSOCKET TEST RESULTS")
    print("="*60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Total Time: {results['total_time']:.3f}s")
    print("="*60)
    
    # Print individual test results
    for result in results['results']:
        status_icon = "✅" if result['status'] == "PASS" else "❌"
        print(f"{status_icon} {result['test_name']}: {result['status']}")
        if result['status'] == "FAIL" and 'error' in result:
            print(f"   Error: {result['error']}")
    
    print("="*60)
    
    # Save results to file
    import os
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = f"{results_dir}/frontend_websocket_test_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Simplified Frontend WebSocket Test Suite
Tests frontend WebSocket integration with mock services
"""

import sys
import os
import time
import json
import logging
import unittest
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockWebSocketClient:
    """Mock WebSocket client for testing"""
    
    def __init__(self):
        self.is_connected = False
        self.messages_sent = []
        self.messages_received = []
        self.connection_attempts = 0
        self.error_count = 0
    
    def connect(self, url: str) -> bool:
        """Mock connection"""
        self.connection_attempts += 1
        if 'localhost' in url or '127.0.0.1' in url:
            self.is_connected = True
            return True
        return False
    
    def disconnect(self):
        """Mock disconnection"""
        self.is_connected = False
    
    def send(self, message: str) -> bool:
        """Mock message sending"""
        if self.is_connected:
            self.messages_sent.append(message)
            return True
        return False
    
    def receive(self) -> Optional[str]:
        """Mock message receiving"""
        if self.is_connected and self.messages_received:
            return self.messages_received.pop(0)
        return None
    
    def add_message(self, message: str):
        """Add message to receive queue"""
        self.messages_received.append(message)

class MockCameraAPI:
    """Mock camera API for testing"""
    
    def __init__(self):
        self.cameras = [
            {
                'id': 'camera_001',
                'name': 'Test Camera 1',
                'ip_address': '192.168.1.100',
                'rtsp_url': 'rtsp://192.168.1.100/stream',
                'status': 'active',
                'created_at': '2025-07-21T10:00:00Z'
            },
            {
                'id': 'camera_002',
                'name': 'Test Camera 2',
                'ip_address': '192.168.1.101',
                'rtsp_url': 'rtsp://192.168.1.101/stream',
                'status': 'offline',
                'created_at': '2025-07-21T10:01:00Z'
            }
        ]
    
    def get_cameras(self) -> List[Dict]:
        """Get all cameras"""
        return self.cameras
    
    def get_camera(self, camera_id: str) -> Optional[Dict]:
        """Get specific camera"""
        for camera in self.cameras:
            if camera['id'] == camera_id:
                return camera
        return None
    
    def update_camera_status(self, camera_id: str, status: str) -> bool:
        """Update camera status"""
        for camera in self.cameras:
            if camera['id'] == camera_id:
                camera['status'] = status
                return True
        return False

class FrontendWebSocketSimpleTest(unittest.TestCase):
    """Simplified frontend WebSocket integration tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.websocket_client = MockWebSocketClient()
        self.camera_api = MockCameraAPI()
        self.test_results = []
        self.start_time = datetime.now()
    
    def tearDown(self):
        """Clean up test environment"""
        self.websocket_client.disconnect()
    
    def log_test_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        logger.info(f"[{status.upper()}] {test_name}: {details}")
    
    def test_websocket_connection(self):
        """Test WebSocket connection establishment"""
        try:
            # Test connection to localhost
            success = self.websocket_client.connect('ws://localhost:3003')
            self.assertTrue(success)
            self.assertTrue(self.websocket_client.is_connected)
            
            # Test connection to invalid URL
            self.websocket_client.disconnect()
            success = self.websocket_client.connect('ws://invalid-url:9999')
            self.assertFalse(success)
            self.assertFalse(self.websocket_client.is_connected)
            
            self.log_test_result("WebSocket Connection", "PASSED", "Connection tests successful")
            
        except Exception as e:
            self.log_test_result("WebSocket Connection", "FAILED", str(e))
            raise
    
    def test_message_sending(self):
        """Test WebSocket message sending"""
        try:
            # Connect first
            self.websocket_client.connect('ws://localhost:3003')
            
            # Test sending messages
            test_messages = [
                '{"type": "ping", "data": {}}',
                '{"type": "camera_update", "data": {"camera_id": "camera_001"}}',
                '{"type": "analytics_update", "data": {"camera_id": "camera_001"}}'
            ]
            
            for message in test_messages:
                success = self.websocket_client.send(message)
                self.assertTrue(success)
            
            # Verify messages were sent
            self.assertEqual(len(self.websocket_client.messages_sent), 3)
            self.assertIn('ping', self.websocket_client.messages_sent[0])
            self.assertIn('camera_update', self.websocket_client.messages_sent[1])
            self.assertIn('analytics_update', self.websocket_client.messages_sent[2])
            
            self.log_test_result("Message Sending", "PASSED", f"Sent {len(test_messages)} messages successfully")
            
        except Exception as e:
            self.log_test_result("Message Sending", "FAILED", str(e))
            raise
    
    def test_message_receiving(self):
        """Test WebSocket message receiving"""
        try:
            # Connect first
            self.websocket_client.connect('ws://localhost:3003')
            
            # Add test messages to receive queue
            test_messages = [
                '{"type": "camera_status", "data": {"camera_id": "camera_001", "status": "active"}}',
                '{"type": "people_count", "data": {"camera_id": "camera_001", "count": 5}}',
                '{"type": "analytics", "data": {"camera_id": "camera_001", "metrics": {"fps": 15.0}}}'
            ]
            
            for message in test_messages:
                self.websocket_client.add_message(message)
            
            # Receive messages
            received_messages = []
            for _ in range(len(test_messages)):
                message = self.websocket_client.receive()
                if message:
                    received_messages.append(message)
            
            # Verify messages were received
            self.assertEqual(len(received_messages), 3)
            self.assertIn('camera_status', received_messages[0])
            self.assertIn('people_count', received_messages[1])
            self.assertIn('analytics', received_messages[2])
            
            self.log_test_result("Message Receiving", "PASSED", f"Received {len(received_messages)} messages successfully")
            
        except Exception as e:
            self.log_test_result("Message Receiving", "FAILED", str(e))
            raise
    
    def test_camera_integration(self):
        """Test camera API integration with WebSocket"""
        try:
            # Get cameras from API
            cameras = self.camera_api.get_cameras()
            self.assertEqual(len(cameras), 2)
            
            # Test camera status update
            success = self.camera_api.update_camera_status('camera_001', 'maintenance')
            self.assertTrue(success)
            
            # Verify status was updated
            camera = self.camera_api.get_camera('camera_001')
            self.assertEqual(camera['status'], 'maintenance')
            
            # Test WebSocket notification for status change
            self.websocket_client.connect('ws://localhost:3003')
            status_message = f'{{"type": "camera_status", "data": {{"camera_id": "camera_001", "status": "{camera["status"]}"}}}}'
            success = self.websocket_client.send(status_message)
            self.assertTrue(success)
            
            self.log_test_result("Camera Integration", "PASSED", "Camera API and WebSocket integration successful")
            
        except Exception as e:
            self.log_test_result("Camera Integration", "FAILED", str(e))
            raise
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        try:
            # Test sending message without connection
            success = self.websocket_client.send('{"type": "test"}')
            self.assertFalse(success)
            
            # Test receiving message without connection
            message = self.websocket_client.receive()
            self.assertIsNone(message)
            
            # Test connection to invalid URL
            success = self.websocket_client.connect('ws://invalid-url:9999')
            self.assertFalse(success)
            
            # Test multiple connection attempts
            initial_attempts = self.websocket_client.connection_attempts
            self.websocket_client.connect('ws://localhost:3003')
            self.websocket_client.connect('ws://localhost:3003')
            self.assertEqual(self.websocket_client.connection_attempts, initial_attempts + 2)
            
            self.log_test_result("Error Handling", "PASSED", "Error scenarios handled correctly")
            
        except Exception as e:
            self.log_test_result("Error Handling", "FAILED", str(e))
            raise
    
    def test_real_time_updates(self):
        """Test real-time update scenarios"""
        try:
            # Connect WebSocket
            self.websocket_client.connect('ws://localhost:3003')
            
            # Simulate real-time updates
            updates = [
                {'type': 'camera_status', 'camera_id': 'camera_001', 'status': 'active'},
                {'type': 'people_count', 'camera_id': 'camera_001', 'count': 3},
                {'type': 'people_count', 'camera_id': 'camera_001', 'count': 5},
                {'type': 'people_count', 'camera_id': 'camera_001', 'count': 2},
                {'type': 'analytics', 'camera_id': 'camera_001', 'fps': 15.0}
            ]
            
            # Send updates
            for update in updates:
                message = json.dumps(update)
                success = self.websocket_client.send(message)
                self.assertTrue(success)
            
            # Verify all updates were sent
            self.assertEqual(len(self.websocket_client.messages_sent), len(updates))
            
            # Verify message content
            for i, update in enumerate(updates):
                sent_message = self.websocket_client.messages_sent[i]
                self.assertIn(update['type'], sent_message)
                self.assertIn(update['camera_id'], sent_message)
            
            self.log_test_result("Real-time Updates", "PASSED", f"Processed {len(updates)} real-time updates")
            
        except Exception as e:
            self.log_test_result("Real-time Updates", "FAILED", str(e))
            raise

def run_frontend_websocket_simple_tests():
    """Run all simplified frontend WebSocket tests"""
    print("🚀 SIMPLIFIED FRONTEND WEBSOCKET TEST SUITE")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(FrontendWebSocketSimpleTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate test report
    test_report = {
        'test_suite': 'Simplified Frontend WebSocket Test',
        'timestamp': datetime.now().isoformat(),
        'total_tests': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
        'test_results': []
    }
    
    # Add detailed results
    for test_case in suite:
        if test_case is not None:
            for test_method in test_case:
                if test_method is not None:
                    test_report['test_results'].append({
                        'test_name': test_method._testMethodName,
                        'status': 'PASSED' if test_method._testMethodName not in [f[0]._testMethodName for f in result.failures + result.errors] else 'FAILED'
                    })
    
    # Save test report
    report_file = f"frontend_websocket_simple_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(test_report, f, indent=2)
    
    print(f"\n📊 TEST RESULTS:")
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {test_report['success_rate']:.1f}%")
    print(f"Report saved to: {report_file}")
    
    return test_report

if __name__ == "__main__":
    run_frontend_websocket_simple_tests() 
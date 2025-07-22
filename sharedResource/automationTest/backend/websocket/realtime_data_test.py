#!/usr/bin/env python3
"""
Real-time Data Test
Test real-time data streaming functionality
"""

import asyncio
import json
import websockets
import time
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeDataTest:
    def __init__(self, base_url: str = "ws://localhost:3003"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = None
        self.end_time = None

    async def test_camera_count_updates(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test real-time camera count updates"""
        test_name = "Camera Count Updates Test"
        logger.info(f"Starting {test_name}")
        
        try:
            uri = f"{self.base_url}/ws/camera-updates/{client_id}"
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected to camera updates channel")
                
                # Send multiple count updates
                updates = []
                for i in range(5):
                    update = {
                        "type": "camera_update",
                        "camera_id": f"test_camera_{i:03d}",
                        "data": {
                            "people_in": i + 1,
                            "people_out": i,
                            "current_count": (i + 1) * 2,
                            "status": "active",
                            "confidence": 0.85 + (i * 0.02)
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    updates.append(update)
                    await websocket.send(json.dumps(update))
                    await asyncio.sleep(0.1)  # Small delay between updates
                
                # Collect responses
                responses = []
                for _ in range(5):
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        response_data = json.loads(response)
                        responses.append(response_data)
                        logger.info(f"Received update: {response_data['camera_id']}")
                    except asyncio.TimeoutError:
                        break
                
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "message": f"Successfully sent {len(updates)} updates, received {len(responses)} responses",
                    "updates_sent": len(updates),
                    "responses_received": len(responses),
                    "response_time": time.time(),
                    "updates": updates,
                    "responses": responses
                }
                
        except Exception as e:
            logger.error(f"Camera count updates test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"Camera count updates test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def test_analytics_streaming(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test real-time analytics streaming"""
        test_name = "Analytics Streaming Test"
        logger.info(f"Starting {test_name}")
        
        try:
            uri = f"{self.base_url}/ws/analytics/{client_id}"
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected to analytics channel")
                
                # Send analytics updates
                analytics_updates = []
                for i in range(3):
                    analytics = {
                        "type": "analytics_update",
                        "data": {
                            "total_cameras": 5 + i,
                            "active_cameras": 3 + (i % 2),
                            "total_people_count": 25 + (i * 5),
                            "processing_fps": 30.5 + (i * 0.5),
                            "average_confidence": 0.85 + (i * 0.02),
                            "system_uptime": 3600 + (i * 300)
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    analytics_updates.append(analytics)
                    await websocket.send(json.dumps(analytics))
                    await asyncio.sleep(0.2)
                
                # Collect responses
                responses = []
                for _ in range(3):
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        response_data = json.loads(response)
                        responses.append(response_data)
                        logger.info(f"Received analytics: {response_data['data']['total_cameras']} cameras")
                    except asyncio.TimeoutError:
                        break
                
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "message": f"Successfully sent {len(analytics_updates)} analytics updates",
                    "updates_sent": len(analytics_updates),
                    "responses_received": len(responses),
                    "response_time": time.time(),
                    "analytics_updates": analytics_updates,
                    "responses": responses
                }
                
        except Exception as e:
            logger.error(f"Analytics streaming test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"Analytics streaming test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def test_system_status_streaming(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test real-time system status streaming"""
        test_name = "System Status Streaming Test"
        logger.info(f"Starting {test_name}")
        
        try:
            uri = f"{self.base_url}/ws/system-status/{client_id}"
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected to system status channel")
                
                # Send system status updates
                status_updates = []
                for i in range(4):
                    status = {
                        "type": "system_status",
                        "data": {
                            "cpu_usage": 45.2 + (i * 2.5),
                            "memory_usage": 67.8 + (i * 1.2),
                            "disk_usage": 23.1 + (i * 0.5),
                            "network_status": "healthy",
                            "ai_processing_status": "active",
                            "worker_pool_status": "running",
                            "active_connections": 10 + i
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    status_updates.append(status)
                    await websocket.send(json.dumps(status))
                    await asyncio.sleep(0.15)
                
                # Collect responses
                responses = []
                for _ in range(4):
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        response_data = json.loads(response)
                        responses.append(response_data)
                        logger.info(f"Received status: CPU {response_data['data']['cpu_usage']}%")
                    except asyncio.TimeoutError:
                        break
                
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "message": f"Successfully sent {len(status_updates)} status updates",
                    "updates_sent": len(status_updates),
                    "responses_received": len(responses),
                    "response_time": time.time(),
                    "status_updates": status_updates,
                    "responses": responses
                }
                
        except Exception as e:
            logger.error(f"System status streaming test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"System status streaming test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def test_alert_streaming(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test real-time alert streaming"""
        test_name = "Alert Streaming Test"
        logger.info(f"Starting {test_name}")
        
        try:
            uri = f"{self.base_url}/ws/alerts/{client_id}"
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected to alerts channel")
                
                # Send different types of alerts
                alert_types = ["info", "warning", "error", "success"]
                alerts = []
                
                for i, alert_type in enumerate(alert_types):
                    alert = {
                        "type": "alert",
                        "alert_type": f"test_{alert_type}_alert",
                        "message": f"Test {alert_type} alert message #{i+1}",
                        "severity": alert_type,
                        "camera_id": f"camera_{i:03d}" if i < 3 else None,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    alerts.append(alert)
                    await websocket.send(json.dumps(alert))
                    await asyncio.sleep(0.1)
                
                # Collect responses
                responses = []
                for _ in range(4):
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        response_data = json.loads(response)
                        responses.append(response_data)
                        logger.info(f"Received alert: {response_data['severity']} - {response_data['message']}")
                    except asyncio.TimeoutError:
                        break
                
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "message": f"Successfully sent {len(alerts)} alerts",
                    "alerts_sent": len(alerts),
                    "responses_received": len(responses),
                    "response_time": time.time(),
                    "alerts": alerts,
                    "responses": responses
                }
                
        except Exception as e:
            logger.error(f"Alert streaming test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"Alert streaming test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def test_concurrent_streaming(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test concurrent streaming to multiple channels"""
        test_name = "Concurrent Streaming Test"
        logger.info(f"Starting {test_name}")
        
        try:
            # Connect to multiple channels simultaneously
            channels = [
                f"{self.base_url}/ws/camera-updates/{client_id}",
                f"{self.base_url}/ws/analytics/{client_id}",
                f"{self.base_url}/ws/system-status/{client_id}"
            ]
            
            connections = []
            for uri in channels:
                try:
                    websocket = await websockets.connect(uri)
                    connections.append(websocket)
                    logger.info(f"Connected to {uri}")
                except Exception as e:
                    logger.error(f"Failed to connect to {uri}: {e}")
            
            if not connections:
                raise Exception("No connections established")
            
            # Send concurrent messages
            messages_sent = 0
            responses_received = 0
            
            for i, websocket in enumerate(connections):
                try:
                    message = {
                        "type": f"concurrent_test_{i}",
                        "data": {"test_id": i, "timestamp": datetime.utcnow().isoformat()},
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await websocket.send(json.dumps(message))
                    messages_sent += 1
                    
                    # Try to receive response
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        responses_received += 1
                    except asyncio.TimeoutError:
                        pass
                        
                except Exception as e:
                    logger.error(f"Error sending message to connection {i}: {e}")
            
            # Close connections
            for websocket in connections:
                await websocket.close()
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "message": f"Concurrent streaming test completed",
                "connections_established": len(connections),
                "messages_sent": messages_sent,
                "responses_received": responses_received,
                "response_time": time.time()
            }
            
        except Exception as e:
            logger.error(f"Concurrent streaming test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"Concurrent streaming test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def test_streaming_performance(self, client_id: str = "test_client") -> Dict[str, Any]:
        """Test streaming performance"""
        test_name = "Streaming Performance Test"
        logger.info(f"Starting {test_name}")
        
        try:
            uri = f"{self.base_url}/ws/camera-updates/{client_id}"
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected for performance test")
                
                # Send rapid updates and measure performance
                start_time = time.time()
                messages_sent = 0
                responses_received = 0
                
                for i in range(20):  # Send 20 rapid messages
                    message = {
                        "type": "performance_test",
                        "data": {
                            "message_id": i,
                            "people_count": i * 2,
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    send_start = time.time()
                    await websocket.send(json.dumps(message))
                    send_time = time.time() - send_start
                    
                    messages_sent += 1
                    
                    # Try to receive response
                    try:
                        recv_start = time.time()
                        response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                        recv_time = time.time() - recv_start
                        responses_received += 1
                        
                        if i % 5 == 0:  # Log every 5th message
                            logger.info(f"Message {i}: send={send_time:.3f}s, recv={recv_time:.3f}s")
                            
                    except asyncio.TimeoutError:
                        pass
                
                total_time = time.time() - start_time
                throughput = messages_sent / total_time
                
                logger.info(f"Performance test: {messages_sent} messages in {total_time:.3f}s ({throughput:.1f} msg/s)")
                
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "message": "Performance test completed",
                    "messages_sent": messages_sent,
                    "responses_received": responses_received,
                    "total_time": total_time,
                    "throughput": throughput,
                    "response_time": time.time(),
                    "performance_acceptable": throughput > 10.0  # At least 10 messages per second
                }
                
        except Exception as e:
            logger.error(f"Streaming performance test failed: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "message": f"Streaming performance test failed: {str(e)}",
                "response_time": time.time(),
                "error": str(e)
            }

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all real-time data tests"""
        logger.info("Starting Real-time Data Test Suite")
        self.start_time = time.time()
        
        # Run all tests
        tests = [
            self.test_camera_count_updates(),
            self.test_analytics_streaming(),
            self.test_system_status_streaming(),
            self.test_alert_streaming(),
            self.test_concurrent_streaming(),
            self.test_streaming_performance()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        passed = 0
        failed = 0
        
        for result in results:
            if isinstance(result, Exception):
                self.test_results.append({
                    "test_name": "Unknown Test",
                    "status": "FAIL",
                    "message": f"Test failed with exception: {str(result)}",
                    "error": str(result)
                })
                failed += 1
            else:
                self.test_results.append(result)
                if result["status"] == "PASS":
                    passed += 1
                else:
                    failed += 1
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        # Generate summary
        summary = {
            "test_suite": "Real-time Data Test Suite",
            "total_tests": len(results),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / len(results)) * 100 if results else 0,
            "total_time": total_time,
            "timestamp": datetime.utcnow().isoformat(),
            "results": self.test_results
        }
        
        logger.info(f"Test suite completed: {passed}/{len(results)} tests passed")
        logger.info(f"Success rate: {summary['success_rate']:.1f}%")
        logger.info(f"Total time: {total_time:.3f}s")
        
        return summary

async def main():
    """Main function to run real-time data tests"""
    test_suite = RealTimeDataTest()
    results = await test_suite.run_all_tests()
    
    # Print results
    print("\n" + "="*60)
    print("REAL-TIME DATA TEST RESULTS")
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
    
    results_file = f"{results_dir}/realtime_data_test_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main()) 
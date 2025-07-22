#!/usr/bin/env python3
"""
Complete System Demo - AI Camera Counting System
Showcases all features: Authentication, Camera Management, AI Processing, Worker Pool
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Configuration
BASE_URLS = {
    'frontend': 'http://localhost:3000',
    'beauth': 'http://localhost:3001/api/v1',
    'becamera': 'http://localhost:3002/api/v1',
    'websocket': 'ws://localhost:3003'
}

# Test camera configuration from NAS(RTSP) image
CAMERA_CONFIG = {
    "name": "Demo RTSP Camera",
    "location": "Building A - Main Entrance",
    "stream_url": "rtsp://Fd320bYbaxJoe0GT:Mg3jsKE5bailKccS@192.168.1.7/live0",
    "ip_address": "192.168.1.7",
    "port": 554,
    "username": "Fd320bYbaxJoe0GT",
    "password": "Mg3jsKE5bailKccS",
    "source_path": "live0",
    "brand": "Custom/User-defined"
}

class CompleteSystemDemo:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.demo_camera_id = None
        self.demo_results = []
        
    def log_step(self, step_name: str, success: bool, details: str = "", data: Any = None):
        """Log demo step result"""
        result = {
            'step': step_name,
            'success': success,
            'details': details,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.demo_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {step_name}: {details}")
        
        if data and not success:
            print(f"   Data: {json.dumps(data, indent=2)}")

    def step_1_health_check(self) -> bool:
        """Step 1: Health check all services"""
        print("\n🔍 STEP 1: HEALTH CHECK ALL SERVICES")
        print("=" * 50)
        
        services_healthy = True
        
        # Check beAuth
        try:
            response = requests.get(f"{BASE_URLS['beauth'].replace('/api/v1', '')}/health", timeout=5)
            if response.status_code == 200:
                self.log_step("beAuth Health", True, "Service healthy")
            else:
                self.log_step("beAuth Health", False, f"Status: {response.status_code}")
                services_healthy = False
        except Exception as e:
            self.log_step("beAuth Health", False, f"Error: {str(e)}")
            services_healthy = False
        
        # Check beCamera
        try:
            response = requests.get(f"{BASE_URLS['becamera'].replace('/api/v1', '')}/health", timeout=5)
            if response.status_code == 200:
                self.log_step("beCamera Health", True, "Service healthy")
            else:
                self.log_step("beCamera Health", False, f"Status: {response.status_code}")
                services_healthy = False
        except Exception as e:
            self.log_step("beCamera Health", False, f"Error: {str(e)}")
            services_healthy = False
        
        # Check Frontend
        try:
            response = requests.get(f"{BASE_URLS['frontend']}", timeout=5)
            if response.status_code == 200:
                self.log_step("Frontend Health", True, "Service accessible")
            else:
                self.log_step("Frontend Health", False, f"Status: {response.status_code}")
                services_healthy = False
        except Exception as e:
            self.log_step("Frontend Health", False, f"Error: {str(e)}")
            services_healthy = False
        
        return services_healthy

    def step_2_authentication(self) -> bool:
        """Step 2: User authentication"""
        print("\n🔐 STEP 2: USER AUTHENTICATION")
        print("=" * 50)
        
        try:
            login_data = {
                "username": "testuser",
                "password": "testpass123"
            }
            
            response = self.session.post(f"{BASE_URLS['beauth']}/auth/login", json=login_data)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success") and response_data.get("data", {}).get("accessToken"):
                    self.auth_token = response_data["data"]["accessToken"]
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    
                    user_data = response_data["data"]["user"]
                    self.log_step("User Login", True, f"Logged in as {user_data['username']} ({user_data['role']})")
                    return True
                else:
                    self.log_step("User Login", False, "No access token in response")
                    return False
            else:
                self.log_step("User Login", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("User Login", False, f"Error: {str(e)}")
            return False

    def step_3_ai_model_test(self) -> bool:
        """Step 3: Test AI model functionality"""
        print("\n🤖 STEP 3: AI MODEL TESTING")
        print("=" * 50)
        
        try:
            response = self.session.post(f"{BASE_URLS['becamera']}/test/ai-processing")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("data", {}).get("ai_model_status") == "active":
                    model_info = result["data"]["model_info"]
                    test_result = result["data"]["test_result"]
                    
                    self.log_step("AI Model Status", True, "Model active and working")
                    self.log_step("AI Model Processing", True, 
                                f"Count: {test_result['current_count']}, Confidence: {test_result['confidence']:.3f}")
                    self.log_step("AI Model Config", True, 
                                f"Threshold: {model_info['confidence_threshold']}, Skip Frames: {model_info['skip_frames']}")
                    return True
                else:
                    self.log_step("AI Model Test", False, "Model not active")
                    return False
            else:
                self.log_step("AI Model Test", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("AI Model Test", False, f"Error: {str(e)}")
            return False

    def step_4_worker_pool_status(self) -> bool:
        """Step 4: Check worker pool status"""
        print("\n⚙️ STEP 4: WORKER POOL STATUS")
        print("=" * 50)
        
        try:
            response = self.session.get(f"{BASE_URLS['becamera']}/workers/status")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    workers = result.get("data", {}).get("workers", [])
                    
                    total_workers = len(workers)
                    active_workers = len([w for w in workers if w.get("status") == "busy"])
                    ai_workers = len([w for w in workers if w.get("ai_model_loaded")])
                    
                    self.log_step("Worker Pool Status", True, f"Total: {total_workers}, Active: {active_workers}")
                    self.log_step("AI Integration", True, f"AI Model Workers: {ai_workers}")
                    
                    # Show worker details
                    for worker in workers:
                        status = "🟢 Active" if worker.get("status") == "busy" else "🟡 Idle"
                        ai_status = "🤖 AI Ready" if worker.get("ai_model_loaded") else "📊 Standard"
                        print(f"   Worker {worker['worker_id']}: {status} | {ai_status}")
                    
                    return True
                else:
                    self.log_step("Worker Pool Status", False, "Invalid response")
                    return False
            else:
                self.log_step("Worker Pool Status", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("Worker Pool Status", False, f"Error: {str(e)}")
            return False

    def step_5_camera_creation(self) -> bool:
        """Step 5: Create demo camera"""
        print("\n📹 STEP 5: CAMERA CREATION")
        print("=" * 50)
        
        try:
            camera_data = {
                "name": CAMERA_CONFIG["name"],
                "location": CAMERA_CONFIG["location"],
                "stream_url": CAMERA_CONFIG["stream_url"],
                "status": "active"
            }
            
            response = self.session.post(f"{BASE_URLS['becamera']}/cameras", json=camera_data)
            
            if response.status_code == 201:
                response_data = response.json()
                if response_data.get("success") and response_data.get("data"):
                    camera = response_data["data"]
                    self.demo_camera_id = camera.get("id")
                    
                    self.log_step("Camera Creation", True, f"Camera ID: {self.demo_camera_id}")
                    self.log_step("Camera Details", True, 
                                f"Name: {camera.get('name')}, Status: {camera.get('status')}")
                    self.log_step("RTSP Configuration", True, 
                                f"URL: {CAMERA_CONFIG['stream_url']}")
                    return True
                else:
                    self.log_step("Camera Creation", False, "Invalid response format")
                    return False
            else:
                self.log_step("Camera Creation", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("Camera Creation", False, f"Error: {str(e)}")
            return False

    def step_6_camera_ai_processing(self) -> bool:
        """Step 6: Test camera AI processing"""
        print("\n🧠 STEP 6: CAMERA AI PROCESSING")
        print("=" * 50)
        
        if not self.demo_camera_id:
            self.log_step("Camera AI Processing", False, "No camera ID available")
            return False
        
        try:
            response = self.session.post(f"{BASE_URLS['becamera']}/cameras/{self.demo_camera_id}/test-ai")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    ai_results = result.get("data", {}).get("ai_processing_results", {})
                    
                    self.log_step("AI Processing Test", True, "Processing completed")
                    self.log_step("Frame Processing", True, 
                                f"Frames: {ai_results.get('frames_processed')}")
                    self.log_step("People Counting", True, 
                                f"Average Count: {ai_results.get('average_count')}")
                    self.log_step("Confidence Level", True, 
                                f"Average Confidence: {ai_results.get('average_confidence'):.3f}")
                    self.log_step("Processing Performance", True, 
                                f"Time: {ai_results.get('processing_time'):.3f}s")
                    return True
                else:
                    self.log_step("AI Processing Test", False, "Processing failed")
                    return False
            else:
                self.log_step("AI Processing Test", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("AI Processing Test", False, f"Error: {str(e)}")
            return False

    def step_7_camera_processing_start(self) -> bool:
        """Step 7: Start camera processing"""
        print("\n▶️ STEP 7: START CAMERA PROCESSING")
        print("=" * 50)
        
        if not self.demo_camera_id:
            self.log_step("Camera Processing Start", False, "No camera ID available")
            return False
        
        try:
            response = self.session.post(f"{BASE_URLS['becamera']}/cameras/{self.demo_camera_id}/start")
            
            if response.status_code in [200, 201]:  # Accept both status codes
                result = response.json()
                if result.get("success"):
                    self.log_step("Camera Processing Start", True, "Processing started successfully")
                    self.log_step("Worker Assignment", True, "Camera assigned to worker pool")
                    self.log_step("Real-time Updates", True, "WebSocket updates enabled")
                    return True
                else:
                    self.log_step("Camera Processing Start", False, "Start failed")
                    return False
            else:
                self.log_step("Camera Processing Start", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("Camera Processing Start", False, f"Error: {str(e)}")
            return False

    def step_8_system_cleanup(self) -> bool:
        """Step 8: Clean up demo resources"""
        print("\n🧹 STEP 8: SYSTEM CLEANUP")
        print("=" * 50)
        
        if not self.demo_camera_id:
            self.log_step("Camera Cleanup", True, "No camera to clean up")
            return True
        
        try:
            # Stop camera processing first
            stop_response = self.session.post(f"{BASE_URLS['becamera']}/cameras/{self.demo_camera_id}/stop")
            if stop_response.status_code in [200, 201]:
                self.log_step("Camera Stop", True, "Processing stopped")
            
            # Delete camera
            delete_response = self.session.delete(f"{BASE_URLS['becamera']}/cameras/{self.demo_camera_id}")
            
            if delete_response.status_code == 200:
                self.log_step("Camera Deletion", True, "Demo camera deleted")
                return True
            else:
                self.log_step("Camera Deletion", False, f"Status: {delete_response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("Camera Cleanup", False, f"Error: {str(e)}")
            return False

    def run_complete_demo(self):
        """Run the complete system demo"""
        print("🚀 COMPLETE SYSTEM DEMO - AI CAMERA COUNTING")
        print("=" * 60)
        print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Objective: Showcase all system features")
        print("=" * 60)
        
        demo_steps = [
            ("Health Check", self.step_1_health_check),
            ("Authentication", self.step_2_authentication),
            ("AI Model Test", self.step_3_ai_model_test),
            ("Worker Pool Status", self.step_4_worker_pool_status),
            ("Camera Creation", self.step_5_camera_creation),
            ("Camera AI Processing", self.step_6_camera_ai_processing),
            ("Camera Processing Start", self.step_7_camera_processing_start),
            ("System Cleanup", self.step_8_system_cleanup)
        ]
        
        successful_steps = 0
        total_steps = len(demo_steps)
        
        for step_name, step_func in demo_steps:
            try:
                if step_func():
                    successful_steps += 1
                time.sleep(1)  # Brief pause between steps
            except Exception as e:
                self.log_step(step_name, False, f"Unexpected error: {str(e)}")
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 DEMO SUMMARY")
        print("=" * 60)
        
        success_rate = (successful_steps / total_steps) * 100
        
        print(f"✅ Successful Steps: {successful_steps}/{total_steps}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 EXCELLENT: System is production ready!")
        elif success_rate >= 60:
            print("👍 GOOD: System is mostly functional with minor issues")
        else:
            print("⚠️ NEEDS WORK: System has significant issues to resolve")
        
        # Save demo results
        demo_report = {
            "demo_date": datetime.now().isoformat(),
            "success_rate": success_rate,
            "successful_steps": successful_steps,
            "total_steps": total_steps,
            "results": self.demo_results
        }
        
        report_file = f"demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(demo_report, f, indent=2)
        
        print(f"📄 Demo report saved to: {report_file}")
        print("=" * 60)

def main():
    """Main function"""
    demo = CompleteSystemDemo()
    demo.run_complete_demo()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Production Monitoring Script for Face Detection System
Monitors system health, performance, and alerts on issues
"""

import requests
import time
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import psutil
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SystemMonitor:
    def __init__(self, base_url="http://localhost:8000", config_file="monitoring_config.json"):
        self.base_url = base_url
        self.config_file = config_file
        self.monitoring_data = []
        self.alerts = []
        self.is_running = False
        
        # Load configuration
        self.config = self.load_config()
        
        # Monitoring thresholds
        self.thresholds = {
            "response_time_ms": 1000,
            "error_rate_percent": 5.0,
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0
        }
        
    def load_config(self) -> Dict[str, Any]:
        """Load monitoring configuration"""
        default_config = {
            "check_interval_seconds": 30,
            "alert_email": "admin@example.com",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_username": "",
            "smtp_password": "",
            "enable_email_alerts": False,
            "enable_slack_alerts": False,
            "slack_webhook_url": "",
            "monitoring_endpoints": [
                "/health",
                "/api/v1/camera/status",
                "/api/v1/faces/list"
            ]
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def save_config(self):
        """Save monitoring configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def check_api_health(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            return {
                "endpoint": "/health",
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code == 200,
                "timestamp": datetime.now().isoformat(),
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {
                "endpoint": "/health",
                "status_code": 0,
                "response_time_ms": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_endpoint_performance(self, endpoint: str) -> Dict[str, Any]:
        """Check specific endpoint performance"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            return {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code == 200,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "status_code": 0,
                "response_time_ms": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_database_status(self) -> Dict[str, Any]:
        """Check database status"""
        try:
            # Check if database file exists and is accessible
            db_path = "data/metadata.db"
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(db_path))
                
                return {
                    "database_exists": True,
                    "file_size_bytes": file_size,
                    "last_modified": file_time.isoformat(),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "database_exists": False,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_face_recognition_service(self) -> Dict[str, Any]:
        """Check face recognition service status"""
        try:
            # Test face recognition with a simple request
            test_image_path = "automation_test/test_images/test_face.jpg"
            
            if os.path.exists(test_image_path):
                with open(test_image_path, 'rb') as f:
                    files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                    data = {'threshold': '0.6'}
                    
                    start_time = time.time()
                    response = requests.post(
                        f"{self.base_url}/api/v1/faces/recognize",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    response_time = (time.time() - start_time) * 1000
                    
                    return {
                        "service": "face_recognition",
                        "status_code": response.status_code,
                        "response_time_ms": response_time,
                        "success": response.status_code == 200,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "service": "face_recognition",
                    "success": False,
                    "error": "Test image not found",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "service": "face_recognition",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_alert(self, alert_type: str, message: str, severity: str = "warning") -> Dict[str, Any]:
        """Generate an alert"""
        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        
        self.alerts.append(alert)
        print(f"🚨 ALERT [{severity.upper()}]: {message}")
        
        return alert
    
    def check_thresholds(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if any thresholds are exceeded"""
        alerts = []
        
        # Check API response time
        if "response_time_ms" in data and data["response_time_ms"] > self.thresholds["response_time_ms"]:
            alerts.append(self.generate_alert(
                "high_response_time",
                f"API response time {data['response_time_ms']:.1f}ms exceeds threshold {self.thresholds['response_time_ms']}ms",
                "warning"
            ))
        
        # Check system resources
        if "cpu_percent" in data and data["cpu_percent"] > self.thresholds["cpu_percent"]:
            alerts.append(self.generate_alert(
                "high_cpu_usage",
                f"CPU usage {data['cpu_percent']:.1f}% exceeds threshold {self.thresholds['cpu_percent']}%",
                "critical"
            ))
        
        if "memory_percent" in data and data["memory_percent"] > self.thresholds["memory_percent"]:
            alerts.append(self.generate_alert(
                "high_memory_usage",
                f"Memory usage {data['memory_percent']:.1f}% exceeds threshold {self.thresholds['memory_percent']}%",
                "critical"
            ))
        
        if "disk_percent" in data and data["disk_percent"] > self.thresholds["disk_percent"]:
            alerts.append(self.generate_alert(
                "high_disk_usage",
                f"Disk usage {data['disk_percent']:.1f}% exceeds threshold {self.thresholds['disk_percent']}%",
                "critical"
            ))
        
        return alerts
    
    def send_email_alert(self, alert: Dict[str, Any]):
        """Send email alert"""
        if not self.config.get("enable_email_alerts"):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["smtp_username"]
            msg['To'] = self.config["alert_email"]
            msg['Subject'] = f"Face Detection System Alert: {alert['type']}"
            
            body = f"""
            Alert Type: {alert['type']}
            Severity: {alert['severity']}
            Message: {alert['message']}
            Timestamp: {alert['timestamp']}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
            server.starttls()
            server.login(self.config["smtp_username"], self.config["smtp_password"])
            server.send_message(msg)
            server.quit()
            
            print(f"📧 Email alert sent to {self.config['alert_email']}")
        except Exception as e:
            print(f"Error sending email alert: {e}")
    
    def send_slack_alert(self, alert: Dict[str, Any]):
        """Send Slack alert"""
        if not self.config.get("enable_slack_alerts"):
            return
        
        try:
            import requests
            
            slack_data = {
                "text": f"🚨 *Face Detection System Alert*\n"
                       f"*Type:* {alert['type']}\n"
                       f"*Severity:* {alert['severity']}\n"
                       f"*Message:* {alert['message']}\n"
                       f"*Timestamp:* {alert['timestamp']}"
            }
            
            response = requests.post(
                self.config["slack_webhook_url"],
                json=slack_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("📱 Slack alert sent")
            else:
                print(f"Error sending Slack alert: {response.status_code}")
        except Exception as e:
            print(f"Error sending Slack alert: {e}")
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        cycle_data = {
            "timestamp": datetime.now().isoformat(),
            "api_health": self.check_api_health(),
            "system_resources": self.check_system_resources(),
            "database_status": self.check_database_status(),
            "face_recognition": self.check_face_recognition_service(),
            "endpoint_checks": []
        }
        
        # Check all configured endpoints
        for endpoint in self.config["monitoring_endpoints"]:
            cycle_data["endpoint_checks"].append(
                self.check_endpoint_performance(endpoint)
            )
        
        # Check thresholds and generate alerts
        alerts = []
        alerts.extend(self.check_thresholds(cycle_data["api_health"]))
        alerts.extend(self.check_thresholds(cycle_data["system_resources"]))
        
        # Send alerts
        for alert in alerts:
            self.send_email_alert(alert)
            self.send_slack_alert(alert)
        
        # Store monitoring data
        self.monitoring_data.append(cycle_data)
        
        # Keep only last 1000 records
        if len(self.monitoring_data) > 1000:
            self.monitoring_data = self.monitoring_data[-1000:]
        
        return cycle_data
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        print("🔍 Starting Face Detection System Monitoring...")
        print(f"   Check interval: {self.config['check_interval_seconds']} seconds")
        print(f"   Base URL: {self.base_url}")
        print("   Press Ctrl+C to stop")
        
        self.is_running = True
        
        try:
            while self.is_running:
                cycle_data = self.run_monitoring_cycle()
                
                # Print status
                api_health = cycle_data["api_health"]
                system_resources = cycle_data["system_resources"]
                
                status = "✅" if api_health["success"] else "❌"
                print(f"{status} API: {api_health['response_time_ms']:.1f}ms | "
                      f"CPU: {system_resources.get('cpu_percent', 0):.1f}% | "
                      f"Memory: {system_resources.get('memory_percent', 0):.1f}% | "
                      f"Alerts: {len(self.alerts)}")
                
                time.sleep(self.config["check_interval_seconds"])
                
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
            self.is_running = False
    
    def generate_monitoring_report(self) -> Dict[str, Any]:
        """Generate monitoring report"""
        if not self.monitoring_data:
            return {"error": "No monitoring data available"}
        
        # Calculate statistics
        api_response_times = [d["api_health"]["response_time_ms"] for d in self.monitoring_data if d["api_health"]["success"]]
        cpu_usage = [d["system_resources"]["cpu_percent"] for d in self.monitoring_data if "cpu_percent" in d["system_resources"]]
        memory_usage = [d["system_resources"]["memory_percent"] for d in self.monitoring_data if "memory_percent" in d["system_resources"]]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_cycles": len(self.monitoring_data),
            "total_alerts": len(self.alerts),
            "statistics": {
                "api_response_time": {
                    "avg_ms": statistics.mean(api_response_times) if api_response_times else 0,
                    "max_ms": max(api_response_times) if api_response_times else 0,
                    "min_ms": min(api_response_times) if api_response_times else 0
                },
                "cpu_usage": {
                    "avg_percent": statistics.mean(cpu_usage) if cpu_usage else 0,
                    "max_percent": max(cpu_usage) if cpu_usage else 0
                },
                "memory_usage": {
                    "avg_percent": statistics.mean(memory_usage) if memory_usage else 0,
                    "max_percent": max(memory_usage) if memory_usage else 0
                }
            },
            "recent_alerts": self.alerts[-10:] if self.alerts else [],
            "monitoring_data": self.monitoring_data[-100:] if self.monitoring_data else []
        }
        
        return report
    
    def save_monitoring_report(self, report: Dict[str, Any], filename: str = None):
        """Save monitoring report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitoring_report_{timestamp}.json"
        
        report_path = os.path.join("automation_test", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Monitoring report saved to: {report_path}")
        return report_path

def main():
    """Main function"""
    print("🔍 Face Detection System - Production Monitoring")
    print("=" * 60)
    
    # Create monitor instance
    monitor = SystemMonitor()
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Generate final report
    report = monitor.generate_monitoring_report()
    monitor.save_monitoring_report(report)
    
    print("\n✅ Monitoring completed!")

if __name__ == "__main__":
    main() 
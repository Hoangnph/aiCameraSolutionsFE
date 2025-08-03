#!/usr/bin/env python3
"""
🚀 Auto Server Management
Tự động khởi động và quản lý server ổn định
"""

import subprocess
import time
import requests
import sys
import signal
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('auto_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AutoServer:
    def __init__(self):
        self.process = None
        self.running = False
        self.restart_count = 0
        self.max_restarts = 5
        
    def kill_all_processes(self):
        """Kill all existing processes"""
        try:
            # Kill uvicorn processes
            subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True)
            # Kill any processes on port 8000
            subprocess.run(['lsof', '-ti:8000', '|', 'xargs', 'kill', '-9'], shell=True)
            logger.info("🔧 Killed all existing processes")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"⚠️ Error killing processes: {e}")
    
    def start_server(self):
        """Start API server with proper directory"""
        try:
            # Ensure we're in the correct directory
            os.chdir('/Users/macintoshhd/Project/Project/AI_OCR/feMain/labs/face_detection')
            logger.info(f"📁 Working directory: {os.getcwd()}")
            
            # Start server
            self.process = subprocess.Popen([
                'python', '-m', 'uvicorn', 'src.api.main:app',
                '--host', '0.0.0.0', '--port', '8000', '--reload'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            logger.info("⏳ Waiting for server to start...")
            time.sleep(10)
            
            # Check if process is still running
            if self.process.poll() is None:
                logger.info("✅ API server started successfully")
                
                # Test health check
                if self.test_health():
                    logger.info("✅ Health check passed")
                    self.running = True
                    return True
                else:
                    logger.error("❌ Health check failed")
                    return False
            else:
                stdout, stderr = self.process.communicate()
                logger.error(f"❌ API server failed to start:")
                logger.error(f"STDOUT: {stdout.decode()}")
                logger.error(f"STDERR: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting API server: {e}")
            return False
    
    def test_health(self):
        """Test server health"""
        try:
            response = requests.get('http://localhost:8000/health', timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    def monitor_and_restart(self):
        """Monitor server and restart if needed"""
        logger.info("🔄 Starting auto-monitoring...")
        
        while self.restart_count < self.max_restarts:
            try:
                # Check if process is still running
                if self.process and self.process.poll() is not None:
                    logger.warning("⚠️ Server stopped, restarting...")
                    self.restart_count += 1
                    logger.info(f"🔄 Restart attempt {self.restart_count}/{self.max_restarts}")
                    
                    if not self.start_server():
                        logger.error("❌ Failed to restart server")
                        continue
                
                # Test health check every 30 seconds
                if self.test_health():
                    logger.info("✅ Server is healthy")
                    self.restart_count = 0  # Reset counter on success
                else:
                    logger.warning("⚠️ Server health check failed")
                    if self.process:
                        self.process.terminate()
                        self.process.wait()
                
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("\n🛑 Stopping auto server...")
                self.stop_server()
                break
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                time.sleep(10)
        
        if self.restart_count >= self.max_restarts:
            logger.error(f"❌ Max restarts ({self.max_restarts}) reached")
    
    def stop_server(self):
        """Stop API server"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            logger.info("✅ API server stopped")
        self.running = False
    
    def run(self):
        """Run auto server"""
        logger.info("🚀 Starting Auto Server Management")
        logger.info("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_server())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_server())
        
        # Kill existing processes
        self.kill_all_processes()
        
        # Start server
        if self.start_server():
            self.monitor_and_restart()
        else:
            logger.error("❌ Failed to start API server")
            sys.exit(1)

if __name__ == "__main__":
    server = AutoServer()
    server.run() 
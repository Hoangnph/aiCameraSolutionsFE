#!/usr/bin/env python3
"""
🚀 Start Frontend Only
Khởi động frontend server cho Face Detection System
"""

import os
import sys
import subprocess
import signal
import time
import psutil

def check_port_available(port):
    """Check if port is available"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return False

def kill_process_on_port(port):
    """Kill process running on specific port"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        print(f"🔄 Killing process {proc.pid} on port {port}")
                        proc.terminate()
                        proc.wait(timeout=5)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        print(f"⚠️ Error killing process on port {port}: {e}")
    return False

def check_frontend_files():
    """Check if frontend files exist"""
    print("📁 Checking frontend files...")
    
    fe_dir = "fe"
    index_file = os.path.join(fe_dir, "index.html")
    
    if not os.path.exists(fe_dir):
        print(f"❌ Frontend directory '{fe_dir}' not found!")
        return False
    
    if not os.path.exists(index_file):
        print(f"❌ Frontend file '{index_file}' not found!")
        return False
    
    print(f"✅ Frontend files found in '{fe_dir}'")
    return True

def start_frontend_server():
    """Start frontend HTTP server"""
    print("\n🚀 Starting Frontend Server")
    print("=" * 40)
    
    # Check if port 3000 is available
    if not check_port_available(3000):
        print("⚠️ Port 3000 is in use. Attempting to kill existing process...")
        kill_process_on_port(3000)
        time.sleep(2)
    
    if not check_port_available(3000):
        print("❌ Port 3000 is still in use. Please manually stop the process.")
        return False
    
    # Check frontend files
    if not check_frontend_files():
        return False
    
    try:
        print("🌐 Starting HTTP server on port 3000...")
        print("📂 Serving from: fe/")
        print("🌍 Frontend will be available at: http://localhost:3000")
        print("\n" + "="*50)
        print("🚀 FRONTEND SERVER STARTED!")
        print("="*50)
        print("📱 Open your browser and go to: http://localhost:3000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("="*50)
        
        # Change to fe directory and start server
        os.chdir("fe")
        
        # Start HTTP server
        subprocess.run([
            sys.executable, "-m", "http.server", "3000"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Frontend server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting frontend server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 Face Detection System - Frontend Only")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("fe"):
        print("❌ Please run this script from the face_detection directory")
        print("   Current directory:", os.getcwd())
        return
    
    # Start frontend
    success = start_frontend_server()
    
    if success:
        print("\n✅ Frontend server started successfully!")
    else:
        print("\n❌ Failed to start frontend server!")

if __name__ == "__main__":
    main() 
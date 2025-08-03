#!/usr/bin/env python3
"""
🚀 Start Frontend in Background
Khởi động frontend server trong background
"""

import os
import sys
import subprocess
import time
import psutil
import signal

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

def start_frontend_background():
    """Start frontend server in background"""
    print("\n🚀 Starting Frontend Server in Background")
    print("=" * 50)
    
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
        print("🌐 Starting HTTP server on port 3000 in background...")
        print("📂 Serving from: fe/")
        print("🌍 Frontend will be available at: http://localhost:3000")
        
        # Change to fe directory
        os.chdir("fe")
        
        # Start HTTP server in background
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "3000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ Frontend server started successfully!")
            print(f"📋 Process ID: {process.pid}")
            print(f"🌍 Frontend URL: http://localhost:3000")
            print(f"⏹️  To stop: kill {process.pid} or run stop_all.py")
            
            # Save PID to file for easy stopping
            with open("../frontend.pid", "w") as f:
                f.write(str(process.pid))
            print(f"💾 PID saved to: frontend.pid")
            
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend server failed to start!")
            print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Face Detection System - Frontend Background")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("fe"):
        print("❌ Please run this script from the face_detection directory")
        print("   Current directory:", os.getcwd())
        return
    
    # Start frontend in background
    success = start_frontend_background()
    
    if success:
        print("\n✅ Frontend server started in background!")
        print("📱 You can now open http://localhost:3000 in your browser")
        print("🔄 The server will continue running until you stop it")
    else:
        print("\n❌ Failed to start frontend server!")

if __name__ == "__main__":
    main() 
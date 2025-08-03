#!/usr/bin/env python3
"""
🎛️ Manage Frontend
Comprehensive script to manage frontend server
"""

import os
import sys
import subprocess
import psutil
import time
import argparse

def check_frontend_status():
    """Check if frontend server is running"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == 3000:
                        return True, proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except:
        pass
    return False, None

def start_frontend():
    """Start frontend server"""
    print("🚀 Starting Frontend Server...")
    print("=" * 40)
    
    # Check if already running
    is_running, pid = check_frontend_status()
    if is_running:
        print(f"⚠️  Frontend server is already running (PID: {pid})")
        return True
    
    # Get project directory (3 levels up from scripts/management/)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fe_dir = os.path.join(project_dir, "fe")
    
    # Check if fe directory exists
    if not os.path.exists(fe_dir):
        print("❌ 'fe' directory not found!")
        print(f"   Expected: {fe_dir}")
        return False
    
    try:
        # Change to fe directory
        os.chdir(fe_dir)
        
        print("📂 Serving from: fe/")
        print("🌍 Frontend URL: http://localhost:3000")
        print("⏹️  Press Ctrl+C to stop")
        print("=" * 40)
        
        # Start HTTP server
        subprocess.run([
            sys.executable, "-m", "http.server", "3000"
        ])
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

def stop_frontend():
    """Stop frontend server"""
    print("🛑 Stopping Frontend Server...")
    print("=" * 40)
    
    is_running, pid = check_frontend_status()
    if not is_running:
        print("ℹ️  Frontend server is not running")
        return True
    
    try:
        # Kill process
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=5)
        print(f"✅ Frontend server stopped (PID: {pid})")
        return True
        
    except Exception as e:
        print(f"❌ Error stopping frontend: {e}")
        return False

def restart_frontend():
    """Restart frontend server"""
    print("🔄 Restarting Frontend Server...")
    print("=" * 40)
    
    # Stop first
    stop_frontend()
    time.sleep(2)
    
    # Start again
    return start_frontend()

def show_status():
    """Show frontend server status"""
    print("📊 Frontend Server Status")
    print("=" * 30)
    
    is_running, pid = check_frontend_status()
    
    if is_running:
        print(f"✅ Frontend server is running")
        print(f"📋 Process ID: {pid}")
        print(f"🌍 URL: http://localhost:3000")
        
        # Test if server responds
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=2)
            if response.status_code == 200:
                print("✅ Server is responding")
            else:
                print(f"⚠️  Server responded with status: {response.status_code}")
        except:
            print("❌ Server is not responding")
    else:
        print("❌ Frontend server is not running")
        print("💡 Use 'start' command to start the server")

def main():
    parser = argparse.ArgumentParser(description="Manage Frontend Server")
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    print("🎛️ Face Detection System - Frontend Manager")
    print("=" * 50)
    
    if args.action == 'start':
        success = start_frontend()
        if success:
            print("\n✅ Frontend server started!")
        else:
            print("\n❌ Failed to start frontend server!")
            
    elif args.action == 'stop':
        success = stop_frontend()
        if success:
            print("\n✅ Frontend server stopped!")
        else:
            print("\n❌ Failed to stop frontend server!")
            
    elif args.action == 'restart':
        success = restart_frontend()
        if success:
            print("\n✅ Frontend server restarted!")
        else:
            print("\n❌ Failed to restart frontend server!")
            
    elif args.action == 'status':
        show_status()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🛑 Stop Frontend
Script to stop frontend server
"""

import subprocess
import psutil
import time

def stop_frontend():
    """Stop frontend server on port 3000"""
    print("🛑 Stopping Frontend Server...")
    print("=" * 40)
    
    try:
        # Find and kill process on port 3000
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == 3000:
                        print(f"🔄 Killing process {proc.pid} on port 3000")
                        proc.terminate()
                        proc.wait(timeout=5)
                        print("✅ Frontend server stopped successfully!")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
        
        print("ℹ️  No frontend server found on port 3000")
        return True
        
    except Exception as e:
        print(f"❌ Error stopping frontend server: {e}")
        return False

def main():
    print("🛑 Face Detection System - Stop Frontend")
    print("=" * 45)
    
    success = stop_frontend()
    
    if success:
        print("\n✅ Frontend server stopped!")
    else:
        print("\n❌ Failed to stop frontend server!")

if __name__ == "__main__":
    main() 
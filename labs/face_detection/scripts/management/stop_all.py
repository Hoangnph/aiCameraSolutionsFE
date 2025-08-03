#!/usr/bin/env python3
"""
🛑 Stop All Servers Script
Dừng tất cả servers của Face Detection System
"""

import subprocess
import sys
import time

def kill_processes_on_port(port):
    """Kill all processes on a specific port"""
    try:
        # Find processes on port
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"🔪 Killing process {pid} on port {port}")
                    subprocess.run(["kill", "-9", pid])
                    time.sleep(0.5)
            print(f"✅ Killed all processes on port {port}")
        else:
            print(f"ℹ️  No processes found on port {port}")
    except Exception as e:
        print(f"⚠️  Error killing processes on port {port}: {e}")

def main():
    """Main function"""
    print("🛑 Stop All Servers Script")
    print("=" * 50)
    
    # Ports to check
    ports = [8000, 3000]  # Backend and Frontend ports
    
    print("🔍 Checking for running servers...")
    
    for port in ports:
        print(f"\n📡 Checking port {port}...")
        kill_processes_on_port(port)
    
    print("\n✅ All servers stopped!")
    print("💡 To restart, run:")
    print("   - Backend only: python start_backend.py")
    print("   - Frontend only: python start_frontend.py")
    print("   - Both: python start_all.py")

if __name__ == "__main__":
    main() 
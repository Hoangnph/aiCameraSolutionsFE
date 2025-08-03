#!/usr/bin/env python3
"""
🚀 Start Frontend
Simple script to start frontend server
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting Frontend Server...")
    print("=" * 40)
    
    # Check if fe directory exists
    if not os.path.exists("fe"):
        print("❌ 'fe' directory not found!")
        print("   Please run from face_detection directory")
        return
    
    # Change to fe directory
    os.chdir("fe")
    
    print("📂 Serving from: fe/")
    print("🌍 Frontend URL: http://localhost:3000")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        # Start HTTP server
        subprocess.run([
            sys.executable, "-m", "http.server", "3000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

if __name__ == "__main__":
    main() 
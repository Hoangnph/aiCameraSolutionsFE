#!/usr/bin/env python3
"""
🚀 Quick Start Frontend
Simple script to start frontend server quickly
"""

import os
import sys
import subprocess

def main():
    print("🚀 Quick Start Frontend")
    print("=" * 30)
    
    # Check if fe directory exists
    if not os.path.exists("fe"):
        print("❌ 'fe' directory not found!")
        return
    
    # Change to fe directory
    os.chdir("fe")
    
    print("📂 Serving from: fe/")
    print("🌍 Frontend URL: http://localhost:3000")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 30)
    
    # Start HTTP server
    subprocess.run([sys.executable, "-m", "http.server", "3000"])

if __name__ == "__main__":
    main() 
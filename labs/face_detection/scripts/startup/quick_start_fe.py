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
    
    # Get project directory (3 levels up from scripts/startup/)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fe_dir = os.path.join(project_dir, "fe")
    
    # Check if fe directory exists
    if not os.path.exists(fe_dir):
        print("❌ 'fe' directory not found!")
        print(f"   Expected: {fe_dir}")
        return
    
    # Change to fe directory
    os.chdir(fe_dir)
    
    print("📂 Serving from: fe/")
    print("🌍 Frontend URL: http://localhost:3000")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 30)
    
    # Start HTTP server
    subprocess.run([sys.executable, "-m", "http.server", "3000"])

if __name__ == "__main__":
    main() 
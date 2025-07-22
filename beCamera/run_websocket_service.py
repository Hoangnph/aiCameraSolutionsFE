#!/usr/bin/env python3
"""
Script to run the WebSocket service for AI Camera Counting System
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import the WebSocket service
from websocket_service import app

if __name__ == "__main__":
    print("🚀 Starting WebSocket Service...")
    print("📍 Port: 3004")
    print("🌐 URL: ws://localhost:3004")
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=3004,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 WebSocket Service stopped by user")
    except Exception as e:
        print(f"❌ Error starting WebSocket Service: {e}")
        sys.exit(1) 
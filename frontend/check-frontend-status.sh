#!/bin/bash

echo "🔍 Checking Frontend Status..."

# Check if React server is running
echo "📋 Checking React development server..."
if lsof -i :3000 >/dev/null 2>&1; then
    echo "✅ React server is running on port 3000"
    
    # Test the server response
    echo "🌐 Testing server response..."
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo "✅ Server is responding correctly"
    else
        echo "❌ Server is not responding"
    fi
else
    echo "❌ React server is not running on port 3000"
fi

# Check dependencies
echo "📦 Checking dependencies..."
if npm list axios socket.io-client >/dev/null 2>&1; then
    echo "✅ Required dependencies are installed"
else
    echo "❌ Missing required dependencies"
fi

# Check build
echo "🔨 Testing build..."
if npm run build >/dev/null 2>&1; then
    echo "✅ Build is successful"
else
    echo "❌ Build failed"
fi

# Check for infinite loops
echo "🔄 Checking for potential infinite loops..."
if ps aux | grep -i "react-scripts" | grep -v grep | wc -l | grep -q "1"; then
    echo "✅ Only one React process is running"
else
    echo "⚠️  Multiple React processes detected"
fi

echo "🎉 Frontend status check completed!" 
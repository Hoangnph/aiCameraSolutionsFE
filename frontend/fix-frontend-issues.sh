#!/bin/bash

echo "🔧 Fixing Frontend Issues..."

# Stop any running processes on port 3000
echo "📋 Stopping processes on port 3000..."
pkill -f "react-scripts" 2>/dev/null
docker stop ai_camera_frontend 2>/dev/null

# Clean up
echo "🧹 Cleaning up..."
rm -rf node_modules package-lock.json build

# Install dependencies
echo "📦 Installing dependencies..."
npm install --legacy-peer-deps

# Check if dependencies are installed
echo "✅ Checking dependencies..."
if npm list axios socket.io-client >/dev/null 2>&1; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Dependencies installation failed"
    exit 1
fi

# Build the project
echo "🔨 Building project..."
if npm run build; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi

# Start development server
echo "🚀 Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
npm start 
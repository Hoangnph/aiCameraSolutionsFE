#!/bin/bash

# AI Camera Counting System - Development Environment Stop Script

echo "🛑 Stopping AI Camera Counting System Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Stop frontend
stop_frontend() {
    print_status "Stopping React frontend..."
    
    # Kill any process running on port 3000
    pkill -f "react-scripts start" 2>/dev/null || true
    pkill -f "npm start" 2>/dev/null || true
    
    # Kill any process on port 3000
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    
    print_success "Frontend stopped"
}

# Stop beCamera service
stop_becamera() {
    print_status "Stopping beCamera service..."
    
    cd beCamera
    docker-compose down 2>/dev/null || true
    cd ..
    
    print_success "beCamera service stopped"
}

# Stop beAuth service
stop_beauth() {
    print_status "Stopping beAuth service..."
    
    cd beAuth
    docker-compose down 2>/dev/null || true
    cd ..
    
    print_success "beAuth service stopped"
}

# Stop shared resources
stop_shared_resources() {
    print_status "Stopping shared PostgreSQL and Redis..."
    
    # Stop containers by name
    docker stop ai-camera-postgres ai-camera-redis 2>/dev/null || true
    docker rm ai-camera-postgres ai-camera-redis 2>/dev/null || true
    
    print_success "Shared resources stopped"
}

# Clean up Docker resources
cleanup_docker() {
    print_status "Cleaning up Docker resources..."
    
    # Remove unused containers
    docker container prune -f 2>/dev/null || true
    
    # Remove unused networks
    docker network prune -f 2>/dev/null || true
    
    print_success "Docker cleanup completed"
}

# Main execution
main() {
    stop_frontend
    stop_becamera
    stop_beauth
    stop_shared_resources
    cleanup_docker
    
    print_success "🎉 All services stopped successfully!"
    echo ""
    echo "📋 Summary:"
    echo "   ✅ Frontend stopped"
    echo "   ✅ beCamera service stopped"
    echo "   ✅ beAuth service stopped"
    echo "   ✅ PostgreSQL stopped"
    echo "   ✅ Redis stopped"
    echo "   ✅ Docker cleanup completed"
    echo ""
}

# Run main function
main "$@" 
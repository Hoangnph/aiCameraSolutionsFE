#!/bin/bash

# AI Camera Counting System - Development Environment Startup Script
# This script starts all services with shared PostgreSQL/Redis resources

set -e

echo "🚀 Starting AI Camera Counting System Development Environment..."

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

# Check if Docker is running
check_docker() {
    print_status "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop first."
        exit 1
    fi
    print_success "Docker is running"
}

# Stop and remove existing containers
cleanup_containers() {
    print_status "Cleaning up existing containers..."
    
    # Stop containers if they exist
    docker stop ai-camera-postgres ai-camera-redis ai-auth-service ai-camera-service 2>/dev/null || true
    docker rm ai-camera-postgres ai-camera-redis ai-auth-service ai-camera-service 2>/dev/null || true
    
    print_success "Cleanup completed"
}

# Start shared PostgreSQL and Redis
start_shared_resources() {
    print_status "Starting shared PostgreSQL and Redis..."
    
    cd beAuth
    
    # Start PostgreSQL and Redis
    docker-compose up -d postgres redis
    
    # Wait for services to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    timeout=60
    while ! docker exec ai-camera-postgres pg_isready -U postgres -d people_counting_db > /dev/null 2>&1; do
        if [ $timeout -le 0 ]; then
            print_error "PostgreSQL failed to start within 60 seconds"
            exit 1
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    print_status "Waiting for Redis to be ready..."
    timeout=30
    while ! docker exec ai-camera-redis redis-cli ping > /dev/null 2>&1; do
        if [ $timeout -le 0 ]; then
            print_error "Redis failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    print_success "Shared resources started successfully"
    cd ..
}

# Start beAuth service
start_beauth() {
    print_status "Starting beAuth service..."
    
    cd beAuth
    
    # Start the auth service
    docker-compose up -d
    
    # Wait for service to be ready
    print_status "Waiting for beAuth service to be ready..."
    timeout=60
    while ! curl -f http://localhost:3001/health > /dev/null 2>&1; do
        if [ $timeout -le 0 ]; then
            print_error "beAuth service failed to start within 60 seconds"
            exit 1
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    print_success "beAuth service started successfully"
    cd ..
}

# Start beCamera service
start_becamera() {
    print_status "Starting beCamera service..."
    
    cd beCamera
    
    # Build and start the camera service
    docker-compose up -d
    
    # Wait for service to be ready
    print_status "Waiting for beCamera service to be ready..."
    timeout=60
    while ! curl -f http://localhost:3002/health > /dev/null 2>&1; do
        if [ $timeout -le 0 ]; then
            print_error "beCamera service failed to start within 60 seconds"
            exit 1
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    print_success "beCamera service started successfully"
    cd ..
}

# Start frontend
start_frontend() {
    print_status "Starting React frontend..."
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend in background
    npm start &
    FRONTEND_PID=$!
    
    # Wait for frontend to be ready
    print_status "Waiting for frontend to be ready..."
    timeout=60
    while ! curl -f http://localhost:3000 > /dev/null 2>&1; do
        if [ $timeout -le 0 ]; then
            print_error "Frontend failed to start within 60 seconds"
            exit 1
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    print_success "Frontend started successfully"
}

# Health check all services
health_check() {
    print_status "Performing health checks..."
    
    # Check beAuth
    if curl -f http://localhost:3001/health > /dev/null 2>&1; then
        print_success "beAuth service: HEALTHY"
    else
        print_error "beAuth service: UNHEALTHY"
    fi
    
    # Check beCamera
    if curl -f http://localhost:3002/health > /dev/null 2>&1; then
        print_success "beCamera service: HEALTHY"
    else
        print_error "beCamera service: UNHEALTHY"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend: HEALTHY"
    else
        print_error "Frontend: UNHEALTHY"
    fi
    
    # Check PostgreSQL
    if docker exec ai-camera-postgres pg_isready -U postgres -d people_counting_db > /dev/null 2>&1; then
        print_success "PostgreSQL: HEALTHY"
    else
        print_error "PostgreSQL: UNHEALTHY"
    fi
    
    # Check Redis
    if docker exec ai-camera-redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis: HEALTHY"
    else
        print_error "Redis: UNHEALTHY"
    fi
}

# Display service URLs
show_urls() {
    echo ""
    echo "🌐 Service URLs:"
    echo "   Frontend:     http://localhost:3000"
    echo "   beAuth API:   http://localhost:3001"
    echo "   beCamera API: http://localhost:3002"
    echo "   PostgreSQL:   localhost:5432"
    echo "   Redis:        localhost:6379"
    echo ""
    echo "📊 Health Check URLs:"
    echo "   beAuth:       http://localhost:3001/health"
    echo "   beCamera:     http://localhost:3002/health"
    echo ""
    echo "🔧 Development Tools:"
    echo "   Docker logs:  docker logs <container_name>"
    echo "   Stop all:     ./stop-dev.sh"
    echo ""
}

# Main execution
main() {
    check_docker
    cleanup_containers
    start_shared_resources
    start_beauth
    start_becamera
    start_frontend
    health_check
    show_urls
    
    print_success "🎉 All services started successfully!"
    print_status "Press Ctrl+C to stop all services"
    
    # Keep script running and handle cleanup on exit
    trap 'echo ""; print_status "Stopping services..."; docker stop ai-camera-postgres ai-camera-redis ai-auth-service ai-camera-service 2>/dev/null || true; kill $FRONTEND_PID 2>/dev/null || true; print_success "Services stopped"; exit 0' INT TERM
    
    # Wait for user interrupt
    wait
}

# Run main function
main "$@" 
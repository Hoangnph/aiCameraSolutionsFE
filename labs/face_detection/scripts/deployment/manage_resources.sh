#!/bin/bash

# Face Detection System - Resource Management Script
# This script helps manage the running resources and services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVER_URL="http://localhost:8000"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/logs/resource_management.log"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS") echo -e "${GREEN}✅ $message${NC}" ;;
        "ERROR") echo -e "${RED}❌ $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "INFO") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Check if server is running
check_server() {
    log "Checking server status..."
    if curl -s "$SERVER_URL/health" > /dev/null 2>&1; then
        print_status "SUCCESS" "Server is running on $SERVER_URL"
        return 0
    else
        print_status "ERROR" "Server is not responding on $SERVER_URL"
        return 1
    fi
}

# Start the server
start_server() {
    log "Starting Face Detection System server..."
    
    # Check if already running
    if check_server; then
        print_status "WARNING" "Server is already running"
        return 0
    fi
    
    # Kill any existing processes
    pkill -f "uvicorn.*src.api.main:app" 2>/dev/null || true
    
    # Start server in background
    cd "$PROJECT_DIR"
    nohup python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload > "$PROJECT_DIR/logs/server.log" 2>&1 &
    
    # Wait for server to start
    sleep 5
    
    if check_server; then
        print_status "SUCCESS" "Server started successfully"
        log "Server started successfully"
    else
        print_status "ERROR" "Failed to start server"
        log "Failed to start server"
        return 1
    fi
}

# Stop the server
stop_server() {
    log "Stopping Face Detection System server..."
    
    # Kill uvicorn processes
    pkill -f "uvicorn.*src.api.main:app" 2>/dev/null || true
    
    # Wait a moment
    sleep 2
    
    if check_server; then
        print_status "WARNING" "Server is still running"
        return 1
    else
        print_status "SUCCESS" "Server stopped successfully"
        log "Server stopped successfully"
    fi
}

# Restart the server
restart_server() {
    log "Restarting Face Detection System server..."
    stop_server
    sleep 2
    start_server
}

# Check system health
check_health() {
    log "Checking system health..."
    
    if ! check_server; then
        print_status "ERROR" "Server is not running"
        return 1
    fi
    
    # Get health status
    health_response=$(curl -s "$SERVER_URL/health")
    
    if echo "$health_response" | grep -q '"success":true'; then
        print_status "SUCCESS" "System health check passed"
        echo "$health_response" | python -m json.tool 2>/dev/null || echo "$health_response"
    else
        print_status "ERROR" "System health check failed"
        echo "$health_response"
        return 1
    fi
}

# Check database status
check_database() {
    log "Checking database status..."
    
    # Check if database files exist
    if [ -f "$PROJECT_DIR/data/metadata.db" ]; then
        print_status "SUCCESS" "SQLite database exists"
    else
        print_status "WARNING" "SQLite database not found"
    fi
    
    if [ -f "$PROJECT_DIR/data/face_vectors.db" ]; then
        print_status "SUCCESS" "Vector database exists"
    else
        print_status "WARNING" "Vector database not found"
    fi
    
    # Check database records via API
    if check_server; then
        faces_response=$(curl -s "$SERVER_URL/api/v1/faces/list")
        if echo "$faces_response" | grep -q '"success":true'; then
            face_count=$(echo "$faces_response" | python -c "import sys, json; data=json.load(sys.stdin); print(len(data['data']['faces']))" 2>/dev/null || echo "0")
            print_status "SUCCESS" "Database accessible - $face_count faces registered"
        else
            print_status "ERROR" "Database not accessible via API"
        fi
    fi
}

# Check camera status
check_camera() {
    log "Checking camera status..."
    
    if ! check_server; then
        print_status "ERROR" "Server not running"
        return 1
    fi
    
    camera_response=$(curl -s "$SERVER_URL/api/v1/camera/status")
    
    if echo "$camera_response" | grep -q '"success":true'; then
        print_status "SUCCESS" "Camera service is healthy"
        echo "$camera_response" | python -m json.tool 2>/dev/null || echo "$camera_response"
    else
        print_status "ERROR" "Camera service not responding"
        echo "$camera_response"
    fi
}

# Show system status
show_status() {
    log "Showing system status..."
    
    echo -e "\n${BLUE}=== Face Detection System Status ===${NC}\n"
    
    # Server status
    if check_server; then
        print_status "SUCCESS" "Server: RUNNING"
    else
        print_status "ERROR" "Server: STOPPED"
    fi
    
    # Process status
    if pgrep -f "uvicorn.*src.api.main:app" > /dev/null; then
        print_status "SUCCESS" "Process: ACTIVE"
    else
        print_status "ERROR" "Process: INACTIVE"
    fi
    
    # Port status
    if lsof -i :8000 > /dev/null 2>&1; then
        print_status "SUCCESS" "Port 8000: IN USE"
    else
        print_status "ERROR" "Port 8000: AVAILABLE"
    fi
    
    # Database status
    check_database
    
    # Camera status
    check_camera
    
    echo -e "\n${BLUE}=== Resource Usage ===${NC}\n"
    
    # Memory usage
    if pgrep -f "uvicorn.*src.api.main:app" > /dev/null; then
        memory_usage=$(ps -o rss= -p $(pgrep -f "uvicorn.*src.api.main:app") | awk '{print $1/1024 " MB"}')
        print_status "INFO" "Memory Usage: $memory_usage"
    fi
    
    # Disk usage
    disk_usage=$(du -sh "$PROJECT_DIR/data" 2>/dev/null | cut -f1 || echo "N/A")
    print_status "INFO" "Database Size: $disk_usage"
    
    upload_size=$(du -sh "$PROJECT_DIR/uploads" 2>/dev/null | cut -f1 || echo "N/A")
    print_status "INFO" "Uploads Size: $upload_size"
}

# Test API endpoints
test_api() {
    log "Testing API endpoints..."
    
    if ! check_server; then
        print_status "ERROR" "Server not running"
        return 1
    fi
    
    echo -e "\n${BLUE}=== API Endpoint Tests ===${NC}\n"
    
    # Test health endpoint
    if curl -s "$SERVER_URL/health" | grep -q '"success":true'; then
        print_status "SUCCESS" "Health endpoint: OK"
    else
        print_status "ERROR" "Health endpoint: FAILED"
    fi
    
    # Test root endpoint
    if curl -s "$SERVER_URL/" | grep -q '"success":true'; then
        print_status "SUCCESS" "Root endpoint: OK"
    else
        print_status "ERROR" "Root endpoint: FAILED"
    fi
    
    # Test face list endpoint
    if curl -s "$SERVER_URL/api/v1/faces/list" | grep -q '"success":true'; then
        print_status "SUCCESS" "Face list endpoint: OK"
    else
        print_status "ERROR" "Face list endpoint: FAILED"
    fi
    
    # Test camera status endpoint
    if curl -s "$SERVER_URL/api/v1/camera/status" | grep -q '"success":true'; then
        print_status "SUCCESS" "Camera status endpoint: OK"
    else
        print_status "ERROR" "Camera status endpoint: FAILED"
    fi
}

# Clean up resources
cleanup() {
    log "Cleaning up resources..."
    
    # Stop server
    stop_server
    
    # Clean up temporary files
    rm -f "$PROJECT_DIR/logs/server.log"
    
    print_status "SUCCESS" "Cleanup completed"
}

# Show help
show_help() {
    echo -e "${BLUE}Face Detection System - Resource Management${NC}\n"
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the server"
    echo "  stop        Stop the server"
    echo "  restart     Restart the server"
    echo "  status      Show system status"
    echo "  health      Check system health"
    echo "  test        Test API endpoints"
    echo "  cleanup     Clean up resources"
    echo "  help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 test"
}

# Main script logic
case "${1:-help}" in
    "start")
        start_server
        ;;
    "stop")
        stop_server
        ;;
    "restart")
        restart_server
        ;;
    "status")
        show_status
        ;;
    "health")
        check_health
        ;;
    "test")
        test_api
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|*)
        show_help
        ;;
esac 
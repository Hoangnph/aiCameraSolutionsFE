#!/bin/bash

# Face Detection System - Deployment Script
# Manages Docker container deployment and operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="face-detection-system"
COMPOSE_FILE="docker-compose.yml"
DOCKERFILE="Dockerfile"

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

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_status "ERROR" "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_status "SUCCESS" "Docker is running"
}

# Build the Docker image
build_image() {
    print_status "INFO" "Building Docker image..."
    
    if docker build -t $PROJECT_NAME:latest .; then
        print_status "SUCCESS" "Docker image built successfully"
    else
        print_status "ERROR" "Failed to build Docker image"
        exit 1
    fi
}

# Start the services
start_services() {
    print_status "INFO" "Starting services..."
    
    if docker-compose -f $COMPOSE_FILE up -d; then
        print_status "SUCCESS" "Services started successfully"
    else
        print_status "ERROR" "Failed to start services"
        exit 1
    fi
}

# Stop the services
stop_services() {
    print_status "INFO" "Stopping services..."
    
    if docker-compose -f $COMPOSE_FILE down; then
        print_status "SUCCESS" "Services stopped successfully"
    else
        print_status "ERROR" "Failed to stop services"
        exit 1
    fi
}

# Restart the services
restart_services() {
    print_status "INFO" "Restarting services..."
    
    stop_services
    sleep 2
    start_services
}

# Show service status
show_status() {
    print_status "INFO" "Service status:"
    docker-compose -f $COMPOSE_FILE ps
    
    print_status "INFO" "Container logs:"
    docker-compose -f $COMPOSE_FILE logs --tail=10
}

# Check service health
check_health() {
    print_status "INFO" "Checking service health..."
    
    # Wait for service to be ready
    sleep 10
    
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "SUCCESS" "Service is healthy"
        curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "Health check response received"
    else
        print_status "ERROR" "Service is not responding"
        return 1
    fi
}

# Run tests in container
run_tests() {
    print_status "INFO" "Running tests in container..."
    
    # Run automation tests
    docker-compose -f $COMPOSE_FILE exec face-detection-api python automation_test/run_system_tests.py
    
    # Run performance tests
    docker-compose -f $COMPOSE_FILE exec face-detection-api python performance_test.py
    
    # Run security tests
    docker-compose -f $COMPOSE_FILE exec face-detection-api python security_test.py
}

# Clean up containers and images
cleanup() {
    print_status "INFO" "Cleaning up containers and images..."
    
    # Stop and remove containers
    docker-compose -f $COMPOSE_FILE down --rmi all --volumes --remove-orphans
    
    # Remove images
    docker rmi $PROJECT_NAME:latest 2>/dev/null || true
    
    print_status "SUCCESS" "Cleanup completed"
}

# Show logs
show_logs() {
    print_status "INFO" "Showing service logs:"
    docker-compose -f $COMPOSE_FILE logs -f
}

# Execute command in container
exec_command() {
    local command=$1
    print_status "INFO" "Executing command in container: $command"
    docker-compose -f $COMPOSE_FILE exec face-detection-api $command
}

# Build and deploy
deploy() {
    print_status "INFO" "Starting deployment..."
    
    check_docker
    build_image
    start_services
    
    print_status "INFO" "Waiting for services to start..."
    sleep 15
    
    if check_health; then
        print_status "SUCCESS" "Deployment completed successfully!"
        print_status "INFO" "API is available at: http://localhost:8000"
        print_status "INFO" "API Documentation: http://localhost:8000/docs"
    else
        print_status "ERROR" "Deployment failed - service is not healthy"
        exit 1
    fi
}

# Show help
show_help() {
    echo -e "${BLUE}Face Detection System - Deployment Script${NC}\n"
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      Build and deploy the application"
    echo "  start       Start the services"
    echo "  stop        Stop the services"
    echo "  restart     Restart the services"
    echo "  status      Show service status"
    echo "  health      Check service health"
    echo "  logs        Show service logs"
    echo "  test        Run tests in container"
    echo "  exec CMD    Execute command in container"
    echo "  cleanup     Clean up containers and images"
    echo "  help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 deploy"
    echo "  $0 status"
    echo "  $0 test"
    echo "  $0 exec 'python manage_resources.sh status'"
}

# Main script logic
case "${1:-help}" in
    "deploy")
        deploy
        ;;
    "start")
        check_docker
        start_services
        ;;
    "stop")
        check_docker
        stop_services
        ;;
    "restart")
        check_docker
        restart_services
        ;;
    "status")
        check_docker
        show_status
        ;;
    "health")
        check_health
        ;;
    "logs")
        check_docker
        show_logs
        ;;
    "test")
        check_docker
        run_tests
        ;;
    "exec")
        if [ -z "$2" ]; then
            print_status "ERROR" "Please provide a command to execute"
            exit 1
        fi
        check_docker
        exec_command "$2"
        ;;
    "cleanup")
        check_docker
        cleanup
        ;;
    "help"|*)
        show_help
        ;;
esac 
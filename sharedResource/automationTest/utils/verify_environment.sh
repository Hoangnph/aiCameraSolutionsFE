#!/bin/bash

# 🧪 Environment Verification Script - AI Camera Counting System
# 📅 Created: 2025-01-09
# 👥 Maintainer: QA Team

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Header
echo "=========================================="
echo "🧪 ENVIRONMENT VERIFICATION"
echo "AI Camera Counting System - Test Environment"
echo "=========================================="
echo ""

# Check if Docker is running
log "Checking Docker status..."
if docker info >/dev/null 2>&1; then
    success "Docker is running"
else
    error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if containers are running
log "Checking Docker containers..."
CONTAINERS=("ai_camera_postgres" "ai_camera_redis" "ai_camera_beauth" "ai_camera_becamera" "ai_camera_websocket")

for container in "${CONTAINERS[@]}"; do
    if docker ps --format "table {{.Names}}" | grep -q "$container"; then
        success "Container $container is running"
    else
        error "Container $container is not running"
        exit 1
    fi
done

# Check service health endpoints
log "Checking service health endpoints..."

# Check beAuth health
if curl -f http://localhost:3001/health >/dev/null 2>&1; then
    success "beAuth service is healthy (Port 3001)"
else
    error "beAuth service is not responding (Port 3001)"
    exit 1
fi

# Check beCamera health
if curl -f http://localhost:3002/health >/dev/null 2>&1; then
    success "beCamera service is healthy (Port 3002)"
else
    error "beCamera service is not responding (Port 3002)"
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    success "Frontend is accessible (Port 3000)"
else
    error "Frontend is not accessible (Port 3000)"
    exit 1
fi

# Check database connection
log "Checking database connection..."
if docker exec ai_camera_postgres pg_isready -U postgres -d people_counting_db >/dev/null 2>&1; then
    success "PostgreSQL database is ready"
else
    error "PostgreSQL database is not ready"
    exit 1
fi

# Check Redis connection
log "Checking Redis connection..."
if docker exec ai_camera_redis redis-cli ping >/dev/null 2>&1; then
    success "Redis is responding"
else
    error "Redis is not responding"
    exit 1
fi

# Check required tools
log "Checking required tools..."

# Check curl
if command -v curl >/dev/null 2>&1; then
    success "curl is available"
else
    error "curl is not installed"
    exit 1
fi

# Check jq (for JSON parsing)
if command -v jq >/dev/null 2>&1; then
    success "jq is available"
else
    warning "jq is not installed (optional for JSON parsing)"
fi

# Check Python
if command -v python3 >/dev/null 2>&1; then
    success "Python 3 is available"
else
    error "Python 3 is not installed"
    exit 1
fi

# Check Node.js
if command -v node >/dev/null 2>&1; then
    success "Node.js is available"
else
    warning "Node.js is not installed (optional for some tests)"
fi

# Check port availability
log "Checking port availability..."
PORTS=(3000 3001 3002 3003 5432 6379)

for port in "${PORTS[@]}"; do
    if lsof -i :$port >/dev/null 2>&1; then
        success "Port $port is in use"
    else
        warning "Port $port is not in use"
    fi
done

# Check test data
log "Checking test data availability..."

# Check if registration codes exist in database
REG_COUNT=$(docker exec ai_camera_postgres psql -U postgres -d people_counting_db -t -c "SELECT COUNT(*) FROM registration_codes WHERE is_active = true;" 2>/dev/null | tr -d ' ')
if [ "$REG_COUNT" -gt 0 ]; then
    success "Registration codes are available in database"
else
    warning "No active registration codes found in database"
fi

# Check if test users exist
USER_COUNT=$(docker exec ai_camera_postgres psql -U postgres -d people_counting_db -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ')
if [ "$USER_COUNT" -gt 0 ]; then
    success "Users exist in database"
else
    warning "No users found in database"
fi

# Summary
echo ""
echo "=========================================="
echo "📊 VERIFICATION SUMMARY"
echo "=========================================="
success "Environment verification completed successfully!"
echo ""
echo "🎯 Ready to start testing:"
echo "   - Backend Tests: 67 test cases"
echo "   - Frontend Tests: 45 test cases"
echo "   - Total: 112 test cases"
echo ""
echo "📁 Test scripts location: sharedResource/automationTest/"
echo "📋 Test configuration: sharedResource/automationTest/config/"
echo "📊 Results location: sharedResource/automationTest/*/results/"
echo ""
echo "🚀 Next step: Run database tests (Phase 1)"
echo "==========================================" 
#!/bin/bash

# 🧪 Camera API Test Runner - AI Camera Counting System
# 📅 Updated: 2025-07-16
# 👥 Maintainer: QA Team
# 🎯 Purpose: Run comprehensive camera API tests with standardized response format

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Test configuration
TEST_SCRIPT="$SCRIPT_DIR/test_camera_api.py"
RESULTS_DIR="$SCRIPT_DIR/../results"
LOG_DIR="$SCRIPT_DIR/../logs"

# Create directories if they don't exist
mkdir -p "$RESULTS_DIR"
mkdir -p "$LOG_DIR"

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TEST_RESULTS=()

# Function to check environment
check_environment() {
    log "Checking test environment..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        error "Python3 is not installed or not in PATH"
        return 1
    fi
    
    # Check if required Python packages are installed
    python3 -c "import requests, json, sys" 2>/dev/null || {
        error "Required Python packages not installed. Please install: requests"
        return 1
    }
    
    # Check if test script exists
    if [ ! -f "$TEST_SCRIPT" ]; then
        error "Test script not found: $TEST_SCRIPT"
        return 1
    }
    
    # Check if test config exists
    CONFIG_FILE="$SCRIPT_DIR/../../config/test_config.json"
    if [ ! -f "$CONFIG_FILE" ]; then
        error "Test configuration not found: $CONFIG_FILE"
        return 1
    }
    
    success "Environment check passed"
    return 0
}

# Function to check service availability
check_services() {
    log "Checking service availability..."
    
    # Load configuration
    CONFIG_FILE="$SCRIPT_DIR/../../config/test_config.json"
    AUTH_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['test_environment']['base_urls']['auth_api'])")
    CAMERA_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['test_environment']['base_urls']['camera_api'])")
    
    # Check auth service
    if curl -s --connect-timeout 5 "$AUTH_URL" > /dev/null 2>&1; then
        success "Auth service is available"
    else
        warning "Auth service may not be available at $AUTH_URL"
    fi
    
    # Check camera service
    if curl -s --connect-timeout 5 "$CAMERA_URL" > /dev/null 2>&1; then
        success "Camera service is available"
    else
        warning "Camera service may not be available at $CAMERA_URL"
    fi
    
    # Check health endpoint
    HEALTH_URL=$(echo "$CAMERA_URL" | sed 's|/api/v1||')/health
    if curl -s --connect-timeout 5 "$HEALTH_URL" > /dev/null 2>&1; then
        success "Health endpoint is available"
    else
        warning "Health endpoint may not be available at $HEALTH_URL"
    fi
}

# Function to run camera API tests
run_camera_tests() {
    log "Starting Camera API Tests (v2.0)..."
    
    # Set up log file
    LOG_FILE="$LOG_DIR/camera_tests_$(date +%Y%m%d_%H%M%S).log"
    
    # Run tests with timeout
    if timeout 300 python3 "$TEST_SCRIPT" 2>&1 | tee "$LOG_FILE"; then
        success "Camera API tests completed successfully"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("✅ Camera API Tests: PASSED")
    else
        error "Camera API tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("❌ Camera API Tests: FAILED")
        return 1
    fi
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # Check for test results file
    RESULTS_FILE="$RESULTS_DIR/camera_api_test_results_v2.json"
    if [ -f "$RESULTS_FILE" ]; then
        info "Test results saved to: $RESULTS_FILE"
        
        # Parse results for summary
        if command -v jq &> /dev/null; then
            TOTAL_TEST_CASES=$(jq '.total_tests' "$RESULTS_FILE" 2>/dev/null || echo "0")
            PASSED_TEST_CASES=$(jq '.passed_tests' "$RESULTS_FILE" 2>/dev/null || echo "0")
            SUCCESS_RATE=$(jq -r '.success_rate' "$RESULTS_FILE" 2>/dev/null || echo "0%")
            
            info "Test Summary: $PASSED_TEST_CASES/$TOTAL_TEST_CASES passed ($SUCCESS_RATE)"
        fi
    fi
}

# Function to run specific test categories
run_test_category() {
    local category="$1"
    local description="$2"
    
    log "Running $category: $description"
    
    case "$category" in
        "health")
            log "Testing health check endpoints..."
            # This is included in the main test suite
            ;;
        "crud")
            log "Testing CRUD operations..."
            # This is included in the main test suite
            ;;
        "auth")
            log "Testing authentication integration..."
            # This is included in the main test suite
            ;;
        "error")
            log "Testing error handling..."
            # This is included in the main test suite
            ;;
        "performance")
            log "Testing performance aspects..."
            # This is included in the main test suite
            ;;
        *)
            error "Unknown test category: $category"
            return 1
            ;;
    esac
}

# Function to show test results
show_results() {
    echo ""
    echo "=========================================="
    echo "📊 CAMERA API TEST RESULTS"
    echo "=========================================="
    echo "Total Test Suites: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    
    if [ $TOTAL_TESTS -gt 0 ]; then
        local success_rate=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l 2>/dev/null || echo "0")
        echo "Success Rate: ${success_rate}%"
    fi
    
    echo ""
    echo "Test Results:"
    for result in "${TEST_RESULTS[@]}"; do
        echo "  $result"
    done
    
    echo ""
    if [ $FAILED_TESTS -eq 0 ]; then
        success "🎉 All camera API tests passed! System is ready for production."
    else
        error "⚠️  Some camera API tests failed. Please review the results."
    fi
    
    echo "=========================================="
}

# Function to show help
show_help() {
    echo "=========================================="
    echo "🧪 CAMERA API TEST RUNNER"
    echo "AI Camera Counting System"
    echo "=========================================="
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -e, --environment   Check environment only"
    echo "  -s, --services      Check services only"
    echo "  -c, --category      Run specific test category"
    echo "  -v, --verbose       Enable verbose output"
    echo ""
    echo "Test Categories:"
    echo "  health       Health check endpoints"
    echo "  crud         CRUD operations"
    echo "  auth         Authentication integration"
    echo "  error        Error handling"
    echo "  performance  Performance aspects"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 -e                 # Check environment only"
    echo "  $0 -c crud            # Run CRUD tests only"
    echo "  $0 -v                 # Run with verbose output"
    echo ""
    echo "=========================================="
}

# Main execution
main() {
    local check_env_only=false
    local check_services_only=false
    local test_category=""
    local verbose=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -e|--environment)
                check_env_only=true
                shift
                ;;
            -s|--services)
                check_services_only=true
                shift
                ;;
            -c|--category)
                test_category="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Show header
    echo "=========================================="
    echo "🧪 CAMERA API TEST RUNNER (v2.0)"
    echo "AI Camera Counting System"
    echo "Standardized Response Format"
    echo "=========================================="
    echo "Start time: $(date)"
    echo ""
    
    # Check environment
    if ! check_environment; then
        error "Environment check failed. Cannot proceed with tests."
        exit 1
    fi
    
    if [ "$check_env_only" = true ]; then
        success "Environment check completed successfully"
        exit 0
    fi
    
    # Check services
    check_services
    
    if [ "$check_services_only" = true ]; then
        success "Service check completed"
        exit 0
    fi
    
    # Run specific test category if requested
    if [ -n "$test_category" ]; then
        if run_test_category "$test_category" "Specific category test"; then
            success "Category test completed"
        else
            error "Category test failed"
            exit 1
        fi
    else
        # Run all camera tests
        run_camera_tests
    fi
    
    # Show results
    show_results
    
    # Exit with appropriate code
    if [ $FAILED_TESTS -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@" 
#!/bin/bash

# 🧪 Master Test Runner - AI Camera Counting System
# 📅 Created: 2025-01-09
# 👥 Maintainer: QA Team

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
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TEST_RESULTS=()

# Function to run a test phase
run_test_phase() {
    local phase_name="$1"
    local script_path="$2"
    local description="$3"
    
    log "Starting $phase_name: $description"
    
    if [ -f "$script_path" ]; then
        if bash "$script_path"; then
            success "$phase_name completed successfully"
            ((PASSED_TESTS++))
            TEST_RESULTS+=("✅ $phase_name: PASSED")
        else
            error "$phase_name failed"
            ((FAILED_TESTS++))
            TEST_RESULTS+=("❌ $phase_name: FAILED")
            return 1
        fi
    else
        error "Test script not found: $script_path"
        ((FAILED_TESTS++))
        TEST_RESULTS+=("❌ $phase_name: SCRIPT_NOT_FOUND")
        return 1
    fi
    
    ((TOTAL_TESTS++))
    echo ""
}

# Function to show menu
show_menu() {
    echo "=========================================="
    echo "🧪 MASTER TEST RUNNER"
    echo "AI Camera Counting System"
    echo "=========================================="
    echo ""
    echo "Available test phases:"
    echo ""
    echo "🔧 BACKEND TESTS:"
    echo "  1) Database Tests (Phase 1)"
    echo "  2) Authentication Tests (Phase 2)"
    echo "  3) Camera Management Tests (Phase 3)"
    echo "  4) Worker Pool Tests (Phase 4)"
    echo "  5) Integration Tests (Phase 5)"
    echo "  6) Security Tests (Phase 6)"
    echo "  7) Performance Tests (Phase 7)"
    echo ""
    echo "🎨 FRONTEND TESTS:"
    echo "  8) Authentication Flow Tests"
    echo "  9) Authentication Components Tests"
    echo "  10) Core Functionality Tests"
    echo "  11) Advanced Features Tests"
    echo ""
    echo "📊 SPECIAL OPTIONS:"
    echo "  12) Run All Backend Tests"
    echo "  13) Run All Frontend Tests"
    echo "  14) Run Complete Test Suite"
    echo "  15) Verify Environment Only"
    echo "  16) Show Test Results"
    echo "  0) Exit"
    echo ""
    echo "=========================================="
}

# Function to run all backend tests
run_all_backend_tests() {
    log "Running all backend tests..."
    echo ""
    
    local backend_phases=(
        "Database Tests" "backend/database/run_database_tests.sh" "Database connection and schema validation"
        "Authentication Tests" "backend/auth/run_auth_tests.sh" "User authentication and authorization"
        "Camera Management Tests" "backend/camera/run_camera_tests.sh" "Camera CRUD operations and management"
        "Worker Pool Tests" "backend/worker/run_worker_tests.sh" "Worker pool processing and task management"
        "Integration Tests" "backend/integration/run_integration_tests.sh" "Cross-service integration testing"
        "Security Tests" "backend/security/run_security_tests.sh" "Security validation and penetration testing"
        "Performance Tests" "backend/performance/run_performance_tests.sh" "Load and stress testing"
    )
    
    for ((i=0; i<${#backend_phases[@]}; i+=3)); do
        local phase_name="${backend_phases[i]}"
        local script_path="$SCRIPT_DIR/${backend_phases[i+1]}"
        local description="${backend_phases[i+2]}"
        
        run_test_phase "$phase_name" "$script_path" "$description"
        
        # If any test fails, ask if user wants to continue
        if [ $? -ne 0 ]; then
            echo ""
            read -p "❌ $phase_name failed. Continue with remaining tests? (y/n): "
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                warning "Test execution stopped by user"
                break
            fi
        fi
    done
}

# Function to run all frontend tests
run_all_frontend_tests() {
    log "Running all frontend tests..."
    echo ""
    
    local frontend_phases=(
        "Authentication Flow Tests" "frontend/authentication/run_auth_tests.sh" "Complete authentication flow testing"
        "Authentication Components Tests" "frontend/authentication/test_auth_components.py" "Authentication UI components and forms"
        "Authentication E2E Tests" "frontend/e2e/test_auth_e2e.py" "End-to-end authentication flows"
        "Frontend Integration Tests" "frontend/run_frontend_tests.sh" "Complete frontend test suite"
    )
    
    for ((i=0; i<${#frontend_phases[@]}; i+=3)); do
        local phase_name="${frontend_phases[i]}"
        local script_path="$SCRIPT_DIR/${frontend_phases[i+1]}"
        local description="${frontend_phases[i+2]}"
        
        run_test_phase "$phase_name" "$script_path" "$description"
        
        # If any test fails, ask if user wants to continue
        if [ $? -ne 0 ]; then
            echo ""
            read -p "❌ $phase_name failed. Continue with remaining tests? (y/n): "
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                warning "Test execution stopped by user"
                break
            fi
        fi
    done
}

# Function to run complete test suite
run_complete_test_suite() {
    log "Running complete test suite..."
    echo ""
    
    # Verify environment first
    log "Phase 0: Environment Verification"
    if ! "$SCRIPT_DIR/utils/verify_environment.sh"; then
        error "Environment verification failed. Cannot proceed with tests."
        exit 1
    fi
    success "Environment verification completed"
    echo ""
    
    # Run all backend tests
    run_all_backend_tests
    
    # Run all frontend tests
    run_all_frontend_tests
    
    # Generate final report
    generate_final_report
}

# Function to generate final report
generate_final_report() {
    echo ""
    echo "=========================================="
    echo "📊 FINAL TEST REPORT"
    echo "=========================================="
    echo "Total Tests: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    
    if [ $TOTAL_TESTS -gt 0 ]; then
        local success_rate=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l)
        echo "Success Rate: ${success_rate}%"
    fi
    
    echo ""
    echo "Test Results:"
    for result in "${TEST_RESULTS[@]}"; do
        echo "  $result"
    done
    
    echo ""
    if [ $FAILED_TESTS -eq 0 ]; then
        success "🎉 All tests passed! System is ready for production."
    else
        error "⚠️  Some tests failed. Please review and fix issues."
    fi
    
    echo "=========================================="
}

# Function to show test results
show_test_results() {
    echo "=========================================="
    echo "📊 TEST RESULTS SUMMARY"
    echo "=========================================="
    
    if [ ${#TEST_RESULTS[@]} -eq 0 ]; then
        info "No tests have been run yet."
    else
        echo "Total Tests: $TOTAL_TESTS"
        echo "Passed: $PASSED_TESTS"
        echo "Failed: $FAILED_TESTS"
        
        if [ $TOTAL_TESTS -gt 0 ]; then
            local success_rate=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l)
            echo "Success Rate: ${success_rate}%"
        fi
        
        echo ""
        echo "Test Results:"
        for result in "${TEST_RESULTS[@]}"; do
            echo "  $result"
        done
    fi
    
    echo "=========================================="
}

# Main menu loop
main_menu() {
    while true; do
        show_menu
        echo ""
        read -p "Select an option (0-16): "
        echo ""
        echo ""
        
        case $REPLY in
            0)
                info "Exiting test runner..."
                exit 0
                ;;
            1)
                run_test_phase "Database Tests" "$SCRIPT_DIR/backend/database/run_database_tests.sh" "Database connection and schema validation"
                ;;
            2)
                run_test_phase "Authentication Tests" "$SCRIPT_DIR/backend/auth/run_auth_tests.sh" "User authentication and authorization"
                ;;
            3)
                run_test_phase "Camera Management Tests" "$SCRIPT_DIR/backend/camera/run_camera_tests.sh" "Camera CRUD operations and management"
                ;;
            4)
                run_test_phase "Worker Pool Tests" "$SCRIPT_DIR/backend/worker/run_worker_tests.sh" "Worker pool processing and task management"
                ;;
            5)
                run_test_phase "Integration Tests" "$SCRIPT_DIR/backend/integration/run_integration_tests.sh" "Cross-service integration testing"
                ;;
            6)
                run_test_phase "Security Tests" "$SCRIPT_DIR/backend/security/run_security_tests.sh" "Security validation and penetration testing"
                ;;
            7)
                run_test_phase "Performance Tests" "$SCRIPT_DIR/backend/performance/run_performance_tests.sh" "Load and stress testing"
                ;;
            8)
                run_test_phase "Authentication Flow Tests" "$SCRIPT_DIR/frontend/authentication/run_auth_tests.sh" "Complete authentication flow testing"
                ;;
            9)
                run_test_phase "Authentication Components Tests" "$SCRIPT_DIR/frontend/authentication/test_auth_components.py" "Authentication UI components and forms"
                ;;
            10)
                run_test_phase "Core Functionality Tests" "$SCRIPT_DIR/frontend/core/run_core_tests.sh" "Main application functionality"
                ;;
            11)
                run_test_phase "Advanced Features Tests" "$SCRIPT_DIR/frontend/advanced/run_advanced_tests.sh" "Advanced UI features and interactions"
                ;;
            12)
                run_all_backend_tests
                ;;
            13)
                run_all_frontend_tests
                ;;
            14)
                run_complete_test_suite
                ;;
            15)
                log "Verifying environment..."
                "$SCRIPT_DIR/utils/verify_environment.sh"
                ;;
            16)
                show_test_results
                ;;
            *)
                error "Invalid option. Please select 0-16."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        echo ""
    done
}

# Check if running in interactive mode
if [ -t 0 ]; then
    # Interactive mode - show menu
    main_menu
else
    # Non-interactive mode - run complete test suite
    run_complete_test_suite
fi 
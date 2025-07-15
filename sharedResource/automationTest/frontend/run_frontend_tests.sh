#!/bin/bash

# Frontend Test Automation Script
# Runs all frontend tests including unit tests, component tests, and E2E tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_DIR="../../frontend"
TEST_DIR="."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_DIR="results"
LOG_FILE="${RESULTS_DIR}/frontend_test_results_${TIMESTAMP}.log"

# Create results directory
mkdir -p "${RESULTS_DIR}"

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

# Function to check if service is running
check_service() {
    local service_name=$1
    local service_url=$2
    
    print_status "Checking if $service_name is running..."
    
    if curl -s --max-time 5 "$service_url" > /dev/null 2>&1; then
        print_success "$service_name is running"
        return 0
    else
        print_error "$service_name is not running at $service_url"
        return 1
    fi
}

# Function to run unit tests
run_unit_tests() {
    print_status "Running frontend unit tests..."
    
    cd "$FRONTEND_DIR"
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "node_modules not found, installing dependencies..."
        npm install
    fi
    
    # Run unit tests
    if npm test -- --watchAll=false --coverage --passWithNoTests 2>&1 | tee -a "../$LOG_FILE"; then
        print_success "Unit tests completed successfully"
        return 0
    else
        print_error "Unit tests failed"
        return 1
    fi
}

# Function to run component tests
run_component_tests() {
    print_status "Running authentication component tests..."
    
    cd "$TEST_DIR"
    
    # Check if Python and Selenium are available
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed"
        return 1
    fi
    
    # Check if ChromeDriver is available
    if ! command -v chromedriver &> /dev/null; then
        print_warning "ChromeDriver not found, attempting to install..."
        # This would need to be implemented based on the system
        print_error "Please install ChromeDriver manually"
        return 1
    fi
    
    # Run component tests
    if python3 authentication/test_auth_components.py 2>&1 | tee -a "$LOG_FILE"; then
        print_success "Component tests completed successfully"
        return 0
    else
        print_error "Component tests failed"
        return 1
    fi
}

# Function to run E2E tests
run_e2e_tests() {
    print_status "Running authentication E2E tests..."
    
    cd "$TEST_DIR"
    
    # Run E2E tests
    if python3 e2e/test_auth_e2e.py 2>&1 | tee -a "$LOG_FILE"; then
        print_success "E2E tests completed successfully"
        return 0
    else
        print_error "E2E tests failed"
        return 1
    fi
}

# Function to generate test report
generate_report() {
    print_status "Generating test report..."
    
    local report_file="${RESULTS_DIR}/frontend_test_report_${TIMESTAMP}.md"
    
    cat > "$report_file" << EOF
# Frontend Test Report

**Generated:** $(date)
**Timestamp:** $TIMESTAMP

## Test Summary

- **Unit Tests:** $1
- **Component Tests:** $2
- **E2E Tests:** $3
- **Overall Status:** $4

## Detailed Results

### Unit Tests
\`\`\`
$(grep -A 20 "Test Results" "$LOG_FILE" | head -20 || echo "No unit test results found")
\`\`\`

### Component Tests
\`\`\`
$(grep -A 20 "Frontend Authentication Components Test Suite" "$LOG_FILE" | head -20 || echo "No component test results found")
\`\`\`

### E2E Tests
\`\`\`
$(grep -A 20 "Frontend Authentication E2E Test Suite" "$LOG_FILE" | head -20 || echo "No E2E test results found")
\`\`\`

## Recommendations

$(if [ "$4" = "PASSED" ]; then
    echo "- All tests passed successfully"
    echo "- Frontend authentication is working correctly"
    echo "- Ready for production deployment"
else
    echo "- Some tests failed, review the logs above"
    echo "- Fix failing tests before deployment"
    echo "- Consider running tests in isolation to identify specific issues"
fi)

## Next Steps

1. Review any failed tests
2. Fix identified issues
3. Re-run tests to verify fixes
4. Deploy to staging environment
5. Run integration tests

---
*Report generated automatically by frontend test automation script*
EOF

    print_success "Test report generated: $report_file"
}

# Main execution
main() {
    print_status "Starting frontend test automation..."
    print_status "Timestamp: $TIMESTAMP"
    print_status "Results will be saved to: $LOG_FILE"
    
    # Initialize counters
    unit_tests_result="FAILED"
    component_tests_result="FAILED"
    e2e_tests_result="FAILED"
    overall_result="FAILED"
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    
    # Check if frontend is running
    if ! check_service "Frontend" "http://localhost:3000"; then
        print_warning "Frontend is not running, starting it..."
        cd "$FRONTEND_DIR"
        npm start &
        FRONTEND_PID=$!
        
        # Wait for frontend to start
        print_status "Waiting for frontend to start..."
        sleep 30
        
        # Check again
        if ! check_service "Frontend" "http://localhost:3000"; then
            print_error "Failed to start frontend"
            exit 1
        fi
    fi
    
    # Check if backend is running
    if ! check_service "Backend Auth" "http://localhost:3001/health"; then
        print_warning "Backend auth service is not running"
        print_warning "Some tests may fail"
    fi
    
    # Run tests
    print_status "Starting test execution..."
    
    # Run unit tests
    if run_unit_tests; then
        unit_tests_result="PASSED"
    fi
    
    # Run component tests
    if run_component_tests; then
        component_tests_result="PASSED"
    fi
    
    # Run E2E tests
    if run_e2e_tests; then
        e2e_tests_result="PASSED"
    fi
    
    # Determine overall result
    if [ "$unit_tests_result" = "PASSED" ] && [ "$component_tests_result" = "PASSED" ] && [ "$e2e_tests_result" = "PASSED" ]; then
        overall_result="PASSED"
    fi
    
    # Generate report
    generate_report "$unit_tests_result" "$component_tests_result" "$e2e_tests_result" "$overall_result"
    
    # Print summary
    echo ""
    print_status "Test Execution Summary:"
    echo "  Unit Tests: $unit_tests_result"
    echo "  Component Tests: $component_tests_result"
    echo "  E2E Tests: $e2e_tests_result"
    echo "  Overall: $overall_result"
    echo ""
    
    if [ "$overall_result" = "PASSED" ]; then
        print_success "All frontend tests passed! 🎉"
        exit 0
    else
        print_error "Some tests failed. Check the logs for details."
        exit 1
    fi
}

# Cleanup function
cleanup() {
    if [ ! -z "$FRONTEND_PID" ]; then
        print_status "Cleaning up frontend process..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
}

# Set up trap for cleanup
trap cleanup EXIT

# Run main function
main "$@" 
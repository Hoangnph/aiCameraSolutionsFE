#!/bin/bash

# Comprehensive Test Runner for AI Camera Counting System
# This script runs all automated tests and generates reports

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
RESULTS_DIR="$BACKEND_DIR/results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AI Camera Counting System - Test Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Timestamp: $TIMESTAMP"
echo -e "Script Directory: $SCRIPT_DIR"
echo -e "Results Directory: $RESULTS_DIR"
echo ""

# Function to check if services are running
check_services() {
    echo -e "${YELLOW}Checking service health...${NC}"
    
    # Check beAuth service
    if curl -s http://localhost:3001/health > /dev/null; then
        echo -e "${GREEN}✅ beAuth Service: Healthy${NC}"
    else
        echo -e "${RED}❌ beAuth Service: Not responding${NC}"
        return 1
    fi
    
    # Check beCamera service
    if curl -s http://localhost:3002/health > /dev/null; then
        echo -e "${GREEN}✅ beCamera Service: Healthy${NC}"
    else
        echo -e "${RED}❌ beCamera Service: Not responding${NC}"
        return 1
    fi
    
    # Check PostgreSQL
    if docker exec becamera_postgres pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL Database: Healthy${NC}"
    else
        echo -e "${RED}❌ PostgreSQL Database: Not responding${NC}"
        return 1
    fi
    
    # Check Redis
    if docker exec becamera_redis redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Redis Cache: Healthy${NC}"
    else
        echo -e "${RED}❌ Redis Cache: Not responding${NC}"
        return 1
    fi
    
    echo ""
}

# Function to run backend tests
run_backend_tests() {
    echo -e "${YELLOW}Running Backend Tests...${NC}"
    cd "$BACKEND_DIR"
    
    # Run comprehensive test suite
    echo -e "${BLUE}Running Comprehensive Backend Test Suite...${NC}"
    python3 comprehensive_test_suite.py
    
    # Check if test results file was created
    if [ -f "results/comprehensive_test_results.json" ]; then
        echo -e "${GREEN}✅ Backend tests completed successfully${NC}"
        
        # Parse and display summary
        TOTAL_TESTS=$(jq '.summary.total_tests' results/comprehensive_test_results.json)
        PASSED_TESTS=$(jq '.summary.passed_tests' results/comprehensive_test_results.json)
        FAILED_TESTS=$(jq '.summary.failed_tests' results/comprehensive_test_results.json)
        SUCCESS_RATE=$(jq '.summary.success_rate' results/comprehensive_test_results.json)
        
        echo -e "${BLUE}Backend Test Summary:${NC}"
        echo -e "  Total Tests: $TOTAL_TESTS"
        echo -e "  Passed: $PASSED_TESTS"
        echo -e "  Failed: $FAILED_TESTS"
        echo -e "  Success Rate: ${SUCCESS_RATE}%"
        
        # Copy results to timestamped file
        cp results/comprehensive_test_results.json "results/comprehensive_test_results_${TIMESTAMP}.json"
        
    else
        echo -e "${RED}❌ Backend tests failed or results not generated${NC}"
        return 1
    fi
    
    echo ""
}

# Function to run individual API tests
run_api_tests() {
    echo -e "${YELLOW}Running Individual API Tests...${NC}"
    cd "$BACKEND_DIR"
    
    # Run auth API tests
    if [ -f "auth/test_auth_api.py" ]; then
        echo -e "${BLUE}Running Auth API Tests...${NC}"
        python3 auth/test_auth_api.py
    fi
    
    # Run camera API tests
    if [ -f "camera/test_camera_api.py" ]; then
        echo -e "${BLUE}Running Camera API Tests...${NC}"
        python3 camera/test_camera_api.py
    fi
    
    # Run database tests
    if [ -f "database/test_database_connection.py" ]; then
        echo -e "${BLUE}Running Database Tests...${NC}"
        python3 database/test_database_connection.py
    fi
    
    echo ""
}

# Function to generate test report
generate_report() {
    echo -e "${YELLOW}Generating Test Report...${NC}"
    
    REPORT_FILE="$RESULTS_DIR/test_report_${TIMESTAMP}.md"
    
    cat > "$REPORT_FILE" << EOF
# AI Camera Counting System - Test Report

**Generated**: $(date)
**Timestamp**: $TIMESTAMP

## Test Summary

### Backend Tests
- **Total Tests**: $(jq '.summary.total_tests' "$RESULTS_DIR/comprehensive_test_results.json")
- **Passed**: $(jq '.summary.passed_tests' "$RESULTS_DIR/comprehensive_test_results.json")
- **Failed**: $(jq '.summary.failed_tests' "$RESULTS_DIR/comprehensive_test_results.json")
- **Success Rate**: $(jq '.summary.success_rate' "$RESULTS_DIR/comprehensive_test_results.json")%

## Detailed Results

### Passed Tests
$(jq -r '.results[] | select(.status == "PASSED") | "- " + .test_name + ": " + .details' "$RESULTS_DIR/comprehensive_test_results.json" 2>/dev/null || echo "No passed tests found")

### Failed Tests
$(jq -r '.results[] | select(.status == "FAILED") | "- " + .test_name + ": " + .details' "$RESULTS_DIR/comprehensive_test_results.json" 2>/dev/null || echo "No failed tests found")

## System Health

### Services Status
- **beAuth Service**: $(curl -s http://localhost:3001/health > /dev/null && echo "✅ Healthy" || echo "❌ Not responding")
- **beCamera Service**: $(curl -s http://localhost:3002/health > /dev/null && echo "✅ Healthy" || echo "❌ Not responding")
- **PostgreSQL Database**: $(docker exec becamera_postgres pg_isready -U postgres > /dev/null 2>&1 && echo "✅ Healthy" || echo "❌ Not responding")
- **Redis Cache**: $(docker exec becamera_redis redis-cli ping > /dev/null 2>&1 && echo "✅ Healthy" || echo "❌ Not responding")

## Recommendations

### Immediate Actions
1. Fix failed tests
2. Address any service health issues
3. Review error logs for failed tests

### Next Steps
1. Implement remaining test cases
2. Add performance and security tests
3. Prepare for production deployment

EOF

    echo -e "${GREEN}✅ Test report generated: $REPORT_FILE${NC}"
    echo ""
}

# Function to display final summary
display_summary() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}TEST EXECUTION SUMMARY${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    if [ -f "$RESULTS_DIR/comprehensive_test_results.json" ]; then
        TOTAL_TESTS=$(jq '.summary.total_tests' "$RESULTS_DIR/comprehensive_test_results.json")
        PASSED_TESTS=$(jq '.summary.passed_tests' "$RESULTS_DIR/comprehensive_test_results.json")
        FAILED_TESTS=$(jq '.summary.failed_tests' "$RESULTS_DIR/comprehensive_test_results.json")
        SUCCESS_RATE=$(jq '.summary.success_rate' "$RESULTS_DIR/comprehensive_test_results.json")
        
        echo -e "Total Tests: ${BLUE}$TOTAL_TESTS${NC}"
        echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
        echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
        echo -e "Success Rate: ${YELLOW}${SUCCESS_RATE}%${NC}"
        
        if [ "$FAILED_TESTS" -gt 0 ]; then
            echo ""
            echo -e "${YELLOW}Failed Tests:${NC}"
            jq -r '.results[] | select(.status == "FAILED") | "- " + .test_name + ": " + .details' "$RESULTS_DIR/comprehensive_test_results.json" 2>/dev/null || echo "No failed tests found"
        fi
    else
        echo -e "${RED}❌ Test results not found${NC}"
    fi
    
    echo ""
    echo -e "Results saved to: ${BLUE}$RESULTS_DIR${NC}"
    echo -e "Report generated: ${BLUE}$RESULTS_DIR/test_report_${TIMESTAMP}.md${NC}"
    echo ""
}

# Main execution
main() {
    echo -e "${BLUE}Starting comprehensive test execution...${NC}"
    echo ""
    
    # Check services
    if ! check_services; then
        echo -e "${RED}❌ Service health check failed. Please ensure all services are running.${NC}"
        exit 1
    fi
    
    # Run backend tests
    if ! run_backend_tests; then
        echo -e "${RED}❌ Backend tests failed.${NC}"
        exit 1
    fi
    
    # Run individual API tests
    run_api_tests
    
    # Generate report
    generate_report
    
    # Display summary
    display_summary
    
    echo -e "${GREEN}✅ All tests completed successfully!${NC}"
}

# Run main function
main "$@" 
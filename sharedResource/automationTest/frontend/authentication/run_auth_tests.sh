#!/bin/bash

# Authentication Flow Test Runner
# This script runs all authentication-related tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Configuration
BASE_URL="${BASE_URL:-http://localhost:3000}"
HEADLESS="${HEADLESS:-true}"
LOG_DIR="$SCRIPT_DIR/logs"
RESULTS_DIR="$SCRIPT_DIR/../results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$RESULTS_DIR"

# Log file
LOG_FILE="$LOG_DIR/auth_tests_${TIMESTAMP}.log"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Authentication Flow Tests${NC}"
echo -e "${BLUE}================================${NC}"
echo "Timestamp: $(date)"
echo "Base URL: $BASE_URL"
echo "Headless: $HEADLESS"
echo "Log file: $LOG_FILE"
echo ""

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Function to check if frontend is running
check_frontend() {
    log_message "${YELLOW}Checking if frontend is running...${NC}"
    
    if curl -s "$BASE_URL" > /dev/null 2>&1; then
        log_message "${GREEN}✅ Frontend is running at $BASE_URL${NC}"
        return 0
    else
        log_message "${RED}❌ Frontend is not running at $BASE_URL${NC}"
        log_message "${YELLOW}Please start the frontend server first:${NC}"
        log_message "  cd frontend && npm start"
        return 1
    fi
}

# Function to check dependencies
check_dependencies() {
    log_message "${YELLOW}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_message "${RED}❌ Python3 is not installed${NC}"
        return 1
    fi
    
    # Check pip packages
    python3 -c "import selenium" 2>/dev/null || {
        log_message "${YELLOW}Installing selenium...${NC}"
        pip3 install selenium
    }
    
    python3 -c "import requests" 2>/dev/null || {
        log_message "${YELLOW}Installing requests...${NC}"
        pip3 install requests
    }
    
    log_message "${GREEN}✅ Dependencies check passed${NC}"
    return 0
}

# Function to run authentication flow tests
run_auth_flow_tests() {
    log_message "${BLUE}Running Authentication Flow Tests...${NC}"
    
    cd "$SCRIPT_DIR"
    
    HEADLESS_FLAG=""
    if [ "$HEADLESS" = "true" ]; then
        HEADLESS_FLAG="--headless"
    fi
    
    if python3 test_auth_flow.py --base-url "$BASE_URL" $HEADLESS_FLAG; then
        log_message "${GREEN}✅ Authentication flow tests PASSED${NC}"
        return 0
    else
        log_message "${RED}❌ Authentication flow tests FAILED${NC}"
        return 1
    fi
}

# Function to run component tests
run_component_tests() {
    log_message "${BLUE}Running Authentication Component Tests...${NC}"
    
    cd "$SCRIPT_DIR"
    
    if python3 test_auth_components.py --base-url "$BASE_URL"; then
        log_message "${GREEN}✅ Authentication component tests PASSED${NC}"
        return 0
    else
        log_message "${RED}❌ Authentication component tests FAILED${NC}"
        return 1
    fi
}

# Function to generate test report
generate_report() {
    log_message "${BLUE}Generating test report...${NC}"
    
    REPORT_FILE="$RESULTS_DIR/auth_test_report_${TIMESTAMP}.html"
    
    cat > "$REPORT_FILE" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Authentication Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .success { color: green; }
        .error { color: red; }
        .warning { color: orange; }
        .log { background-color: #f8f8f8; padding: 10px; border-radius: 3px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Authentication Test Report</h1>
        <p><strong>Timestamp:</strong> $(date)</p>
        <p><strong>Base URL:</strong> $BASE_URL</p>
        <p><strong>Headless:</strong> $HEADLESS</p>
    </div>
    
    <h2>Test Results</h2>
    <div class="log">
$(cat "$LOG_FILE" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    </div>
</body>
</html>
EOF
    
    log_message "${GREEN}✅ Test report generated: $REPORT_FILE${NC}"
}

# Main execution
main() {
    log_message "${BLUE}Starting Authentication Tests...${NC}"
    
    # Check dependencies
    if ! check_dependencies; then
        log_message "${RED}❌ Dependency check failed${NC}"
        exit 1
    fi
    
    # Check if frontend is running
    if ! check_frontend; then
        log_message "${RED}❌ Frontend check failed${NC}"
        exit 1
    fi
    
    # Run tests
    TESTS_PASSED=0
    TESTS_FAILED=0
    
    # Run authentication flow tests
    if run_auth_flow_tests; then
        ((TESTS_PASSED++))
    else
        ((TESTS_FAILED++))
    fi
    
    # Run component tests
    if run_component_tests; then
        ((TESTS_PASSED++))
    else
        ((TESTS_FAILED++))
    fi
    
    # Generate report
    generate_report
    
    # Summary
    log_message ""
    log_message "${BLUE}================================${NC}"
    log_message "${BLUE}  Test Summary${NC}"
    log_message "${BLUE}================================${NC}"
    log_message "Tests Passed: $TESTS_PASSED"
    log_message "Tests Failed: $TESTS_FAILED"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        log_message "${GREEN}🎉 All authentication tests PASSED!${NC}"
        exit 0
    else
        log_message "${RED}❌ Some authentication tests FAILED!${NC}"
        exit 1
    fi
}

# Run main function
main "$@" 
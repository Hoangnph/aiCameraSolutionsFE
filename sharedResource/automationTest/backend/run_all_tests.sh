#!/bin/bash

# Comprehensive Test Runner for AI Camera Counting System
# Runs all test suites and generates summary reports

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
LOGS_DIR="$SCRIPT_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create directories
mkdir -p "$RESULTS_DIR" "$LOGS_DIR"

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}AI Camera Counting System - Test Suite Runner${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Results Directory: $RESULTS_DIR"
echo -e "Logs Directory: $LOGS_DIR"
echo ""

# Function to run test and capture results
run_test() {
    local test_name="$1"
    local test_script="$2"
    local log_file="$LOGS_DIR/${test_name}_${TIMESTAMP}.log"
    
    echo -e "${YELLOW}Running $test_name...${NC}"
    
    if python3 "$test_script" > "$log_file" 2>&1; then
        echo -e "${GREEN}✓ $test_name completed successfully${NC}"
        return 0
    else
        echo -e "${RED}✗ $test_name failed${NC}"
        return 1
    fi
}

# Function to extract test results from JSON
extract_results() {
    local json_file="$1"
    if [[ -f "$json_file" ]]; then
        python3 -c "
import json
try:
    with open('$json_file', 'r') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    if 'summary' in data:
        # Comprehensive test format
        passed = data['summary'].get('passed_tests', 0)
        total = data['summary'].get('total_tests', 0)
    elif 'passed' in data and 'total_tests' in data:
        # Direct format
        passed = data.get('passed', 0)
        total = data.get('total_tests', 0)
    else:
        # Try to count from results array
        results = data.get('results', [])
        passed = sum(1 for r in results if r.get('status') == 'PASSED')
        total = len(results)
    
    print(f\"{passed}/{total}\")
except Exception as e:
    print('0/0')
"
    else
        echo "0/0"
    fi
}

# Initialize counters
total_tests=0
total_passed=0
test_results=()

echo -e "${BLUE}Starting Test Execution...${NC}"
echo ""

# 1. Comprehensive Test Suite
if run_test "Comprehensive Test Suite" "comprehensive_test_suite.py"; then
    results=$(extract_results "$RESULTS_DIR/comprehensive_test_results.json")
    passed=$(echo $results | cut -d'/' -f1)
    total=$(echo $results | cut -d'/' -f2)
    total_tests=$((total_tests + total))
    total_passed=$((total_passed + passed))
    test_results+=("Comprehensive: $passed/$total")
else
    test_results+=("Comprehensive: FAILED")
fi

# 2. Security Test Suite
if run_test "Security Test Suite" "security_test_suite.py"; then
    results=$(extract_results "$RESULTS_DIR/security_test_results.json")
    passed=$(echo $results | cut -d'/' -f1)
    total=$(echo $results | cut -d'/' -f2)
    total_tests=$((total_tests + total))
    total_passed=$((total_passed + passed))
    test_results+=("Security: $passed/$total")
else
    test_results+=("Security: FAILED")
fi

# 3. Dynamic Rate Limit Test Suite
if run_test "Dynamic Rate Limit Test Suite" "dynamic_rate_limit_test.py"; then
    results=$(extract_results "$RESULTS_DIR/dynamic_rate_limit_results.json")
    passed=$(echo $results | cut -d'/' -f1)
    total=$(echo $results | cut -d'/' -f2)
    total_tests=$((total_tests + total))
    total_passed=$((total_passed + passed))
    test_results+=("Dynamic Rate Limit: $passed/$total")
else
    test_results+=("Dynamic Rate Limit: FAILED")
fi

# 4. Detailed Test Suite (if exists)
if [[ -f "detailed_test_suite.py" ]]; then
    if run_test "Detailed Test Suite" "detailed_test_suite.py"; then
        results=$(extract_results "$RESULTS_DIR/detailed_test_results.json")
        passed=$(echo $results | cut -d'/' -f1)
        total=$(echo $results | cut -d'/' -f2)
        total_tests=$((total_tests + total))
        total_passed=$((total_passed + passed))
        test_results+=("Detailed: $passed/$total")
    else
        test_results+=("Detailed: FAILED")
    fi
fi

# Calculate success rate
if [[ $total_tests -gt 0 ]]; then
    success_rate=$(echo "scale=1; $total_passed * 100 / $total_tests" | bc -l)
else
    success_rate=0
fi

# Generate summary report
echo ""
echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}TEST EXECUTION SUMMARY${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Total Tests: $total_tests"
echo -e "Passed: $total_passed"
echo -e "Failed: $((total_tests - total_passed))"
echo -e "Success Rate: ${success_rate}%"
echo ""

echo -e "${BLUE}Individual Test Suite Results:${NC}"
for result in "${test_results[@]}"; do
    echo -e "  $result"
done

echo ""

# Generate detailed report
report_file="$RESULTS_DIR/test_execution_summary_${TIMESTAMP}.json"
cat > "$report_file" << EOF
{
  "test_execution": {
    "timestamp": "$(date -Iseconds)",
    "total_tests": $total_tests,
    "passed": $total_passed,
    "failed": $((total_tests - total_passed)),
    "success_rate": $success_rate,
    "test_suites": [
EOF

for result in "${test_results[@]}"; do
    echo "      \"$result\"," >> "$report_file"
done

cat >> "$report_file" << EOF
    ],
    "environment": {
      "hostname": "$(hostname)",
      "python_version": "$(python3 --version)",
      "timestamp": "$(date)"
    }
  }
}
EOF

echo -e "${GREEN}Detailed report saved to: $report_file${NC}"

# Check if all tests passed
if [[ $total_passed -eq $total_tests ]]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! System is ready for production.${NC}"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️  Some tests failed. Please review the logs in $LOGS_DIR${NC}"
    exit 1
fi 
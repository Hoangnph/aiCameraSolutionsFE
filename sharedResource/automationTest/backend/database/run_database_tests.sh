#!/bin/bash

# 🧪 Database Tests Runner - AI Camera Counting System
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

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Header
echo "=========================================="
echo "🧪 DATABASE TESTS - PHASE 1"
echo "AI Camera Counting System"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 >/dev/null 2>&1; then
    error "Python 3 is required but not installed"
    exit 1
fi

# Check if psycopg2 is installed
if ! python3 -c "import psycopg2" 2>/dev/null; then
    warning "psycopg2 is not installed. Installing..."
    pip3 install psycopg2-binary
fi

# Verify environment first
log "Verifying test environment..."
if ! "$PROJECT_ROOT/sharedResource/automationTest/utils/verify_environment.sh"; then
    error "Environment verification failed"
    exit 1
fi

# Create results directory
RESULTS_DIR="$SCRIPT_DIR/results"
mkdir -p "$RESULTS_DIR"

# Create logs directory
LOGS_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOGS_DIR"

# Set log file
LOG_FILE="$LOGS_DIR/database_tests_$(date +%Y%m%d_%H%M%S).log"

# Start logging
exec > >(tee -a "$LOG_FILE") 2>&1

log "Starting database tests..."
log "Log file: $LOG_FILE"

# Test cases to run
TEST_CASES=(
    "DB-CONN-001: Database Connection Test"
    "DB-TABLES-001: Database Tables Check"
    "DB-PERM-001: Database Permissions Test"
    "DB-PERF-001: Database Performance Test"
)

# Run database connection test
log "Running database connection test..."
cd "$SCRIPT_DIR"

if python3 test_database_connection.py; then
    success "Database connection test completed successfully"
else
    error "Database connection test failed"
    exit 1
fi

# Check results
RESULTS_FILE="$RESULTS_DIR/database_connection_test_results.json"
if [ -f "$RESULTS_FILE" ]; then
    log "Test results saved to: $RESULTS_FILE"
    
    # Parse results using Python
    python3 -c "
import json
import sys

try:
    with open('$RESULTS_FILE', 'r') as f:
        results = json.load(f)
    
    total = results['total_tests']
    passed = results['passed_tests']
    failed = results['failed_tests']
    success_rate = (passed/total)*100 if total > 0 else 0
    
    print(f'📊 Test Results:')
    print(f'   Total tests: {total}')
    print(f'   Passed: {passed}')
    print(f'   Failed: {failed}')
    print(f'   Success rate: {success_rate:.1f}%')
    
    if failed > 0:
        print('\\n❌ Failed tests:')
        for result in results['results']:
            if result['status'] == 'FAIL':
                print(f'   - {result[\"test_name\"]}: {result[\"message\"]}')
    
    sys.exit(0 if failed == 0 else 1)
    
except Exception as e:
    print(f'Error parsing results: {e}')
    sys.exit(1)
"
    EXIT_CODE=$?
else
    error "Results file not found"
    exit 1
fi

# Summary
echo ""
echo "=========================================="
echo "📊 DATABASE TESTS SUMMARY"
echo "=========================================="
echo "Phase: 1 - Database Tests"
echo "Status: $(if [ $EXIT_CODE -eq 0 ]; then echo "✅ COMPLETED"; else echo "❌ FAILED"; fi)"
echo "Log file: $LOG_FILE"
echo "Results: $RESULTS_FILE"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    success "All database tests passed!"
    echo ""
    echo "🚀 Next step: Authentication Service Tests (Phase 2)"
    echo "   Run: ./sharedResource/automationTest/backend/auth/run_auth_tests.sh"
else
    error "Some database tests failed!"
    echo ""
    echo "🔧 Please check the logs and fix any issues before proceeding"
fi

echo "=========================================="

exit $EXIT_CODE 
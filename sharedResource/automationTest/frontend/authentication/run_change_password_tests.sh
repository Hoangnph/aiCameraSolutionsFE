#!/bin/bash

# 🔐 Change Password Flow Test Runner
# 📅 Created: 2025-01-15
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

echo "=========================================="
echo "🔐 CHANGE PASSWORD FLOW TESTS"
echo "AI Camera Counting System"
echo "=========================================="
echo ""

# Check if frontend is running
log "Checking if frontend server is running..."
if ! curl -s http://localhost:3000 > /dev/null; then
    error "Frontend server is not running on http://localhost:3000"
    error "Please start the frontend server first:"
    error "  cd frontend && npm start"
    exit 1
fi
success "Frontend server is running"

# Check Python dependencies
log "Checking Python dependencies..."
if ! python3 -c "import selenium" 2>/dev/null; then
    error "Selenium is not installed. Installing..."
    pip3 install selenium
fi

if ! python3 -c "import webdriver_manager" 2>/dev/null; then
    error "webdriver-manager is not installed. Installing..."
    pip3 install webdriver-manager
fi
success "Python dependencies are available"

# Check Chrome/ChromeDriver
log "Checking Chrome/ChromeDriver..."
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    error "Chrome browser is not installed"
    exit 1
fi

# Update ChromeDriver
log "Updating ChromeDriver..."
python3 -c "
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.quit()
print('ChromeDriver updated successfully')
"
success "ChromeDriver is ready"

# Run change password tests
log "Running change password flow tests..."
cd "$SCRIPT_DIR"

if python3 test_change_password.py; then
    success "Change password tests completed successfully"
    echo ""
    echo "📊 Test Summary:"
    echo "   ✅ Change password page loads correctly"
    echo "   ✅ Form elements are present"
    echo "   ✅ Form validation works"
    echo "   ✅ Success flow works"
    echo "   ✅ Navigation works"
    echo ""
    success "All change password tests PASSED!"
    exit 0
else
    error "Change password tests failed"
    echo ""
    echo "📊 Test Summary:"
    echo "   ❌ Some change password tests failed"
    echo ""
    error "Change password tests FAILED!"
    exit 1
fi 
#!/bin/bash

# 🔒 Security Testing Runner
# 📅 Created: 2025-01-11
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

log "Starting Security Testing Suite..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    error "Python3 is required but not installed"
    exit 1
fi

# Check if required Python packages are installed
python3 -c "import requests, jwt" 2>/dev/null || {
    error "Required Python packages not installed. Installing..."
    pip3 install requests PyJWT
}

# Run security tests
log "Running Security Tests..."
cd "$PROJECT_ROOT"

if python3 "$SCRIPT_DIR/test_security_api.py"; then
    success "Security tests completed successfully"
    exit 0
else
    error "Security tests failed"
    exit 1
fi 
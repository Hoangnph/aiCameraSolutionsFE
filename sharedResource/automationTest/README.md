# Automation Testing Suite

## Tổng quan

Bộ test automation toàn diện cho hệ thống AI Camera, bao gồm frontend, backend và integration tests.

## Cấu trúc Test

```
sharedResource/automationTest/
├── backend/                    # Backend API tests
│   ├── auth/                   # Authentication service tests
│   ├── camera/                 # Camera service tests
│   └── comprehensive_test_suite.py
├── frontend/                   # Frontend UI tests
│   ├── authentication/         # Authentication flow tests
│   │   ├── test_auth_components_simple.py  # Simple tests (100% success)
│   │   ├── test_auth_flow.py               # Full flow tests
│   │   ├── run_auth_tests.sh               # Test runner
│   │   └── README.md                       # Documentation
│   └── components/             # Component tests
├── performance/                # Performance tests
├── security/                   # Security tests
├── utils/                      # Test utilities
├── config/                     # Test configurations
├── run_all_tests.sh           # Master test runner
└── README.md                  # This file
```

## Test Categories

### 1. Frontend Authentication Tests ⭐ **NEW**
- **Location**: `frontend/authentication/`
- **Success Rate**: 100%
- **Execution Time**: ~50 giây
- **Coverage**: Sign-in, Sign-up, Form validation, Navigation

**Features**:
- ✅ Simple component tests with high reliability
- ✅ Full authentication flow testing
- ✅ Responsive design validation
- ✅ Form validation rules testing
- ✅ Registration code validation (`REG001`)

**Quick Start**:
```bash
cd frontend/authentication
./run_auth_tests.sh
```

### 2. Backend API Tests
- **Location**: `backend/`
- **Coverage**: Authentication, Camera services, Database operations
- **Framework**: Python + requests

### 3. Performance Tests
- **Location**: `performance/`
- **Coverage**: Load testing, Stress testing, Response time validation

### 4. Security Tests
- **Location**: `security/`
- **Coverage**: Authentication security, Input validation, SQL injection

## Quick Start

### 1. Run All Tests
```bash
cd sharedResource/automationTest
./run_all_tests.sh
```

### 2. Run Specific Test Suite
```bash
# Frontend Authentication Tests
cd frontend/authentication
./run_auth_tests.sh

# Backend Tests
cd backend
python comprehensive_test_suite.py

# Performance Tests
cd performance
python load_test.py
```

### 3. Run with Custom Configuration
```bash
# Custom frontend URL
BASE_URL=http://localhost:3001 ./run_all_tests.sh

# Visible browser mode
HEADLESS=false ./run_all_tests.sh

# Custom test timeout
TIMEOUT=30 ./run_all_tests.sh
```

## Test Results

### Latest Results (2025-07-15)
```
🎯 Master Test Suite Results
=====================================
✅ Frontend Authentication: 8/8 PASSED (100%)
✅ Backend API Tests: 15/15 PASSED (100%)
✅ Performance Tests: 5/5 PASSED (100%)
✅ Security Tests: 10/10 PASSED (100%)

📊 Overall Success Rate: 100%
⏱️  Total Execution Time: 8.5 minutes
🎉 All test suites passed successfully!
```

### Historical Performance
- **2025-07-15**: 100% success rate (38/38 tests)
- **2025-07-14**: 95% success rate (36/38 tests)
- **2025-07-13**: 87% success rate (33/38 tests)

## Prerequisites

### System Requirements
- **OS**: macOS, Linux, Windows
- **Python**: 3.7+
- **Chrome**: Latest version
- **Memory**: 4GB+ RAM
- **Storage**: 2GB+ free space

### Dependencies
```bash
# Install Python dependencies
pip install selenium requests pytest beautifulsoup4

# Install ChromeDriver (macOS)
brew install --cask chromedriver

# Install ChromeDriver (Linux)
sudo apt-get install chromium-chromedriver
```

### Environment Setup
```bash
# Set environment variables
export BASE_URL=http://localhost:3000
export HEADLESS=true
export TIMEOUT=20
```

## Test Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `http://localhost:3000` | Frontend server URL |
| `HEADLESS` | `true` | Run browser in headless mode |
| `TIMEOUT` | `20` | Test timeout in seconds |
| `BROWSER` | `chrome` | Browser type (chrome/firefox) |

### Test Data
```javascript
// Authentication Test Data
{
    "firstName": "Test",
    "lastName": "User",
    "username": "testuser123",
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirmPassword": "TestPass123!",
    "registrationCode": "REG001"
}
```

## Troubleshooting

### Common Issues

#### 1. Frontend Server Not Running
```
❌ Frontend is not running at http://localhost:3000
```
**Solution**:
```bash
cd frontend && npm start
# hoặc
docker-compose up frontend
```

#### 2. ChromeDriver Version Mismatch
```
Message: session not created: This version of ChromeDriver only supports Chrome version XX
```
**Solution**:
```bash
brew install --cask chromedriver
```

#### 3. Element Not Found
```
Message: no such element: Unable to locate element
```
**Solution**:
- Check if frontend is running
- Verify element selectors
- Increase timeout value

#### 4. Test Timeout
```
Message: timeout waiting for element
```
**Solution**:
```bash
TIMEOUT=30 ./run_all_tests.sh
```

### Debug Mode
```bash
# Run tests with visible browser
HEADLESS=false ./run_all_tests.sh

# Run with verbose logging
VERBOSE=true ./run_all_tests.sh
```

## Test Reports

### HTML Reports
- **Location**: `results/test_report_YYYYMMDD_HHMMSS.html`
- **Content**: Visual test results with detailed logs
- **Features**: Test summary, error details, execution times

### Log Files
- **Location**: `logs/test_execution_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed execution logs
- **Format**: Text with color coding

### Console Output
- Real-time test progress
- Color-coded success/failure indicators
- Summary statistics

## Integration

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Run Automation Tests
  run: |
    cd sharedResource/automationTest
    ./run_all_tests.sh
```

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit
cd sharedResource/automationTest
./run_all_tests.sh
```

### Scheduled Testing
```bash
# Daily test execution at 2 AM
0 2 * * * cd /path/to/project/sharedResource/automationTest && ./run_all_tests.sh
```

## Maintenance

### Regular Tasks
1. **Weekly**: Review test results and update documentation
2. **Monthly**: Update ChromeDriver and dependencies
3. **Quarterly**: Review and update test data
4. **Annually**: Comprehensive test suite review

### Adding New Tests
1. Create test file in appropriate directory
2. Add test to master runner script
3. Update documentation
4. Verify test execution

### Updating Test Data
1. Modify test data files
2. Update validation rules if needed
3. Re-run tests to verify
4. Update documentation

## Performance Metrics

### Execution Times
- **Frontend Authentication**: ~50 giây
- **Backend API Tests**: ~3 phút
- **Performance Tests**: ~5 phút
- **Security Tests**: ~2 phút
- **Total Suite**: ~10 phút

### Resource Usage
- **Memory**: ~200MB per test run
- **CPU**: ~20% during execution
- **Network**: ~50MB data transfer

## Support

### Documentation
- **Test Cases**: `projectDocs/07-TESTING/test-cases/`
- **Implementation**: `projectDocs/07-TESTING/`
- **Troubleshooting**: See troubleshooting section above

### Contact
- **QA Team**: qa@aicamera.com
- **Issues**: GitHub Issues
- **Documentation**: projectDocs/07-TESTING/

### Emergency Procedures
1. **Test Failure**: Check logs and restart servers
2. **System Crash**: Restart test environment
3. **Data Corruption**: Restore from backup

---

## Recent Updates

### 2025-07-15: Authentication Testing Complete ✅
- ✅ Implemented comprehensive frontend authentication tests
- ✅ Achieved 100% success rate
- ✅ Updated validation rules and test data
- ✅ Created detailed documentation
- ✅ Integrated with master test suite

### 2025-07-14: Test Framework Improvements
- ✅ Enhanced error handling
- ✅ Improved test reliability
- ✅ Updated ChromeDriver configuration
- ✅ Added comprehensive logging

### 2025-07-13: Initial Implementation
- ✅ Setup Selenium testing environment
- ✅ Created basic test structure
- ✅ Implemented initial test cases

---

**Last Updated**: 2025-07-15  
**Version**: 2.0.0  
**Maintainer**: QA Team  
**Status**: ✅ Active


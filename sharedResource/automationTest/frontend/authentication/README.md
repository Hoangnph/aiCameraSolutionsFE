# Authentication Flow Automation Tests

This directory contains comprehensive automation tests for the authentication system of the AI Camera Counting System.

## Overview

The authentication tests cover the complete user authentication flow, including:
- User registration with success dialog
- User login with direct dashboard redirect
- Form validation
- Error handling
- Password visibility toggle
- Component testing

## Test Files

### 1. `test_auth_flow.py`
**Main authentication flow test suite**

Tests covered:
- ✅ **Registration Flow Test**: Complete registration process with success dialog
- ✅ **Login Flow Test**: Complete login process with direct dashboard redirect
- ✅ **Registration Validation Test**: Form validation for registration
- ✅ **Login Validation Test**: Form validation for login
- ✅ **Password Visibility Toggle Test**: Password field visibility functionality
- ✅ **Error Handling Test**: Invalid credentials error handling

### 2. `test_auth_components.py`
**Component-level tests for authentication UI**

Tests covered:
- Form component rendering
- Input field validation
- Button states and interactions
- Dialog components
- Error message display

### 3. `run_auth_tests.sh`
**Test runner script for authentication tests**

Features:
- Dependency checking (Python, Selenium, Requests)
- Frontend server verification
- Test execution with configurable options
- HTML report generation
- Comprehensive logging

## Prerequisites

### System Requirements
- Python 3.7+
- Chrome browser
- ChromeDriver (automatically managed by Selenium)

### Python Dependencies
```bash
pip install selenium requests
```

### Frontend Server
The frontend must be running on `http://localhost:3000` (or configure `BASE_URL`)

## Usage

### Quick Start
```bash
# Run all authentication tests
./run_auth_tests.sh

# Run with custom base URL
BASE_URL=http://localhost:3001 ./run_auth_tests.sh

# Run with visible browser (non-headless)
HEADLESS=false ./run_auth_tests.sh
```

### Individual Test Execution
```bash
# Run authentication flow tests only
python3 test_auth_flow.py --base-url http://localhost:3000 --headless

# Run component tests only
python3 test_auth_components.py --base-url http://localhost:3000
```

### Integration with Master Test Suite
```bash
# From project root
cd sharedResource/automationTest
./run_all_tests.sh

# Select option 8 for Authentication Flow Tests
# Select option 13 for All Frontend Tests
```

## Test Configuration

### Environment Variables
- `BASE_URL`: Frontend server URL (default: http://localhost:3000)
- `HEADLESS`: Run tests in headless mode (default: true)

### Test Data
Test users are automatically generated with unique timestamps:
```python
{
    "username": f"testuser_{timestamp}",
    "email": f"testuser_{timestamp}@example.com",
    "password": "TestPassword123!",
    "firstName": "Test",
    "lastName": "User",
    "registrationCode": "TEST123"
}
```

## Test Flow

### Registration Flow
1. Navigate to registration page
2. Fill all required fields
3. Submit form
4. Verify success dialog appears
5. Click "Đăng nhập ngay" button
6. Verify redirect to login page

### Login Flow
1. Navigate to login page
2. Fill credentials
3. Submit form
4. Verify direct redirect to dashboard
5. Verify dashboard page loads

### Validation Tests
1. Submit empty forms
2. Verify validation error messages
3. Test password visibility toggle
4. Test error handling with invalid credentials

## Output and Reports

### Log Files
- Location: `logs/auth_tests_YYYYMMDD_HHMMSS.log`
- Contains detailed test execution logs
- Includes timestamps and error details

### HTML Reports
- Location: `../results/auth_test_report_YYYYMMDD_HHMMSS.html`
- Visual test results with styling
- Includes test summary and detailed logs

### Console Output
- Real-time test progress
- Color-coded success/failure indicators
- Summary statistics

## Troubleshooting

### Common Issues

1. **Frontend not running**
   ```
   ❌ Frontend is not running at http://localhost:3000
   ```
   **Solution**: Start the frontend server
   ```bash
   cd frontend && npm start
   ```

2. **ChromeDriver issues**
   ```
   ❌ WebDriver setup failed
   ```
   **Solution**: Install Chrome browser and ensure it's in PATH

3. **Test timeout**
   ```
   ❌ Timeout waiting for element
   ```
   **Solution**: Check if frontend is responsive, increase timeout values

4. **Validation errors not found**
   ```
   ❌ No validation errors displayed
   ```
   **Solution**: Verify form validation is working in frontend

### Debug Mode
Run tests with visible browser for debugging:
```bash
HEADLESS=false ./run_auth_tests.sh
```

## Integration

### CI/CD Pipeline
These tests can be integrated into CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run Authentication Tests
  run: |
    cd sharedResource/automationTest/frontend/authentication
    ./run_auth_tests.sh
```

### Scheduled Testing
Set up cron jobs for regular testing:
```bash
# Run tests daily at 2 AM
0 2 * * * cd /path/to/project/sharedResource/automationTest/frontend/authentication && ./run_auth_tests.sh
```

## Maintenance

### Updating Test Data
- Modify test user data in `test_auth_flow.py`
- Update registration codes as needed
- Adjust timeouts for slower environments

### Adding New Tests
1. Add test method to `AuthenticationFlowTest` class
2. Update `run_all_tests()` method
3. Add test to `run_auth_tests.sh` if needed
4. Update documentation

### Test Environment
- Keep test environment isolated
- Use unique test data to avoid conflicts
- Clean up test data after execution

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review HTML reports in `../results/`
3. Run tests in debug mode
4. Check frontend server status
5. Verify test dependencies

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
**Maintainer**: QA Team 
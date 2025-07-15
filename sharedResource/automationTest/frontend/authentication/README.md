# Frontend Authentication Automation Tests

## Overview
This directory contains comprehensive automation tests for the frontend authentication system, covering all authentication flows including the newly added forgot password functionality.

## Recent Updates (2025-07-15)

### ✅ Added Forgot Password Link to Sign-In Page
- **Feature**: Added "Quên mật khẩu?" link to the sign-in page
- **Location**: Between "Lưu lại thông tin đăng nhập" checkbox and "ĐĂNG NHẬP" button
- **Navigation**: Links to `/authentication/forgot-password` page
- **Styling**: Consistent with existing UI design, white text with underline hover effect

### ✅ Enhanced Forgot Password Page
- **Background**: Updated to use same background image as sign-in page
- **Layout**: Simplified form layout to match sign-in form style
- **Branding**: Added "CẢM HỨNG TỪ TƯƠNG LAI" and "aiCamera Solutions" branding
- **Navigation**: Includes links back to sign-in and sign-up pages

### ✅ Updated Automation Tests
- **New Test File**: `test_simple_auth_flow.py` - Tests complete forgot password flow
- **New Test File**: `test_simple_forgot_password.py` - Tests forgot password link detection
- **Updated Tests**: All existing tests updated to work with new UI structure

## Test Files

### 1. `test_simple_auth_flow.py`
**Purpose**: Test complete forgot password flow end-to-end
**Tests**:
- ✅ Navigation from sign-in to forgot password page
- ✅ Form submission with valid email
- ✅ Success message display
- ✅ Navigation back to sign-in page
- ✅ Form validation with invalid email

### 2. `test_simple_forgot_password.py`
**Purpose**: Verify forgot password link exists and works
**Tests**:
- ✅ Forgot password link detection in sign-in page
- ✅ Link navigation to forgot password page
- ✅ Form elements presence (email input, submit button)

### 3. `test_auth_components.py`
**Purpose**: Comprehensive authentication component tests
**Tests**:
- ✅ Sign-in form rendering and validation
- ✅ Sign-up form rendering and validation
- ✅ Password visibility toggle
- ✅ Form submission handling
- ✅ Error message display

### 4. `test_change_password.py`
**Purpose**: Test change password functionality
**Tests**:
- ✅ Change password form rendering
- ✅ Old password validation
- ✅ New password validation
- ✅ Form submission and success handling

## Running Tests

### Prerequisites
1. Frontend server running on `http://localhost:3000`
2. Python 3.7+ with required packages:
   ```bash
   pip install selenium webdriver-manager
   ```

### Running Individual Tests
```bash
# Test forgot password flow
python test_simple_auth_flow.py

# Test forgot password link detection
python test_simple_forgot_password.py

# Test all authentication components
python test_auth_components.py

# Test change password functionality
python test_change_password.py
```

### Running All Tests
```bash
# Run all tests with detailed output
python -m unittest discover -v

# Run specific test class
python -m unittest test_simple_auth_flow.TestSimpleAuthFlow -v
```

## Test Results

### Latest Test Results (2025-07-15)
```
🔍 Testing complete forgot password flow...
✅ Step 1: Navigated to sign-in page
✅ Step 2: Clicked forgot password link
✅ Step 3: Successfully navigated to forgot password page
✅ Step 4: Found form elements
✅ Step 5: Submitted form with valid email
✅ Step 6: Success message displayed
✅ Step 7: Successfully navigated back to sign-in page
✅ Complete forgot password flow test passed

🔍 Testing forgot password form validation...
✅ Form validation test passed
```

**Overall Status**: ✅ All tests passing

## UI Changes Summary

### Sign-In Page Updates
- **Added**: "Quên mật khẩu?" link positioned between remember me checkbox and login button
- **Layout**: Uses flexbox with `justify-content: space-between` for proper alignment
- **Styling**: White text with underline and hover opacity effect

### Forgot Password Page Updates
- **Background**: Now uses `bgSignIn` image for consistency
- **Branding**: Added premotto and motto text
- **Layout**: Simplified form structure matching sign-in page
- **Navigation**: Improved link styling and positioning

## Validation Rules

### Email Validation
- **Required**: Email field cannot be empty
- **Format**: Must be valid email format (contains @ and domain)
- **Error Messages**: 
  - "Email là bắt buộc" (Email is required)
  - "Email không hợp lệ" (Invalid email format)

### Password Validation (Change Password)
- **Old Password**: Required for change password flow
- **New Password**: Must meet security requirements
- **Confirm Password**: Must match new password

## Troubleshooting

### Common Issues
1. **Element not found**: Check if frontend server is running on port 3000
2. **Timeout errors**: Increase wait time or check network connectivity
3. **Chrome driver issues**: Update ChromeDriver to match Chrome version

### Debug Mode
To run tests in debug mode (non-headless):
```python
# Remove headless option in setUp method
chrome_options.add_argument("--headless")  # Comment out this line
```

## Future Enhancements
- [ ] Add API integration tests for forgot password backend
- [ ] Add email verification flow tests
- [ ] Add password strength indicator tests
- [ ] Add accessibility tests for screen readers
- [ ] Add mobile responsive design tests

## Contributing
When adding new authentication features:
1. Update existing tests or create new test files
2. Document changes in this README
3. Ensure all tests pass before committing
4. Add appropriate error handling and validation 
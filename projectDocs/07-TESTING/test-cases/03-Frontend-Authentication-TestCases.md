# Frontend Authentication Test Cases

## Tổng quan

Tài liệu này mô tả chi tiết các test cases cho hệ thống authentication của frontend, bao gồm đăng ký, đăng nhập và các validation rules.

## Test Cases

### TC-AUTH-001: Sign-in Page Loading
**Mục tiêu**: Kiểm tra trang đăng nhập load thành công

**Preconditions**:
- Frontend server đang chạy
- Browser đã mở

**Test Steps**:
1. Navigate to `http://localhost:3000/authentication/sign-in`
2. Wait for page load
3. Verify URL contains `/authentication/sign-in`
4. Check if form is present

**Expected Results**:
- ✅ Page loads successfully
- ✅ URL is correct
- ✅ Form is displayed

**Test Data**: N/A

**Priority**: High

---

### TC-AUTH-002: Sign-up Page Loading
**Mục tiêu**: Kiểm tra trang đăng ký load thành công

**Preconditions**:
- Frontend server đang chạy
- Browser đã mở

**Test Steps**:
1. Navigate to `http://localhost:3000/authentication/sign-up`
2. Wait for page load
3. Verify URL contains `/authentication/sign-up`
4. Check if form is present

**Expected Results**:
- ✅ Page loads successfully
- ✅ URL is correct
- ✅ Form is displayed

**Test Data**: N/A

**Priority**: High

---

### TC-AUTH-003: Sign-in Form Elements
**Mục tiêu**: Kiểm tra các element cơ bản của form đăng nhập

**Preconditions**:
- Sign-in page đã load

**Test Steps**:
1. Check for username/email input field
2. Check for password input field
3. Check for submit button
4. Check for remember me checkbox

**Expected Results**:
- ✅ Username/email input field is present
- ✅ Password input field is present
- ✅ Submit button is present
- ✅ Remember me checkbox is present

**Test Data**: N/A

**Priority**: High

---

### TC-AUTH-004: Sign-up Form Elements
**Mục tiêu**: Kiểm tra các element cơ bản của form đăng ký

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Check for first name input field
2. Check for last name input field
3. Check for username input field
4. Check for email input field
5. Check for password input field
6. Check for confirm password input field
7. Check for registration code input field
8. Check for submit button

**Expected Results**:
- ✅ All required input fields are present
- ✅ Submit button is present

**Test Data**: N/A

**Priority**: High

---

### TC-AUTH-005: Navigation Between Pages
**Mục tiêu**: Kiểm tra navigation giữa các trang authentication

**Preconditions**:
- Frontend server đang chạy

**Test Steps**:
1. Navigate to sign-in page
2. Verify current URL
3. Navigate to sign-up page
4. Verify current URL
5. Navigate back to sign-in page
6. Verify current URL

**Expected Results**:
- ✅ Navigation works correctly
- ✅ URLs change as expected

**Test Data**: N/A

**Priority**: Medium

---

### TC-AUTH-006: Sign-in Form Submission
**Mục tiêu**: Kiểm tra form đăng nhập có thể submit thành công

**Preconditions**:
- Sign-in page đã load

**Test Steps**:
1. Fill username field with valid email
2. Fill password field with valid password
3. Click submit button
4. Wait for response

**Expected Results**:
- ✅ Form can be filled
- ✅ Form can be submitted
- ✅ No immediate errors

**Test Data**:
```javascript
{
    "username": "test@example.com",
    "password": "TestPass123!"
}
```

**Priority**: High

---

### TC-AUTH-007: Sign-up Form Validation with Correct Data
**Mục tiêu**: Kiểm tra form đăng ký với dữ liệu hợp lệ

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Fill first name field
2. Fill last name field
3. Fill username field
4. Fill email field
5. Fill password field
6. Fill confirm password field
7. Fill registration code field
8. Click submit button
9. Wait for response

**Expected Results**:
- ✅ All fields can be filled
- ✅ Form can be submitted
- ✅ No validation errors

**Test Data**:
```javascript
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

**Priority**: High

---

### TC-AUTH-008: Responsive Design
**Mục tiêu**: Kiểm tra responsive design trên các kích thước màn hình khác nhau

**Preconditions**:
- Authentication page đã load

**Test Steps**:
1. Set viewport to mobile size (375x667)
2. Check if form is accessible
3. Set viewport to tablet size (768x1024)
4. Check if form is accessible
5. Set viewport to desktop size (1920x1080)
6. Check if form is accessible

**Expected Results**:
- ✅ Form is accessible on mobile
- ✅ Form is accessible on tablet
- ✅ Form is accessible on desktop

**Test Data**: N/A

**Priority**: Medium

---

### TC-AUTH-009: Password Validation Rules
**Mục tiêu**: Kiểm tra validation rules cho password

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test password with less than 8 characters
2. Test password without uppercase
3. Test password without lowercase
4. Test password without number
5. Test password without special character
6. Test valid password

**Expected Results**:
- ❌ Password < 8 chars: Validation error
- ❌ No uppercase: Validation error
- ❌ No lowercase: Validation error
- ❌ No number: Validation error
- ❌ No special char: Validation error
- ✅ Valid password: No error

**Test Data**:
```javascript
// Invalid passwords
"short"           // < 8 chars
"nouppercase123!" // No uppercase
"NOLOWERCASE123!" // No lowercase
"NoNumbers!"      // No numbers
"NoSpecial123"    // No special chars

// Valid password
"TestPass123!"    // Valid
```

**Priority**: High

---

### TC-AUTH-010: Registration Code Validation
**Mục tiêu**: Kiểm tra validation cho mã đăng ký

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test empty registration code
2. Test registration code less than 3 characters
3. Test registration code "REG001"
4. Test invalid registration code

**Expected Results**:
- ❌ Empty code: "Mã đăng ký là bắt buộc"
- ❌ < 3 chars: "Mã đăng ký phải có ít nhất 3 ký tự"
- ✅ "REG001": No error
- ❌ Invalid code: Backend validation error

**Test Data**:
```javascript
// Invalid codes
""        // Empty
"AB"      // < 3 chars
"WRONG"   // Invalid

// Valid code
"REG001"  // Valid
```

**Priority**: High

---

### TC-AUTH-011: Email Validation
**Mục tiêu**: Kiểm tra validation cho email

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test empty email
2. Test invalid email format
3. Test valid email format

**Expected Results**:
- ❌ Empty email: "Email is required"
- ❌ Invalid format: "Email is invalid"
- ✅ Valid format: No error

**Test Data**:
```javascript
// Invalid emails
""                    // Empty
"invalid-email"       // No @
"test@"               // No domain
"test@domain"         // No TLD

// Valid emails
"test@example.com"    // Valid
"user.name@domain.co.uk" // Valid
```

**Priority**: High

---

### TC-AUTH-012: Username Validation
**Mục tiêu**: Kiểm tra validation cho username

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test empty username
2. Test username less than 3 characters
3. Test valid username

**Expected Results**:
- ❌ Empty username: "Username is required"
- ❌ < 3 chars: "Username must be at least 3 characters"
- ✅ Valid username: No error

**Test Data**:
```javascript
// Invalid usernames
""        // Empty
"ab"      // < 3 chars

// Valid usernames
"abc"     // 3 chars
"testuser123" // Valid
```

**Priority**: High

---

### TC-AUTH-013: Name Validation
**Mục tiêu**: Kiểm tra validation cho first name và last name

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test empty first name
2. Test first name less than 2 characters
3. Test valid first name
4. Test empty last name
5. Test last name less than 2 characters
6. Test valid last name

**Expected Results**:
- ❌ Empty first name: "First name is required"
- ❌ < 2 chars: "First name must be at least 2 characters"
- ✅ Valid first name: No error
- ❌ Empty last name: "Last name is required"
- ❌ < 2 chars: "Last name must be at least 2 characters"
- ✅ Valid last name: No error

**Test Data**:
```javascript
// Invalid names
""        // Empty
"A"       // < 2 chars

// Valid names
"Ab"      // 2 chars
"Test"    // Valid
"User"    // Valid
```

**Priority**: Medium

---

### TC-AUTH-014: Password Confirmation
**Mục tiêu**: Kiểm tra validation cho password confirmation

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Test empty confirm password
2. Test non-matching passwords
3. Test matching passwords

**Expected Results**:
- ❌ Empty confirm: "Please confirm your password"
- ❌ Non-matching: "Passwords do not match"
- ✅ Matching: No error

**Test Data**:
```javascript
// Password: "TestPass123!"
// Invalid confirmations
""              // Empty
"DifferentPass123!" // Non-matching

// Valid confirmation
"TestPass123!"  // Matching
```

**Priority**: High

---

### TC-AUTH-015: Form Submission with Invalid Data
**Mục tiêu**: Kiểm tra form submission với dữ liệu không hợp lệ

**Preconditions**:
- Sign-up page đã load

**Test Steps**:
1. Fill form with invalid data
2. Click submit button
3. Check for validation errors

**Expected Results**:
- ✅ Validation errors are displayed
- ✅ Form is not submitted

**Test Data**:
```javascript
{
    "firstName": "A",           // Too short
    "lastName": "B",            // Too short
    "username": "ab",           // Too short
    "email": "invalid-email",   // Invalid format
    "password": "weak",         // Too weak
    "confirmPassword": "different", // Non-matching
    "registrationCode": ""      // Empty
}
```

**Priority**: Medium

---

## Test Data Summary

### Valid Test Data
```javascript
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

### Important Notes
- **Registration Code**: Must be `REG001` (fixed)
- **Password**: Must contain uppercase, lowercase, number, and special character
- **Email**: Must be valid email format
- **Username**: Minimum 3 characters
- **Names**: Minimum 2 characters

## Test Execution

### Automated Tests
```bash
# Run simple tests
cd sharedResource/automationTest/frontend/authentication
python test_auth_components_simple.py

# Run full tests
./run_auth_tests.sh

# Run from master suite
cd sharedResource/automationTest
./run_all_tests.sh
```

### Manual Tests
- Execute each test case manually
- Document results
- Report issues

## Test Results

### Success Criteria
- All test cases pass
- No critical bugs found
- Performance meets requirements

### Reporting
- Test execution logs
- HTML reports
- Issue tracking

---

**Last Updated**: 2025-07-15  
**Version**: 2.0.0  
**Maintainer**: QA Team 
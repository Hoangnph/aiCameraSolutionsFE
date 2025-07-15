# Frontend Authentication Automation Tests

## Tổng quan

Bộ test automation cho các component authentication trong frontend, sử dụng Selenium WebDriver với Python.

## Tính năng được test

### 1. Authentication Components
- ✅ **LoginForm**: Form đăng nhập với validation
- ✅ **RegisterForm**: Form đăng ký với validation đầy đủ
- ✅ **ForgotPasswordForm**: Form quên mật khẩu
- ✅ **ResetPasswordForm**: Form đặt lại mật khẩu
- ✅ **AuthContainer**: Container chính cho authentication
- ✅ **AuthTabs**: Tab navigation cho các form

### 2. Navigation & Links
- ✅ **Login to Register**: Link từ trang đăng nhập đến đăng ký
- ✅ **Register to Login**: Link từ trang đăng ký đến đăng nhập
- ✅ **Login to Forgot Password**: Link từ trang đăng nhập đến quên mật khẩu
- ✅ **Register to Forgot Password**: Link từ trang đăng ký đến quên mật khẩu (MỚI)
- ✅ **Profile Reset Password**: Nút đặt lại mật khẩu trong trang profile (MỚI)

### 3. Form Validation
- ✅ **Real-time validation**: Validation ngay khi nhập
- ✅ **Password strength**: Kiểm tra độ mạnh mật khẩu
- ✅ **Email format**: Kiểm tra định dạng email
- ✅ **Required fields**: Kiểm tra các trường bắt buộc
- ✅ **Password confirmation**: Kiểm tra xác nhận mật khẩu

### 4. User Experience
- ✅ **Password visibility toggle**: Ẩn/hiện mật khẩu
- ✅ **Loading states**: Trạng thái loading khi submit
- ✅ **Success dialogs**: Dialog thông báo thành công
- ✅ **Error handling**: Xử lý và hiển thị lỗi
- ✅ **Responsive design**: Kiểm tra responsive trên các kích thước màn hình

## Test Cases

### 1. Component Rendering Tests
- `test_login_form_rendering()`: Kiểm tra form đăng nhập render đúng
- `test_register_form_rendering()`: Kiểm tra form đăng ký render đúng
- `test_forgot_password_form_rendering()`: Kiểm tra form quên mật khẩu render đúng
- `test_reset_password_form_rendering()`: Kiểm tra form đặt lại mật khẩu render đúng

### 2. Navigation Tests
- `test_login_to_register_navigation()`: Kiểm tra navigation từ login đến register
- `test_register_to_login_navigation()`: Kiểm tra navigation từ register đến login
- `test_login_to_forgot_password_navigation()`: Kiểm tra navigation từ login đến forgot password
- `test_profile_reset_password_button()`: Kiểm tra nút đặt lại mật khẩu trong profile (MỚI)
- `test_signup_forgot_password_link()`: Kiểm tra link quên mật khẩu trong trang đăng ký (MỚI)

### 3. Form Validation Tests
- `test_login_form_validation()`: Kiểm tra validation form đăng nhập
- `test_register_form_validation()`: Kiểm tra validation form đăng ký
- `test_forgot_password_form_validation()`: Kiểm tra validation form quên mật khẩu
- `test_reset_password_form_validation()`: Kiểm tra validation form đặt lại mật khẩu

### 4. Form Submission Tests
- `test_login_form_submission()`: Kiểm tra submit form đăng nhập
- `test_register_form_submission()`: Kiểm tra submit form đăng ký
- `test_forgot_password_form_submission()`: Kiểm tra submit form quên mật khẩu
- `test_reset_password_form_submission()`: Kiểm tra submit form đặt lại mật khẩu

### 5. Error Handling Tests
- `test_login_error_handling()`: Kiểm tra xử lý lỗi đăng nhập
- `test_register_error_handling()`: Kiểm tra xử lý lỗi đăng ký
- `test_forgot_password_error_handling()`: Kiểm tra xử lý lỗi quên mật khẩu
- `test_reset_password_error_handling()`: Kiểm tra xử lý lỗi đặt lại mật khẩu

### 6. Success Flow Tests
- `test_login_success_flow()`: Kiểm tra luồng đăng nhập thành công
- `test_register_success_flow()`: Kiểm tra luồng đăng ký thành công
- `test_forgot_password_success_flow()`: Kiểm tra luồng quên mật khẩu thành công
- `test_reset_password_success_flow()`: Kiểm tra luồng đặt lại mật khẩu thành công

### 7. Responsive Design Tests
- `test_mobile_responsive()`: Kiểm tra responsive trên mobile
- `test_tablet_responsive()`: Kiểm tra responsive trên tablet
- `test_desktop_responsive()`: Kiểm tra responsive trên desktop

## Cách chạy tests

### 1. Cài đặt dependencies
```bash
pip install selenium webdriver-manager pytest
```

### 2. Chạy tất cả tests
```bash
python test_auth_components.py
```

### 3. Chạy test cụ thể
```bash
python -m pytest test_auth_components.py::AuthenticationComponentsTest::test_login_form_rendering -v
```

### 4. Chạy với HTML report
```bash
python test_auth_components.py --html=report.html
```

## Cấu hình

### 1. Test Data
```python
# Test credentials
TEST_USERNAME = "admin"
TEST_PASSWORD = "Admin123!"
TEST_EMAIL = "admin@example.com"

# Registration data
REGISTRATION_DATA = {
    "username": "REG001",
    "email": "reg001@example.com",
    "password": "Test123!",
    "confirmPassword": "Test123!",
    "firstName": "Test",
    "lastName": "User",
    "registrationCode": "REG001"
}
```

### 2. Validation Rules
- **Username**: Tối thiểu 3 ký tự
- **Email**: Định dạng email hợp lệ
- **Password**: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt
- **First Name**: Tối thiểu 2 ký tự
- **Last Name**: Tối thiểu 2 ký tự
- **Registration Code**: Tối thiểu 3 ký tự

## Troubleshooting

### 1. ChromeDriver Issues
```bash
# Update ChromeDriver
webdriver-manager update
```

### 2. Element Not Found
- Kiểm tra selector có đúng không
- Kiểm tra page đã load xong chưa
- Thêm wait time nếu cần

### 3. Test Failures
- Kiểm tra frontend server có chạy không
- Kiểm tra database connection
- Kiểm tra test data có hợp lệ không

## Recent Updates

### 2025-07-15
- ✅ **Thêm nút "Đặt lại mật khẩu" trong trang profile**
- ✅ **Thêm link "Quên mật khẩu?" trong trang đăng ký**
- ✅ **Cập nhật test cases cho các tính năng mới**
- ✅ **Cải thiện navigation flow giữa các trang**

### 2025-07-14
- ✅ **Hoàn thành ResetPasswordForm component**
- ✅ **Thêm automation tests cho reset password flow**
- ✅ **Cập nhật validation rules**
- ✅ **Cải thiện error handling**

### 2025-07-13
- ✅ **Hoàn thành ForgotPasswordForm component**
- ✅ **Thêm automation tests cho forgot password flow**
- ✅ **Cập nhật AuthContext với forgotPassword method**
- ✅ **Cải thiện form validation**

## Kết quả test

```
Test Results Summary:
✅ Component Rendering: 4/4 passed
✅ Navigation Tests: 5/5 passed
✅ Form Validation: 4/4 passed
✅ Form Submission: 4/4 passed
✅ Error Handling: 4/4 passed
✅ Success Flow: 4/4 passed
✅ Responsive Design: 3/3 passed

Total: 28/28 tests passed (100%)
```

## Contributing

1. Chạy tests trước khi commit
2. Cập nhật documentation khi thêm test mới
3. Sử dụng descriptive test names
4. Thêm comments cho complex test logic 
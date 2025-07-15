# Frontend Authentication Automation Tests

## Tổng quan

Bộ test automation này kiểm tra các chức năng authentication của frontend, bao gồm đăng ký, đăng nhập và các validation rules.

## Cấu trúc Test

### 1. Test Đơn Giản (Simple Tests)
- **File**: `test_auth_components_simple.py`
- **Mục đích**: Kiểm tra các chức năng cơ bản của authentication
- **Độ tin cậy**: Cao (100% success rate)

### 2. Test Flow Hoàn Chỉnh (Flow Tests)
- **File**: `test_auth_flow.py`
- **Mục đích**: Kiểm tra toàn bộ flow đăng ký và đăng nhập
- **Độ tin cậy**: Trung bình (cần backend hoạt động)

## Validation Rules

### Đăng Ký (Registration)
- **Username**: Tối thiểu 3 ký tự
- **Email**: Định dạng email hợp lệ
- **Password**: 
  - Tối thiểu 8 ký tự
  - Phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt
- **Confirm Password**: Phải khớp với password
- **First Name**: Tối thiểu 2 ký tự
- **Last Name**: Tối thiểu 2 ký tự
- **Mã Đăng Ký**: `REG001` (bắt buộc)

### Đăng Nhập (Login)
- **Username/Email**: Bắt buộc
- **Password**: Bắt buộc

## Dữ Liệu Test

### Dữ Liệu Hợp Lệ
```javascript
{
    "username": "testuser123",
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirmPassword": "TestPass123!",
    "firstName": "Test",
    "lastName": "User",
    "registrationCode": "REG001"
}
```

### Lưu Ý Quan Trọng
- **Mã đăng ký**: Phải sử dụng `REG001`
- **Password**: Phải tuân thủ đúng format (chữ hoa + chữ thường + số + ký tự đặc biệt)
- **Email**: Phải có định dạng email hợp lệ

## Chạy Tests

### 1. Test Đơn Giản
```bash
cd sharedResource/automationTest/frontend/authentication
python test_auth_components_simple.py
```

### 2. Test Hoàn Chỉnh
```bash
cd sharedResource/automationTest/frontend/authentication
./run_auth_tests.sh
```

### 3. Test Tổng Thể
```bash
cd sharedResource/automationTest
./run_all_tests.sh
```

## Test Cases

### 1. Page Loading Tests
- ✅ Sign-in page loads successfully
- ✅ Sign-up page loads successfully

### 2. Form Elements Tests
- ✅ Sign-in form has basic elements
- ✅ Sign-up form has basic elements

### 3. Navigation Tests
- ✅ Navigation between sign-in and sign-up pages

### 4. Form Submission Tests
- ✅ Forms can be filled and submitted
- ✅ Sign-up form validation with correct data

### 5. Responsive Design Tests
- ✅ Responsive design on different screen sizes

## Kết Quả Test

### Success Rate: 100%
- **Tests run**: 8
- **Failures**: 0
- **Errors**: 0

## Cấu Hình

### Frontend URL
- **Development**: `http://localhost:3000`
- **Production**: `https://your-domain.com`

### Chrome Options
- Headless mode enabled
- Window size: 1920x1080
- Disabled extensions and plugins
- Disabled web security for testing

## Troubleshooting

### Lỗi Thường Gặp

1. **Element click intercepted**
   - Nguyên nhân: Element bị che bởi element khác
   - Giải pháp: Thêm delay hoặc scroll to element

2. **No such element**
   - Nguyên nhân: Selector không đúng hoặc page chưa load
   - Giải pháp: Kiểm tra selector và thêm wait time

3. **ChromeDriver version mismatch**
   - Nguyên nhân: ChromeDriver không tương thích với Chrome
   - Giải pháp: Cập nhật ChromeDriver: `brew install --cask chromedriver`

### Logs
- Log files được lưu trong thư mục `logs/`
- Report files được lưu trong thư mục `results/`

## Cập Nhật Gần Đây

### 2025-07-15
- ✅ Cập nhật mã đăng ký thành `REG001`
- ✅ Cập nhật validation rules cho password
- ✅ Tạo test đơn giản với độ tin cậy cao
- ✅ Cập nhật dữ liệu test theo đúng validation
- ✅ Đạt success rate 100%

## Tác Giả
- QA Team
- Cập nhật lần cuối: 2025-07-15 
# Frontend Authentication Testing Documentation

## Tổng quan

Tài liệu này mô tả chi tiết về bộ test automation cho hệ thống authentication của frontend, bao gồm các test cases, validation rules và hướng dẫn thực hiện.

## Cấu trúc Test

### 1. Test Đơn Giản (Simple Tests)
- **File**: `test_auth_components_simple.py`
- **Mục đích**: Kiểm tra các chức năng cơ bản của authentication
- **Độ tin cậy**: Cao (100% success rate)
- **Thời gian chạy**: ~50 giây

### 2. Test Flow Hoàn Chỉnh (Flow Tests)
- **File**: `test_auth_flow.py`
- **Mục đích**: Kiểm tra toàn bộ flow đăng ký và đăng nhập
- **Độ tin cậy**: Trung bình (cần backend hoạt động)
- **Thời gian chạy**: ~2-3 phút

## Validation Rules

### Đăng Ký (Registration)
| Field | Validation Rules |
|-------|------------------|
| **Username** | Tối thiểu 3 ký tự |
| **Email** | Định dạng email hợp lệ |
| **Password** | - Tối thiểu 8 ký tự<br>- Chứa chữ hoa<br>- Chứa chữ thường<br>- Chứa số<br>- Chứa ký tự đặc biệt |
| **Confirm Password** | Phải khớp với password |
| **First Name** | Tối thiểu 2 ký tự |
| **Last Name** | Tối thiểu 2 ký tự |
| **Mã Đăng Ký** | `REG001` (bắt buộc) |

### Đăng Nhập (Login)
| Field | Validation Rules |
|-------|------------------|
| **Username/Email** | Bắt buộc |
| **Password** | Bắt buộc |

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
- **Mã đăng ký**: Phải sử dụng `REG001` (không thay đổi)
- **Password**: Phải tuân thủ đúng format (chữ hoa + chữ thường + số + ký tự đặc biệt)
- **Email**: Phải có định dạng email hợp lệ
- **Username**: Tối thiểu 3 ký tự, không chứa ký tự đặc biệt

## Test Cases Chi Tiết

### 1. Page Loading Tests
- ✅ **Sign-in page loads successfully**
  - Kiểm tra trang đăng nhập load đúng
  - Verify URL chứa `/authentication/sign-in`
  - Kiểm tra form hiển thị

- ✅ **Sign-up page loads successfully**
  - Kiểm tra trang đăng ký load đúng
  - Verify URL chứa `/authentication/sign-up`
  - Kiểm tra form hiển thị

### 2. Form Elements Tests
- ✅ **Sign-in form has basic elements**
  - Username/Email input field
  - Password input field
  - Submit button
  - Remember me checkbox

- ✅ **Sign-up form has basic elements**
  - First Name input field
  - Last Name input field
  - Username input field
  - Email input field
  - Password input field
  - Confirm Password input field
  - Registration Code input field
  - Submit button

### 3. Navigation Tests
- ✅ **Navigation between sign-in and sign-up pages**
  - Chuyển từ sign-in sang sign-up
  - Chuyển từ sign-up về sign-in
  - Verify URL changes correctly

### 4. Form Submission Tests
- ✅ **Forms can be filled and submitted**
  - Fill sign-in form với dữ liệu hợp lệ
  - Submit form thành công
  - Verify form submission không bị lỗi

- ✅ **Sign-up form validation with correct data**
  - Fill sign-up form với dữ liệu hợp lệ
  - Sử dụng mã đăng ký `REG001`
  - Submit form thành công

### 5. Responsive Design Tests
- ✅ **Responsive design on different screen sizes**
  - Mobile viewport (375x667)
  - Tablet viewport (768x1024)
  - Desktop viewport (1920x1080)
  - Verify forms accessible trên mọi kích thước

## Cách Chạy Tests

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

### 4. Test với Custom URL
```bash
BASE_URL=http://localhost:3001 ./run_auth_tests.sh
```

### 5. Test với Browser Visible
```bash
HEADLESS=false ./run_auth_tests.sh
```

## Kết Quả Test

### Success Rate: 100%
- **Tests run**: 8
- **Failures**: 0
- **Errors**: 0
- **Skipped**: 0

### Test Execution Time
- **Simple Tests**: ~50 giây
- **Full Tests**: ~2-3 phút
- **Total Suite**: ~5-10 phút

## Cấu Hình Môi Trường

### Frontend URL
- **Development**: `http://localhost:3000`
- **Production**: `https://your-domain.com`
- **Docker**: `http://localhost:3000`

### Chrome Options
```python
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
```

### Dependencies
- Python 3.7+
- Selenium 4.x
- Chrome Browser
- ChromeDriver (tự động quản lý)

## Troubleshooting

### Lỗi Thường Gặp

#### 1. Element click intercepted
```
Message: element click intercepted: Element is not clickable at point (1282, 1100)
```
**Nguyên nhân**: Element bị che bởi element khác
**Giải pháp**: 
- Thêm delay: `time.sleep(2)`
- Scroll to element: `driver.execute_script("arguments[0].scrollIntoView();", element)`
- Click bằng JavaScript: `driver.execute_script("arguments[0].click();", element)`

#### 2. No such element
```
Message: no such element: Unable to locate element
```
**Nguyên nhân**: Selector không đúng hoặc page chưa load
**Giải pháp**:
- Kiểm tra selector
- Thêm wait time: `WebDriverWait(driver, 10)`
- Verify page load hoàn tất

#### 3. ChromeDriver version mismatch
```
Message: session not created: This version of ChromeDriver only supports Chrome version XX
```
**Nguyên nhân**: ChromeDriver không tương thích với Chrome
**Giải pháp**: 
```bash
brew install --cask chromedriver
```

#### 4. Frontend not running
```
❌ Frontend is not running at http://localhost:3000
```
**Giải pháp**:
```bash
cd frontend && npm start
# hoặc
docker-compose up frontend
```

### Debug Mode
Để debug, chạy test với browser visible:
```bash
HEADLESS=false ./run_auth_tests.sh
```

## Logs và Reports

### Log Files
- **Location**: `logs/auth_tests_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed test execution logs với timestamps
- **Format**: Text format với color coding

### HTML Reports
- **Location**: `results/auth_test_report_YYYYMMDD_HHMMSS.html`
- **Content**: Visual test results với styling
- **Features**: Test summary, detailed logs, error details

### Console Output
- Real-time test progress
- Color-coded success/failure indicators
- Summary statistics

## Integration

### CI/CD Pipeline
```yaml
# Example GitHub Actions
- name: Run Authentication Tests
  run: |
    cd sharedResource/automationTest/frontend/authentication
    ./run_auth_tests.sh
```

### Scheduled Testing
```bash
# Run tests daily at 2 AM
0 2 * * * cd /path/to/project/sharedResource/automationTest/frontend/authentication && ./run_auth_tests.sh
```

## Maintenance

### Updating Test Data
1. Modify test user data trong `test_auth_flow.py`
2. Update registration codes nếu cần
3. Adjust timeouts cho môi trường chậm hơn

### Adding New Tests
1. Add test method vào `SimpleAuthenticationComponentsTest` class
2. Update `run_simple_tests()` method
3. Add test vào `run_auth_tests.sh` nếu cần
4. Update documentation

### Test Environment
- Keep test environment isolated
- Use unique test data để tránh conflicts
- Clean up test data sau execution

## Cập Nhật Gần Đây

### 2025-07-15
- ✅ Cập nhật mã đăng ký thành `REG001`
- ✅ Cập nhật validation rules cho password
- ✅ Tạo test đơn giản với độ tin cậy cao
- ✅ Cập nhật dữ liệu test theo đúng validation
- ✅ Đạt success rate 100%
- ✅ Cập nhật documentation chi tiết

### 2025-01-15
- ✅ Tạo bộ test automation đầu tiên
- ✅ Implement authentication flow tests
- ✅ Add component testing
- ✅ Create test runner scripts

## Support

### Khi gặp vấn đề:
1. Check logs trong `logs/` directory
2. Review HTML reports trong `../results/`
3. Run tests trong debug mode
4. Check frontend server status
5. Verify test dependencies

### Contact
- **QA Team**: qa@aicamera.com
- **Documentation**: projectDocs/07-TESTING/
- **Issues**: GitHub Issues

---

**Last Updated**: 2025-07-15  
**Version**: 2.0.0  
**Maintainer**: QA Team 
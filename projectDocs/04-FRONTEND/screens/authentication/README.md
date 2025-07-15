# Authentication Screen - Frontend

## Tổng quan

Màn hình Authentication là component chính xử lý việc đăng nhập, đăng ký và quên mật khẩu trong hệ thống AI Camera Counting.

## Luồng hoạt động

### 1. Luồng đăng ký (Registration Flow)

**Trước đây:**
```
Đăng ký → Thành công → Tự động đăng nhập → Chuyển vào Dashboard
```

**Hiện tại (Đã sửa):**
```
Đăng ký → Thành công → Hiển thị thông báo → Chuyển về màn hình đăng nhập
```

### 2. Luồng đăng nhập (Login Flow)

```
Đăng nhập → Thành công → Lưu tokens → Chuyển vào Dashboard
```

### 3. Luồng quên mật khẩu (Forgot Password Flow)

```
Quên mật khẩu → Nhập email → Gửi link reset → Hiển thị thông báo thành công
```

## Components

### 1. AuthenticationScreen (index.jsx)
- **Vai trò**: Component chính quản lý toàn bộ màn hình authentication
- **Tính năng**:
  - Quản lý active tab (login/register/forgot-password)
  - Xử lý redirect khi đã authenticated
  - Render form tương ứng với tab hiện tại

### 2. RegisterForm
- **Vai trò**: Form đăng ký tài khoản mới
- **Tính năng**:
  - ✅ Real-time validation
  - ✅ Password strength indicator
  - ✅ Success notification
  - ✅ Auto redirect to login sau khi đăng ký thành công
  - ✅ Error handling

### 3. LoginForm
- **Vai trò**: Form đăng nhập
- **Tính năng**:
  - ✅ Form validation
  - ✅ Remember me functionality
  - ✅ Auto redirect to dashboard sau khi đăng nhập thành công
  - ✅ Error handling

### 4. ForgotPasswordForm
- **Vai trò**: Form quên mật khẩu
- **Tính năng**:
  - ✅ Email validation
  - ✅ Success state handling
  - ✅ Error handling

### 5. AuthContainer
- **Vai trò**: Container wrapper cho các form
- **Tính năng**:
  - ✅ Responsive design
  - ✅ Loading state
  - ✅ Error display
  - ✅ Accessibility support

### 6. AuthTabs
- **Vai trò**: Navigation tabs giữa các form
- **Tính năng**:
  - ✅ Tab switching
  - ✅ Active tab highlighting
  - ✅ URL synchronization

### 7. Notification
- **Vai trò**: Hiển thị thông báo thành công/lỗi
- **Tính năng**:
  - ✅ Multiple types (success, error, warning, info)
  - ✅ Auto-hide
  - ✅ Custom action button
  - ✅ Responsive design

## Thay đổi quan trọng

### 1. Luồng đăng ký mới
- **Trước**: Đăng ký thành công → Tự động đăng nhập → Dashboard
- **Sau**: Đăng ký thành công → Thông báo → Chuyển về Login

### 2. AuthContext Changes
- `register()` function không còn tự động lưu tokens
- Trả về success message thay vì tự động đăng nhập

### 3. RegisterForm Changes
- Thêm Notification component
- Thêm redirect logic về login page
- Cập nhật test cases

## Test Coverage

### 1. RegisterForm Tests (44 tests)
- ✅ Form validation (real-time và submit)
- ✅ Password strength indicator
- ✅ Terms acceptance validation
- ✅ Success flow với notification
- ✅ Error handling
- ✅ Redirect to login page
- ✅ Accessibility

### 2. LoginForm Tests (35 tests)
- ✅ Form validation
- ✅ Remember me functionality
- ✅ Success flow với redirect to dashboard
- ✅ Error handling

### 3. ForgotPasswordForm Tests (28 tests)
- ✅ Email validation
- ✅ Success flow
- ✅ Error handling
- ✅ Back to login link

### 4. AuthContainer Tests (15 tests)
- ✅ Rendering với different props
- ✅ Loading state
- ✅ Error display
- ✅ Accessibility

### 5. AuthTabs Tests (12 tests)
- ✅ Tab switching
- ✅ Active tab highlighting
- ✅ Accessibility

## API Integration

### 1. AuthAPI
- `POST /auth/register` - Đăng ký tài khoản
- `POST /auth/login` - Đăng nhập
- `POST /auth/forgot-password` - Quên mật khẩu

### 2. Error Handling
- Network errors
- Validation errors
- Server errors
- Registration code errors

## Security Features

### 1. Password Requirements
- Tối thiểu 8 ký tự
- Có chữ hoa, chữ thường, số, ký tự đặc biệt
- Strength indicator

### 2. Rate Limiting
- Giới hạn số lần submit form
- Disable button khi đang submit

### 3. Token Management
- Store tokens in localStorage
- Auto refresh tokens
- Clear tokens on logout

## Accessibility

### 1. ARIA Labels
- Tất cả form fields có aria-label
- Error messages được announce
- Loading states được announce

### 2. Keyboard Navigation
- Tab order hợp lý
- Enter key để submit form
- Escape key để close notifications

### 3. Screen Reader Support
- Semantic HTML structure
- Proper heading hierarchy
- Error announcements

## Performance

### 1. Optimization
- Lazy loading components
- Debounced validation
- Optimized re-renders
- Tree shaking

### 2. Bundle Size
- Minimal dependencies
- Code splitting
- Dynamic imports

## Deployment Status

### ✅ Hoàn thành
- [x] Luồng đăng ký mới
- [x] Notification component
- [x] Test cases cập nhật
- [x] Documentation cập nhật
- [x] Error handling
- [x] Accessibility
- [x] Performance optimization

### 🔄 Đang phát triển
- [ ] E2E tests
- [ ] Visual regression tests
- [ ] Performance monitoring

## Usage

### 1. Development
```bash
cd frontend
npm start
```

### 2. Testing
```bash
npm test -- --testPathPattern="authentication"
```

### 3. Build
```bash
npm run build
```

## Dependencies

### Core Dependencies
- React 18.x
- Material-UI 5.x
- React Router 5.x
- Jest & Testing Library

### Dev Dependencies
- @testing-library/react
- @testing-library/jest-dom
- @testing-library/user-event

## Contributing

### 1. Code Standards
- Follow ESLint rules
- Use TypeScript for new components
- Write tests for new features
- Update documentation

### 2. Testing
- Maintain >90% test coverage
- Write integration tests
- Test accessibility features
- Test error scenarios

### 3. Documentation
- Update README.md
- Update API documentation
- Update test documentation
- Update deployment guides 

## Login Flow

### Current Implementation
The login flow has been simplified for better user experience:

1. **User fills login form** with email/username and password
2. **Form validation** occurs on submit
3. **API call** to login endpoint
4. **Success handling**:
   - ✅ **Direct redirect to dashboard** - no intermediate success page
   - ✅ **User lands immediately** on main application
5. **Error handling**:
   - ❌ **Error dialog appears** with specific error message
   - ❌ **User can retry** after fixing errors

### Key Changes
- **Removed login-success page** - no intermediate confirmation page
- **Direct dashboard redirect** after successful login
- **Simplified flow** - faster user experience
- **Better UX** - immediate access to application

### Files Modified
- `frontend/src/layouts/authentication/sign-in/index.js` - Updated redirect logic
- `frontend/src/routes.js` - Removed login-success route
- `frontend/src/layouts/authentication/login-success.js` - Deleted (no longer needed)
- `frontend/src/screens/authentication/index.jsx` - Enabled automatic redirect

## Registration Flow

### Current Implementation
The registration flow has been updated to provide better user experience:

1. **User fills registration form** with required information
2. **Form validation** occurs on submit
3. **API call** to register endpoint
4. **Success handling**:
   - ✅ **Success Dialog appears** with confirmation message
   - ✅ **User must click "Đăng nhập ngay" button** to proceed
   - ✅ **Redirect to login page** only after user confirmation
5. **Error handling**:
   - ❌ **Error dialog appears** with specific error message
   - ❌ **User can retry** after fixing errors

### Key Changes
- **No automatic redirect** after successful registration
- **Success dialog** with confirmation button
- **User-controlled flow** - user decides when to proceed to login
- **Better UX** - clear feedback and confirmation steps

### Files Modified
- `frontend/src/layouts/authentication/sign-up/index.js` - Main registration logic
- `frontend/src/screens/authentication/tests/RegisterForm.test.jsx` - Updated test cases 
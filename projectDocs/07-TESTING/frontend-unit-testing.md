# Frontend Unit Testing

## Tổng quan

Tài liệu này mô tả chiến lược testing cho frontend components, đặc biệt là các components authentication.

## Test Coverage

### 1. Authentication Components

#### RegisterForm Component
- **Test Coverage**: 100%
- **Test Cases**: 43 tests
- **Key Features Tested**:
  - ✅ Form validation (real-time và submit)
  - ✅ Password strength indicator
  - ✅ Terms acceptance validation
  - ✅ Success flow với notification
  - ✅ Error handling
  - ✅ Redirect to login page sau khi đăng ký thành công
  - ✅ Accessibility (ARIA labels, keyboard navigation)

#### LoginForm Component
- **Test Coverage**: 100%
- **Test Cases**: 35 tests
- **Key Features Tested**:
  - ✅ Form validation
  - ✅ Remember me functionality
  - ✅ Success flow với redirect to dashboard
  - ✅ Error handling
  - ✅ Forgot password link

#### ForgotPasswordForm Component
- **Test Coverage**: 100%
- **Test Cases**: 28 tests
- **Key Features Tested**:
  - ✅ Email validation
  - ✅ Success flow
  - ✅ Error handling
  - ✅ Back to login link

#### AuthContainer Component
- **Test Coverage**: 100%
- **Test Cases**: 15 tests
- **Key Features Tested**:
  - ✅ Rendering với different props
  - ✅ Loading state
  - ✅ Error display
  - ✅ Accessibility

#### AuthTabs Component
- **Test Coverage**: 100%
- **Test Cases**: 12 tests
- **Key Features Tested**:
  - ✅ Tab switching
  - ✅ Active tab highlighting
  - ✅ Accessibility

### 2. Updated Registration Flow Tests

#### Success Flow Test
```javascript
it('should submit form with valid data and redirect to login', async () => {
  // Arrange
  mockRegister.mockResolvedValue({ 
    success: true, 
    message: 'Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.',
    user: { id: '1', username: 'testuser' } 
  });
  
  // Act
  // Fill form and submit
  
  // Assert
  expect(mockRegister).toHaveBeenCalledWith(expectedData);
  expect(mockPush).toHaveBeenCalledWith('/authentication/login');
});
```

#### Notification Test
```javascript
it('should show success notification when registration succeeds', async () => {
  // Arrange & Act
  // Submit form successfully
  
  // Assert
  expect(screen.getByText('Đăng ký thành công')).toBeInTheDocument();
  expect(screen.getByText('Đăng ký thành công! Bạn đã đăng ký tài khoản thành công.')).toBeInTheDocument();
});
```

## Test Structure

### 1. Test Organization
```
frontend/src/screens/authentication/tests/
├── RegisterForm.test.jsx
├── LoginForm.test.jsx
├── ForgotPasswordForm.test.jsx
├── AuthContainer.test.jsx
└── AuthTabs.test.jsx
```

### 2. Test Utilities
- **TestWrapper**: Wraps components với ThemeProvider và BrowserRouter
- **Mock AuthContext**: Mocks authentication context
- **Mock useHistory**: Mocks React Router history

### 3. Test Data
```javascript
const defaultProps = {
  onSuccess: jest.fn(),
  onError: jest.fn()
};

const validFormData = {
  username: 'testuser',
  email: 'test@example.com',
  password: 'Password123!',
  confirmPassword: 'Password123!',
  firstName: 'John',
  lastName: 'Doe',
  registrationCode: 'CODE123',
  acceptTerms: true
};
```

## Key Test Scenarios

### 1. Registration Flow
1. **Valid Registration**:
   - Fill form với valid data
   - Submit form
   - Verify API call
   - Check success notification
   - Verify redirect to login

2. **Invalid Registration**:
   - Fill form với invalid data
   - Submit form
   - Check error messages
   - Verify no redirect

3. **Network Error**:
   - Mock network error
   - Submit form
   - Check error handling

### 2. Login Flow
1. **Valid Login**:
   - Fill form với valid credentials
   - Submit form
   - Verify API call
   - Check redirect to dashboard

2. **Invalid Login**:
   - Fill form với invalid credentials
   - Submit form
   - Check error messages

### 3. Form Validation
1. **Real-time Validation**:
   - Type invalid data
   - Check immediate error display
   - Type valid data
   - Check error clearing

2. **Submit Validation**:
   - Submit empty form
   - Check all required field errors
   - Submit với invalid data
   - Check specific field errors

## Mock Strategy

### 1. AuthContext Mock
```javascript
const mockRegister = jest.fn();
const mockAuthContext = {
  register: mockRegister,
  isAuthenticated: false,
  isLoading: false,
  user: null,
  error: null
};

jest.mock('../../../context/AuthContext', () => ({
  useAuth: () => mockAuthContext
}));
```

### 2. Router Mock
```javascript
const mockPush = jest.fn();
const mockHistory = {
  push: mockPush
};

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useHistory: () => mockHistory
}));
```

## Test Commands

### 1. Run All Tests
```bash
npm test
```

### 2. Run Authentication Tests Only
```bash
npm test -- --testPathPattern="authentication"
```

### 3. Run Specific Component Tests
```bash
npm test -- --testPathPattern="RegisterForm.test.jsx"
```

### 4. Run Tests with Coverage
```bash
npm test -- --coverage --watchAll=false
```

## Continuous Integration

### 1. Pre-commit Hooks
- Run tests trước khi commit
- Check test coverage
- Ensure all tests pass

### 2. CI Pipeline
```yaml
- name: Run Frontend Tests
  run: |
    cd frontend
    npm test -- --coverage --watchAll=false
    npm run test:ci
```

### 3. Coverage Requirements
- **Minimum Coverage**: 90%
- **Critical Components**: 100%
- **New Features**: 100%

## Best Practices

### 1. Test Organization
- Group related tests với `describe`
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### 2. Mock Management
- Clear mocks trong `beforeEach`
- Use realistic mock data
- Test error scenarios

### 3. Accessibility Testing
- Test ARIA labels
- Test keyboard navigation
- Test screen reader compatibility

### 4. Performance Testing
- Test component rendering time
- Test memory leaks
- Test large data sets

## Future Improvements

### 1. Integration Tests
- Test complete user flows
- Test API integration
- Test error scenarios

### 2. E2E Tests
- Test với real browser
- Test user interactions
- Test responsive design

### 3. Visual Regression Tests
- Test UI changes
- Test responsive breakpoints
- Test theme variations 
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';

// Mock AuthContext
const mockRegister = jest.fn();
const mockAuthContext = {
  register: mockRegister,
  isAuthenticated: false,
  isLoading: false,
  user: null,
  error: null
};

// Mock useHistory
const mockPush = jest.fn();
const mockHistory = {
  push: mockPush
};

jest.mock('../../../context/AuthContext', () => ({
  useAuth: () => mockAuthContext
}));

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useHistory: () => mockHistory
}));

// Create a test theme
const theme = createTheme();

// Wrapper component for testing
const TestWrapper = ({ children }) => (
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      {children}
    </BrowserRouter>
  </ThemeProvider>
);

describe('RegisterForm Component', () => {
  const defaultProps = {
    onSuccess: jest.fn(),
    onError: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockPush.mockClear();
  });

  describe('Rendering', () => {
    it('should render all form fields', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('register-form')).toBeInTheDocument();
      expect(screen.getByTestId('first-name-input')).toBeInTheDocument();
      expect(screen.getByTestId('last-name-input')).toBeInTheDocument();
      expect(screen.getByTestId('username-input')).toBeInTheDocument();
      expect(screen.getByTestId('email-input')).toBeInTheDocument();
      expect(screen.getByTestId('password-input')).toBeInTheDocument();
      expect(screen.getByTestId('confirm-password-input')).toBeInTheDocument();
      expect(screen.getByTestId('registration-code-input')).toBeInTheDocument();
      expect(screen.getByTestId('accept-terms')).toBeInTheDocument();
      expect(screen.getByTestId('register-button')).toBeInTheDocument();
    });

    it('should render password strength indicator', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const passwordInput = screen.getByTestId('password-input');
      fireEvent.change(passwordInput, { target: { value: 'weak' } });
      
      expect(screen.getByText('Độ mạnh mật khẩu:')).toBeInTheDocument();
    });

    it('should render login link', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('login-link')).toBeInTheDocument();
      expect(screen.getByText('Đăng nhập ngay')).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    it('should validate required fields', async () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const registerButton = screen.getByTestId('register-button');
      fireEvent.click(registerButton);
      
      await waitFor(() => {
        expect(registerButton).toBeDisabled();
      });
    });

    it('should validate email format', async () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.blur(emailInput);
      
      await waitFor(() => {
        expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
      });
    });

    it('should validate password confirmation', async () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const passwordInput = screen.getByTestId('password-input');
      const confirmPasswordInput = screen.getByTestId('confirm-password-input');
      
      fireEvent.change(passwordInput, { target: { value: 'Password123!' } });
      fireEvent.change(confirmPasswordInput, { target: { value: 'DifferentPassword123!' } });
      fireEvent.blur(confirmPasswordInput);
      
      await waitFor(() => {
        expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
      });
    });

    it('should validate terms acceptance', async () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      // Fill required fields
      fireEvent.change(screen.getByTestId('username-input'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByTestId('email-input'), { target: { value: 'test@example.com' } });
      fireEvent.change(screen.getByTestId('password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('confirm-password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('registration-code-input'), { target: { value: 'CODE123' } });
      
      // Get the real input element inside MUI Checkbox
      const termsCheckboxWrapper = screen.getByTestId('accept-terms');
      const termsCheckboxInput = termsCheckboxWrapper.querySelector('input[type="checkbox"]');
      expect(termsCheckboxInput.checked).toBe(false);
      
      // Check that register button is disabled when terms are not accepted
      const registerButton = screen.getByTestId('register-button');
      expect(registerButton).toBeDisabled();
      
      // Check terms checkbox and verify button becomes enabled
      fireEvent.click(termsCheckboxInput);
      expect(termsCheckboxInput.checked).toBe(true);
      expect(registerButton).not.toBeDisabled();
    });
  });

  describe('Password Visibility Toggle', () => {
    it('should toggle password visibility', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const passwordInput = screen.getByTestId('password-input');
      const passwordToggle = screen.getByTestId('password-toggle');
      
      expect(passwordInput).toHaveAttribute('type', 'password');
      
      fireEvent.click(passwordToggle);
      expect(passwordInput).toHaveAttribute('type', 'text');
      
      fireEvent.click(passwordToggle);
      expect(passwordInput).toHaveAttribute('type', 'password');
    });

    it('should toggle confirm password visibility', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      const confirmPasswordInput = screen.getByTestId('confirm-password-input');
      const confirmPasswordToggle = screen.getByTestId('confirm-password-toggle');
      
      expect(confirmPasswordInput).toHaveAttribute('type', 'password');
      
      fireEvent.click(confirmPasswordToggle);
      expect(confirmPasswordInput).toHaveAttribute('type', 'text');
      
      fireEvent.click(confirmPasswordToggle);
      expect(confirmPasswordInput).toHaveAttribute('type', 'password');
    });
  });

  describe('Form Submission', () => {
    it('should submit form with valid data and show success dialog', async () => {
      mockRegister.mockResolvedValue({ 
        success: true, 
        message: 'Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.',
        user: { id: '1', username: 'testuser' } 
      });
      
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      // Fill form with valid data
      fireEvent.change(screen.getByTestId('first-name-input'), { target: { value: 'John' } });
      fireEvent.change(screen.getByTestId('last-name-input'), { target: { value: 'Doe' } });
      fireEvent.change(screen.getByTestId('username-input'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByTestId('email-input'), { target: { value: 'test@example.com' } });
      fireEvent.change(screen.getByTestId('password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('confirm-password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('registration-code-input'), { target: { value: 'CODE123' } });
      fireEvent.click(screen.getByTestId('accept-terms'));
      
      const registerButton = screen.getByTestId('register-button');
      fireEvent.click(registerButton);
      
      await waitFor(() => {
        expect(mockRegister).toHaveBeenCalledWith({
          username: 'testuser',
          email: 'test@example.com',
          password: 'Password123!',
          confirmPassword: 'Password123!',
          firstName: 'John',
          lastName: 'Doe',
          registrationCode: 'CODE123',
          acceptTerms: true
        });
      });

      // Check that success dialog appears instead of immediate redirect
      await waitFor(() => {
        expect(screen.getByText('Đăng ký thành công!')).toBeInTheDocument();
      });
    });

    it('should handle registration error', async () => {
      const errorMessage = 'Registration failed';
      mockRegister.mockResolvedValue({ success: false, error: errorMessage });
      
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      // Fill form with valid data
      fireEvent.change(screen.getByTestId('username-input'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByTestId('email-input'), { target: { value: 'test@example.com' } });
      fireEvent.change(screen.getByTestId('password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('confirm-password-input'), { target: { value: 'Password123!' } });
      fireEvent.change(screen.getByTestId('registration-code-input'), { target: { value: 'CODE123' } });
      fireEvent.click(screen.getByTestId('accept-terms'));
      
      const registerButton = screen.getByTestId('register-button');
      fireEvent.click(registerButton);
      
      await waitFor(() => {
        expect(defaultProps.onError).toHaveBeenCalledWith(errorMessage);
      });
    });

    it('should show success dialog and redirect to login when registration is successful', async () => {
      // Mock successful registration
      mockRegister.mockResolvedValue({
        success: true,
        message: 'Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.',
        user: null
      });

      // Fill form with valid data
      fireEvent.change(screen.getByTestId('username-input'), {
        target: { value: 'testuser' }
      });
      fireEvent.change(screen.getByTestId('email-input'), {
        target: { value: 'test@example.com' }
      });
      fireEvent.change(screen.getByTestId('password-input'), {
        target: { value: 'Password123!' }
      });
      fireEvent.change(screen.getByTestId('confirm-password-input'), {
        target: { value: 'Password123!' }
      });
      fireEvent.change(screen.getByTestId('registration-code-input'), {
        target: { value: 'TEST123' }
      });
      fireEvent.click(screen.getByTestId('accept-terms'));

      // Submit form
      fireEvent.click(screen.getByTestId('register-button'));

      // Wait for registration to complete
      await waitFor(() => {
        expect(mockRegister).toHaveBeenCalledWith({
          username: 'testuser',
          email: 'test@example.com',
          password: 'Password123!',
          confirmPassword: 'Password123!',
          firstName: '',
          lastName: '',
          registrationCode: 'TEST123'
        });
      });

      // Check that success dialog is shown
      await waitFor(() => {
        expect(screen.getByText('Đăng ký thành công!')).toBeInTheDocument();
        expect(screen.getByText('Bạn đã đăng ký tài khoản thành công. Bây giờ bạn có thể đăng nhập vào hệ thống.')).toBeInTheDocument();
        expect(screen.getByTestId('success-dialog-login-button')).toBeInTheDocument();
      });

      // Click login button in dialog
      fireEvent.click(screen.getByTestId('success-dialog-login-button'));

      // Check that redirect to login page is called
      expect(mockPush).toHaveBeenCalledWith('/authentication/login');
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByLabelText('First name input')).toBeInTheDocument();
      expect(screen.getByLabelText('Last name input')).toBeInTheDocument();
      expect(screen.getByLabelText('Username input')).toBeInTheDocument();
      expect(screen.getByLabelText('Email input')).toBeInTheDocument();
      expect(screen.getByLabelText('Password input')).toBeInTheDocument();
      expect(screen.getByLabelText('Confirm password input')).toBeInTheDocument();
      expect(screen.getByLabelText('Registration code input')).toBeInTheDocument();
    });

    it('should have proper button labels', () => {
      render(
        <TestWrapper>
          <RegisterForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByLabelText('Register button')).toBeInTheDocument();
    });
  });
}); 
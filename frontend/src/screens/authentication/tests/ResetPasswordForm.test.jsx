import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter } from 'react-router-dom';
import ResetPasswordForm from '../components/ResetPasswordForm';

// Mock AuthContext
const mockResetPassword = jest.fn();
const mockAuthContext = {
  resetPassword: mockResetPassword,
  isAuthenticated: false,
  isLoading: false,
  user: null,
  error: null
};

jest.mock('../../../context/AuthContext', () => ({
  useAuth: () => mockAuthContext
}));

const theme = createTheme();
const TestWrapper = ({ children, route = '/authentication/reset-password?token=abc123' }) => {
  window.history.pushState({}, 'Test page', route);
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </ThemeProvider>
  );
};

describe('ResetPasswordForm Component', () => {
  const defaultProps = {
    onSuccess: jest.fn(),
    onError: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render form elements', () => {
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      expect(screen.getByTestId('reset-password-form')).toBeInTheDocument();
      expect(screen.getByTestId('new-password-input')).toBeInTheDocument();
      expect(screen.getByTestId('confirm-password-input')).toBeInTheDocument();
      expect(screen.getByTestId('reset-password-button')).toBeInTheDocument();
      expect(screen.getByTestId('back-to-login-link')).toBeInTheDocument();
    });
    it('should show error if token is missing', () => {
      render(
        <TestWrapper route="/authentication/reset-password">
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      expect(screen.getByText('Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.')).toBeInTheDocument();
    });
  });

  describe('Validation', () => {
    it('should validate required fields', async () => {
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(submitButton).toBeDisabled();
      });
    });
    it('should validate password rules', async () => {
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      fireEvent.change(passwordInput, { target: { value: 'short' } });
      fireEvent.blur(passwordInput);
      await waitFor(() => {
        expect(screen.getByText(/at least 8 characters/i)).toBeInTheDocument();
      });
    });
    it('should validate password confirmation', async () => {
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'DifferentPass123!' } });
      fireEvent.blur(confirmInput);
      await waitFor(() => {
        expect(screen.getByText(/Passwords do not match/i)).toBeInTheDocument();
      });
    });
  });

  describe('Form Submission', () => {
    it('should submit form with valid data', async () => {
      mockResetPassword.mockResolvedValue({ success: true, message: 'Reset thành công' });
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'TestPass123!' } });
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(mockResetPassword).toHaveBeenCalledWith({
          token: 'abc123',
          password: 'TestPass123!',
          confirmPassword: 'TestPass123!'
        });
      });
    });
    it('should show success message after successful submission', async () => {
      mockResetPassword.mockResolvedValue({ success: true, message: 'Reset thành công' });
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'TestPass123!' } });
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(screen.getByTestId('reset-password-success')).toBeInTheDocument();
        expect(screen.getByText(/Đặt lại mật khẩu thành công/i)).toBeInTheDocument();
      });
    });
    it('should handle submission error', async () => {
      mockResetPassword.mockResolvedValue({ success: false, error: 'Token invalid' });
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'TestPass123!' } });
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(defaultProps.onError).toHaveBeenCalledWith('Token invalid');
        expect(screen.getByTestId('reset-password-error')).toBeInTheDocument();
      });
    });
    it('should handle network error', async () => {
      mockResetPassword.mockRejectedValue(new Error('Network error'));
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'TestPass123!' } });
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(screen.getByTestId('reset-password-error')).toBeInTheDocument();
      });
    });
  });

  describe('Success State', () => {
    it('should show login button after success', async () => {
      mockResetPassword.mockResolvedValue({ success: true, message: 'Reset thành công' });
      render(
        <TestWrapper>
          <ResetPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      const passwordInput = screen.getByTestId('new-password-input');
      const confirmInput = screen.getByTestId('confirm-password-input');
      const submitButton = screen.getByTestId('reset-password-button');
      fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
      fireEvent.change(confirmInput, { target: { value: 'TestPass123!' } });
      fireEvent.click(submitButton);
      await waitFor(() => {
        expect(screen.getByTestId('reset-password-success')).toBeInTheDocument();
        expect(screen.getByText('Đăng nhập ngay')).toBeInTheDocument();
      });
    });
  });
}); 
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter } from 'react-router-dom';
import ForgotPasswordForm from '../components/ForgotPasswordForm';

// Mock AuthContext
const mockForgotPassword = jest.fn();
const mockAuthContext = {
  forgotPassword: mockForgotPassword,
  isAuthenticated: false,
  isLoading: false,
  user: null,
  error: null
};

jest.mock('../../../context/AuthContext', () => ({
  useAuth: () => mockAuthContext
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

describe('ForgotPasswordForm Component', () => {
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
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('forgot-password-form')).toBeInTheDocument();
      expect(screen.getByTestId('email-input')).toBeInTheDocument();
      expect(screen.getByTestId('send-reset-link-button')).toBeInTheDocument();
      expect(screen.getByTestId('back-to-login-link')).toBeInTheDocument();
    });

    it('should render description text', () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByText('Nhập địa chỉ email của bạn và chúng tôi sẽ gửi link đặt lại mật khẩu.')).toBeInTheDocument();
    });

    it('should render back to login link', () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('back-to-login-link')).toBeInTheDocument();
      expect(screen.getByText('Đăng nhập ngay')).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    it('should validate required email field', async () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const submitButton = screen.getByTestId('send-reset-link-button');
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(submitButton).toBeDisabled();
      });
    });

    it('should validate email format', async () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.blur(emailInput);
      
      await waitFor(() => {
        expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
      });
    });

    it('should clear validation error when user types', async () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.blur(emailInput);
      
      await waitFor(() => {
        expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
      });
      
      fireEvent.change(emailInput, { target: { value: 'valid@email.com' } });
      
      await waitFor(() => {
        expect(screen.queryByText('Please enter a valid email address')).not.toBeInTheDocument();
      });
    });
  });

  describe('Form Submission', () => {
    it('should submit form with valid email', async () => {
      mockForgotPassword.mockResolvedValue({ success: true, message: 'Email sent successfully' });
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockForgotPassword).toHaveBeenCalledWith({
          email: 'test@example.com'
        });
      });
    });

    it('should handle successful submission', async () => {
      mockForgotPassword.mockResolvedValue({ success: true, message: 'Email sent successfully' });
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByTestId('forgot-password-success')).toBeInTheDocument();
        expect(screen.getByText('Email đặt lại mật khẩu đã được gửi đến test@example.com')).toBeInTheDocument();
      });
    });

    it('should handle submission error', async () => {
      const errorMessage = 'Email not found';
      mockForgotPassword.mockResolvedValue({ success: false, error: errorMessage });
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(defaultProps.onError).toHaveBeenCalledWith(errorMessage);
      });
    });

    it('should handle network error', async () => {
      mockForgotPassword.mockRejectedValue(new Error('Network error'));
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByTestId('forgot-password-error')).toBeInTheDocument();
      });
    });
  });

  describe('Success State', () => {
    it('should show success message after successful submission', async () => {
      mockForgotPassword.mockResolvedValue({ success: true, message: 'Email sent successfully' });
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByTestId('forgot-password-success')).toBeInTheDocument();
        expect(screen.getByText('Vui lòng kiểm tra hộp thư email của bạn và làm theo hướng dẫn để đặt lại mật khẩu.')).toBeInTheDocument();
        expect(screen.getByTestId('resend-link')).toBeInTheDocument();
        expect(screen.getByTestId('back-to-login')).toBeInTheDocument();
      });
    });

    it('should allow resending email', async () => {
      mockForgotPassword.mockResolvedValue({ success: true, message: 'Email sent successfully' });
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      // First submission
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByTestId('forgot-password-success')).toBeInTheDocument();
      });
      
      // Click resend link
      const resendLink = screen.getByTestId('resend-link');
      fireEvent.click(resendLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('forgot-password-form')).toBeInTheDocument();
      });
    });
  });

  describe('Loading State', () => {
    it('should show loading state during submission', async () => {
      mockForgotPassword.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
      
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const emailInput = screen.getByTestId('email-input');
      const submitButton = screen.getByTestId('send-reset-link-button');
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.click(submitButton);
      
      expect(screen.getByText('Đang gửi...')).toBeInTheDocument();
      expect(submitButton).toBeDisabled();
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByLabelText('Email input')).toBeInTheDocument();
      expect(screen.getByLabelText('Send reset link button')).toBeInTheDocument();
    });

    it('should have proper form structure', () => {
      render(
        <TestWrapper>
          <ForgotPasswordForm {...defaultProps} />
        </TestWrapper>
      );
      
      const form = screen.getByTestId('forgot-password-form');
      expect(form.tagName).toBe('FORM');
    });
  });
}); 
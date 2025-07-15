import React from 'react';
import { render, screen } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AuthContainer from '../components/AuthContainer';

// Create a test theme
const theme = createTheme();

// Wrapper component for testing
const TestWrapper = ({ children }) => (
  <ThemeProvider theme={theme}>
    {children}
  </ThemeProvider>
);

describe('AuthContainer Component', () => {
  const defaultProps = {
    children: <div data-testid="test-children">Test Content</div>
  };

  describe('Rendering', () => {
    it('should render with default props', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('auth-container')).toBeInTheDocument();
      expect(screen.getByTestId('auth-title')).toBeInTheDocument();
      expect(screen.getByTestId('auth-content')).toBeInTheDocument();
      expect(screen.getByTestId('test-children')).toBeInTheDocument();
    });

    it('should render with custom title', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} title="Custom Title" />
        </TestWrapper>
      );
      
      expect(screen.getByText('Custom Title')).toBeInTheDocument();
    });

    it('should render with subtitle', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} subtitle="Custom Subtitle" />
        </TestWrapper>
      );
      
      expect(screen.getByText('Custom Subtitle')).toBeInTheDocument();
    });

    it('should render children correctly', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('test-children')).toBeInTheDocument();
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });
  });

  describe('Loading State', () => {
    it('should show loading spinner when loading is true', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} loading={true} />
        </TestWrapper>
      );
      
      // Check if loading overlay is present
      const container = screen.getByTestId('auth-container');
      expect(container).toBeInTheDocument();
    });

    it('should not show loading spinner when loading is false', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} loading={false} />
        </TestWrapper>
      );
      
      // Loading spinner should not be visible
      expect(screen.getByTestId('auth-content')).toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('should display error message when error is provided', () => {
      const errorMessage = 'Test error message';
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} error={errorMessage} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('auth-error')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    it('should not display error message when error is null', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} error={null} />
        </TestWrapper>
      );
      
      expect(screen.queryByTestId('auth-error')).not.toBeInTheDocument();
    });

    it('should not display error message when error is not provided', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.queryByTestId('auth-error')).not.toBeInTheDocument();
    });
  });

  describe('Title and Subtitle', () => {
    it('should render title when provided', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} title="Test Title" />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('auth-title')).toBeInTheDocument();
      expect(screen.getByText('Test Title')).toBeInTheDocument();
    });

    it('should render subtitle when provided', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} subtitle="Test Subtitle" />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('auth-subtitle')).toBeInTheDocument();
      expect(screen.getByText('Test Subtitle')).toBeInTheDocument();
    });

    it('should not render title section when title is not provided', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} title={null} />
        </TestWrapper>
      );
      
      expect(screen.queryByTestId('auth-title')).not.toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have proper test IDs for testing', () => {
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} />
        </TestWrapper>
      );
      
      expect(screen.getByTestId('auth-container')).toBeInTheDocument();
      expect(screen.getByTestId('auth-content')).toBeInTheDocument();
    });

    it('should have proper error announcement for screen readers', () => {
      const errorMessage = 'Test error message';
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} error={errorMessage} />
        </TestWrapper>
      );
      
      const errorAlert = screen.getByTestId('auth-error');
      expect(errorAlert).toHaveAttribute('role', 'alert');
    });
  });

  describe('Styling', () => {
    it('should apply custom className when provided', () => {
      const customClass = 'custom-auth-container';
      render(
        <TestWrapper>
          <AuthContainer {...defaultProps} className={customClass} />
        </TestWrapper>
      );
      
      const container = screen.getByTestId('auth-container');
      expect(container).toHaveClass(customClass);
    });
  });
}); 
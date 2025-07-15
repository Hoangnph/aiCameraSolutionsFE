import React, { useState, useEffect } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import { Box } from '@mui/material';
import AuthContainer from './components/AuthContainer';
import AuthTabs from './components/AuthTabs';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import ForgotPasswordForm from './components/ForgotPasswordForm';
import ResetPasswordForm from './components/ResetPasswordForm';
import { useAuth } from '../../context/AuthContext';

const AuthenticationScreen = () => {
  const history = useHistory();
  const location = useLocation();
  const { isAuthenticated, isLoading } = useAuth();
  
  // Get active tab from URL or default to login
  const getInitialTab = () => {
    const path = location.pathname;
    if (path.includes('/register')) return 'register';
    if (path.includes('/forgot-password')) return 'forgot';
    if (path.includes('/reset-password')) return 'reset';
    return 'login';
  };

  const [activeTab, setActiveTab] = useState(getInitialTab());
  const [error, setError] = useState(null);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      const redirectTo = location.search.includes('redirect=') 
        ? new URLSearchParams(location.search).get('redirect')
        : '/dashboard';
      history.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, history, location]);

  // Handle tab change
  const handleTabChange = (newTab) => {
    setActiveTab(newTab);
    setError(null); // Clear errors when switching tabs
    
    // Update URL
    const basePath = '/authentication';
    switch (newTab) {
      case 'register':
        history.push(`${basePath}/register`);
        break;
      case 'forgot':
        history.push(`${basePath}/forgot-password`);
        break;
      default:
        history.push(`${basePath}/login`);
    }
  };

  // Handle form success
  const handleFormSuccess = (data) => {
    setError(null);
    // Redirect will be handled by useEffect above
  };

  // Handle form error
  const handleFormError = (errorMessage) => {
    setError(errorMessage);
  };

  // Get title and subtitle based on active tab
  const getTabContent = () => {
    switch (activeTab) {
      case 'register':
        return {
          title: 'Tạo tài khoản mới',
          subtitle: 'Điền thông tin để đăng ký tài khoản'
        };
      case 'forgot':
        return {
          title: 'Quên mật khẩu',
          subtitle: 'Nhập email để nhận link đặt lại mật khẩu'
        };
      case 'reset':
        return {
          title: 'Đặt lại mật khẩu',
          subtitle: 'Nhập mật khẩu mới cho tài khoản của bạn'
        };
      default:
        return {
          title: 'Đăng nhập',
          subtitle: 'Chào mừng bạn quay trở lại'
        };
    }
  };

  const { title, subtitle } = getTabContent();

  // Render form based on active tab
  const renderForm = () => {
    switch (activeTab) {
      case 'register':
        return (
          <RegisterForm
            onSuccess={handleFormSuccess}
            onError={handleFormError}
          />
        );
      case 'forgot':
        return (
          <ForgotPasswordForm
            onSuccess={handleFormSuccess}
            onError={handleFormError}
          />
        );
      case 'reset':
        return (
          <ResetPasswordForm
            onSuccess={handleFormSuccess}
            onError={handleFormError}
          />
        );
      default:
        return (
          <LoginForm
            onSuccess={handleFormSuccess}
            onError={handleFormError}
          />
        );
    }
  };

  if (isLoading) {
    return (
      <AuthContainer
        title="Đang tải..."
        loading={true}
      />
    );
  }

  return (
    <AuthContainer
      title={title}
      subtitle={subtitle}
      error={error}
      data-testid="auth-container"
    >
      <AuthTabs
        activeTab={activeTab}
        onTabChange={handleTabChange}
      />
      
      <Box data-testid="auth-form-container">
        {renderForm()}
      </Box>
    </AuthContainer>
  );
};

export default AuthenticationScreen; 
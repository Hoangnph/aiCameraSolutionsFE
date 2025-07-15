import React from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import { AuthTabsProps } from '../types/auth.types';

// Styled Components
const StyledTabs = styled(Tabs)(({ theme }) => ({
  marginBottom: theme.spacing(3),
  '& .MuiTabs-indicator': {
    backgroundColor: theme.palette.primary.main,
    height: 3,
  },
  '& .MuiTab-root': {
    textTransform: 'none',
    fontWeight: 600,
    fontSize: '1rem',
    minWidth: 120,
    '&.Mui-selected': {
      color: theme.palette.primary.main,
    },
  },
}));

const StyledTab = styled(Tab)(({ theme }) => ({
  color: theme.palette.text.secondary,
  '&.Mui-selected': {
    color: theme.palette.primary.main,
  },
}));

const AuthTabs = ({
  activeTab,
  onTabChange,
  className,
}) => {
  const handleTabChange = (event, newValue) => {
    onTabChange(newValue);
  };

  return (
    <Box className={className} data-testid="auth-tabs">
      <StyledTabs
        value={activeTab}
        onChange={handleTabChange}
        variant="fullWidth"
        aria-label="authentication tabs"
      >
        <StyledTab
          label="Đăng nhập"
          value="login"
          data-testid="login-tab"
          aria-label="Login tab"
        />
        <StyledTab
          label="Đăng ký"
          value="register"
          data-testid="register-tab"
          aria-label="Register tab"
        />
        <StyledTab
          label="Quên mật khẩu"
          value="forgot"
          data-testid="forgot-tab"
          aria-label="Forgot password tab"
        />
      </StyledTabs>
    </Box>
  );
};

export default AuthTabs; 
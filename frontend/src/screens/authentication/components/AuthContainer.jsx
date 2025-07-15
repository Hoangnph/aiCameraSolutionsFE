import React from 'react';
import { Box, Container, Paper, CircularProgress, Alert } from '@mui/material';
import { styled } from '@mui/material/styles';

// Styled Components
const StyledContainer = styled(Container)(({ theme }) => ({
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(2),
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(1),
  },
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[10],
  maxWidth: 480,
  width: '100%',
  position: 'relative',
  overflow: 'hidden',
  background: 'rgba(255, 255, 255, 0.95)',
  backdropFilter: 'blur(10px)',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(3),
    margin: theme.spacing(1),
  },
}));

const LoadingOverlay = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: 'rgba(255, 255, 255, 0.8)',
  backdropFilter: 'blur(4px)',
  zIndex: 1,
}));

const AuthContainer = ({
  children,
  title = "Authentication",
  subtitle,
  loading = false,
  error = null,
  className,
}) => {
  return (
    <StyledContainer maxWidth={false} className={className} data-testid="auth-container">
      <StyledPaper elevation={3}>
        {loading && (
          <LoadingOverlay>
            <CircularProgress size={40} />
          </LoadingOverlay>
        )}
        
        {error && (
          <Alert 
            severity="error" 
            sx={{ mb: 2 }}
            data-testid="auth-error"
          >
            {error}
          </Alert>
        )}
        
        {title && (
          <Box textAlign="center" mb={3}>
            <h1 
              style={{ 
                margin: 0, 
                fontSize: '2rem', 
                fontWeight: 600,
                color: '#333',
                marginBottom: subtitle ? '0.5rem' : '2rem'
              }}
              data-testid="auth-title"
            >
              {title}
            </h1>
            {subtitle && (
              <p 
                style={{ 
                  margin: 0, 
                  fontSize: '1rem', 
                  color: '#666',
                  marginBottom: '2rem'
                }}
                data-testid="auth-subtitle"
              >
                {subtitle}
              </p>
            )}
          </Box>
        )}
        
        <Box data-testid="auth-content">
          {children}
        </Box>
      </StyledPaper>
    </StyledContainer>
  );
};

export default AuthContainer; 
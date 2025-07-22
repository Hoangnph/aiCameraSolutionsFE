import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const SimpleProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [shouldRender, setShouldRender] = useState(false);

  console.log('🔒 SimpleProtectedRoute v6:', {
    isAuthenticated,
    isLoading,
    pathname: location.pathname,
    shouldRender
  });

  useEffect(() => {
    const checkAuth = () => {
      // Check localStorage directly
      const token = localStorage.getItem('authToken');
      const user = localStorage.getItem('user');
      
      console.log('🔒 SimpleProtectedRoute v6 - Auth Check:', {
        hasToken: !!token,
        hasUser: !!user,
        contextAuth: isAuthenticated,
        isLoading
      });

      const isActuallyAuthenticated = !!token && !!user;
      const finalAuth = isAuthenticated || isActuallyAuthenticated;

      if (!isLoading) {
        if (finalAuth) {
          console.log('🔒 SimpleProtectedRoute v6: User authenticated, rendering content');
          setShouldRender(true);
        } else {
          console.log('🔒 SimpleProtectedRoute v6: User not authenticated, redirecting to login');
          // Use navigate for React Router v6
          navigate('/authentication/sign-in', { replace: true });
        }
      }
    };

    checkAuth();
  }, [isAuthenticated, isLoading, navigate]);

  if (isLoading) {
    console.log('🔒 SimpleProtectedRoute v6: Loading state');
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
        sx={{
          backgroundColor: '#0f1535',
          color: 'white'
        }}
      >
        <Typography variant="h4" sx={{ color: '#4318ff', marginBottom: 2 }}>
          Loading...
        </Typography>
        <Typography variant="body2" sx={{ color: '#a3aed0' }}>
          Please wait while we verify your authentication
        </Typography>
      </Box>
    );
  }

  if (!shouldRender) {
    console.log('🔒 SimpleProtectedRoute v6: Not rendering, waiting for auth check');
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
        sx={{
          backgroundColor: '#0f1535',
          color: 'white'
        }}
      >
        <Typography variant="h4" sx={{ color: '#4318ff', marginBottom: 2 }}>
          Checking Authentication...
        </Typography>
        <Typography variant="body2" sx={{ color: '#a3aed0' }}>
          Please wait while we verify your access
        </Typography>
      </Box>
    );
  }

  console.log('🔒 SimpleProtectedRoute v6: Rendering protected content');
  return <>{children}</>;
};

export default SimpleProtectedRoute; 
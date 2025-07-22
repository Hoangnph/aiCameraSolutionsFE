import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const ProtectedRouteV6 = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  const [authChecked, setAuthChecked] = useState(false);

  console.log('🔒 ProtectedRouteV6:', {
    isAuthenticated,
    isLoading,
    pathname: location.pathname,
    authChecked
  });

  useEffect(() => {
    if (!isLoading) {
      setAuthChecked(true);
    }
  }, [isLoading]);

  // Check localStorage directly for immediate authentication check
  const checkLocalStorage = () => {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    return !!token && !!user;
  };

  const isActuallyAuthenticated = checkLocalStorage();
  const finalAuth = isAuthenticated || isActuallyAuthenticated;

  console.log('🔒 ProtectedRouteV6 - Auth Check:', {
    contextAuth: isAuthenticated,
    localStorageAuth: isActuallyAuthenticated,
    finalAuth,
    isLoading,
    authChecked
  });

  if (isLoading || !authChecked) {
    console.log('🔒 ProtectedRouteV6: Loading state');
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

  if (!finalAuth) {
    console.log('🔒 ProtectedRouteV6: Not authenticated, redirecting to login');
    return (
      <Navigate
        to="/authentication/sign-in"
        state={{ from: location }}
        replace
      />
    );
  }

  console.log('🔒 ProtectedRouteV6: Authenticated, rendering content');
  return <>{children}</>;
};

export default ProtectedRouteV6; 
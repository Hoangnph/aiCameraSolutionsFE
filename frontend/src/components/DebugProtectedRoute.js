import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

const DebugProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();
  const [authChecked, setAuthChecked] = useState(false);
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const [debugInfo, setDebugInfo] = useState({});

  console.log('🔍 DebugProtectedRoute:', {
    isAuthenticated,
    isLoading,
    user: !!user,
    pathname: location.pathname,
    authChecked,
    shouldRedirect
  });

  useEffect(() => {
    const checkAuthentication = () => {
      // Check localStorage directly
      const token = localStorage.getItem('authToken');
      const userData = localStorage.getItem('user');
      
      const debugData = {
        hasToken: !!token,
        hasUser: !!userData,
        contextAuth: isAuthenticated,
        isLoading,
        token: token ? token.substring(0, 20) + '...' : null,
        userData: userData ? userData.substring(0, 50) + '...' : null
      };
      
      setDebugInfo(debugData);
      
      console.log('🔍 DebugProtectedRoute - Auth Check:', debugData);

      const isActuallyAuthenticated = !!token && !!userData;
      const finalAuth = isAuthenticated || isActuallyAuthenticated;

      if (!isLoading) {
        if (!finalAuth) {
          console.log('🔍 DebugProtectedRoute: Not authenticated, setting redirect flag');
          setShouldRedirect(true);
        } else {
          console.log('🔍 DebugProtectedRoute: Authenticated, allowing access');
          setShouldRedirect(false);
        }
        setAuthChecked(true);
      }
    };

    checkAuthentication();
  }, [isAuthenticated, isLoading]);

  const forceRedirect = () => {
    console.log('🔍 DebugProtectedRoute: Force redirect to login');
    window.location.href = '/authentication/sign-in';
  };

  // Show loading while checking authentication
  if (isLoading || !authChecked) {
    console.log('🔍 DebugProtectedRoute: Loading state');
    return (
      <Box p={3}>
        <Typography variant="h4" gutterBottom>
          Debug Protected Route - Loading
        </Typography>
        <Typography variant="body1" gutterBottom>
          Checking authentication...
        </Typography>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
          {JSON.stringify(debugInfo, null, 2)}
        </pre>
      </Box>
    );
  }

  // Show debug info if not authenticated
  if (shouldRedirect) {
    console.log('🔍 DebugProtectedRoute: Should redirect, showing debug info');
    return (
      <Box p={3}>
        <Typography variant="h4" gutterBottom color="error">
          🔒 ACCESS DENIED - Debug Info
        </Typography>
        
        <Typography variant="h6" gutterBottom>
          Current Path: {location.pathname}
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          Is Authenticated (Context): {isAuthenticated ? '✅ YES' : '❌ NO'}
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          Is Loading: {isLoading ? '✅ YES' : '❌ NO'}
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          Has User: {user ? '✅ YES' : '❌ NO'}
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          Auth Checked: {authChecked ? '✅ YES' : '❌ NO'}
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          Should Redirect: {shouldRedirect ? '✅ YES' : '❌ NO'}
        </Typography>
        
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            Debug Info:
          </Typography>
          <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
            {JSON.stringify(debugInfo, null, 2)}
          </pre>
        </Box>
        
        <Box mt={3}>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => setShouldRedirect(false)}
            sx={{ mr: 2 }}
          >
            Force Allow Access
          </Button>
          
          <Button 
            variant="contained" 
            color="secondary"
            onClick={forceRedirect}
          >
            Force Redirect to Login
          </Button>
        </Box>
        
        <Box mt={3}>
          <Typography variant="body2" color="textSecondary">
            This page should redirect to login. If you see this, there's an issue with the redirect logic.
          </Typography>
        </Box>
      </Box>
    );
  }

  // Render protected content
  console.log('🔍 DebugProtectedRoute: Rendering protected content');
  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom color="success.main">
        🔓 ACCESS GRANTED - Debug Info
      </Typography>
      
      <Typography variant="h6" gutterBottom>
        Current Path: {location.pathname}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Is Authenticated (Context): {isAuthenticated ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Is Loading: {isLoading ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Has User: {user ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Debug Info:
        </Typography>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
          {JSON.stringify(debugInfo, null, 2)}
        </pre>
      </Box>
      
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Protected Content:
        </Typography>
        {children}
      </Box>
    </Box>
  );
};

export default DebugProtectedRoute; 
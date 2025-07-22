import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

const TestAuth = () => {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  console.log('�� TestAuth Component v6:', {
    isAuthenticated,
    isLoading,
    user: !!user,
    pathname: location.pathname
  });

  const checkLocalStorage = () => {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    console.log('🧪 LocalStorage Check v6:', {
      hasToken: !!token,
      hasUser: !!user,
      token: token ? token.substring(0, 20) + '...' : null
    });
  };

  if (isLoading) {
    return (
      <Box p={3}>
        <Typography variant="h4">Loading Authentication...</Typography>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Authentication Test Page (React Router v6)
      </Typography>
      
      <Typography variant="h6" gutterBottom>
        Current Path: {location.pathname}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Is Authenticated: {isAuthenticated ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Is Loading: {isLoading ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Has User: {user ? '✅ YES' : '❌ NO'}
      </Typography>
      
      <Button 
        variant="contained" 
        onClick={checkLocalStorage}
        sx={{ mt: 2 }}
      >
        Check LocalStorage
      </Button>
      
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Debug Info:
        </Typography>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
          {JSON.stringify({
            isAuthenticated,
            isLoading,
            hasUser: !!user,
            pathname: location.pathname,
            reactRouterVersion: 'v6'
          }, null, 2)}
        </pre>
      </Box>
    </Box>
  );
};

export default TestAuth; 
import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
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

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuthenticated ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{
              pathname: '/authentication/sign-in',
              state: { from: props.location },
            }}
          />
        )
      }
    />
  );
};

export default ProtectedRoute; 
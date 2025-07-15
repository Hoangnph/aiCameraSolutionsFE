import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Icon from '@mui/material/Icon';

const LoadingSpinner = ({ message = "Loading..." }) => {
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
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        width="4rem"
        height="4rem"
        sx={{
          backgroundColor: '#4318ff',
          borderRadius: '50%',
          marginBottom: 2,
          animation: 'spin 1s linear infinite',
          '@keyframes spin': {
            '0%': {
              transform: 'rotate(0deg)',
            },
            '100%': {
              transform: 'rotate(360deg)',
            },
          },
        }}
      >
        <Icon fontSize="large" sx={{ color: 'white' }}>
          refresh
        </Icon>
      </Box>
      <Typography variant="h4" sx={{ color: '#4318ff', marginBottom: 1 }}>
        {message}
      </Typography>
      <Typography variant="body2" sx={{ color: '#a3aed0' }}>
        Please wait while we process your request
      </Typography>
    </Box>
  );
};

export default LoadingSpinner; 
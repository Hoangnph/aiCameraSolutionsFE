import React from 'react';
import { useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const DebugRoute = () => {
  const location = useLocation();

  console.log('🔍 DebugRoute Component:', {
    pathname: location.pathname,
    search: location.search,
    hash: location.hash,
    state: location.state
  });

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Debug Route Component
      </Typography>
      
      <Typography variant="h6" gutterBottom>
        Current Path: {location.pathname}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Search: {location.search}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        Hash: {location.hash}
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        State: {JSON.stringify(location.state)}
      </Typography>
      
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Component Info:
        </Typography>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
          {JSON.stringify({
            componentName: 'DebugRoute',
            pathname: location.pathname,
            timestamp: new Date().toISOString()
          }, null, 2)}
        </pre>
      </Box>
    </Box>
  );
};

export default DebugRoute; 
import React from 'react';
import { 
  Snackbar, 
  Alert, 
  AlertTitle,
  Box,
  Typography,
  Button
} from '@mui/material';
import { CheckCircle, Error, Info, Warning } from '@mui/icons-material';

const Notification = ({ 
  open, 
  message, 
  type = 'success', 
  title,
  onClose, 
  autoHideDuration = 6000,
  showAction = false,
  actionText = 'Đóng',
  onAction
}) => {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle />;
      case 'error':
        return <Error />;
      case 'warning':
        return <Warning />;
      case 'info':
        return <Info />;
      default:
        return <CheckCircle />;
    }
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    if (onClose) {
      onClose();
    }
  };

  const handleAction = () => {
    if (onAction) {
      onAction();
    }
    if (onClose) {
      onClose();
    }
  };

  return (
    <Snackbar
      open={open}
      autoHideDuration={autoHideDuration}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      sx={{
        '& .MuiSnackbarContent-root': {
          minWidth: 400,
          maxWidth: 600,
        }
      }}
    >
      <Alert
        onClose={handleClose}
        severity={type}
        icon={getIcon()}
        sx={{ 
          width: '100%',
          '& .MuiAlert-message': {
            width: '100%'
          }
        }}
        action={
          showAction ? (
            <Button 
              color="inherit" 
              size="small" 
              onClick={handleAction}
              sx={{ 
                color: 'inherit',
                textTransform: 'none',
                fontWeight: 600
              }}
            >
              {actionText}
            </Button>
          ) : null
        }
      >
        {title && (
          <AlertTitle sx={{ fontWeight: 600, mb: 0.5 }}>
            {title}
          </AlertTitle>
        )}
        <Typography variant="body2" component="div">
          {message}
        </Typography>
      </Alert>
    </Snackbar>
  );
};

export default Notification; 
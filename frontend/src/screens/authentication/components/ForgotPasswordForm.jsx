import React, { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Link,
  Alert
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { useAuth } from '../../../context/AuthContext';
import { validateEmail } from '../utils/validation';
import { createForgotPasswordData, handleAuthError } from '../utils/authHelpers';

// Styled Components
const StyledForm = styled('form')(({ theme }) => ({
  width: '100%',
}));

const StyledTextField = styled(TextField)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.spacing(1),
  },
}));

const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
  height: 48,
  borderRadius: theme.spacing(1),
  textTransform: 'none',
  fontSize: '1rem',
  fontWeight: 600,
}));

const ForgotPasswordForm = ({
  onSuccess,
  onError,
  className,
}) => {
  const { forgotPassword } = useAuth();
  
  // Form state
  const [formData, setFormData] = useState({
    email: ''
  });
  
  // UI state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Handle input changes
  const handleInputChange = (field) => (event) => {
    const value = event.target.value;
    
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  // Handle field blur (for validation)
  const handleFieldBlur = (field) => () => {
    setTouched(prev => ({
      ...prev,
      [field]: true
    }));

    // Validate field
    const value = formData[field];
    let error = '';

    if (field === 'email') {
      error = validateEmail(value);
    }

    if (error) {
      setErrors(prev => ({
        ...prev,
        [field]: error
      }));
    }
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    // Validate email
    const emailError = validateEmail(formData.email);
    if (emailError) {
      newErrors.email = emailError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Mark all fields as touched
    setTouched({
      email: true
    });

    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const forgotPasswordData = createForgotPasswordData(formData);
      const result = await forgotPassword(forgotPasswordData);
      
      if (result.success) {
        setIsSubmitted(true);
        if (onSuccess) {
          onSuccess(result.message);
        }
      } else {
        if (onError) {
          onError(result.error);
        }
      }
    } catch (error) {
      const errorMessage = handleAuthError(error);
      setErrors({ submit: errorMessage });
      
      if (onError) {
        onError(errorMessage);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Check if form is valid
  const isFormValid = () => {
    return formData.email.trim() !== '' && Object.keys(errors).length === 0;
  };

  // Success message
  if (isSubmitted) {
    return (
      <Box textAlign="center" data-testid="forgot-password-success">
        <Alert severity="success" sx={{ mb: 3 }}>
          Email đặt lại mật khẩu đã được gửi đến {formData.email}
        </Alert>
        
        <Typography variant="body1" color="textSecondary" mb={3}>
          Vui lòng kiểm tra hộp thư email của bạn và làm theo hướng dẫn để đặt lại mật khẩu.
        </Typography>
        
        <Typography variant="body2" color="textSecondary" mb={2}>
          Không nhận được email? Kiểm tra thư mục spam hoặc{' '}
          <Link
            component="button"
            onClick={() => setIsSubmitted(false)}
            sx={{ textDecoration: 'none', fontWeight: 600 }}
            data-testid="resend-link"
          >
            gửi lại
          </Link>
        </Typography>
        
        <Link
          href="/authentication/login"
          sx={{ textDecoration: 'none', fontWeight: 600 }}
          data-testid="back-to-login"
        >
          Quay lại đăng nhập
        </Link>
      </Box>
    );
  }

  return (
    <StyledForm onSubmit={handleSubmit} className={className} data-testid="forgot-password-form">
      {errors.submit && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="forgot-password-error">
          {errors.submit}
        </Alert>
      )}

      <Typography variant="body1" color="textSecondary" mb={3}>
        Nhập địa chỉ email của bạn và chúng tôi sẽ gửi link đặt lại mật khẩu.
      </Typography>

      <StyledTextField
        fullWidth
        label="Email"
        type="email"
        name="email"
        value={formData.email}
        onChange={handleInputChange('email')}
        onBlur={handleFieldBlur('email')}
        error={touched.email && !!errors.email}
        helperText={touched.email && errors.email}
        disabled={isSubmitting}
        inputProps={{
          'data-testid': 'email-input',
          'aria-label': 'Email input'
        }}
      />

      <StyledButton
        type="submit"
        fullWidth
        variant="contained"
        disabled={!isFormValid() || isSubmitting}
        data-testid="send-reset-link-button"
        aria-label="Send reset link button"
      >
        {isSubmitting ? 'Đang gửi...' : 'Gửi link đặt lại mật khẩu'}
      </StyledButton>

      <Box textAlign="center" mt={2}>
        <Typography variant="body2" color="textSecondary">
          Nhớ mật khẩu?{' '}
          <Link
            href="/authentication/login"
            sx={{ textDecoration: 'none', fontWeight: 600 }}
            data-testid="back-to-login-link"
          >
            Đăng nhập ngay
          </Link>
        </Typography>
      </Box>
    </StyledForm>
  );
};

export default ForgotPasswordForm; 
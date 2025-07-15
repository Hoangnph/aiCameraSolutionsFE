import React, { useState, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  FormControlLabel, 
  Checkbox, 
  Typography, 
  Link,
  InputAdornment,
  IconButton,
  Alert
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { useAuth } from '../../../context/AuthContext';
import { validateEmail, validateFieldRealTime } from '../utils/validation';
import { createLoginData, handleAuthError } from '../utils/authHelpers';

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

const LoginForm = ({
  onSuccess,
  onError,
  redirectTo = '/dashboard',
  className,
}) => {
  const { login } = useAuth();
  
  // Form state
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  });
  
  // UI state
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  // Handle input changes
  const handleInputChange = (field) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    
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

    if (field === 'username') {
      error = validateEmail(value);
    } else if (field === 'password') {
      error = validateFieldRealTime('password', value);
    }

    if (error) {
      setErrors(prev => ({
        ...prev,
        [field]: error
      }));
    }
  };

  // Toggle password visibility
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    // Validate username/email
    const usernameError = validateEmail(formData.username);
    if (usernameError) {
      newErrors.username = usernameError;
    }

    // Validate password
    const passwordError = validateFieldRealTime('password', formData.password);
    if (passwordError) {
      newErrors.password = passwordError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Mark all fields as touched
    setTouched({
      username: true,
      password: true
    });

    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const loginData = createLoginData(formData);
      const result = await login(loginData);
      
      if (result.success) {
        if (onSuccess) {
          onSuccess(result.user);
        }
        // Redirect will be handled by AuthContext
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
    return formData.username.trim() !== '' && 
           formData.password.trim() !== '' && 
           Object.keys(errors).length === 0;
  };

  return (
    <StyledForm onSubmit={handleSubmit} className={className} data-testid="login-form">
      {errors.submit && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="login-error">
          {errors.submit}
        </Alert>
      )}

      <StyledTextField
        fullWidth
        label="Email hoặc Username"
        type="text"
        name="username"
        value={formData.username}
        onChange={handleInputChange('username')}
        onBlur={handleFieldBlur('username')}
        error={touched.username && !!errors.username}
        helperText={touched.username && errors.username}
        disabled={isSubmitting}
        inputProps={{
          'data-testid': 'email-input',
          'aria-label': 'Email or username input'
        }}
      />

      <StyledTextField
        fullWidth
        label="Mật khẩu"
        type={showPassword ? 'text' : 'password'}
        name="password"
        value={formData.password}
        onChange={handleInputChange('password')}
        onBlur={handleFieldBlur('password')}
        error={touched.password && !!errors.password}
        helperText={touched.password && errors.password}
        disabled={isSubmitting}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={togglePasswordVisibility}
                edge="end"
                data-testid="password-toggle"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
        inputProps={{
          'data-testid': 'password-input',
          'aria-label': 'Password input'
        }}
      />

      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.rememberMe}
              onChange={handleInputChange('rememberMe')}
              disabled={isSubmitting}
              data-testid="remember-me"
            />
          }
          label="Ghi nhớ đăng nhập"
        />
        
        <Link
          href="/authentication/forgot-password"
          variant="body2"
          sx={{ textDecoration: 'none' }}
          data-testid="forgot-password-link"
        >
          Quên mật khẩu?
        </Link>
      </Box>

      <StyledButton
        type="submit"
        fullWidth
        variant="contained"
        disabled={!isFormValid() || isSubmitting}
        data-testid="login-button"
        aria-label="Sign in button"
      >
        {isSubmitting ? 'Đang đăng nhập...' : 'Đăng nhập'}
      </StyledButton>

      <Box textAlign="center" mt={2}>
        <Typography variant="body2" color="textSecondary">
          Chưa có tài khoản?{' '}
          <Link
            href="/authentication/register"
            sx={{ textDecoration: 'none', fontWeight: 600 }}
            data-testid="register-link"
          >
            Đăng ký ngay
          </Link>
        </Typography>
      </Box>
    </StyledForm>
  );
};

export default LoginForm; 
import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  FormControlLabel,
  Checkbox,
  Link,
  Alert,
  InputAdornment,
  IconButton,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Portal,
  Modal
} from '@mui/material';
import { Visibility, VisibilityOff, CheckCircle } from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { useAuth } from '../../../context/AuthContext';
import Notification from '../../../components/Notification';
import { 
  validateEmail, 
  validateUsername, 
  validateFieldRealTime,
  validatePasswordConfirmation,
  validateTermsAcceptance,
  calculatePasswordStrength
} from '../utils/validation';
import { createRegisterData, handleAuthError } from '../utils/authHelpers';

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

const PasswordStrengthBar = styled(Box)(({ theme, strength }) => ({
  marginTop: theme.spacing(1),
  marginBottom: theme.spacing(2),
}));

const RegisterForm = ({
  onSuccess,
  onError,
  redirectTo = '/dashboard',
  className,
}) => {
  const { register } = useAuth();
  const history = useHistory();
  
  // Form state
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    registrationCode: '',
    acceptTerms: false
  });
  
  // UI state
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, label: 'Weak', color: '#ff4444' });
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    type: 'success',
    title: ''
  });
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);

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

    // Update password strength
    if (field === 'password') {
      setPasswordStrength(calculatePasswordStrength(value));
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
    } else if (field === 'username') {
      error = validateUsername(value);
    } else if (field === 'password') {
      error = validateFieldRealTime('password', value);
    } else if (field === 'confirmPassword') {
      error = validatePasswordConfirmation(formData.password, value);
    } else if (field === 'firstName') {
      error = validateFieldRealTime('firstName', value);
    } else if (field === 'lastName') {
      error = validateFieldRealTime('lastName', value);
    } else if (field === 'registrationCode') {
      error = validateFieldRealTime('registrationCode', value);
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

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    // Validate all fields
    const fields = ['username', 'email', 'password', 'confirmPassword', 'registrationCode'];
    fields.forEach(field => {
      const value = formData[field];
      let error = '';

      if (field === 'email') {
        error = validateEmail(value);
      } else if (field === 'username') {
        error = validateUsername(value);
      } else if (field === 'password') {
        error = validateFieldRealTime('password', value);
      } else if (field === 'confirmPassword') {
        error = validatePasswordConfirmation(formData.password, value);
      } else if (field === 'registrationCode') {
        error = validateFieldRealTime('registrationCode', value);
      }

      if (error) {
        newErrors[field] = error;
      }
    });

    // Validate terms acceptance
    const termsError = validateTermsAcceptance(formData.acceptTerms);
    if (termsError) {
      newErrors.acceptTerms = termsError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('DEBUG: Form submitted');
    
    // Mark all fields as touched
    setTouched({
      username: true,
      email: true,
      password: true,
      confirmPassword: true,
      firstName: true,
      lastName: true,
      registrationCode: true,
      acceptTerms: true
    });

    // Validate form
    if (!validateForm()) {
      console.log('DEBUG: Form validation failed');
      return;
    }

    console.log('DEBUG: Form validation passed, starting registration');
    setIsSubmitting(true);

    try {
      const registerData = createRegisterData(formData);
      console.log('DEBUG: Calling register API');
      const result = await register(registerData);
      console.log('DEBUG: Register API response:', result);
      console.log('DEBUG: About to check result.success');
      
      if (result.success) {
        console.log('DEBUG: Registration successful, showing dialog');
        console.log('DEBUG: About to show alert');
        alert('Đăng ký thành công! Bạn đã đăng ký tài khoản thành công.');
        console.log('DEBUG: Alert shown, setting notification');
        setNotification({
          open: true,
          message: 'Đăng ký thành công! Bạn đã đăng ký tài khoản thành công.',
          type: 'success',
          title: 'Đăng ký thành công'
        });
        console.log('DEBUG: Notification set, setting dialog');
        setShowSuccessDialog(true);
        console.log('DEBUG: Dialog state set to true');
        
        // Gọi onSuccess callback
        // if (onSuccess) {
        //   console.log('DEBUG: Calling onSuccess callback');
        //   onSuccess(result);
        // }
      } else {
        console.log('DEBUG: Registration failed:', result.error);
        if (onError) {
          onError(result.error);
        }
      }
    } catch (error) {
      console.log('DEBUG: Registration error:', error);
      const errorMessage = handleAuthError(error);
      setErrors({ submit: errorMessage });
      
      if (onError) {
        onError(errorMessage);
      }
    } finally {
      setIsSubmitting(false);
      console.log('DEBUG: Form submission completed');
    }
  };

  // Check if form is valid
  const isFormValid = () => {
    return formData.username.trim() !== '' && 
           formData.email.trim() !== '' && 
           formData.password.trim() !== '' && 
           formData.confirmPassword.trim() !== '' && 
           formData.registrationCode.trim() !== '' &&
           formData.acceptTerms &&
           Object.keys(errors).length === 0;
  };

  // Handle success dialog close
  const handleSuccessDialogClose = () => {
    console.log('DEBUG: Dialog close button clicked');
    setShowSuccessDialog(false);
    
    // Delay redirect để đảm bảo dialog đóng hoàn toàn
    setTimeout(() => {
      history.push('/authentication/login');
    }, 100);
  };

  console.log('DEBUG: Current dialog state:', showSuccessDialog);
  console.log('DEBUG: Current notification state:', notification);

  return (
    <StyledForm onSubmit={handleSubmit} className={className} data-testid="register-form">
      {errors.submit && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="register-error">
          {errors.submit}
        </Alert>
      )}

      <Box display="flex" gap={2}>
        <StyledTextField
          fullWidth
          label="Họ"
          type="text"
          name="firstName"
          value={formData.firstName}
          onChange={handleInputChange('firstName')}
          onBlur={handleFieldBlur('firstName')}
          error={touched.firstName && !!errors.firstName}
          helperText={touched.firstName && errors.firstName}
          disabled={isSubmitting}
          inputProps={{
            'data-testid': 'first-name-input',
            'aria-label': 'First name input'
          }}
        />
        <StyledTextField
          fullWidth
          label="Tên"
          type="text"
          name="lastName"
          value={formData.lastName}
          onChange={handleInputChange('lastName')}
          onBlur={handleFieldBlur('lastName')}
          error={touched.lastName && !!errors.lastName}
          helperText={touched.lastName && errors.lastName}
          disabled={isSubmitting}
          inputProps={{
            'data-testid': 'last-name-input',
            'aria-label': 'Last name input'
          }}
        />
      </Box>

      <StyledTextField
        fullWidth
        label="Tên đăng nhập"
        type="text"
        name="username"
        value={formData.username}
        onChange={handleInputChange('username')}
        onBlur={handleFieldBlur('username')}
        error={touched.username && !!errors.username}
        helperText={touched.username && errors.username}
        disabled={isSubmitting}
        inputProps={{
          'data-testid': 'username-input',
          'aria-label': 'Username input'
        }}
      />

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

      {formData.password && (
        <PasswordStrengthBar>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
            <Typography variant="body2" color="textSecondary">
              Độ mạnh mật khẩu:
            </Typography>
            <Typography 
              variant="body2" 
              style={{ color: passwordStrength.color, fontWeight: 600 }}
            >
              {passwordStrength.label}
            </Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={(passwordStrength.score / 7) * 100}
            sx={{ 
              height: 8, 
              borderRadius: 4,
              backgroundColor: '#e0e0e0',
              '& .MuiLinearProgress-bar': {
                backgroundColor: passwordStrength.color
              }
            }}
          />
        </PasswordStrengthBar>
      )}

      <StyledTextField
        fullWidth
        label="Xác nhận mật khẩu"
        type={showConfirmPassword ? 'text' : 'password'}
        name="confirmPassword"
        value={formData.confirmPassword}
        onChange={handleInputChange('confirmPassword')}
        onBlur={handleFieldBlur('confirmPassword')}
        error={touched.confirmPassword && !!errors.confirmPassword}
        helperText={touched.confirmPassword && errors.confirmPassword}
        disabled={isSubmitting}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle confirm password visibility"
                onClick={toggleConfirmPasswordVisibility}
                edge="end"
                data-testid="confirm-password-toggle"
              >
                {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
        inputProps={{
          'data-testid': 'confirm-password-input',
          'aria-label': 'Confirm password input'
        }}
      />

      <StyledTextField
        fullWidth
        label="Mã đăng ký"
        type="text"
        name="registrationCode"
        value={formData.registrationCode}
        onChange={handleInputChange('registrationCode')}
        onBlur={handleFieldBlur('registrationCode')}
        error={touched.registrationCode && !!errors.registrationCode}
        helperText={touched.registrationCode && errors.registrationCode}
        disabled={isSubmitting}
        inputProps={{
          'data-testid': 'registration-code-input',
          'aria-label': 'Registration code input'
        }}
      />

      <Box mb={2}>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.acceptTerms}
              onChange={handleInputChange('acceptTerms')}
              disabled={isSubmitting}
              data-testid="accept-terms"
            />
          }
          label={
            <Typography variant="body2">
              Tôi đồng ý với{' '}
              <Link href="/terms" target="_blank" sx={{ textDecoration: 'none' }}>
                Điều khoản sử dụng
              </Link>
              {' '}và{' '}
              <Link href="/privacy" target="_blank" sx={{ textDecoration: 'none' }}>
                Chính sách bảo mật
              </Link>
            </Typography>
          }
        />
        {touched.acceptTerms && errors.acceptTerms && (
          <Typography variant="caption" color="error" display="block" mt={1} data-testid="terms-error">
            {errors.acceptTerms}
          </Typography>
        )}
      </Box>

      <StyledButton
        type="submit"
        fullWidth
        variant="contained"
        disabled={!isFormValid() || isSubmitting}
        data-testid="register-button"
        aria-label="Register button"
      >
        {isSubmitting ? 'Đang đăng ký...' : 'Đăng ký'}
      </StyledButton>

      <Box textAlign="center" mt={2}>
        <Typography variant="body2" color="textSecondary">
          Đã có tài khoản?{' '}
          <Link
            href="/authentication/login"
            sx={{ textDecoration: 'none', fontWeight: 600 }}
            data-testid="login-link"
          >
            Đăng nhập ngay
          </Link>
        </Typography>
      </Box>
      <Notification
        open={notification.open}
        message={notification.message}
        type={notification.type}
        title={notification.title}
        onClose={() => setNotification({ ...notification, open: false })}
      />
      
      {/* Success Dialog */}
      <Portal>
        <Modal
          open={showSuccessDialog}
          onClose={handleSuccessDialogClose}
          aria-labelledby="success-dialog-title"
          aria-describedby="success-dialog-description"
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 99999
          }}
        >
          <Box
            sx={{
              position: 'relative',
              bgcolor: 'background.paper',
              borderRadius: 4,
              boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
              p: 4,
              maxWidth: 400,
              width: '90%',
              outline: 'none'
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <CheckCircle sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" sx={{ fontWeight: 600 }}>
                Đăng ký thành công!
              </Typography>
            </Box>
            
            <Typography variant="body1" sx={{ textAlign: 'center', mb: 3 }}>
              Bạn đã đăng ký tài khoản thành công. Bây giờ bạn có thể đăng nhập vào hệ thống.
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <Button 
                onClick={handleSuccessDialogClose} 
                variant="contained" 
                color="primary"
                data-testid="success-dialog-login-button"
                sx={{
                  borderRadius: 99,
                  px: 4,
                  py: 1.2,
                  fontWeight: 600,
                  fontSize: 16,
                  background: 'linear-gradient(90deg,#5e72e4,#825ee4)',
                  color: '#fff',
                  boxShadow: '0 2px 8px rgba(94,114,228,0.12)',
                  '&:hover': {
                    background: 'linear-gradient(90deg,#825ee4,#5e72e4)'
                  }
                }}
              >
                Đăng nhập ngay
              </Button>
            </Box>
          </Box>
        </Modal>
      </Portal>
    </StyledForm>
  );
};

export default RegisterForm; 
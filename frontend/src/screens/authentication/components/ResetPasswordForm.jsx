import React, { useState } from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import { Box, TextField, Button, Typography, Alert, Link } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useAuth } from '../../../context/AuthContext';
import { validatePassword, validatePasswordConfirmation } from '../utils/validation';

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

const ResetPasswordForm = ({ onSuccess, onError, className }) => {
  const { resetPassword } = useAuth();
  const location = useLocation();
  const history = useHistory();

  // Lấy token từ URL
  const searchParams = new URLSearchParams(location.search);
  const token = searchParams.get('token') || '';

  // Form state
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: '',
  });

  // UI state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  // Handle input changes
  const handleInputChange = (field) => (event) => {
    const value = event.target.value;
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Handle field blur (for validation)
  const handleFieldBlur = (field) => () => {
    setTouched(prev => ({ ...prev, [field]: true }));
    let error = '';
    if (field === 'password') error = validatePassword(formData.password);
    if (field === 'confirmPassword') error = validatePasswordConfirmation(formData.password, formData.confirmPassword);
    if (error) setErrors(prev => ({ ...prev, [field]: error }));
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};
    const passwordError = validatePassword(formData.password);
    if (passwordError) newErrors.password = passwordError;
    const confirmError = validatePasswordConfirmation(formData.password, formData.confirmPassword);
    if (confirmError) newErrors.confirmPassword = confirmError;
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setTouched({ password: true, confirmPassword: true });
    if (!validateForm()) return;
    setIsSubmitting(true);
    try {
      const result = await resetPassword({ token, password: formData.password, confirmPassword: formData.confirmPassword });
      if (result.success) {
        setIsSubmitted(true);
        setSuccessMessage('Đặt lại mật khẩu thành công! Bạn có thể đăng nhập với mật khẩu mới.');
        if (onSuccess) onSuccess(result.message);
      } else {
        setErrors({ submit: result.error || 'Đặt lại mật khẩu thất bại.' });
        if (onError) onError(result.error);
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Đặt lại mật khẩu thất bại.' });
      if (onError) onError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!token) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.
      </Alert>
    );
  }

  if (isSubmitted) {
    return (
      <Box textAlign="center" data-testid="reset-password-success">
        <Alert severity="success" sx={{ mb: 3 }}>{successMessage}</Alert>
        <Button
          variant="contained"
          color="primary"
          onClick={() => history.push('/authentication/login')}
          sx={{ mt: 2 }}
        >
          Đăng nhập ngay
        </Button>
      </Box>
    );
  }

  return (
    <StyledForm onSubmit={handleSubmit} className={className} data-testid="reset-password-form">
      {errors.submit && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="reset-password-error">
          {errors.submit}
        </Alert>
      )}
      <Typography variant="body1" color="textSecondary" mb={3}>
        Nhập mật khẩu mới cho tài khoản của bạn.
      </Typography>
      <StyledTextField
        fullWidth
        label="Mật khẩu mới"
        type="password"
        name="password"
        value={formData.password}
        onChange={handleInputChange('password')}
        onBlur={handleFieldBlur('password')}
        error={touched.password && !!errors.password}
        helperText={touched.password && errors.password}
        disabled={isSubmitting}
        inputProps={{ 'data-testid': 'new-password-input', 'aria-label': 'New password input' }}
      />
      <StyledTextField
        fullWidth
        label="Nhập lại mật khẩu mới"
        type="password"
        name="confirmPassword"
        value={formData.confirmPassword}
        onChange={handleInputChange('confirmPassword')}
        onBlur={handleFieldBlur('confirmPassword')}
        error={touched.confirmPassword && !!errors.confirmPassword}
        helperText={touched.confirmPassword && errors.confirmPassword}
        disabled={isSubmitting}
        inputProps={{ 'data-testid': 'confirm-password-input', 'aria-label': 'Confirm new password input' }}
      />
      <StyledButton
        type="submit"
        fullWidth
        variant="contained"
        disabled={!formData.password || !formData.confirmPassword || isSubmitting || Object.keys(errors).length > 0}
        data-testid="reset-password-button"
        aria-label="Reset password button"
      >
        {isSubmitting ? 'Đang đặt lại...' : 'Đặt lại mật khẩu'}
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

export default ResetPasswordForm; 
import { ValidationSchema, ValidationRule, PasswordStrength } from '../types/auth.types';

// Validation Rules
export const validationSchema: ValidationSchema = {
  username: {
    required: true,
    minLength: 3,
    maxLength: 30,
    pattern: /^[a-zA-Z0-9]+$/,
    message: 'Username must be 3-30 characters, alphanumeric only'
  },
  email: {
    required: true,
    pattern: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    maxLength: 254,
    message: 'Please enter a valid email address'
  },
  password: {
    required: true,
    minLength: 8,
    maxLength: 128,
    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
    message: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
  },
  confirmPassword: {
    required: true,
    message: 'Please confirm your password'
  },
  firstName: {
    required: false,
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s\-']+$/,
    message: 'First name must be 2-50 characters, letters only'
  },
  lastName: {
    required: false,
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s\-']+$/,
    message: 'Last name must be 2-50 characters, letters only'
  },
  registrationCode: {
    required: true,
    message: 'Registration code is required'
  }
};

// Validation Functions
export const validateField = (value: any, rule: ValidationRule): string | null => {
  // Required validation
  if (rule.required && (!value || value.trim() === '')) {
    return rule.message || 'This field is required';
  }

  // Skip other validations if value is empty and not required
  if (!value || value.trim() === '') {
    return null;
  }

  // Min length validation
  if (rule.minLength && value.length < rule.minLength) {
    return rule.message || `Minimum length is ${rule.minLength} characters`;
  }

  // Max length validation
  if (rule.maxLength && value.length > rule.maxLength) {
    return rule.message || `Maximum length is ${rule.maxLength} characters`;
  }

  // Pattern validation
  if (rule.pattern && !rule.pattern.test(value)) {
    return rule.message || 'Invalid format';
  }

  // Custom validation
  if (rule.custom) {
    const result = rule.custom(value);
    if (typeof result === 'string') {
      return result;
    }
    if (!result) {
      return rule.message || 'Invalid value';
    }
  }

  return null;
};

export const validateForm = (data: Record<string, any>, schema: ValidationSchema): Record<string, string> => {
  const errors: Record<string, string> = {};

  Object.keys(schema).forEach(field => {
    const rule = schema[field];
    const value = data[field];
    const error = validateField(value, rule);
    
    if (error) {
      errors[field] = error;
    }
  });

  return errors;
};

// Password Strength Calculator
export const calculatePasswordStrength = (password: string): PasswordStrength => {
  if (!password) {
    return { score: 0, label: 'Weak', color: '#ff4444' };
  }

  let score = 0;
  const checks = {
    length: password.length >= 8,
    lowercase: /[a-z]/.test(password),
    uppercase: /[A-Z]/.test(password),
    numbers: /\d/.test(password),
    special: /[@$!%*?&]/.test(password)
  };

  // Base score for length
  if (checks.length) score += 1;
  if (checks.lowercase) score += 1;
  if (checks.uppercase) score += 1;
  if (checks.numbers) score += 1;
  if (checks.special) score += 1;

  // Bonus for longer passwords
  if (password.length >= 12) score += 1;
  if (password.length >= 16) score += 1;

  // Determine strength level
  if (score <= 2) {
    return { score, label: 'Weak', color: '#ff4444' };
  } else if (score <= 4) {
    return { score, label: 'Fair', color: '#ffaa00' };
  } else if (score <= 6) {
    return { score, label: 'Good', color: '#00aa00' };
  } else {
    return { score, label: 'Strong', color: '#008800' };
  }
};

// Password Confirmation Validation
export const validatePasswordConfirmation = (password: string, confirmPassword: string): string | null => {
  if (!confirmPassword) {
    return 'Please confirm your password';
  }
  
  if (password !== confirmPassword) {
    return 'Passwords do not match';
  }
  
  return null;
};

// Email Validation
export const validateEmail = (email: string): string | null => {
  if (!email) {
    return 'Email is required';
  }

  const emailPattern = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
  if (!emailPattern.test(email)) {
    return 'Please enter a valid email address';
  }

  if (email.length > 254) {
    return 'Email must be less than 254 characters';
  }

  return null;
};

// Username Validation
export const validateUsername = (username: string): string | null => {
  if (!username) {
    return 'Username is required';
  }

  if (username.length < 3) {
    return 'Username must be at least 3 characters';
  }

  if (username.length > 30) {
    return 'Username must be less than 30 characters';
  }

  const usernamePattern = /^[a-zA-Z0-9]+$/;
  if (!usernamePattern.test(username)) {
    return 'Username must contain only letters and numbers';
  }

  return null;
};

// Name Validation
export const validateName = (name: string, fieldName: string): string | null => {
  if (!name) {
    return null; // Names are optional
  }

  if (name.length < 2) {
    return `${fieldName} must be at least 2 characters`;
  }

  if (name.length > 50) {
    return `${fieldName} must be less than 50 characters`;
  }

  const namePattern = /^[a-zA-Z\s\-']+$/;
  if (!namePattern.test(name)) {
    return `${fieldName} can only contain letters, spaces, hyphens, and apostrophes`;
  }

  return null;
};

// Registration Code Validation
export const validateRegistrationCode = (code: string): string | null => {
  if (!code) {
    return 'Registration code is required';
  }

  if (code.trim() === '') {
    return 'Registration code cannot be empty';
  }

  return null;
};

// Terms Acceptance Validation
export const validateTermsAcceptance = (accepted: boolean): string | null => {
  if (!accepted) {
    return 'You must accept the terms and conditions';
  }

  return null;
};

// Real-time Validation Helpers
export const validateFieldRealTime = (field: string, value: any): string | null => {
  const rule = validationSchema[field];
  if (!rule) {
    return null;
  }

  return validateField(value, rule);
};

// Form State Validation
export const isFormValid = (data: Record<string, any>, errors: Record<string, string>): boolean => {
  // Check if there are any errors
  if (Object.keys(errors).length > 0) {
    return false;
  }

  // Check if all required fields are filled
  const requiredFields = Object.keys(validationSchema).filter(field => 
    validationSchema[field].required
  );

  for (const field of requiredFields) {
    if (!data[field] || data[field].trim() === '') {
      return false;
    }
  }

  return true;
};

// Error Message Helpers
export const getErrorMessage = (error: any): string => {
  if (typeof error === 'string') {
    return error;
  }

  if (error?.message) {
    return error.message;
  }

  if (error?.error?.message) {
    return error.error.message;
  }

  return 'An unexpected error occurred';
};

// API Error Mapping
export const mapAPIError = (error: any): string => {
  if (error?.status === 401) {
    return 'Invalid email or password';
  }

  if (error?.status === 429) {
    return 'Too many requests. Please wait a moment and try again';
  }

  if (error?.status === 500) {
    return 'Server error. Please try again later';
  }

  if (error?.message?.includes('Network')) {
    return 'Network error. Please check your connection and try again';
  }

  return getErrorMessage(error);
};

// Validation Messages
export const validationMessages = {
  INVALID_EMAIL: 'Please enter a valid email address',
  WEAK_PASSWORD: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character',
  PASSWORDS_DONT_MATCH: 'Passwords do not match',
  EMAIL_ALREADY_EXISTS: 'An account with this email already exists',
  USERNAME_ALREADY_EXISTS: 'Username is already taken',
  INVALID_CREDENTIALS: 'Invalid email or password',
  ACCOUNT_LOCKED: 'Account temporarily locked due to multiple failed attempts',
  NETWORK_ERROR: 'Network error. Please check your connection and try again',
  SERVER_ERROR: 'Server error. Please try again later',
  RATE_LIMIT: 'Too many requests. Please wait a moment and try again',
  INVALID_REGISTRATION_CODE: 'Invalid registration code',
  REGISTRATION_CODE_EXPIRED: 'Registration code has expired',
  REGISTRATION_CODE_LIMIT: 'Registration code has reached usage limit',
  TERMS_NOT_ACCEPTED: 'You must accept the terms and conditions'
}; 
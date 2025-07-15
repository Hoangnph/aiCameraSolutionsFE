// Authentication Types
export interface User {
  id: string;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  role: 'admin' | 'user' | 'viewer';
  isActive: boolean;
  lastLogin?: string;
  createdAt: string;
  updatedAt: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  firstName?: string;
  lastName?: string;
  registrationCode: string;
  acceptTerms: boolean;
}

export interface ForgotPasswordData {
  email: string;
}

export interface ResetPasswordData {
  token: string;
  password: string;
  confirmPassword: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  data?: {
    user: User;
    accessToken: string;
    refreshToken: string;
  };
  error?: {
    code: number;
    message: string;
  };
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  accessToken: string | null;
  refreshToken: string | null;
}

export interface FormValidationError {
  field: string;
  message: string;
}

export interface PasswordStrength {
  score: number;
  label: 'Weak' | 'Fair' | 'Good' | 'Strong';
  color: string;
}

export interface AuthFormState {
  data: Record<string, any>;
  errors: Record<string, string>;
  isValid: boolean;
  isSubmitting: boolean;
  isSubmitted: boolean;
}

// Component Props
export interface AuthContainerProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  loading?: boolean;
  error?: string | null;
  className?: string;
}

export interface AuthTabsProps {
  activeTab: 'login' | 'register' | 'forgot';
  onTabChange: (tab: 'login' | 'register' | 'forgot') => void;
  className?: string;
}

export interface LoginFormProps {
  onSuccess?: (user: User) => void;
  onError?: (error: string) => void;
  redirectTo?: string;
  className?: string;
}

export interface RegisterFormProps {
  onSuccess?: (user: User) => void;
  onError?: (error: string) => void;
  redirectTo?: string;
  className?: string;
}

export interface ForgotPasswordFormProps {
  onSuccess?: (message: string) => void;
  onError?: (error: string) => void;
  className?: string;
}

export interface SocialLoginButtonsProps {
  onSuccess?: (user: User) => void;
  onError?: (error: string) => void;
  className?: string;
}

export interface AuthHeaderProps {
  title?: string;
  subtitle?: string;
  className?: string;
}

export interface AuthFooterProps {
  className?: string;
}

// Validation Types
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean | string;
  message?: string;
}

export interface ValidationSchema {
  [field: string]: ValidationRule;
}

// API Error Types
export interface APIError {
  status: number;
  code: string;
  message: string;
  details?: any;
}

// Test Types
export interface TestUser {
  email: string;
  password: string;
  username: string;
  role: string;
}

export interface TestScenario {
  name: string;
  input: Record<string, any>;
  expectedResult: 'success' | 'error';
  expectedError?: string;
} 
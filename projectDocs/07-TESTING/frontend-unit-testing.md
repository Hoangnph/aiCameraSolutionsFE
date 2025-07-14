# Frontend Unit Testing Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn unit testing cho frontend components, services, và utilities trong hệ thống AI Camera Counting, sử dụng Jest và React Testing Library.

### 🎯 Mục tiêu
- Đảm bảo code quality và reliability
- Tăng tốc độ development và debugging
- Giảm thiểu regression bugs
- Cải thiện code maintainability

### 🛠️ Testing Framework Setup

#### Jest Configuration
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/src/__mocks__/fileMock.js',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/serviceWorker.js',
    '!src/reportWebVitals.js',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{test,spec}.{js,jsx,ts,tsx}',
  ],
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|@react-navigation)/)',
  ],
};
```

#### React Testing Library Setup
```javascript
// src/setupTests.js
import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';

// Configure testing library
configure({
  testIdAttribute: 'data-testid',
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() {
    return null;
  }
  disconnect() {
    return null;
  }
  unobserve() {
    return null;
  }
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  observe() {
    return null;
  }
  disconnect() {
    return null;
  }
  unobserve() {
    return null;
  }
};

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});
```

### 🧪 Component Testing

#### Basic Component Test
```typescript
// src/components/CameraCard/__tests__/CameraCard.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import CameraCard from '../CameraCard';

const mockCamera = {
  id: '1',
  name: 'Main Camera',
  location: 'Building A',
  status: 'active',
  ip_address: '192.168.1.100',
  current_count: 25,
  confidence: 0.95,
};

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('CameraCard Component', () => {
  test('renders camera information correctly', () => {
    renderWithRouter(<CameraCard camera={mockCamera} />);
    
    expect(screen.getByText('Main Camera')).toBeInTheDocument();
    expect(screen.getByText('Building A')).toBeInTheDocument();
    expect(screen.getByText('192.168.1.100')).toBeInTheDocument();
    expect(screen.getByText('25')).toBeInTheDocument();
  });

  test('displays correct status indicator', () => {
    renderWithRouter(<CameraCard camera={mockCamera} />);
    
    const statusIndicator = screen.getByTestId('status-indicator');
    expect(statusIndicator).toHaveClass('status-active');
  });

  test('handles click events', () => {
    const mockOnClick = jest.fn();
    renderWithRouter(
      <CameraCard camera={mockCamera} onClick={mockOnClick} />
    );
    
    const card = screen.getByTestId('camera-card');
    fireEvent.click(card);
    
    expect(mockOnClick).toHaveBeenCalledWith(mockCamera.id);
  });

  test('displays confidence score correctly', () => {
    renderWithRouter(<CameraCard camera={mockCamera} />);
    
    const confidenceElement = screen.getByTestId('confidence-score');
    expect(confidenceElement).toHaveTextContent('95%');
  });
});
```

#### Form Component Testing
```typescript
// src/components/LoginForm/__tests__/LoginForm.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from '../LoginForm';

const mockOnSubmit = jest.fn();

describe('LoginForm Component', () => {
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  test('renders login form fields', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('validates required fields', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('validates email format', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid data', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  test('shows loading state during submission', async () => {
    const mockAsyncSubmit = jest.fn().mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 100))
    );
    
    render(<LoginForm onSubmit={mockAsyncSubmit} />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);
    
    expect(screen.getByText(/signing in/i)).toBeInTheDocument();
    expect(submitButton).toBeDisabled();
  });
});
```

### 🔧 Hook Testing

#### Custom Hook Testing
```typescript
// src/hooks/__tests__/useCameraData.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCameraData } from '../useCameraData';
import { cameraAPI } from '@/services/cameraAPI';

// Mock the API
jest.mock('@/services/cameraAPI');
const mockCameraAPI = cameraAPI as jest.Mocked<typeof cameraAPI>;

describe('useCameraData Hook', () => {
  beforeEach(() => {
    mockCameraAPI.getCameras.mockClear();
    mockCameraAPI.getCameraCounts.mockClear();
  });

  test('fetches camera data on mount', async () => {
    const mockCameras = [
      { id: '1', name: 'Camera 1', status: 'active' },
      { id: '2', name: 'Camera 2', status: 'inactive' },
    ];
    
    mockCameraAPI.getCameras.mockResolvedValue(mockCameras);
    
    const { result } = renderHook(() => useCameraData());
    
    expect(result.current.loading).toBe(true);
    expect(result.current.error).toBe(null);
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });
    
    expect(result.current.cameras).toEqual(mockCameras);
    expect(result.current.loading).toBe(false);
    expect(mockCameraAPI.getCameras).toHaveBeenCalledTimes(1);
  });

  test('handles API errors', async () => {
    const error = new Error('Failed to fetch cameras');
    mockCameraAPI.getCameras.mockRejectedValue(error);
    
    const { result } = renderHook(() => useCameraData());
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });
    
    expect(result.current.error).toBe(error);
    expect(result.current.loading).toBe(false);
    expect(result.current.cameras).toEqual([]);
  });

  test('refreshes data when refresh function is called', async () => {
    const mockCameras = [{ id: '1', name: 'Camera 1', status: 'active' }];
    mockCameraAPI.getCameras.mockResolvedValue(mockCameras);
    
    const { result } = renderHook(() => useCameraData());
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });
    
    // Change mock data for refresh
    const updatedCameras = [{ id: '1', name: 'Camera 1 Updated', status: 'active' }];
    mockCameraAPI.getCameras.mockResolvedValue(updatedCameras);
    
    await act(async () => {
      await result.current.refresh();
    });
    
    expect(result.current.cameras).toEqual(updatedCameras);
    expect(mockCameraAPI.getCameras).toHaveBeenCalledTimes(2);
  });
});
```

### 🧪 Service Testing

#### API Service Testing
```typescript
// src/services/__tests__/cameraAPI.test.ts
import { cameraAPI } from '../cameraAPI';

// Mock fetch
global.fetch = jest.fn();

describe('CameraAPI Service', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  test('fetches cameras successfully', async () => {
    const mockCameras = [
      { id: '1', name: 'Camera 1', status: 'active' },
      { id: '2', name: 'Camera 2', status: 'inactive' },
    ];
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockCameras,
    });
    
    const result = await cameraAPI.getCameras();
    
    expect(result).toEqual(mockCameras);
    expect(fetch).toHaveBeenCalledWith('/api/cameras', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token',
      },
    });
  });

  test('handles API errors', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    });
    
    await expect(cameraAPI.getCameras()).rejects.toThrow('Internal Server Error');
  });

  test('creates camera successfully', async () => {
    const newCamera = {
      name: 'New Camera',
      location: 'Building B',
      ip_address: '192.168.1.101',
    };
    
    const createdCamera = { id: '3', ...newCamera, status: 'active' };
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => createdCamera,
    });
    
    const result = await cameraAPI.createCamera(newCamera);
    
    expect(result).toEqual(createdCamera);
    expect(fetch).toHaveBeenCalledWith('/api/cameras', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token',
      },
      body: JSON.stringify(newCamera),
    });
  });

  test('updates camera successfully', async () => {
    const cameraId = '1';
    const updates = { name: 'Updated Camera' };
    
    const updatedCamera = { id: cameraId, name: 'Updated Camera', status: 'active' };
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => updatedCamera,
    });
    
    const result = await cameraAPI.updateCamera(cameraId, updates);
    
    expect(result).toEqual(updatedCamera);
    expect(fetch).toHaveBeenCalledWith(`/api/cameras/${cameraId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token',
      },
      body: JSON.stringify(updates),
    });
  });

  test('deletes camera successfully', async () => {
    const cameraId = '1';
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true }),
    });
    
    await cameraAPI.deleteCamera(cameraId);
    
    expect(fetch).toHaveBeenCalledWith(`/api/cameras/${cameraId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token',
      },
    });
  });
});
```

### 🧪 Utility Testing

#### Utility Function Testing
```typescript
// src/utils/__tests__/formatters.test.ts
import { formatCount, formatConfidence, formatTimestamp } from '../formatters';

describe('Formatters Utility', () => {
  describe('formatCount', () => {
    test('formats positive numbers correctly', () => {
      expect(formatCount(1234)).toBe('1,234');
      expect(formatCount(0)).toBe('0');
      expect(formatCount(999999)).toBe('999,999');
    });

    test('handles negative numbers', () => {
      expect(formatCount(-1234)).toBe('-1,234');
    });

    test('handles decimal numbers', () => {
      expect(formatCount(1234.56)).toBe('1,234.56');
    });

    test('handles null and undefined', () => {
      expect(formatCount(null)).toBe('0');
      expect(formatCount(undefined)).toBe('0');
    });
  });

  describe('formatConfidence', () => {
    test('formats confidence as percentage', () => {
      expect(formatConfidence(0.95)).toBe('95%');
      expect(formatConfidence(0.5)).toBe('50%');
      expect(formatConfidence(1.0)).toBe('100%');
    });

    test('handles edge cases', () => {
      expect(formatConfidence(0)).toBe('0%');
      expect(formatConfidence(1)).toBe('100%');
      expect(formatConfidence(0.123)).toBe('12%');
    });
  });

  describe('formatTimestamp', () => {
    test('formats date correctly', () => {
      const date = new Date('2024-01-15T10:30:00Z');
      expect(formatTimestamp(date)).toBe('Jan 15, 2024 10:30 AM');
    });

    test('handles different date formats', () => {
      const date1 = new Date('2024-12-25T23:59:59Z');
      expect(formatTimestamp(date1)).toBe('Dec 25, 2024 11:59 PM');
    });

    test('handles invalid dates', () => {
      expect(formatTimestamp('invalid-date')).toBe('Invalid Date');
    });
  });
});
```

### 🧪 Context Testing

#### Context Provider Testing
```typescript
// src/context/__tests__/AuthContext.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';

const TestComponent = () => {
  const { user, login, logout, loading } = useAuth();
  
  return (
    <div>
      {loading ? (
        <div data-testid="loading">Loading...</div>
      ) : user ? (
        <div>
          <span data-testid="user-name">{user.name}</span>
          <button data-testid="logout-btn" onClick={logout}>
            Logout
          </button>
        </div>
      ) : (
        <button data-testid="login-btn" onClick={() => login('test@example.com', 'password')}>
          Login
        </button>
      )}
    </div>
  );
};

describe('AuthContext', () => {
  test('provides initial state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    expect(screen.getByTestId('login-btn')).toBeInTheDocument();
    expect(screen.queryByTestId('user-name')).not.toBeInTheDocument();
  });

  test('handles login successfully', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    const loginButton = screen.getByTestId('login-btn');
    fireEvent.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('user-name')).toBeInTheDocument();
      expect(screen.getByTestId('logout-btn')).toBeInTheDocument();
    });
  });

  test('handles logout', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Login first
    const loginButton = screen.getByTestId('login-btn');
    fireEvent.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('user-name')).toBeInTheDocument();
    });
    
    // Then logout
    const logoutButton = screen.getByTestId('logout-btn');
    fireEvent.click(logoutButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('login-btn')).toBeInTheDocument();
      expect(screen.queryByTestId('user-name')).not.toBeInTheDocument();
    });
  });
});
```

### 📊 Test Coverage

#### Coverage Configuration
```javascript
// jest.config.js - Coverage settings
module.exports = {
  // ... other config
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/serviceWorker.js',
    '!src/reportWebVitals.js',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/*.test.{js,jsx,ts,tsx}',
    '!src/**/*.spec.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/components/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    './src/hooks/': {
      branches: 85,
      functions: 85,
      lines: 85,
      statements: 85,
    },
    './src/services/': {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  coverageReporters: ['text', 'lcov', 'html'],
  coverageDirectory: 'coverage',
};
```

### 🚀 Performance Testing

#### Component Performance Testing
```typescript
// src/components/__tests__/CameraList.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { CameraList } from '../CameraList';

const mockCameras = Array.from({ length: 100 }, (_, i) => ({
  id: `${i + 1}`,
  name: `Camera ${i + 1}`,
  status: i % 2 === 0 ? 'active' : 'inactive',
  location: `Building ${String.fromCharCode(65 + (i % 26))}`,
  current_count: Math.floor(Math.random() * 100),
}));

describe('CameraList Performance', () => {
  test('renders large list efficiently', () => {
    const startTime = performance.now();
    
    render(<CameraList cameras={mockCameras} />);
    
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    
    // Should render 100 cameras in less than 100ms
    expect(renderTime).toBeLessThan(100);
    
    // Should render all cameras
    expect(screen.getAllByTestId('camera-card')).toHaveLength(100);
  });

  test('handles frequent updates efficiently', () => {
    const { rerender } = render(<CameraList cameras={mockCameras} />);
    
    const updateTimes = [];
    
    for (let i = 0; i < 10; i++) {
      const startTime = performance.now();
      
      const updatedCameras = mockCameras.map(camera => ({
        ...camera,
        current_count: camera.current_count + i,
      }));
      
      rerender(<CameraList cameras={updatedCameras} />);
      
      const endTime = performance.now();
      updateTimes.push(endTime - startTime);
    }
    
    const averageUpdateTime = updateTimes.reduce((a, b) => a + b, 0) / updateTimes.length;
    
    // Average update time should be less than 50ms
    expect(averageUpdateTime).toBeLessThan(50);
  });
});
```

### 📋 Testing Best Practices

#### Test Organization
```typescript
// Recommended test file structure
describe('ComponentName', () => {
  // Setup
  beforeEach(() => {
    // Common setup
  });

  afterEach(() => {
    // Cleanup
  });

  // Happy path tests
  describe('when rendering successfully', () => {
    test('displays correct content', () => {
      // Test implementation
    });
  });

  // Error handling tests
  describe('when errors occur', () => {
    test('displays error message', () => {
      // Test implementation
    });
  });

  // Edge cases
  describe('edge cases', () => {
    test('handles empty data', () => {
      // Test implementation
    });
  });

  // User interactions
  describe('user interactions', () => {
    test('responds to user input', () => {
      // Test implementation
    });
  });
});
```

#### Test Naming Conventions
```typescript
// Good test names
test('should display user name when user is logged in', () => {});
test('should show loading spinner while fetching data', () => {});
test('should call onSubmit with form data when form is submitted', () => {});
test('should disable submit button when form is invalid', () => {});
test('should display error message when API call fails', () => {});

// Avoid these test names
test('renders correctly', () => {}); // Too vague
test('works', () => {}); // Too vague
test('test1', () => {}); // Not descriptive
```

### 🚨 Common Testing Pitfalls

#### Anti-patterns to Avoid
```typescript
// ❌ Don't test implementation details
test('should call setState', () => {
  const setState = jest.fn();
  // Testing internal implementation
});

// ✅ Do test behavior
test('should update display when data changes', () => {
  // Testing observable behavior
});

// ❌ Don't test third-party libraries
test('should use React Router', () => {
  // Testing library functionality
});

// ✅ Do test integration with libraries
test('should navigate to camera detail page when camera is clicked', () => {
  // Testing your component's behavior with the library
});

// ❌ Don't test everything
test('should have exactly 3 div elements', () => {
  // Testing implementation details
});

// ✅ Do test important behavior
test('should display camera information', () => {
  // Testing user-visible behavior
});
```

### 📊 Test Metrics

#### Quality Metrics
- **Test Coverage**: > 80% for critical components
- **Test Reliability**: > 95% pass rate
- **Test Speed**: < 30 seconds for full suite
- **Test Maintainability**: < 10% test code changes per feature

#### Performance Metrics
- **Component Render Time**: < 100ms for complex components
- **Test Execution Time**: < 5 seconds per test file
- **Memory Usage**: < 100MB for test suite
- **Bundle Size Impact**: < 5% increase from test utilities

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
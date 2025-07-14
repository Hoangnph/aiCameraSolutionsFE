# End-to-End Testing Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn E2E testing cho hệ thống AI Camera Counting, sử dụng Playwright để test user flows từ frontend đến backend.

### 🎯 Mục tiêu
- Đảm bảo user experience hoàn chỉnh
- Test real-world user scenarios
- Validate system integration
- Kiểm tra performance và reliability

### 🛠️ Playwright Setup

#### Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

#### Test Utilities
```typescript
// tests/e2e/utils/test-helpers.ts
import { Page, expect } from '@playwright/test';

export class TestHelpers {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto('/login');
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.click('[data-testid="login-button"]');
    await this.page.waitForURL('/dashboard');
  }

  async createCamera(cameraData: {
    name: string;
    location: string;
    ipAddress: string;
  }) {
    await this.page.goto('/cameras/new');
    await this.page.fill('[data-testid="camera-name"]', cameraData.name);
    await this.page.fill('[data-testid="camera-location"]', cameraData.location);
    await this.page.fill('[data-testid="camera-ip"]', cameraData.ipAddress);
    await this.page.click('[data-testid="save-camera"]');
    await this.page.waitForURL('/cameras');
  }

  async waitForCountUpdate(expectedCount: number) {
    await this.page.waitForFunction(
      (count) => {
        const countElement = document.querySelector('[data-testid="count-display"]');
        return countElement && countElement.textContent === count.toString();
      },
      expectedCount,
      { timeout: 10000 }
    );
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }
}
```

### 🧪 Authentication Flow Testing

#### Login Flow
```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Authentication Flow', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // Fill login form
    await page.fill('[data-testid="email-input"]', 'admin@example.com');
    await page.fill('[data-testid="password-input"]', 'admin123');
    await page.click('[data-testid="login-button"]');
    
    // Verify successful login
    await page.waitForURL('/dashboard');
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
    await expect(page.locator('[data-testid="dashboard-title"]')).toContainText('Dashboard');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // Fill login form with invalid credentials
    await page.fill('[data-testid="email-input"]', 'invalid@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpassword');
    await page.click('[data-testid="login-button"]');
    
    // Verify error message
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText('Invalid credentials');
  });

  test('should validate form fields', async ({ page }) => {
    await page.goto('/login');
    
    // Try to submit empty form
    await page.click('[data-testid="login-button"]');
    
    // Verify validation messages
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await helpers.login('admin@example.com', 'admin123');
    
    // Click logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    
    // Verify logout
    await page.waitForURL('/login');
    await expect(page.locator('[data-testid="login-form"]')).toBeVisible();
  });
});
```

### 🧪 Camera Management Testing

#### Camera CRUD Operations
```typescript
// tests/e2e/cameras/camera-management.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Camera Management', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await helpers.login('admin@example.com', 'admin123');
  });

  test('should create new camera', async ({ page }) => {
    await page.goto('/cameras/new');
    
    // Fill camera form
    await page.fill('[data-testid="camera-name"]', 'Test Camera');
    await page.fill('[data-testid="camera-location"]', 'Building A');
    await page.fill('[data-testid="camera-ip"]', '192.168.1.100');
    await page.selectOption('[data-testid="camera-status"]', 'active');
    
    // Submit form
    await page.click('[data-testid="save-camera"]');
    
    // Verify success
    await page.waitForURL('/cameras');
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('text=Test Camera')).toBeVisible();
  });

  test('should edit existing camera', async ({ page }) => {
    // Create camera first
    await helpers.createCamera({
      name: 'Original Camera',
      location: 'Building A',
      ipAddress: '192.168.1.100'
    });
    
    // Edit camera
    await page.click('[data-testid="edit-camera-1"]');
    await page.fill('[data-testid="camera-name"]', 'Updated Camera');
    await page.click('[data-testid="save-camera"]');
    
    // Verify update
    await expect(page.locator('text=Updated Camera')).toBeVisible();
  });

  test('should delete camera', async ({ page }) => {
    // Create camera first
    await helpers.createCamera({
      name: 'Camera to Delete',
      location: 'Building A',
      ipAddress: '192.168.1.101'
    });
    
    // Delete camera
    await page.click('[data-testid="delete-camera-1"]');
    await page.click('[data-testid="confirm-delete"]');
    
    // Verify deletion
    await expect(page.locator('text=Camera to Delete')).not.toBeVisible();
  });

  test('should display camera list', async ({ page }) => {
    await page.goto('/cameras');
    
    // Verify camera list elements
    await expect(page.locator('[data-testid="camera-list"]')).toBeVisible();
    await expect(page.locator('[data-testid="add-camera-button"]')).toBeVisible();
  });
});
```

### 🧪 Real-time Counting Testing

#### Live Camera Feed Testing
```typescript
// tests/e2e/counting/live-counting.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Real-time Counting', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await helpers.login('admin@example.com', 'admin123');
  });

  test('should display live camera feed', async ({ page }) => {
    // Create camera first
    await helpers.createCamera({
      name: 'Live Test Camera',
      location: 'Building A',
      ipAddress: '192.168.1.100'
    });
    
    // Navigate to camera view
    await page.click('[data-testid="view-camera-1"]');
    
    // Verify camera feed elements
    await expect(page.locator('[data-testid="camera-feed"]')).toBeVisible();
    await expect(page.locator('[data-testid="count-display"]')).toBeVisible();
    await expect(page.locator('[data-testid="confidence-display"]')).toBeVisible();
  });

  test('should update count in real-time', async ({ page }) => {
    // Navigate to camera view
    await page.goto('/cameras/1');
    
    // Wait for initial count
    await expect(page.locator('[data-testid="count-display"]')).toBeVisible();
    
    // Simulate count update
    await page.evaluate(() => {
      // Mock WebSocket message
      window.mockCountUpdate({ count: 5, confidence: 0.95 });
    });
    
    // Verify count update
    await expect(page.locator('[data-testid="count-display"]')).toContainText('5');
    await expect(page.locator('[data-testid="confidence-display"]')).toContainText('95%');
  });

  test('should handle camera connection issues', async ({ page }) => {
    await page.goto('/cameras/1');
    
    // Simulate connection loss
    await page.evaluate(() => {
      window.mockConnectionError();
    });
    
    // Verify error handling
    await expect(page.locator('[data-testid="connection-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="retry-button"]')).toBeVisible();
  });

  test('should display multiple cameras simultaneously', async ({ page }) => {
    // Create multiple cameras
    await helpers.createCamera({
      name: 'Camera 1',
      location: 'Building A',
      ipAddress: '192.168.1.100'
    });
    
    await helpers.createCamera({
      name: 'Camera 2',
      location: 'Building B',
      ipAddress: '192.168.1.101'
    });
    
    // Navigate to dashboard
    await page.goto('/dashboard');
    
    // Verify multiple camera feeds
    await expect(page.locator('[data-testid="camera-feed-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="camera-feed-2"]')).toBeVisible();
  });
});
```

### 🧪 Analytics and Reporting Testing

#### Dashboard Analytics
```typescript
// tests/e2e/analytics/dashboard-analytics.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Dashboard Analytics', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await helpers.login('admin@example.com', 'admin123');
  });

  test('should display dashboard analytics', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Verify dashboard elements
    await expect(page.locator('[data-testid="total-cameras"]')).toBeVisible();
    await expect(page.locator('[data-testid="total-counts"]')).toBeVisible();
    await expect(page.locator('[data-testid="average-confidence"]')).toBeVisible();
    await expect(page.locator('[data-testid="counts-chart"]')).toBeVisible();
  });

  test('should filter analytics by date range', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Select date range
    await page.click('[data-testid="date-range-picker"]');
    await page.click('[data-testid="last-7-days"]');
    
    // Verify filtered data
    await expect(page.locator('[data-testid="filtered-counts"]')).toBeVisible();
  });

  test('should export analytics report', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Click export button
    await page.click('[data-testid="export-report"]');
    
    // Verify download
    const downloadPromise = page.waitForEvent('download');
    await page.click('[data-testid="confirm-export"]');
    const download = await downloadPromise;
    
    expect(download.suggestedFilename()).toMatch(/analytics-report-.*\.csv/);
  });

  test('should display camera-specific analytics', async ({ page }) => {
    // Create camera first
    await helpers.createCamera({
      name: 'Analytics Test Camera',
      location: 'Building A',
      ipAddress: '192.168.1.100'
    });
    
    // Navigate to camera analytics
    await page.click('[data-testid="camera-analytics-1"]');
    
    // Verify camera-specific analytics
    await expect(page.locator('[data-testid="camera-name"]')).toContainText('Analytics Test Camera');
    await expect(page.locator('[data-testid="camera-counts-chart"]')).toBeVisible();
    await expect(page.locator('[data-testid="camera-confidence-chart"]')).toBeVisible();
  });
});
```

### 🧪 User Management Testing

#### User Roles and Permissions
```typescript
// tests/e2e/users/user-management.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('User Management', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  test('should create new user as admin', async ({ page }) => {
    await helpers.login('admin@example.com', 'admin123');
    await page.goto('/users/new');
    
    // Fill user form
    await page.fill('[data-testid="user-email"]', 'newuser@example.com');
    await page.fill('[data-testid="user-password"]', 'password123');
    await page.fill('[data-testid="user-first-name"]', 'John');
    await page.fill('[data-testid="user-last-name"]', 'Doe');
    await page.selectOption('[data-testid="user-role"]', 'user');
    
    // Submit form
    await page.click('[data-testid="save-user"]');
    
    // Verify success
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });

  test('should restrict access based on user role', async ({ page }) => {
    // Login as regular user
    await helpers.login('user@example.com', 'user123');
    
    // Try to access admin-only page
    await page.goto('/users');
    
    // Verify access denied
    await expect(page.locator('[data-testid="access-denied"]')).toBeVisible();
  });

  test('should edit user profile', async ({ page }) => {
    await helpers.login('user@example.com', 'user123');
    await page.goto('/profile');
    
    // Edit profile
    await page.fill('[data-testid="first-name"]', 'Updated Name');
    await page.click('[data-testid="save-profile"]');
    
    // Verify update
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="first-name"]')).toHaveValue('Updated Name');
  });
});
```

### 🧪 Error Handling Testing

#### Error Scenarios
```typescript
// tests/e2e/errors/error-handling.spec.ts
import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Error Handling', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await helpers.login('admin@example.com', 'admin123');
  });

  test('should handle network errors gracefully', async ({ page }) => {
    // Simulate network error
    await page.route('**/api/cameras', route => route.abort());
    
    await page.goto('/cameras');
    
    // Verify error handling
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="retry-button"]')).toBeVisible();
  });

  test('should handle server errors', async ({ page }) => {
    // Simulate server error
    await page.route('**/api/cameras', route => 
      route.fulfill({ status: 500, body: 'Internal Server Error' })
    );
    
    await page.goto('/cameras');
    
    // Verify error handling
    await expect(page.locator('[data-testid="server-error"]')).toBeVisible();
  });

  test('should handle validation errors', async ({ page }) => {
    await page.goto('/cameras/new');
    
    // Submit invalid form
    await page.click('[data-testid="save-camera"]');
    
    // Verify validation errors
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="ip-error"]')).toBeVisible();
  });

  test('should handle session timeout', async ({ page }) => {
    // Simulate session timeout
    await page.evaluate(() => {
      localStorage.removeItem('token');
    });
    
    await page.goto('/dashboard');
    
    // Verify redirect to login
    await page.waitForURL('/login');
    await expect(page.locator('[data-testid="session-expired"]')).toBeVisible();
  });
});
```

### 📊 Performance Testing

#### Load Testing Scenarios
```typescript
// tests/e2e/performance/load-testing.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Testing', () => {
  test('should handle multiple concurrent users', async ({ browser }) => {
    const contexts = [];
    const pages = [];
    
    // Create multiple browser contexts
    for (let i = 0; i < 5; i++) {
      const context = await browser.newContext();
      const page = await context.newPage();
      contexts.push(context);
      pages.push(page);
    }
    
    // Navigate all pages to dashboard
    await Promise.all(pages.map(page => page.goto('/dashboard')));
    
    // Verify all pages load successfully
    for (const page of pages) {
      await expect(page.locator('[data-testid="dashboard"]')).toBeVisible();
    }
    
    // Cleanup
    await Promise.all(contexts.map(context => context.close()));
  });

  test('should load dashboard within performance budget', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Dashboard should load within 3 seconds
    expect(loadTime).toBeLessThan(3000);
  });

  test('should handle large datasets efficiently', async ({ page }) => {
    await page.goto('/cameras');
    
    // Create many cameras (simulated)
    await page.evaluate(() => {
      // Mock 1000 cameras
      window.mockLargeDataset(1000);
    });
    
    // Verify performance
    await expect(page.locator('[data-testid="camera-list"]')).toBeVisible();
    
    // Check for virtual scrolling or pagination
    const visibleCameras = await page.locator('[data-testid="camera-item"]').count();
    expect(visibleCameras).toBeLessThanOrEqual(50); // Should not render all 1000
  });
});
```

### 📋 E2E Test Checklist

#### Setup Phase
- [ ] Configure Playwright
- [ ] Setup test environment
- [ ] Create test data
- [ ] Configure test users
- [ ] Setup monitoring

#### Test Execution
- [ ] Run authentication tests
- [ ] Run camera management tests
- [ ] Run real-time counting tests
- [ ] Run analytics tests
- [ ] Run user management tests
- [ ] Run error handling tests
- [ ] Run performance tests

#### Validation Phase
- [ ] Verify all user flows work
- [ ] Check error handling
- [ ] Validate performance
- [ ] Test cross-browser compatibility
- [ ] Verify mobile responsiveness

### 🎯 Success Metrics

#### User Experience Metrics
- **Page Load Time**: < 3 seconds for all pages
- **Interactive Time**: < 1 second for user interactions
- **Error Rate**: < 1% for user flows
- **Success Rate**: > 99% for critical paths

#### Performance Metrics
- **Dashboard Load Time**: < 2 seconds
- **Camera Feed Latency**: < 500ms
- **Real-time Updates**: < 100ms
- **Mobile Performance**: < 5 seconds on 3G

#### Reliability Metrics
- **Test Reliability**: > 95% pass rate
- **Cross-browser Compatibility**: 100% on supported browsers
- **Mobile Responsiveness**: 100% on target devices
- **Error Recovery**: 100% graceful error handling

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
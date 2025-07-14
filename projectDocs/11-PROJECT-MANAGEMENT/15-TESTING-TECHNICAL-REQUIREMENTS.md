# Testing Technical Requirements
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các yêu cầu kỹ thuật chi tiết cho Testing & Quality Assurance của hệ thống AI Camera Counting, bao gồm E2E testing strategy, performance testing, security testing, load testing, test data management, visual regression testing, API contract testing, accessibility testing.

### 🎯 Mục tiêu kỹ thuật
- Đảm bảo chất lượng toàn diện với 100% test coverage cho critical paths
- Performance testing đáp ứng SLA: response time <200ms, throughput >1000 req/s
- Security testing: zero critical vulnerabilities
- Accessibility testing: WCAG 2.1 AA compliance

### 🏗️ E2E Testing Strategy

#### Playwright Implementation
```typescript
// E2E Test Configuration
import { test, expect } from '@playwright/test';

test.describe('AI Camera System E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
  });

  test('User can login and view dashboard', async ({ page }) => {
    // Login flow
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="login-button"]');
    
    // Verify dashboard loads
    await expect(page.locator('[data-testid="dashboard"]')).toBeVisible();
    await expect(page.locator('[data-testid="camera-list"]')).toBeVisible();
  });

  test('Camera counting functionality works', async ({ page }) => {
    // Navigate to camera view
    await page.click('[data-testid="camera-1"]');
    
    // Verify real-time counting
    await expect(page.locator('[data-testid="count-display"]')).toBeVisible();
    
    // Simulate camera feed
    await page.evaluate(() => {
      // Mock camera data
      window.mockCameraData = { count: 5, confidence: 0.95 };
    });
    
    // Verify count updates
    await expect(page.locator('[data-testid="count-value"]')).toHaveText('5');
  });
});
```

#### Test Scenarios Coverage
- **Authentication Flow**: Login, logout, password reset, session management
- **Camera Management**: Add, edit, delete, status monitoring
- **Real-time Counting**: Live feed, count accuracy, confidence scoring
- **Analytics & Reporting**: Data visualization, export, filtering
- **User Management**: Role-based access, permissions, user creation
- **System Integration**: API calls, WebSocket connections, data persistence

### 📈 Performance Testing

#### JMeter Load Testing
```xml
<!-- JMeter Test Plan -->
<TestPlan>
  <ThreadGroup>
    <stringProp name="ThreadGroup.num_threads">100</stringProp>
    <stringProp name="ThreadGroup.ramp_time">60</stringProp>
    
    <HTTPSamplerProxy>
      <stringProp name="HTTPSampler.domain">api.aicamera.com</stringProp>
      <stringProp name="HTTPSampler.path">/api/v1/cameras</stringProp>
      <stringProp name="HTTPSampler.method">GET</stringProp>
    </HTTPSamplerProxy>
    
    <ResponseAssertion>
      <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
      <stringProp name="Assertion.test_type">Assertion.equals</stringProp>
      <stringProp name="Assertion.test_string">200</stringProp>
    </ResponseAssertion>
  </ThreadGroup>
</TestPlan>
```

#### K6 Performance Testing
```javascript
// K6 Performance Test
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests must complete below 200ms
    http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
  },
};

export default function () {
  const response = http.get('http://api.aicamera.com/api/v1/cameras');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  
  sleep(1);
}
```

#### Performance Benchmarks
- **Response Time**: <200ms for 95% of requests
- **Throughput**: >1000 requests/second
- **Concurrent Users**: Support 500+ simultaneous users
- **Memory Usage**: <2GB per instance
- **CPU Usage**: <80% under normal load

### 🔒 Security Testing

#### OWASP ZAP Integration
```python
# Security Testing with OWASP ZAP
from zapv2 import ZAPv2

class SecurityTester:
    def __init__(self, target_url: str):
        self.zap = ZAPv2()
        self.target_url = target_url
    
    def run_security_scan(self):
        """Run comprehensive security scan"""
        # Spider the application
        self.zap.spider.scan(self.target_url)
        
        # Active scan for vulnerabilities
        self.zap.ascan.scan(self.target_url)
        
        # Generate report
        report = self.zap.core.htmlreport()
        
        return self._analyze_results(report)
    
    def test_authentication(self):
        """Test authentication security"""
        # Test SQL injection
        # Test XSS
        # Test CSRF
        # Test authentication bypass
        pass
```

#### Security Test Cases
- **SQL Injection**: Test all input fields for SQL injection vulnerabilities
- **XSS (Cross-Site Scripting)**: Test for reflected and stored XSS
- **CSRF (Cross-Site Request Forgery)**: Test for CSRF vulnerabilities
- **Authentication Bypass**: Test for authentication bypass methods
- **Authorization**: Test role-based access control
- **Data Encryption**: Verify data encryption in transit and at rest
- **API Security**: Test API endpoints for security vulnerabilities

### ⚡ Load Testing

#### Stress Testing
```python
# Stress Testing Implementation
import asyncio
import aiohttp
import time
from typing import List

class StressTester:
    def __init__(self, base_url: str, max_concurrent: int = 1000):
        self.base_url = base_url
        self.max_concurrent = max_concurrent
        self.results = []
    
    async def stress_test(self, duration: int = 300):
        """Run stress test for specified duration"""
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(self.max_concurrent):
                task = asyncio.create_task(self._make_request(session))
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
        return self._analyze_results()
    
    async def _make_request(self, session):
        """Make individual request"""
        start = time.time()
        try:
            async with session.get(f"{self.base_url}/api/v1/cameras") as response:
                duration = time.time() - start
                self.results.append({
                    'status': response.status,
                    'duration': duration,
                    'success': response.status == 200
                })
        except Exception as e:
            self.results.append({
                'status': 'error',
                'duration': time.time() - start,
                'success': False,
                'error': str(e)
            })
```

#### Spike Testing
```python
# Spike Testing
class SpikeTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def spike_test(self):
        """Test system behavior under sudden load spikes"""
        # Normal load: 100 users
        await self._load_test(100, 60)
        
        # Spike: 1000 users for 30 seconds
        await self._load_test(1000, 30)
        
        # Return to normal: 100 users
        await self._load_test(100, 60)
```

### 📊 Test Data Management

#### Test Data Generation
```python
# Test Data Management
import factory
from faker import Faker
from typing import Dict, List

fake = Faker()

class CameraFactory(factory.Factory):
    class Meta:
        model = Camera
    
    id = factory.Faker('uuid4')
    name = factory.Faker('company')
    location = factory.Faker('address')
    ip_address = factory.Faker('ipv4')
    status = factory.Iterator(['active', 'inactive', 'maintenance'])

class CountDataFactory(factory.Factory):
    class Meta:
        model = CountData
    
    camera_id = factory.Faker('uuid4')
    count = factory.Faker('random_int', min=0, max=100)
    confidence = factory.Faker('pyfloat', min_value=0.5, max_value=1.0)
    timestamp = factory.Faker('date_time_this_month')

class TestDataManager:
    def __init__(self):
        self.factories = {
            'camera': CameraFactory,
            'count_data': CountDataFactory,
            'user': UserFactory
        }
    
    def generate_test_data(self, entity_type: str, count: int = 10):
        """Generate test data for specified entity"""
        factory = self.factories.get(entity_type)
        if not factory:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        return [factory() for _ in range(count)]
    
    def create_test_scenario(self, scenario_name: str):
        """Create complex test scenarios"""
        scenarios = {
            'high_load': self._create_high_load_scenario,
            'data_quality': self._create_data_quality_scenario,
            'security': self._create_security_scenario
        }
        
        return scenarios[scenario_name]()
```

#### Data Masking & Privacy
```python
# Data Masking for Privacy
import hashlib
import re

class DataMasker:
    def __init__(self):
        self.masking_rules = {
            'email': self._mask_email,
            'phone': self._mask_phone,
            'ip_address': self._mask_ip,
            'password': self._mask_password
        }
    
    def mask_sensitive_data(self, data: Dict) -> Dict:
        """Mask sensitive data in test data"""
        masked_data = data.copy()
        
        for key, value in masked_data.items():
            for pattern, mask_func in self.masking_rules.items():
                if pattern in key.lower():
                    masked_data[key] = mask_func(value)
        
        return masked_data
    
    def _mask_email(self, email: str) -> str:
        """Mask email address"""
        if '@' in email:
            username, domain = email.split('@')
            return f"{username[0]}***@{domain}"
        return email
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number"""
        return re.sub(r'\d', '*', phone)
```

### 🎨 Visual Regression Testing

#### Percy Integration
```typescript
// Visual Regression Testing with Percy
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('Dashboard layout remains consistent', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Take screenshot for visual comparison
    await expect(page).toHaveScreenshot('dashboard.png');
  });

  test('Camera card components are consistent', async ({ page }) => {
    await page.goto('http://localhost:3000/cameras');
    
    // Test individual components
    const cameraCard = page.locator('[data-testid="camera-card"]').first();
    await expect(cameraCard).toHaveScreenshot('camera-card.png');
  });

  test('Responsive design works across breakpoints', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('dashboard-mobile.png');
    
    // Test tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('dashboard-tablet.png');
    
    // Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('dashboard-desktop.png');
  });
});
```

### 🔗 API Contract Testing

#### Pact Contract Testing
```javascript
// API Contract Testing with Pact
const { Pact } = require('@pact-foundation/pact');
const { Matchers } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'ai-camera-frontend',
  provider: 'ai-camera-backend',
  port: 1234,
  log: './pact.log',
  dir: './pacts',
  logLevel: 'INFO',
  spec: 2
});

describe('Camera API Contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  describe('GET /api/v1/cameras', () => {
    beforeEach(() => {
      const interaction = {
        state: 'cameras exist',
        uponReceiving: 'a request for cameras',
        withRequest: {
          method: 'GET',
          path: '/api/v1/cameras',
          headers: {
            'Authorization': 'Bearer token123'
          }
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json'
          },
          body: Matchers.eachLike({
            id: Matchers.string('550e8400-e29b-41d4-a716-446655440000'),
            name: Matchers.string('Main Camera'),
            status: Matchers.string('active')
          })
        }
      };
      return provider.addInteraction(interaction);
    });

    it('should return camera list', async () => {
      const response = await fetch('http://localhost:1234/api/v1/cameras', {
        headers: { 'Authorization': 'Bearer token123' }
      });
      
      expect(response.status).toBe(200);
      const cameras = await response.json();
      expect(cameras).toHaveLength(1);
      expect(cameras[0].name).toBe('Main Camera');
    });
  });
});
```

### ♿ Accessibility Testing

#### axe-core Integration
```typescript
// Accessibility Testing with axe-core
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Tests', () => {
  test('Dashboard meets WCAG 2.1 AA standards', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('All interactive elements are keyboard accessible', async ({ page }) => {
    await page.goto('http://localhost:3000/cameras');
    
    // Test keyboard navigation
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toBeVisible();
    
    // Test all interactive elements
    const interactiveElements = page.locator('button, a, input, select, textarea');
    const count = await interactiveElements.count();
    
    for (let i = 0; i < count; i++) {
      await page.keyboard.press('Tab');
      await expect(page.locator(':focus')).toBeVisible();
    }
  });

  test('Color contrast meets WCAG standards', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze();
    
    const colorContrastViolations = accessibilityScanResults.violations
      .filter(violation => violation.id === 'color-contrast');
    
    expect(colorContrastViolations).toHaveLength(0);
  });

  test('Screen reader compatibility', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    
    // Test ARIA labels
    const elementsWithAria = page.locator('[aria-label], [aria-labelledby]');
    await expect(elementsWithAria).toHaveCount(5); // Expected number of ARIA elements
    
    // Test semantic HTML
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    await expect(headings).toHaveCount(3); // Expected number of headings
  });
});
```

### 📋 Implementation Checklist

#### Phase 1: Foundation Setup (Week 1)
- [ ] Setup testing framework (Playwright, Jest, Cypress)
- [ ] Configure CI/CD pipeline for automated testing
- [ ] Setup test data management system
- [ ] Configure performance testing tools (JMeter, K6)
- [ ] Setup security testing tools (OWASP ZAP)

#### Phase 2: Test Development (Week 2)
- [ ] Implement E2E test scenarios
- [ ] Create performance test scripts
- [ ] Setup security test automation
- [ ] Implement visual regression tests
- [ ] Setup API contract testing

#### Phase 3: Quality Assurance (Week 3)
- [ ] Implement accessibility testing
- [ ] Setup load and stress testing
- [ ] Create comprehensive test data
- [ ] Implement test reporting and analytics
- [ ] Setup test environment management

#### Phase 4: Production Readiness (Week 4)
- [ ] Setup production-like test environment
- [ ] Implement automated test execution
- [ ] Configure test monitoring and alerting
- [ ] Setup test result analysis
- [ ] Implement continuous testing

### 🎯 Success Metrics

#### Quality Metrics
- **Test Coverage**: >90% for critical paths
- **Test Execution Time**: <30 minutes for full test suite
- **Test Reliability**: >95% pass rate
- **Bug Detection Rate**: >80% of issues caught in testing

#### Performance Metrics
- **Response Time**: <200ms for 95% of requests
- **Throughput**: >1000 requests/second
- **Error Rate**: <1% under normal load
- **Resource Usage**: <80% CPU, <2GB memory

#### Security Metrics
- **Security Vulnerabilities**: 0 critical, <5 medium
- **OWASP Top 10**: 100% coverage
- **Authentication Tests**: 100% pass rate
- **Authorization Tests**: 100% pass rate

#### Accessibility Metrics
- **WCAG 2.1 AA Compliance**: 100%
- **Keyboard Navigation**: Fully functional
- **Screen Reader Compatibility**: Complete
- **Color Contrast**: Meets AA standards

### 🚨 Risk Mitigation

#### Testing Risks
- **Risk**: Incomplete test coverage → Mitigation: Automated coverage reporting
- **Risk**: Flaky tests → Mitigation: Test stability monitoring, retry mechanisms
- **Risk**: Slow test execution → Mitigation: Parallel execution, test optimization

#### Performance Risks
- **Risk**: Performance degradation → Mitigation: Continuous performance monitoring
- **Risk**: Load test failures → Mitigation: Scalability planning, capacity management

#### Security Risks
- **Risk**: Security vulnerabilities → Mitigation: Automated security scanning
- **Risk**: Compliance violations → Mitigation: Regular compliance audits

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Date + 2 weeks]  
**Status**: Ready for Implementation

# Quality Gates Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các quality gates và checkpoints để đảm bảo chất lượng code, performance, và security trước khi deploy vào production.

### 🎯 Quality Gates Objectives
- Đảm bảo code quality và consistency
- Prevent performance degradation
- Maintain security standards
- Ensure reliable deployments
- Track quality metrics over time

### 🚦 Quality Gates Framework

#### Gate 1: Code Quality
```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run type checking
        run: npm run type-check
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Run integration tests
        run: npm run test:integration
      
      - name: Check test coverage
        run: npm run test:coverage
      
      - name: Security audit
        run: npm audit --audit-level moderate
      
      - name: Bundle analysis
        run: npm run build:analyze
```

#### Gate 2: Performance Testing
```yaml
# Performance Gate Configuration
performance-gate:
  thresholds:
    lighthouse:
      performance: 90
      accessibility: 95
      best-practices: 90
      seo: 90
    
    web-vitals:
      lcp: 2500  # Largest Contentful Paint
      fid: 100   # First Input Delay
      cls: 0.1   # Cumulative Layout Shift
    
    api-performance:
      response-time-p95: 200  # 95th percentile
      error-rate: 1           # Percentage
      throughput: 1000        # Requests per second
```

#### Gate 3: Security Scanning
```yaml
# Security Gate Configuration
security-gate:
  tools:
    - name: "OWASP ZAP"
      severity-threshold: "MEDIUM"
      max-vulnerabilities: 5
    
    - name: "Snyk"
      severity-threshold: "HIGH"
      max-vulnerabilities: 0
    
    - name: "SonarQube"
      quality-gate: "Sonar way"
      coverage-threshold: 80
      duplication-threshold: 5
```

### 📊 Code Quality Metrics

#### Static Analysis
```typescript
// ESLint Configuration
module.exports = {
  extends: [
    '@typescript-eslint/recommended',
    'prettier',
    'plugin:security/recommended'
  ],
  rules: {
    // Code complexity
    'complexity': ['error', 10],
    'max-depth': ['error', 4],
    'max-lines-per-function': ['error', 50],
    
    // Security
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'error',
    
    // Best practices
    'no-console': 'warn',
    'no-debugger': 'error',
    'no-unused-vars': 'error',
    
    // TypeScript specific
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};

// Prettier Configuration
module.exports = {
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false
};
```

#### Test Coverage Requirements
```javascript
// Jest Configuration
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/*.test.{js,jsx,ts,tsx}'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/components/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90
    },
    './src/services/': {
      branches: 85,
      functions: 85,
      lines: 85,
      statements: 85
    }
  },
  coverageReporters: ['text', 'lcov', 'html'],
  coverageDirectory: 'coverage'
};
```

### 🔒 Security Quality Gates

#### Dependency Security
```json
// package.json security scripts
{
  "scripts": {
    "security:audit": "npm audit --audit-level moderate",
    "security:fix": "npm audit fix",
    "security:check": "snyk test",
    "security:monitor": "snyk monitor"
  }
}
```

#### Code Security Scanning
```python
# Security scanning configuration
SECURITY_SCAN_CONFIG = {
    'bandit': {
        'enabled': True,
        'severity_threshold': 'MEDIUM',
        'exclude': ['tests/', 'migrations/']
    },
    'safety': {
        'enabled': True,
        'severity_threshold': 'HIGH'
    },
    'semgrep': {
        'enabled': True,
        'rules': ['security', 'python']
    }
}

# Security test cases
SECURITY_TEST_CASES = [
    {
        'name': 'SQL Injection Test',
        'description': 'Test all input fields for SQL injection',
        'severity': 'HIGH',
        'test_type': 'automated'
    },
    {
        'name': 'XSS Test',
        'description': 'Test for cross-site scripting vulnerabilities',
        'severity': 'HIGH',
        'test_type': 'automated'
    },
    {
        'name': 'Authentication Bypass',
        'description': 'Test authentication mechanisms',
        'severity': 'CRITICAL',
        'test_type': 'manual'
    }
]
```

### ⚡ Performance Quality Gates

#### Frontend Performance
```typescript
// Performance monitoring
interface PerformanceMetrics {
  lcp: number;      // Largest Contentful Paint
  fid: number;      // First Input Delay
  cls: number;      // Cumulative Layout Shift
  ttfb: number;     // Time to First Byte
  fcp: number;      // First Contentful Paint
}

class PerformanceGate {
  private static readonly THRESHOLDS = {
    lcp: 2500,    // 2.5 seconds
    fid: 100,     // 100 milliseconds
    cls: 0.1,     // 0.1
    ttfb: 600,    // 600 milliseconds
    fcp: 1800     // 1.8 seconds
  };

  static checkMetrics(metrics: PerformanceMetrics): boolean {
    return (
      metrics.lcp <= this.THRESHOLDS.lcp &&
      metrics.fid <= this.THRESHOLDS.fid &&
      metrics.cls <= this.THRESHOLDS.cls &&
      metrics.ttfb <= this.THRESHOLDS.ttfb &&
      metrics.fcp <= this.THRESHOLDS.fcp
    );
  }
}
```

#### API Performance
```python
# API Performance monitoring
from prometheus_client import Histogram, Counter
import time
from functools import wraps

# Metrics
api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['endpoint', 'method']
)

api_request_total = Counter(
    'api_request_total',
    'Total API requests',
    ['endpoint', 'method', 'status']
)

def performance_gate(func):
    """Decorator to monitor API performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            status = 'success'
        except Exception as e:
            status = 'error'
            raise
        finally:
            duration = time.time() - start_time
            
            # Record metrics
            api_request_duration.labels(
                endpoint=func.__name__,
                method='POST'
            ).observe(duration)
            
            api_request_total.labels(
                endpoint=func.__name__,
                method='POST',
                status=status
            ).inc()
            
            # Check performance gate
            if duration > 0.2:  # 200ms threshold
                logger.warning(f"Performance gate failed: {func.__name__} took {duration:.3f}s")
        
        return result
    return wrapper
```

### 🧪 Test Quality Gates

#### Test Requirements
```yaml
# Test Quality Gates
test-gates:
  unit-tests:
    coverage: 80
    pass-rate: 95
    execution-time: 300  # seconds
    
  integration-tests:
    coverage: 70
    pass-rate: 90
    execution-time: 600  # seconds
    
  e2e-tests:
    coverage: 60
    pass-rate: 85
    execution-time: 1800  # seconds
    
  performance-tests:
    response-time-p95: 200
    error-rate: 1
    throughput: 1000
```

#### Test Automation
```typescript
// Test automation configuration
const TEST_CONFIG = {
  unit: {
    timeout: 5000,
    retries: 2,
    parallel: true,
    coverage: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  integration: {
    timeout: 10000,
    retries: 1,
    parallel: false,
    coverage: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  e2e: {
    timeout: 30000,
    retries: 1,
    parallel: false,
    coverage: {
      branches: 60,
      functions: 60,
      lines: 60,
      statements: 60
    }
  }
};

// Test quality gate checker
class TestQualityGate {
  static checkCoverage(coverage: CoverageReport): boolean {
    return (
      coverage.branches >= TEST_CONFIG.unit.coverage.branches &&
      coverage.functions >= TEST_CONFIG.unit.coverage.functions &&
      coverage.lines >= TEST_CONFIG.unit.coverage.lines &&
      coverage.statements >= TEST_CONFIG.unit.coverage.statements
    );
  }
  
  static checkPassRate(results: TestResults): boolean {
    const passRate = (results.passed / results.total) * 100;
    return passRate >= 95;
  }
  
  static checkExecutionTime(duration: number): boolean {
    return duration <= TEST_CONFIG.unit.timeout;
  }
}
```

### 📊 Quality Metrics Dashboard

#### Quality Score Calculation
```typescript
interface QualityMetrics {
  codeQuality: number;      // 0-100
  testCoverage: number;     // 0-100
  securityScore: number;    // 0-100
  performanceScore: number; // 0-100
  documentationScore: number; // 0-100
}

class QualityGate {
  private static readonly WEIGHTS = {
    codeQuality: 0.25,
    testCoverage: 0.25,
    securityScore: 0.20,
    performanceScore: 0.20,
    documentationScore: 0.10
  };

  static calculateOverallScore(metrics: QualityMetrics): number {
    return (
      metrics.codeQuality * this.WEIGHTS.codeQuality +
      metrics.testCoverage * this.WEIGHTS.testCoverage +
      metrics.securityScore * this.WEIGHTS.securityScore +
      metrics.performanceScore * this.WEIGHTS.performanceScore +
      metrics.documentationScore * this.WEIGHTS.documentationScore
    );
  }

  static checkQualityGate(score: number): boolean {
    return score >= 80; // Minimum quality score
  }
}
```

#### Quality Reporting
```typescript
// Quality report generator
class QualityReporter {
  static generateReport(metrics: QualityMetrics): QualityReport {
    const overallScore = QualityGate.calculateOverallScore(metrics);
    const passed = QualityGate.checkQualityGate(overallScore);
    
    return {
      timestamp: new Date(),
      overallScore,
      passed,
      metrics,
      recommendations: this.generateRecommendations(metrics)
    };
  }
  
  private static generateRecommendations(metrics: QualityMetrics): string[] {
    const recommendations: string[] = [];
    
    if (metrics.codeQuality < 80) {
      recommendations.push('Improve code quality through better linting and code review');
    }
    
    if (metrics.testCoverage < 80) {
      recommendations.push('Increase test coverage by adding more unit and integration tests');
    }
    
    if (metrics.securityScore < 90) {
      recommendations.push('Address security vulnerabilities identified in security scan');
    }
    
    if (metrics.performanceScore < 85) {
      recommendations.push('Optimize performance bottlenecks identified in performance tests');
    }
    
    return recommendations;
  }
}
```

### 🚦 Deployment Quality Gates

#### Pre-deployment Checks
```yaml
# Pre-deployment quality gates
pre-deployment:
  - name: "Code Review"
    required: true
    approvers: 2
    status: "passed"
  
  - name: "Automated Tests"
    required: true
    pass-rate: 95
    status: "passed"
  
  - name: "Security Scan"
    required: true
    vulnerabilities: 0
    status: "passed"
  
  - name: "Performance Test"
    required: true
    response-time: 200
    status: "passed"
  
  - name: "Documentation"
    required: true
    coverage: 90
    status: "passed"
```

#### Post-deployment Validation
```yaml
# Post-deployment quality gates
post-deployment:
  - name: "Health Check"
    required: true
    timeout: 300
    status: "passed"
  
  - name: "Performance Validation"
    required: true
    duration: 600
    status: "passed"
  
  - name: "User Acceptance Test"
    required: true
    testers: 3
    status: "passed"
  
  - name: "Monitoring Setup"
    required: true
    metrics: "configured"
    status: "passed"
```

### 📋 Quality Gates Checklist

#### Development Phase
- [ ] Code review completed (2+ reviewers)
- [ ] All automated tests passing
- [ ] Test coverage meets requirements
- [ ] Security scan completed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Code quality metrics passed

#### Testing Phase
- [ ] Unit tests: >80% coverage, >95% pass rate
- [ ] Integration tests: >70% coverage, >90% pass rate
- [ ] E2E tests: >60% coverage, >85% pass rate
- [ ] Performance tests: <200ms response time, <1% error rate
- [ ] Security tests: 0 critical vulnerabilities
- [ ] Accessibility tests: WCAG 2.1 AA compliance

#### Deployment Phase
- [ ] Pre-deployment checks passed
- [ ] Deployment successful
- [ ] Health checks passing
- [ ] Performance validation completed
- [ ] User acceptance testing passed
- [ ] Monitoring and alerting configured

#### Post-deployment Phase
- [ ] System stability confirmed
- [ ] Performance metrics within thresholds
- [ ] Error rates below acceptable levels
- [ ] User feedback positive
- [ ] Rollback plan tested (if needed)

### 🎯 Quality Metrics Targets

#### Code Quality
- **Complexity**: < 10 cyclomatic complexity
- **Duplication**: < 5% code duplication
- **Maintainability**: A grade in SonarQube
- **Reliability**: A grade in SonarQube
- **Security**: A grade in SonarQube

#### Test Quality
- **Coverage**: >80% overall coverage
- **Pass Rate**: >95% test pass rate
- **Execution Time**: <30 minutes for full suite
- **Reliability**: <5% flaky tests

#### Performance Quality
- **Response Time**: <200ms (95th percentile)
- **Throughput**: >1000 requests/second
- **Error Rate**: <1% under normal load
- **Resource Usage**: <80% CPU, <2GB memory

#### Security Quality
- **Vulnerabilities**: 0 critical, <5 medium
- **OWASP Top 10**: 100% coverage
- **Authentication**: 100% secure
- **Authorization**: 100% role-based access

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
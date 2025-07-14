# Security Testing Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các procedures và tools cho security testing, bao gồm OWASP Top 10 testing, penetration testing, vulnerability assessment, và security code review.

### 🎯 Security Testing Objectives
- Đảm bảo zero critical security vulnerabilities
- Implement comprehensive security testing
- Maintain security compliance
- Protect sensitive data và user privacy

### 🔒 Security Testing Framework

#### OWASP Top 10 Testing
```yaml
# OWASP Top 10 Test Cases
owasp_testing:
  injection:
    - name: "SQL Injection Testing"
      description: "Test all input fields for SQL injection"
      tools: ["OWASP ZAP", "SQLMap"]
      severity: "CRITICAL"
    
    - name: "NoSQL Injection Testing"
      description: "Test for NoSQL injection vulnerabilities"
      tools: ["OWASP ZAP", "Custom scripts"]
      severity: "HIGH"
  
  broken_authentication:
    - name: "Authentication Bypass"
      description: "Test authentication mechanisms"
      tools: ["Burp Suite", "OWASP ZAP"]
      severity: "CRITICAL"
    
    - name: "Session Management"
      description: "Test session handling"
      tools: ["Burp Suite", "Custom scripts"]
      severity: "HIGH"
  
  sensitive_data_exposure:
    - name: "Data Encryption"
      description: "Verify data encryption"
      tools: ["SSL Labs", "Custom scripts"]
      severity: "HIGH"
    
    - name: "API Security"
      description: "Test API endpoints"
      tools: ["OWASP ZAP", "Postman"]
      severity: "HIGH"
  
  xml_external_entity:
    - name: "XXE Testing"
      description: "Test XML processing"
      tools: ["OWASP ZAP", "Custom scripts"]
      severity: "MEDIUM"
  
  broken_access_control:
    - name: "Authorization Testing"
      description: "Test role-based access"
      tools: ["OWASP ZAP", "Custom scripts"]
      severity: "HIGH"
  
  security_misconfiguration:
    - name: "Configuration Review"
      description: "Review security settings"
      tools: ["Nmap", "Custom scripts"]
      severity: "MEDIUM"
  
  xss:
    - name: "Cross-Site Scripting"
      description: "Test for XSS vulnerabilities"
      tools: ["OWASP ZAP", "Burp Suite"]
      severity: "HIGH"
  
  insecure_deserialization:
    - name: "Deserialization Testing"
      description: "Test object deserialization"
      tools: ["OWASP ZAP", "Custom scripts"]
      severity: "MEDIUM"
  
  vulnerable_components:
    - name: "Dependency Scanning"
      description: "Scan for vulnerable dependencies"
      tools: ["Snyk", "OWASP Dependency Check"]
      severity: "HIGH"
  
  insufficient_logging:
    - name: "Logging Security"
      description: "Test security logging"
      tools: ["Custom scripts", "Log analysis"]
      severity: "MEDIUM"
```

#### Security Testing Tools
```yaml
# Security Testing Tools Configuration
security_tools:
  automated_scanning:
    - name: "OWASP ZAP"
      purpose: "Automated security scanning"
      configuration: "zap-config.xml"
      integration: "CI/CD pipeline"
    
    - name: "Snyk"
      purpose: "Dependency vulnerability scanning"
      configuration: "snyk-config.yml"
      integration: "GitHub Actions"
    
    - name: "SonarQube"
      purpose: "Code security analysis"
      configuration: "sonar-project.properties"
      integration: "CI/CD pipeline"
  
  manual_testing:
    - name: "Burp Suite"
      purpose: "Manual security testing"
      configuration: "burp-config.json"
      usage: "Penetration testing"
    
    - name: "Postman"
      purpose: "API security testing"
      configuration: "postman-collection.json"
      usage: "API vulnerability testing"
```

### 🧪 Security Test Implementation

#### Automated Security Testing
```python
# Security Testing with OWASP ZAP
from zapv2 import ZAPv2
import json
import time

class SecurityTester:
    def __init__(self, target_url: str):
        self.zap = ZAPv2()
        self.target_url = target_url
        self.results = []
    
    def run_comprehensive_scan(self):
        """Run comprehensive security scan"""
        try:
            # Spider the application
            print("Starting spider scan...")
            self.zap.spider.scan(self.target_url)
            
            # Wait for spider to complete
            while int(self.zap.spider.status()) < 100:
                time.sleep(2)
            
            # Active scan for vulnerabilities
            print("Starting active scan...")
            self.zap.ascan.scan(self.target_url)
            
            # Wait for active scan to complete
            while int(self.zap.ascan.status()) < 100:
                time.sleep(5)
            
            # Generate report
            report = self.zap.core.htmlreport()
            
            return self._analyze_results(report)
            
        except Exception as e:
            print(f"Security scan failed: {e}")
            return None
    
    def test_authentication(self):
        """Test authentication security"""
        auth_tests = [
            {
                'name': 'SQL Injection Test',
                'payloads': ["' OR 1=1--", "' UNION SELECT * FROM users--"],
                'endpoints': ['/api/login', '/api/register']
            },
            {
                'name': 'XSS Test',
                'payloads': ['<script>alert("XSS")</script>', 'javascript:alert("XSS")'],
                'endpoints': ['/api/user/profile', '/api/camera/name']
            },
            {
                'name': 'CSRF Test',
                'method': 'POST',
                'endpoints': ['/api/user/update', '/api/camera/update']
            }
        ]
        
        for test in auth_tests:
            self._run_security_test(test)
    
    def test_api_security(self):
        """Test API security endpoints"""
        api_tests = [
            {
                'name': 'Authentication Required',
                'endpoint': '/api/cameras',
                'expected_status': 401
            },
            {
                'name': 'Authorization Test',
                'endpoint': '/api/admin/users',
                'expected_status': 403
            },
            {
                'name': 'Input Validation',
                'endpoint': '/api/camera/create',
                'payload': {'name': '<script>alert("XSS")</script>'},
                'expected_status': 400
            }
        ]
        
        for test in api_tests:
            self._run_api_security_test(test)
    
    def _run_security_test(self, test_config):
        """Run individual security test"""
        print(f"Running {test_config['name']}...")
        
        for endpoint in test_config.get('endpoints', []):
            for payload in test_config.get('payloads', []):
                # Send request with malicious payload
                response = self._send_test_request(endpoint, payload)
                
                # Analyze response for vulnerabilities
                if self._detect_vulnerability(response, test_config['name']):
                    self.results.append({
                        'test': test_config['name'],
                        'endpoint': endpoint,
                        'payload': payload,
                        'vulnerability': 'Detected',
                        'severity': 'HIGH'
                    })
    
    def _run_api_security_test(self, test_config):
        """Run API security test"""
        print(f"Running API test: {test_config['name']}...")
        
        response = self._send_api_request(
            test_config['endpoint'],
            test_config.get('payload', {})
        )
        
        if response.status_code != test_config['expected_status']:
            self.results.append({
                'test': test_config['name'],
                'endpoint': test_config['endpoint'],
                'expected': test_config['expected_status'],
                'actual': response.status_code,
                'vulnerability': 'Security misconfiguration',
                'severity': 'MEDIUM'
            })
    
    def _analyze_results(self, report):
        """Analyze security scan results"""
        vulnerabilities = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        # Parse report and categorize vulnerabilities
        # Implementation depends on report format
        
        return {
            'total_vulnerabilities': sum(vulnerabilities.values()),
            'by_severity': vulnerabilities,
            'report_url': report,
            'recommendations': self._generate_recommendations(vulnerabilities)
        }
```

#### Manual Security Testing
```typescript
// Manual Security Testing Scripts
interface SecurityTest {
  name: string;
  description: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  endpoint: string;
  payload?: any;
  expectedResponse: number;
  vulnerabilityType: string;
}

class ManualSecurityTester {
  private baseUrl: string;
  private authToken: string;

  constructor(baseUrl: string, authToken: string) {
    this.baseUrl = baseUrl;
    this.authToken = authToken;
  }

  async runAuthenticationTests(): Promise<SecurityTestResult[]> {
    const tests: SecurityTest[] = [
      {
        name: 'SQL Injection in Login',
        description: 'Test login endpoint for SQL injection',
        method: 'POST',
        endpoint: '/api/auth/login',
        payload: {
          email: "' OR 1=1--",
          password: 'password'
        },
        expectedResponse: 400,
        vulnerabilityType: 'SQL Injection'
      },
      {
        name: 'XSS in User Profile',
        description: 'Test user profile update for XSS',
        method: 'PUT',
        endpoint: '/api/user/profile',
        payload: {
          name: '<script>alert("XSS")</script>',
          email: 'test@example.com'
        },
        expectedResponse: 400,
        vulnerabilityType: 'XSS'
      },
      {
        name: 'CSRF Token Missing',
        description: 'Test for CSRF protection',
        method: 'POST',
        endpoint: '/api/user/update',
        payload: {
          name: 'Test User'
        },
        expectedResponse: 403,
        vulnerabilityType: 'CSRF'
      }
    ];

    const results: SecurityTestResult[] = [];

    for (const test of tests) {
      const result = await this.runSecurityTest(test);
      results.push(result);
    }

    return results;
  }

  async runAuthorizationTests(): Promise<SecurityTestResult[]> {
    const tests: SecurityTest[] = [
      {
        name: 'Unauthorized Access',
        description: 'Test access without authentication',
        method: 'GET',
        endpoint: '/api/admin/users',
        expectedResponse: 401,
        vulnerabilityType: 'Authorization'
      },
      {
        name: 'Role Escalation',
        description: 'Test user accessing admin endpoints',
        method: 'GET',
        endpoint: '/api/admin/system',
        expectedResponse: 403,
        vulnerabilityType: 'Authorization'
      }
    ];

    const results: SecurityTestResult[] = [];

    for (const test of tests) {
      const result = await this.runSecurityTest(test);
      results.push(result);
    }

    return results;
  }

  private async runSecurityTest(test: SecurityTest): Promise<SecurityTestResult> {
    try {
      const response = await fetch(`${this.baseUrl}${test.endpoint}`, {
        method: test.method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`
        },
        body: test.payload ? JSON.stringify(test.payload) : undefined
      });

      return {
        testName: test.name,
        endpoint: test.endpoint,
        expectedStatus: test.expectedResponse,
        actualStatus: response.status,
        passed: response.status === test.expectedResponse,
        vulnerabilityType: test.vulnerabilityType,
        description: test.description
      };
    } catch (error) {
      return {
        testName: test.name,
        endpoint: test.endpoint,
        expectedStatus: test.expectedResponse,
        actualStatus: 0,
        passed: false,
        vulnerabilityType: test.vulnerabilityType,
        description: test.description,
        error: error.message
      };
    }
  }
}

interface SecurityTestResult {
  testName: string;
  endpoint: string;
  expectedStatus: number;
  actualStatus: number;
  passed: boolean;
  vulnerabilityType: string;
  description: string;
  error?: string;
}
```

### 🔍 Vulnerability Assessment

#### Security Scanning Configuration
```yaml
# Security Scanning Setup
security_scanning:
  automated_scans:
    - name: "Daily Security Scan"
      schedule: "0 2 * * *"
      tools: ["OWASP ZAP", "Snyk"]
      scope: "All environments"
    
    - name: "Weekly Deep Scan"
      schedule: "0 3 * * 0"
      tools: ["OWASP ZAP", "Burp Suite"]
      scope: "Production environment"
    
    - name: "Dependency Scan"
      schedule: "0 4 * * *"
      tools: ["Snyk", "OWASP Dependency Check"]
      scope: "All dependencies"
  
  manual_tests:
    - name: "Penetration Testing"
      frequency: "Monthly"
      scope: "Production environment"
      duration: "1 week"
    
    - name: "Security Code Review"
      frequency: "Every PR"
      scope: "All code changes"
      reviewers: ["Security team"]
```

#### Security Metrics
```yaml
# Security Metrics
security_metrics:
  vulnerability_management:
    - metric: "Critical vulnerabilities"
      target: "0"
      measurement: "Count"
    
    - metric: "High vulnerabilities"
      target: "< 5"
      measurement: "Count"
    
    - metric: "Vulnerability resolution time"
      target: "< 48 hours"
      measurement: "Time"
    
    - metric: "Security test coverage"
      target: "100%"
      measurement: "Percentage"
  
  compliance:
    - metric: "OWASP Top 10 coverage"
      target: "100%"
      measurement: "Percentage"
    
    - metric: "Security policy compliance"
      target: "100%"
      measurement: "Percentage"
    
    - metric: "Data protection compliance"
      target: "100%"
      measurement: "Percentage"
```

### 🛡️ Security Best Practices

#### Code Security Standards
```typescript
// Security Best Practices Implementation
class SecurityStandards {
  // Input Validation
  static validateInput(input: string): boolean {
    // Sanitize input
    const sanitized = this.sanitizeInput(input);
    
    // Check for malicious patterns
    const maliciousPatterns = [
      /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
      /javascript:/gi,
      /on\w+\s*=/gi,
      /union\s+select/gi,
      /drop\s+table/gi
    ];
    
    return !maliciousPatterns.some(pattern => pattern.test(sanitized));
  }
  
  // SQL Injection Prevention
  static buildSafeQuery(query: string, params: any[]): string {
    // Use parameterized queries
    return query.replace(/\?/g, () => {
      const param = params.shift();
      return typeof param === 'string' ? `'${param.replace(/'/g, "''")}'` : param;
    });
  }
  
  // XSS Prevention
  static escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // CSRF Protection
  static generateCSRFToken(): string {
    return crypto.getRandomValues(new Uint8Array(32))
      .reduce((acc, val) => acc + val.toString(16).padStart(2, '0'), '');
  }
  
  // Authentication Validation
  static validateToken(token: string): boolean {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      return decoded && decoded.exp > Date.now() / 1000;
    } catch (error) {
      return false;
    }
  }
}
```

#### Security Headers
```typescript
// Security Headers Configuration
const securityHeaders = {
  'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'X-XSS-Protection': '1; mode=block',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
};

// Apply security headers middleware
app.use((req, res, next) => {
  Object.entries(securityHeaders).forEach(([header, value]) => {
    res.setHeader(header, value);
  });
  next();
});
```

### 📋 Security Testing Checklist

#### Pre-Security Testing
- [ ] Security requirements defined
- [ ] Security tools configured
- [ ] Test environment prepared
- [ ] Security test data created
- [ ] Access credentials prepared

#### Automated Security Testing
- [ ] OWASP ZAP scan completed
- [ ] Snyk dependency scan completed
- [ ] SonarQube security analysis completed
- [ ] Automated vulnerability assessment completed
- [ ] Security metrics collected

#### Manual Security Testing
- [ ] Authentication testing completed
- [ ] Authorization testing completed
- [ ] Input validation testing completed
- [ ] Session management testing completed
- [ ] API security testing completed

#### Post-Security Testing
- [ ] Vulnerabilities documented
- [ ] Risk assessment completed
- [ ] Remediation plan created
- [ ] Security report generated
- [ ] Follow-up testing scheduled

### 🎯 Security Testing Success Criteria

#### Vulnerability Management
- **Critical Vulnerabilities**: 0
- **High Vulnerabilities**: < 5
- **Medium Vulnerabilities**: < 10
- **Low Vulnerabilities**: < 20

#### Security Compliance
- **OWASP Top 10 Coverage**: 100%
- **Security Policy Compliance**: 100%
- **Data Protection Compliance**: 100%
- **Authentication Security**: 100%

#### Security Metrics
- **Vulnerability Detection Rate**: > 95%
- **False Positive Rate**: < 5%
- **Security Test Coverage**: 100%
- **Remediation Time**: < 48 hours

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
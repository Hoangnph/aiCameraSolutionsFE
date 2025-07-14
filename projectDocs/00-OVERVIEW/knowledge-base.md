# Knowledge Base
## AI Camera Counting System

### 📊 Tổng quan

Knowledge base này chứa các thông tin quan trọng, troubleshooting guides, best practices, và solutions cho các vấn đề thường gặp trong dự án AI Camera Counting System.

### 🎯 Knowledge Base Objectives
- Centralize common knowledge và solutions
- Accelerate problem resolution
- Share best practices và lessons learned
- Support team onboarding và training

### 🔍 Quick Reference

#### System Architecture
```mermaid
graph TB
    subgraph "Frontend"
        A[React App] --> B[Authentication]
        A --> C[Camera Dashboard]
        A --> D[Real-time Display]
    end
    
    subgraph "Backend Services"
        E[beAuth - Node.js] --> F[PostgreSQL]
        E --> G[Redis]
        H[beCamera - Python/FastAPI] --> I[AI Model]
        H --> F
        H --> G
    end
    
    subgraph "Infrastructure"
        J[Docker] --> K[Shared Resources]
        L[Monitoring] --> M[Prometheus/Grafana]
    end
```

#### Service Endpoints
```yaml
# Core Service URLs
services:
  frontend: "http://localhost:3000"
  beAuth: "http://localhost:3001"
  beCamera: "http://localhost:8000"
  postgres: "localhost:5432"
  redis: "localhost:6379"
  prometheus: "http://localhost:9090"
  grafana: "http://localhost:3000"

# Health Check Endpoints
health_checks:
  frontend: "/health"
  beAuth: "/api/health"
  beCamera: "/health"
  postgres: "Database connection"
  redis: "Redis connection"
```

### 🚨 Common Issues & Solutions

#### Infrastructure Issues

**Issue 1: Docker containers not starting**
```bash
# Problem: Containers fail to start
# Solution: Check Docker resources and logs

# Diagnostic commands
docker ps -a                    # Check container status
docker logs <container_name>    # View container logs
docker system prune             # Clean up Docker resources

# Common fixes
docker-compose down             # Stop all containers
docker-compose up -d           # Restart containers
docker volume prune             # Clean up volumes
```

**Issue 2: Database connection errors**
```bash
# Problem: Services can't connect to PostgreSQL/Redis
# Solution: Verify database connectivity

# Check PostgreSQL
docker exec -it postgres psql -U postgres -d aicamera
# Expected: PostgreSQL prompt

# Check Redis
docker exec -it redis redis-cli ping
# Expected: PONG

# Check service connections
curl http://localhost:3001/api/health
curl http://localhost:8000/health
```

**Issue 3: Port conflicts**
```bash
# Problem: Port already in use
# Solution: Find and kill conflicting processes

# Find process using port
lsof -i :3000    # Frontend port
lsof -i :3001    # beAuth port
lsof -i :8000    # beCamera port

# Kill process
kill -9 <PID>    # Replace <PID> with actual process ID
```

#### Development Issues

**Issue 4: Node modules not installing**
```bash
# Problem: npm install fails
# Solution: Clear cache and reinstall

npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue 5: Python dependencies issues**
```bash
# Problem: pip install fails
# Solution: Use virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Issue 6: TypeScript compilation errors**
```bash
# Problem: TypeScript errors
# Solution: Check types and configurations

npx tsc --noEmit              # Check for type errors
npm run type-check            # Run type checking
npm run lint                  # Run linting
```

#### Testing Issues

**Issue 7: Tests failing intermittently**
```bash
# Problem: Flaky tests
# Solution: Improve test stability

# Add retry logic
jest --retryTimes 3

# Increase timeout
jest --testTimeout 10000

# Run tests in isolation
jest --runInBand
```

**Issue 8: E2E tests timing out**
```bash
# Problem: Playwright tests timeout
# Solution: Adjust timeouts and wait strategies

# Increase timeout in playwright.config.js
timeout: 30000

# Use proper wait strategies
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-testid="element"]');
```

### 🛠️ Development Workflows

#### Setting Up Development Environment
```bash
# 1. Clone repository
git clone <repository-url>
cd feMain

# 2. Start infrastructure
cd beAuth
docker-compose up -d

# 3. Start services
# Terminal 1 - Frontend
npm install
npm start

# Terminal 2 - beAuth
cd beAuth
npm install
npm run dev

# Terminal 3 - beCamera
cd beCamera
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Code Review Process
```yaml
# Code Review Checklist
review_checklist:
  functionality:
    - [ ] Code works as expected
    - [ ] No breaking changes
    - [ ] Error handling implemented
    - [ ] Edge cases considered
  
  quality:
    - [ ] Follows coding standards
    - [ ] Proper documentation
    - [ ] No code smells
    - [ ] Performance considered
  
  testing:
    - [ ] Unit tests written
    - [ ] Tests pass
    - [ ] Coverage adequate
    - [ ] Integration tests updated
  
  security:
    - [ ] No security vulnerabilities
    - [ ] Input validation
    - [ ] Authentication/authorization
    - [ ] Data protection
```

#### Deployment Process
```bash
# 1. Pre-deployment checks
npm run test
npm run lint
npm run build

# 2. Security scan
npm audit
snyk test

# 3. Performance check
npm run build:analyze

# 4. Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### 📊 Monitoring & Debugging

#### Application Monitoring
```yaml
# Key Metrics to Monitor
system_metrics:
  performance:
    - response_time: "< 200ms"
    - throughput: "> 1000 req/s"
    - error_rate: "< 1%"
    - cpu_usage: "< 80%"
    - memory_usage: "< 2GB"
  
  business_metrics:
    - active_cameras: "Number of active cameras"
    - total_counts: "Total count data"
    - user_sessions: "Active user sessions"
    - ai_accuracy: "Model accuracy rate"
```

#### Debugging Tools
```yaml
# Debugging Commands
frontend_debugging:
  - "React Developer Tools"
  - "Redux DevTools"
  - "Network tab in browser"
  - "Console logging"

backend_debugging:
  - "Postman for API testing"
  - "Database query logging"
  - "Application logs"
  - "Performance profiling"

infrastructure_debugging:
  - "Docker logs"
  - "System resource monitoring"
  - "Network connectivity tests"
  - "Service health checks"
```

### 🔧 Configuration Management

#### Environment Variables
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:3001
REACT_APP_CAMERA_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development

# beAuth (.env)
PORT=3001
DATABASE_URL=postgresql://postgres:password@localhost:5432/aicamera
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key

# beCamera (.env)
DATABASE_URL=postgresql://postgres:password@localhost:5432/aicamera
REDIS_URL=redis://localhost:6379
AI_MODEL_PATH=/path/to/model
```

#### Docker Configuration
```yaml
# docker-compose.yml structure
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: aicamera
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

### 📚 Best Practices

#### Code Organization
```typescript
// Frontend Structure
src/
├── components/          # Reusable components
│   ├── common/         # Shared components
│   ├── forms/          # Form components
│   └── layout/         # Layout components
├── pages/              # Page components
├── services/           # API services
├── hooks/              # Custom hooks
├── utils/              # Utility functions
├── types/              # TypeScript types
└── context/            # React context

// Backend Structure
src/
├── routes/             # API routes
├── middleware/         # Middleware functions
├── services/           # Business logic
├── models/             # Data models
├── utils/              # Utility functions
└── config/             # Configuration
```

#### Testing Strategy
```yaml
# Testing Pyramid
testing_pyramid:
  unit_tests: "70% - Fast, isolated tests"
  integration_tests: "20% - Service integration"
  e2e_tests: "10% - User journey tests"

# Test Naming Convention
test_naming:
  pattern: "describe('Component/Function', () => { it('should do something', () => {}) })"
  examples:
    - "describe('CameraCard', () => { it('should display camera information', () => {}) })"
    - "describe('authService', () => { it('should authenticate user', () => {}) })"
```

#### Performance Optimization
```typescript
// Frontend Optimization
const optimizationTechniques = {
  codeSplitting: "Use React.lazy() for route-based splitting",
  memoization: "Use React.memo() and useMemo()",
  imageOptimization: "Use WebP format and lazy loading",
  bundleAnalysis: "Use webpack-bundle-analyzer"
};

// Backend Optimization
const backendOptimization = {
  caching: "Use Redis for session and data caching",
  database: "Optimize queries and use indexes",
  asyncProcessing: "Use background jobs for heavy tasks",
  compression: "Enable gzip compression"
};
```

### 🔒 Security Guidelines

#### Authentication & Authorization
```typescript
// JWT Token Management
const tokenManagement = {
  expiration: "24 hours",
  refreshStrategy: "Rotate tokens on refresh",
  storage: "HttpOnly cookies for security",
  validation: "Verify token on each request"
};

// Input Validation
const inputValidation = {
  sanitization: "Sanitize all user inputs",
  validation: "Use Pydantic for API validation",
  sqlInjection: "Use parameterized queries",
  xss: "Escape HTML content"
};
```

#### Data Protection
```yaml
# Data Security Measures
data_protection:
  encryption:
    - "Encrypt data at rest"
    - "Use HTTPS for data in transit"
    - "Hash passwords with bcrypt"
  
  access_control:
    - "Role-based access control"
    - "Principle of least privilege"
    - "Regular access reviews"
  
  monitoring:
    - "Log all authentication attempts"
    - "Monitor for suspicious activity"
    - "Regular security audits"
```

### 📈 Performance Guidelines

#### Frontend Performance
```typescript
// Performance Best Practices
const frontendPerformance = {
  loading: "Implement lazy loading",
  caching: "Use service workers for caching",
  optimization: "Minimize bundle size",
  monitoring: "Track Core Web Vitals"
};

// Core Web Vitals Targets
const webVitals = {
  lcp: "< 2.5 seconds",      // Largest Contentful Paint
  fid: "< 100 milliseconds",  // First Input Delay
  cls: "< 0.1"               // Cumulative Layout Shift
};
```

#### Backend Performance
```python
# Performance Optimization
performance_optimization = {
    "database": "Use connection pooling and query optimization",
    "caching": "Implement Redis caching for frequently accessed data",
    "async": "Use async/await for I/O operations",
    "monitoring": "Track response times and error rates"
}
```

### 🚀 Deployment Guidelines

#### Production Checklist
```yaml
# Pre-deployment Checklist
pre_deployment:
  code_quality:
    - [ ] All tests passing
    - [ ] Code review completed
    - [ ] Security scan passed
    - [ ] Performance benchmarks met
  
  documentation:
    - [ ] API documentation updated
    - [ ] Deployment notes prepared
    - [ ] Rollback plan ready
  
  infrastructure:
    - [ ] Environment variables configured
    - [ ] Database migrations applied
    - [ ] Monitoring configured
    - [ ] Backup procedures tested
```

#### Rollback Procedures
```bash
# Rollback Commands
# 1. Identify previous version
git log --oneline -10

# 2. Rollback to previous version
git revert <commit-hash>

# 3. Deploy rollback
docker-compose down
docker-compose up -d

# 4. Verify rollback
curl http://localhost:3001/api/health
curl http://localhost:8000/health
```

### 📞 Support & Escalation

#### Support Channels
```yaml
# Support Matrix
support_channels:
  development_issues:
    - "Team chat for quick questions"
    - "GitHub issues for bugs"
    - "Code review for improvements"
  
  infrastructure_issues:
    - "DevOps team for deployment"
    - "System administrator for hardware"
    - "Cloud provider support"
  
  user_issues:
    - "Help desk for user support"
    - "Documentation for self-service"
    - "Training sessions for users"
```

#### Escalation Procedures
```yaml
# Escalation Levels
escalation_levels:
  level_1:
    - "Team lead for technical issues"
    - "Response time: 4 hours"
  
  level_2:
    - "Project manager for process issues"
    - "Response time: 24 hours"
  
  level_3:
    - "Stakeholder for business issues"
    - "Response time: 48 hours"
```

### 📋 Maintenance Schedule

#### Regular Maintenance Tasks
```yaml
# Maintenance Schedule
daily:
  - "Check system health"
  - "Review error logs"
  - "Monitor performance metrics"

weekly:
  - "Update dependencies"
  - "Review security alerts"
  - "Backup verification"

monthly:
  - "Performance optimization"
  - "Security audit"
  - "Documentation review"

quarterly:
  - "Major system updates"
  - "Comprehensive testing"
  - "Team training"
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
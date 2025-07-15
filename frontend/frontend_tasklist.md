# 📋 **FRONTEND MIGRATION TASKLIST**

## 🎯 **MỤC TIÊU**
Di chuyển toàn bộ code và cấu hình frontend từ thư mục root vào thư mục `frontend/` để tối ưu hóa cấu trúc dự án và dễ dàng quản lý.

---

## 📊 **PHÂN TÍCH HIỆN TẠI**

### **🏗️ Cấu trúc Frontend hiện tại (ở root)**
```
feMain/ (root)
├── src/                    # Source code chính
│   ├── App.js             # Main application component
│   ├── index.js           # Entry point
│   ├── routes.js          # Route definitions
│   ├── components/        # Reusable components
│   ├── context/           # React context
│   ├── layouts/           # Layout components
│   ├── services/          # API services
│   ├── assets/            # Static assets
│   ├── examples/          # Example components
│   └── variables/         # Global variables
├── public/                # Public assets
│   ├── index.html         # Main HTML file
│   ├── favicon.png        # Favicon
│   ├── apple-icon.png     # Apple icon
│   ├── manifest.json      # PWA manifest
│   └── robots.txt         # SEO robots
├── package.json           # Dependencies & scripts
├── package-lock.json      # Locked dependencies
├── jsconfig.json          # JavaScript config
├── .eslintrc.json         # ESLint config
├── .prettierrc.json       # Prettier config
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
├── Dockerfile.frontend.dev # Frontend Docker dev
├── Dockerfile.prod        # Production Docker
├── docker-compose.dev.yml # Dev environment
├── docker-compose.prod.yml # Prod environment
└── genezio.yaml           # Genezio config
```

### **🎯 Cấu trúc mục tiêu**
```
feMain/ (root)
├── frontend/              # Frontend application
│   ├── src/              # Source code
│   ├── public/           # Public assets
│   ├── package.json      # Frontend dependencies
│   ├── package-lock.json # Locked dependencies
│   ├── jsconfig.json     # JavaScript config
│   ├── .eslintrc.json    # ESLint config
│   ├── .prettierrc.json  # Prettier config
│   ├── .env              # Frontend environment
│   ├── .gitignore        # Frontend git ignore
│   ├── Dockerfile.dev    # Frontend Docker dev
│   ├── Dockerfile.prod   # Frontend Docker prod
│   └── README.md         # Frontend documentation
├── beAuth/               # Authentication service
├── beCamera/             # Camera service
├── sharedResource/       # Shared resources
├── projectDocs/          # Project documentation
├── docker-compose.dev.yml # Main dev environment
├── docker-compose.prod.yml # Main prod environment
└── README.md             # Main project README
```

---

## 🚨 **ĐIỂM CẦN CHÚ Ý QUAN TRỌNG**

### **⚠️ Files cấu hình quan trọng cần cập nhật**
1. **Docker Compose files** - Cần cập nhật build context và volume mappings
2. **CI/CD Pipeline** - GitHub Actions cần cập nhật paths
3. **Nginx Configuration** - Cần cập nhật upstream references
4. **Monitoring Config** - Prometheus và Grafana configs
5. **Security Config** - Security policy references
6. **Documentation** - Tất cả docs cần cập nhật paths

### **🔗 External References đã phát hiện**
- `docker-compose.dev.yml` - Frontend service build context
- `docker-compose.prod.yml` - Frontend service configuration
- `.github/workflows/ci-cd.yml` - Frontend build and test steps
- `projectDocs/06-DEPLOYMENT/nginx-configurations/nginx.conf` - Upstream frontend
- `projectDocs/08-MONITORING/configurations/prometheus.yml` - Frontend metrics
- `projectDocs/09-SECURITY/configurations/security-config.yml` - Frontend security
- `sharedResource/README.md` - Service URLs and development guides

---

## 📋 **DANH SÁCH TASKS**

### **🔄 PHASE 1: PREPARATION (CHUẨN BỊ)**

#### **1.1 Backup & Analysis**
- [ ] **Backup current structure**
  - [ ] Create backup of entire root directory
  - [ ] Document current working state
  - [ ] Test current frontend functionality
  - [ ] **CRITICAL**: Test current Docker setup

- [ ] **Analyze dependencies**
  - [ ] Review package.json dependencies
  - [ ] Check import paths in source code
  - [ ] Identify external references
  - [ ] Document internal links and references
  - [ ] **CRITICAL**: Document all Docker volume mappings

#### **1.2 Create Frontend Directory Structure**
- [ ] **Create frontend directory**
  - [ ] Create `frontend/` directory
  - [ ] Set up proper permissions
  - [ ] Initialize git tracking (if needed)

### **📁 PHASE 2: MIGRATION (DI CHUYỂN)**

#### **2.1 Core Source Code Migration**
- [ ] **Move source code**
  - [ ] Move `src/` → `frontend/src/`
  - [ ] Move `public/` → `frontend/public/`
  - [ ] Verify all files moved correctly
  - [ ] Check file permissions
  - [ ] **CRITICAL**: Verify no files left behind

#### **2.2 Configuration Files Migration**
- [ ] **Move configuration files**
  - [ ] Move `package.json` → `frontend/package.json`
  - [ ] Move `package-lock.json` → `frontend/package-lock.json`
  - [ ] Move `jsconfig.json` → `frontend/jsconfig.json`
  - [ ] Move `.eslintrc.json` → `frontend/.eslintrc.json`
  - [ ] Move `.prettierrc.json` → `frontend/.prettierrc.json`
  - [ ] Move `.env` → `frontend/.env`
  - [ ] Move `.gitignore` → `frontend/.gitignore`
  - [ ] **CRITICAL**: Verify .env contains correct API URLs

#### **2.3 Docker Configuration Migration**
- [ ] **Move Docker files**
  - [ ] Move `Dockerfile.frontend.dev` → `frontend/Dockerfile.dev`
  - [ ] Move `Dockerfile.prod` → `frontend/Dockerfile.prod`
  - [ ] Update Dockerfile paths and references
  - [ ] Test Docker builds
  - [ ] **CRITICAL**: Update WORKDIR and COPY paths in Dockerfiles

#### **2.4 Other Configuration Files**
- [ ] **Move other configs**
  - [ ] Move `genezio.yaml` → `frontend/genezio.yaml` (if frontend-specific)
  - [ ] Create `frontend/README.md`
  - [ ] Update any frontend-specific documentation

### **🔧 PHASE 3: CONFIGURATION UPDATE (CẬP NHẬT CẤU HÌNH)**

#### **3.1 Update Import Paths**
- [ ] **Fix internal imports**
  - [ ] Update all relative imports in source code
  - [ ] Fix component import paths
  - [ ] Update service import paths
  - [ ] Update asset import paths
  - [ ] **CRITICAL**: Test all imports work after move

#### **3.2 Update Configuration Files**
- [ ] **Update package.json**
  - [ ] Update build scripts paths
  - [ ] Update test scripts paths
  - [ ] Update any absolute paths
  - [ ] **CRITICAL**: Verify scripts work from frontend directory

- [ ] **Update jsconfig.json**
  - [ ] Update baseUrl and paths
  - [ ] Update include/exclude patterns
  - [ ] **CRITICAL**: Test path resolution works

- [ ] **Update .env file**
  - [ ] Verify environment variables
  - [ ] Update any path references
  - [ ] **CRITICAL**: Ensure API URLs are correct

#### **3.3 Update Docker Configuration**
- [ ] **Update Dockerfiles**
  - [ ] Update WORKDIR paths
  - [ ] Update COPY paths
  - [ ] Update build context
  - [ ] **CRITICAL**: Test Docker builds work

- [ ] **Update docker-compose files**
  - [ ] Update frontend service paths in `docker-compose.dev.yml`
  - [ ] Update frontend service paths in `docker-compose.prod.yml`
  - [ ] Update volume mappings
  - [ ] Update build contexts
  - [ ] **CRITICAL**: Test docker-compose up works

### **🔗 PHASE 4: EXTERNAL REFERENCES UPDATE (CẬP NHẬT THAM CHIẾU)**

#### **4.1 Update Documentation References**
- [ ] **Update projectDocs references**
  - [ ] Update frontend documentation paths
  - [ ] Update API documentation references
  - [ ] Update deployment guides
  - [ ] **CRITICAL**: Update nginx configuration

- [ ] **Update sharedResource references**
  - [ ] Update sharedResource/README.md
  - [ ] Update service URLs and paths
  - [ ] Update development guides

#### **4.2 Update Main Project Files**
- [ ] **Update root README.md**
  - [ ] Update frontend directory references
  - [ ] Update development instructions
  - [ ] Update project structure diagram

- [ ] **Update other root files**
  - [ ] Update any scripts that reference frontend
  - [ ] Update CI/CD configurations
  - [ ] Update deployment scripts
  - [ ] **CRITICAL**: Update GitHub Actions workflow

### **🧪 PHASE 5: TESTING & VALIDATION (KIỂM THỬ)**

#### **5.1 Local Development Testing**
- [ ] **Test frontend development**
  - [ ] `cd frontend && npm install`
  - [ ] `npm start` - Test development server
  - [ ] Test all pages and components
  - [ ] Test API integrations
  - [ ] Test authentication flow
  - [ ] **CRITICAL**: Test hot reload works
  - [ ] **CRITICAL**: Test all routes work

#### **5.2 Build Testing**
- [ ] **Test production build**
  - [ ] `npm run build` - Test build process
  - [ ] Verify build output
  - [ ] Test build artifacts
  - [ ] **CRITICAL**: Test build from frontend directory
  - [ ] **CRITICAL**: Verify static assets are correct

#### **5.3 Docker Testing**
- [ ] **Test Docker builds**
  - [ ] Test development Docker build
  - [ ] Test production Docker build
  - [ ] Test docker-compose integration
  - [ ] **CRITICAL**: Test volume mappings work
  - [ ] **CRITICAL**: Test hot reload in Docker

#### **5.4 Integration Testing**
- [ ] **Test with backend services**
  - [ ] Test with beAuth service
  - [ ] Test with beCamera service
  - [ ] Test database connections
  - [ ] Test WebSocket connections
  - [ ] **CRITICAL**: Test API endpoints work
  - [ ] **CRITICAL**: Test authentication flow

#### **5.5 Comprehensive Testing Checklist**
- [ ] **Functionality Tests**
  - [ ] Login/Logout functionality
  - [ ] Dashboard loading
  - [ ] Camera management
  - [ ] Analytics display
  - [ ] Profile management
  - [ ] Settings configuration

- [ ] **API Integration Tests**
  - [ ] Authentication API calls
  - [ ] Camera API calls
  - [ ] Analytics API calls
  - [ ] WebSocket connections
  - [ ] Error handling

- [ ] **UI/UX Tests**
  - [ ] Responsive design
  - [ ] Component rendering
  - [ ] Navigation flow
  - [ ] Form submissions
  - [ ] Data display

- [ ] **Performance Tests**
  - [ ] Page load times
  - [ ] Bundle size
  - [ ] Memory usage
  - [ ] Network requests

- [ ] **Browser Compatibility**
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
  - [ ] Edge

### **📝 PHASE 6: DOCUMENTATION & CLEANUP (TÀI LIỆU & DỌN DẸP)**

#### **6.1 Create Frontend Documentation**
- [ ] **Create frontend README.md**
  - [ ] Development setup instructions
  - [ ] Build and deployment instructions
  - [ ] API integration guide
  - [ ] Troubleshooting guide
  - [ ] **CRITICAL**: Environment setup guide

#### **6.2 Update Project Documentation**
- [ ] **Update main project docs**
  - [ ] Update projectDocs structure
  - [ ] Update sharedResource README
  - [ ] Update deployment guides
  - [ ] **CRITICAL**: Update all path references

#### **6.3 Cleanup**
- [ ] **Remove old files**
  - [ ] Remove old frontend files from root
  - [ ] Clean up any orphaned references
  - [ ] Update .gitignore if needed
  - [ ] **CRITICAL**: Verify no broken links

---

## 🚨 **RISK ASSESSMENT & MITIGATION**

### **⚠️ Potential Risks**
1. **Broken imports** - Internal references may break
2. **Docker build failures** - Path changes may affect builds
3. **Environment issues** - Environment variables may need updates
4. **Documentation inconsistencies** - External references may be outdated
5. **CI/CD pipeline failures** - GitHub Actions may break
6. **Nginx configuration issues** - Upstream references may fail
7. **Volume mapping issues** - Docker volumes may not work

### **🛡️ Mitigation Strategies**
1. **Comprehensive testing** - Test all functionality after migration
2. **Backup strategy** - Keep backup of original structure
3. **Incremental approach** - Move files in logical groups
4. **Documentation updates** - Update all references systematically
5. **Rollback plan** - Ability to revert if issues occur
6. **Team communication** - Notify team of changes

---

## 📅 **TIMELINE ESTIMATE**

### **Phase 1: Preparation** - 45 minutes
### **Phase 2: Migration** - 60 minutes
### **Phase 3: Configuration Update** - 90 minutes
### **Phase 4: External References Update** - 60 minutes
### **Phase 5: Testing & Validation** - 120 minutes
### **Phase 6: Documentation & Cleanup** - 45 minutes

**Total Estimated Time**: 6 hours

---

## ✅ **SUCCESS CRITERIA**

### **Functional Requirements**
- [ ] Frontend starts successfully with `npm start`
- [ ] All pages load correctly
- [ ] API integrations work properly
- [ ] Authentication flow works
- [ ] Build process completes successfully
- [ ] Docker builds work correctly
- [ ] **CRITICAL**: All routes work correctly
- [ ] **CRITICAL**: Hot reload works in development
- [ ] **CRITICAL**: Production build works

### **Structural Requirements**
- [ ] All frontend code is in `frontend/` directory
- [ ] No broken imports or references
- [ ] Documentation is updated and accurate
- [ ] Development workflow is maintained
- [ ] Deployment process works correctly
- [ ] **CRITICAL**: Docker compose works
- [ ] **CRITICAL**: CI/CD pipeline works
- [ ] **CRITICAL**: Nginx configuration works

### **Testing Requirements**
- [ ] All functionality tests pass
- [ ] All API integration tests pass
- [ ] All UI/UX tests pass
- [ ] All performance tests pass
- [ ] All browser compatibility tests pass
- [ ] **CRITICAL**: No console errors
- [ ] **CRITICAL**: No network errors
- [ ] **CRITICAL**: No build warnings

---

## 📋 **CHECKLIST**

### **Pre-Migration**
- [ ] Backup current structure
- [ ] Document current state
- [ ] Test current functionality
- [ ] Create frontend directory
- [ ] **CRITICAL**: Test current Docker setup

### **Migration**
- [ ] Move source code
- [ ] Move configuration files
- [ ] Move Docker files
- [ ] Update import paths
- [ ] Update configuration files
- [ ] Update external references
- [ ] **CRITICAL**: Update Docker compose files
- [ ] **CRITICAL**: Update CI/CD pipeline

### **Post-Migration**
- [ ] Test development environment
- [ ] Test build process
- [ ] Test Docker builds
- [ ] Test integration with backend
- [ ] Update documentation
- [ ] Clean up old files
- [ ] **CRITICAL**: Test all functionality
- [ ] **CRITICAL**: Test all API integrations
- [ ] **CRITICAL**: Test all routes
- [ ] **CRITICAL**: Test authentication flow

---

## 🔧 **TROUBLESHOOTING GUIDE**

### **Common Issues & Solutions**
1. **Import errors** - Check jsconfig.json paths
2. **Docker build failures** - Verify Dockerfile paths
3. **API connection issues** - Check .env file
4. **Hot reload not working** - Check volume mappings
5. **Build failures** - Check package.json scripts

### **Rollback Procedure**
1. Stop all services
2. Restore backup
3. Update all references back
4. Test functionality
5. Document issues

---

**📅 Created**: [Ngày tạo]  
**👥 Assignee**: Product Owner  
**📊 Status**: Ready to Start  
**�� Priority**: High 
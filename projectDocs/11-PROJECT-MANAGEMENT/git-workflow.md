# Git Workflow Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa Git workflow và best practices cho team development, bao gồm branch strategy, commit conventions, PR process, và code review guidelines.

### 🎯 Mục tiêu
- Đảm bảo code quality và consistency
- Tối ưu hóa collaboration giữa team members
- Giảm thiểu conflicts và merge issues
- Tăng tốc độ development và deployment

### 🌿 Branch Strategy

#### Git Flow Model
```bash
# Main branches
main                    # Production-ready code
develop                 # Integration branch for features

# Supporting branches
feature/feature-name    # New features
bugfix/bug-description  # Bug fixes
hotfix/urgent-fix      # Critical production fixes
release/version-number  # Release preparation
```

#### Branch Naming Conventions
```bash
# Feature branches
feature/user-authentication
feature/camera-counting
feature/real-time-analytics
feature/admin-dashboard

# Bug fix branches
bugfix/login-validation-error
bugfix/camera-feed-display
bugfix/api-timeout-issue

# Hotfix branches
hotfix/security-vulnerability
hotfix/critical-api-failure
hotfix/database-connection-issue

# Release branches
release/v1.0.0
release/v1.1.0
release/v2.0.0
```

### 📝 Commit Conventions

#### Conventional Commits
```bash
# Format: <type>(<scope>): <description>

# Types
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation changes
style:    # Code style changes (formatting, etc.)
refactor: # Code refactoring
test:     # Adding or updating tests
chore:    # Maintenance tasks

# Examples
feat(auth): add JWT token validation
fix(camera): resolve real-time feed lag issue
docs(api): update authentication endpoint documentation
style(frontend): format component files with prettier
refactor(backend): optimize database queries
test(integration): add camera API integration tests
chore(deps): update dependencies to latest versions
```

#### Commit Message Template
```bash
# .gitmessage template
# <type>(<scope>): <description>
#
# [optional body]
#
# [optional footer(s)]
#
# Examples:
# feat(auth): add JWT token validation
# fix(camera): resolve real-time feed lag issue
# docs(api): update authentication endpoint documentation
```

### 🔄 Pull Request Process

#### PR Template
```markdown
<!-- .github/pull_request_template.md -->
## 📋 Description
<!-- Provide a brief description of the changes -->

## 🎯 Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## 🔗 Related Issues
<!-- Link to related issues -->
Closes #123
Related to #456

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed
- [ ] Code coverage maintained/improved

## 📸 Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## 📋 Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is self-documenting
- [ ] No console errors or warnings
- [ ] Performance impact considered
- [ ] Security implications reviewed

## 🚀 Deployment Notes
<!-- Any special deployment considerations -->
```

#### PR Review Checklist
```markdown
## Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] No breaking changes introduced
- [ ] Error handling is appropriate
- [ ] Edge cases are handled

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] No code duplication
- [ ] Follows DRY principle

### Testing
- [ ] Tests are comprehensive
- [ ] Test coverage is adequate
- [ ] Tests are meaningful and not flaky
- [ ] Integration tests included where needed

### Security
- [ ] No security vulnerabilities introduced
- [ ] Input validation is proper
- [ ] Authentication/authorization is correct
- [ ] Sensitive data is handled securely

### Performance
- [ ] No performance regressions
- [ ] Database queries are optimized
- [ ] API responses are efficient
- [ ] Frontend performance is maintained

### Documentation
- [ ] Code is self-documenting
- [ ] Comments added for complex logic
- [ ] API documentation updated if needed
- [ ] README updated if needed
```

### 🔍 Code Review Guidelines

#### Review Process
```bash
# 1. Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat(feature): implement new functionality"

# 3. Push and create PR
git push origin feature/new-feature
# Create PR on GitHub/GitLab

# 4. Address review comments
git add .
git commit -m "fix(feature): address review comments"
git push origin feature/new-feature

# 5. Merge after approval
git checkout develop
git pull origin develop
git merge feature/new-feature
git push origin develop
```

#### Review Best Practices
```markdown
## Review Guidelines

### For Reviewers
- Be constructive and respectful
- Focus on code quality and functionality
- Ask questions rather than making assumptions
- Suggest improvements, don't just point out issues
- Consider the bigger picture and long-term maintainability

### For Authors
- Keep PRs small and focused
- Respond to all review comments
- Be open to feedback and suggestions
- Explain complex decisions in comments
- Update documentation as needed

### Review Priorities
1. **Security**: Check for vulnerabilities
2. **Functionality**: Ensure code works correctly
3. **Performance**: Look for optimization opportunities
4. **Maintainability**: Consider long-term code health
5. **Testing**: Verify adequate test coverage
```

### 🚀 Release Process

#### Release Workflow
```bash
# 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. Update version numbers
# Update package.json, requirements.txt, etc.

# 3. Update changelog
# Add release notes to CHANGELOG.md

# 4. Create PR for release
git add .
git commit -m "chore(release): prepare v1.2.0"
git push origin release/v1.2.0

# 5. After approval, merge to main
git checkout main
git pull origin main
git merge release/v1.2.0
git tag v1.2.0
git push origin main
git push origin v1.2.0

# 6. Merge back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 7. Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

#### Hotfix Process
```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# 2. Make minimal fix
git add .
git commit -m "fix(security): patch critical vulnerability"

# 3. Create PR and merge to main
git push origin hotfix/critical-security-fix
# Create PR, review, merge

# 4. Tag release
git checkout main
git pull origin main
git tag v1.2.1
git push origin v1.2.1

# 5. Merge to develop
git checkout develop
git merge hotfix/critical-security-fix
git push origin develop

# 6. Delete hotfix branch
git branch -d hotfix/critical-security-fix
git push origin --delete hotfix/critical-security-fix
```

### 🔧 Git Configuration

#### Global Git Config
```bash
# Setup user information
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Setup default branch
git config --global init.defaultBranch main

# Setup commit template
git config --global commit.template .gitmessage

# Setup aliases for common commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate"
```

#### Repository-Specific Config
```bash
# .gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Build outputs
dist/
build/
*.egg-info/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment files
.env
.env.local
.env.development
.env.test
.env.production

# Coverage reports
coverage/
.coverage
htmlcov/

# Test outputs
.pytest_cache/
```

### 📊 Git Hooks

#### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Run linting
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Linting failed"
    exit 1
fi

# Run type checking
npm run type-check
if [ $? -ne 0 ]; then
    echo "❌ Type checking failed"
    exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✅ Pre-commit checks passed"
```

#### Commit-msg Hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

# Check commit message format
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format"
    echo "Expected format: <type>(<scope>): <description>"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    exit 1
fi

echo "✅ Commit message format is valid"
```

### 🔄 CI/CD Integration

#### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
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
    
    - name: Run tests
      run: npm test
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: echo "Deploy to production"
```

### 📈 Git Analytics

#### Useful Git Commands
```bash
# View commit history
git log --oneline --graph --decorate

# View file history
git log --follow filename

# View changes in last commit
git show HEAD

# View changes between branches
git diff develop..feature/new-feature

# View commit statistics
git log --stat

# View author statistics
git shortlog -sn

# View file blame
git blame filename

# View stash list
git stash list

# View remote branches
git branch -r

# View local branches
git branch -l
```

### 🚨 Conflict Resolution

#### Merge Conflict Resolution
```bash
# 1. Identify conflicted files
git status

# 2. Open conflicted files and resolve
# Look for <<<<<<< HEAD, =======, >>>>>>> markers

# 3. After resolving, add files
git add resolved-file.js

# 4. Complete merge
git commit -m "fix(merge): resolve conflicts in feature branch"
```

#### Rebase Strategy
```bash
# Interactive rebase to clean up commits
git rebase -i HEAD~3

# Rebase feature branch on develop
git checkout feature/new-feature
git rebase develop

# Resolve conflicts during rebase
git add resolved-file.js
git rebase --continue
```

### 📋 Workflow Checklist

#### Daily Workflow
- [ ] Pull latest changes from remote
- [ ] Create feature branch for new work
- [ ] Make atomic commits with clear messages
- [ ] Push changes and create PR
- [ ] Respond to review comments promptly
- [ ] Keep branches up to date

#### Release Preparation
- [ ] Ensure all tests pass
- [ ] Update version numbers
- [ ] Update changelog
- [ ] Create release branch
- [ ] Perform final testing
- [ ] Merge to main and tag release
- [ ] Deploy to production
- [ ] Announce release

#### Emergency Procedures
- [ ] Create hotfix branch from main
- [ ] Make minimal fix
- [ ] Test thoroughly
- [ ] Merge to main immediately
- [ ] Deploy to production
- [ ] Merge back to develop
- [ ] Document incident

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
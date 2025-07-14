# Development Tools Setup Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn thiết lập môi trường development tools cho team dev, bao gồm IDE setup, linting, formatting, pre-commit hooks, và các công cụ hỗ trợ development.

### 🎯 Mục tiêu
- Thiết lập môi trường development đồng nhất
- Đảm bảo code quality và consistency
- Tự động hóa code formatting và linting
- Tối ưu hóa developer experience

### 🛠️ IDE Setup

#### VS Code Configuration
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "javascript.preferences.importModuleSpecifier": "relative"
}
```

#### Recommended Extensions
```json
// .vscode/extensions.json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "ms-vscode.vscode-json",
    "yzhang.markdown-all-in-one",
    "ms-vscode.vscode-docker",
    "ms-azuretools.vscode-docker"
  ]
}
```

### 📦 Package Management

#### Frontend Dependencies
```json
// package.json - Development Dependencies
{
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-react": "^7.0.0",
    "eslint-plugin-react-hooks": "^4.0.0",
    "eslint-plugin-jsx-a11y": "^6.0.0",
    "prettier": "^3.0.0",
    "husky": "^8.0.0",
    "lint-staged": "^15.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "jest": "^29.0.0",
    "cypress": "^13.0.0"
  }
}
```

#### Backend Dependencies
```python
# requirements-dev.txt
# Development and Testing Dependencies
pytest==7.4.0
pytest-asyncio==0.21.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.0.0
mypy==1.5.0
pre-commit==3.3.0
bandit==1.7.5
safety==2.3.0
```

### 🔧 Linting & Formatting

#### ESLint Configuration
```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint', 'jsx-a11y'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    'jsx-a11y/anchor-is-valid': 'error',
    'jsx-a11y/alt-text': 'error',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

#### Prettier Configuration
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

#### Python Black Configuration
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### Flake8 Configuration
```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info,
    .venv,
    venv
```

### 🐕 Pre-commit Hooks

#### Frontend Pre-commit Setup
```json
// package.json - Scripts
{
  "scripts": {
    "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write src/**/*.{js,jsx,ts,tsx,json,css,md}",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "prepare": "husky install"
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm run format
npm run type-check
```

#### Backend Pre-commit Setup
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### 🧪 Testing Tools

#### Jest Configuration
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/serviceWorker.js',
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
};
```

#### Pytest Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
```

### 🔍 Code Quality Tools

#### TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src",
    "paths": {
      "@/*": ["*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules", "build", "dist"]
}
```

#### MyPy Configuration
```ini
# mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy.plugins.pydantic.*]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
warn_untyped_fields = True
```

### 🚀 Development Scripts

#### Frontend Scripts
```json
// package.json - Additional Scripts
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "analyze": "npm run build && npx vite-bundle-analyzer dist",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "chromatic": "npx chromatic --project-token=CHROMATIC_PROJECT_TOKEN"
  }
}
```

#### Backend Scripts
```python
# scripts/dev_setup.py
#!/usr/bin/env python3
"""Development environment setup script."""

import subprocess
import sys
from pathlib import Path

def run_command(command: str, cwd: Path = None) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}: {e.stderr}")
        return False

def setup_development_environment():
    """Setup development environment."""
    print("🚀 Setting up development environment...")
    
    # Install pre-commit hooks
    if not run_command("pre-commit install"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -r requirements-dev.txt"):
        return False
    
    # Run initial formatting
    if not run_command("black ."):
        return False
    
    # Run initial linting
    if not run_command("flake8 ."):
        return False
    
    print("✅ Development environment setup complete!")
    return True

if __name__ == "__main__":
    success = setup_development_environment()
    sys.exit(0 if success else 1)
```

### 🔧 IDE-Specific Setup

#### VS Code Workspace Settings
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Frontend",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/vite",
      "args": ["--port", "3000"],
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal"
    },
    {
      "name": "Launch Backend (Python)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/beCamera/src/main.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/beCamera/src"
      }
    }
  ]
}
```

#### PyCharm Configuration
```xml
<!-- .idea/runConfigurations/Backend.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Backend" type="PythonConfigurationType">
    <module name="beCamera" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONPATH" value="$PROJECT_DIR$/beCamera/src" />
    </envs>
    <option name="SDK_HOME" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/beCamera" />
    <option name="IS_MODULE_SDK" value="true" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <option name="SCRIPT_NAME" value="$PROJECT_DIR$/beCamera/src/main.py" />
    <option name="PARAMETERS" value="" />
    <option name="SHOW_COMMAND_LINE" value="false" />
    <option name="EMULATE_TERMINAL" value="false" />
    <option name="MODULE_MODE" value="false" />
    <option name="REDIRECT_INPUT" value="false" />
    <option name="INPUT_FILE" value="" />
    <method v="2" />
  </configuration>
</component>
```

### 📊 Code Quality Metrics

#### SonarQube Configuration
```yaml
# sonar-project.properties
sonar.projectKey=ai-camera-counting-system
sonar.projectName=AI Camera Counting System
sonar.projectVersion=1.0.0

sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/dist/**,**/build/**

# Coverage
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.python.coverage.reportPaths=coverage.xml

# Quality Gates
sonar.qualitygate.wait=true
```

### 🚨 Security Tools

#### Bandit Configuration
```yaml
# .bandit
exclude_dirs: ['tests', 'venv', '.venv']
skips: ['B101', 'B601']
```

#### Safety Configuration
```yaml
# .safety
# Ignore specific vulnerabilities if needed
# CVE-2023-1234: package_name==1.2.3
```

### 📋 Setup Checklist

#### Initial Setup
- [ ] Install Node.js (v18+) and npm
- [ ] Install Python (v3.9+) and pip
- [ ] Install Docker Desktop
- [ ] Install VS Code with recommended extensions
- [ ] Clone repository and install dependencies
- [ ] Setup pre-commit hooks
- [ ] Configure IDE settings
- [ ] Run initial linting and formatting
- [ ] Verify all tests pass

#### Daily Development
- [ ] Pull latest changes
- [ ] Run linting before committing
- [ ] Run tests before pushing
- [ ] Check code coverage
- [ ] Update dependencies as needed

#### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Security scan clean
- [ ] Documentation updated

### 🎯 Best Practices

#### Code Organization
- Use consistent file naming conventions
- Group related files in directories
- Keep functions small and focused
- Use meaningful variable names
- Add comments for complex logic

#### Git Workflow
- Write descriptive commit messages
- Use feature branches for new work
- Keep commits atomic and focused
- Review code before merging
- Update documentation with changes

#### Testing Strategy
- Write tests for new features
- Maintain high test coverage
- Use meaningful test names
- Mock external dependencies
- Test error conditions

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 
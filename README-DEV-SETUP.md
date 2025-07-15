# AI Camera Counting System - Development Setup

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### One-Command Setup
```bash
# Run the automated setup script
./setup-dev.sh
```

### Manual Setup (Alternative)
```bash
# 1. Start infrastructure
docker-compose -f docker-compose.dev.yml up -d postgres redis

# 2. Install dependencies
npm install
cd beAuth && npm install && cd ..
cd beCamera && pip install -r requirements.txt && cd ..

# 3. Setup database
cd beAuth && npm run migrate && npm run seed && cd ..

# 4. Start services
./start-dev.sh
```

## 📱 Service URLs
- **Frontend**: http://localhost:3000
- **beAuth API**: http://localhost:3001/api/v1
- **beCamera API**: http://localhost:3002/api/v1
- **WebSocket**: ws://localhost:3003

## 🔑 Default Credentials
- **Admin**: `admin` / `Admin123!`
- **User**: `testuser` / `Test123!`

## 📋 MVP Features
- ✅ Authentication (Login/Register)
- ✅ Dashboard Overview
- ✅ Camera Management
- ✅ Real-time Counting
- ✅ Basic Analytics

## 📚 Documentation
- **Project Tracking**: `projectLogs/tracking_project.md`
- **beAuth Docs**: `beAuth/README.md`
- **beCamera Docs**: `beCamera/docs/`

## 🛠️ Development Commands

### Start All Services
```bash
./start-dev.sh
```

### Start Individual Services
```bash
# Frontend
npm start

# beAuth Service
cd beAuth && npm run dev

# beCamera Service
cd beCamera && uvicorn main:app --reload --port 3002

# Infrastructure only
docker-compose -f docker-compose.dev.yml up -d postgres redis
```

### Database Operations
```bash
# Run migrations
cd beAuth && npm run migrate

# Seed data
cd beAuth && npm run seed

# Reset database
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d postgres redis
```

## 🔧 Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports 3000-3003 are available
2. **Database connection**: Ensure PostgreSQL container is running
3. **Dependencies**: Run `npm install` and `pip install -r requirements.txt`
4. **Permissions**: Make scripts executable with `chmod +x *.sh`

### Reset Everything
```bash
# Stop all services
docker-compose -f docker-compose.dev.yml down -v

# Remove node_modules
rm -rf node_modules beAuth/node_modules

# Remove Python venv
rm -rf beCamera/venv

# Re-run setup
./setup-dev.sh
```

## 📊 Project Structure
```
feMain/
├── src/                    # Frontend React app
├── beAuth/                 # Authentication service (Node.js)
├── beCamera/               # Camera processing service (Python)
├── projectLogs/            # Project tracking & documentation
├── docker-compose.dev.yml  # Development infrastructure
├── setup-dev.sh           # Automated setup script
└── start-dev.sh           # Service startup script
```

---

**Status**: Ready for MVP Development  
**Last Updated**: [Current Date] 
# AI Camera Counting System - Developer Guide

## 🚀 Quick Start (5 minutes)

### 1. Start Infrastructure
```bash
# Start shared resources (PostgreSQL, Redis)
cd beAuth
docker-compose up -d postgres redis
```

### 2. Start All Services
```bash
# Terminal 1: beAuth Service
cd beAuth && docker-compose up -d

# Terminal 2: beCamera Service
cd beCamera && docker-compose up -d

# Terminal 3: Frontend
cd feMain && npm start
```

### 3. Verify Everything Works
```bash
# Health checks
curl http://localhost:3001/health  # beAuth ✅
curl http://localhost:3002/health  # beCamera ✅
curl http://localhost:3000         # Frontend ✅
```

## 📋 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React Dashboard |
| **beAuth API** | http://localhost:3001 | Authentication Service |
| **beCamera API** | http://localhost:3002 | Camera Processing Service |
| **beAuth Docs** | http://localhost:3001/docs | Swagger API Documentation |
| **beCamera Docs** | http://localhost:3002/docs | Swagger API Documentation |

## 🧪 Testing Guide

### API Testing
```bash
# Test Authentication
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test Camera API
curl http://localhost:3002/api/v1/cameras
curl http://localhost:3002/api/v1/analytics/summary
```

### Database Testing
```bash
# Connect to PostgreSQL
docker exec -it ai-camera-postgres psql -U postgres -d people_counting_db

# Test Redis
docker exec -it ai-camera-redis redis-cli ping
```

### Frontend Testing
1. Open http://localhost:3000
2. Test login/logout flow
3. Test camera management
4. Test real-time features

## 🔧 Development Workflow

### Frontend Development
```bash
cd feMain
npm start          # Start development server
npm test           # Run tests
npm run build      # Build for production
```

### Backend Development
```bash
# beAuth (Node.js)
cd beAuth
docker-compose up -d    # Start service
docker logs ai-auth-service  # View logs

# beCamera (Python/FastAPI)
cd beCamera
docker-compose up -d    # Start service
docker logs ai-camera-service  # View logs
```

### Database Development
```bash
# Connect to database
docker exec -it ai-camera-postgres psql -U postgres -d people_counting_db

# Run migrations (if needed)
cd beAuth
npm run migrate
npm run seed
```

## 📊 Database Schema

### Key Tables
- **users**: User accounts and authentication
- **cameras**: Camera configuration and status
- **count_data**: People counting data
- **refresh_tokens**: JWT refresh tokens

### Sample Queries
```sql
-- View all cameras
SELECT * FROM cameras;

-- View recent count data
SELECT * FROM count_data ORDER BY timestamp DESC LIMIT 10;

-- View analytics
SELECT 
  COUNT(*) as total_cameras,
  COUNT(CASE WHEN status = 'active' THEN 1 END) as active_cameras
FROM cameras;
```

## 🔍 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check if ports are in use
lsof -i :3000  # Frontend
lsof -i :3001  # beAuth
lsof -i :3002  # beCamera

# Check Docker containers
docker ps
docker logs <container-name>
```

#### Database Connection Issues
```bash
# Check PostgreSQL
docker exec ai-camera-postgres pg_isready

# Check Redis
docker exec ai-camera-redis redis-cli ping
```

#### Frontend API Issues
```bash
# Check API endpoints
curl http://localhost:3001/health
curl http://localhost:3002/health

# Check CORS settings
# Verify environment variables in .env files
```

### Environment Variables

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:3001/api/v1
REACT_APP_CAMERA_API_URL=http://localhost:3002/api/v1
```

#### beAuth (.env)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=postgres123
```

#### beCamera (env.camera)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=postgres123
```

## 🎯 MVP Features

### Phase 1: Authentication ✅
- [x] User login/logout
- [x] JWT token management
- [x] Protected routes

### Phase 2: Camera Management 🔄
- [ ] List cameras
- [ ] Add/edit camera
- [ ] Camera status monitoring

### Phase 3: Real-time Counting 🔄
- [ ] Live camera feed
- [ ] People counting display
- [ ] Confidence scoring

### Phase 4: Analytics 🔄
- [ ] Dashboard overview
- [ ] Historical data
- [ ] Export functionality

## 📚 API Reference

### Authentication Endpoints
```bash
POST /api/v1/auth/login     # User login
POST /api/v1/auth/register  # User registration
GET  /api/v1/auth/me        # Get current user
POST /api/v1/auth/logout    # User logout
```

### Camera Endpoints
```bash
GET    /api/v1/cameras      # List all cameras
POST   /api/v1/cameras      # Create new camera
GET    /api/v1/cameras/:id  # Get camera details
PUT    /api/v1/cameras/:id  # Update camera
DELETE /api/v1/cameras/:id  # Delete camera
```

### Analytics Endpoints
```bash
GET /api/v1/counts              # Get count data
GET /api/v1/analytics/summary   # Get analytics summary
```

## 🛠️ Development Tools

### Useful Commands
```bash
# Start all services
./start-dev.sh

# Stop all services
./stop-dev.sh

# View all logs
docker-compose logs -f

# Restart specific service
docker-compose restart <service-name>

# Clean up Docker
docker system prune -f
```

### IDE Setup
- **VS Code**: Install Docker, Python, JavaScript extensions
- **Database**: Use pgAdmin or DBeaver for PostgreSQL
- **API Testing**: Use Postman or curl for API testing

## 📞 Support

### Getting Help
1. Check this README first
2. Check service logs: `docker logs <container-name>`
3. Check health endpoints: `/health`
4. Ask team lead or DevOps

### Useful Resources
- **API Docs**: Swagger UI at service URLs
- **Project Docs**: `docs/` directory
- **Shared Resources**: `sharedResource/README.md`

---

**Last Updated**: 2025-07-03  
**Status**: Ready for Development  
**Team**: Dev, Test, DevOps 
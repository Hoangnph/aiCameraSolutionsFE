# 🚀 **Face Detection System - Startup Scripts**

## **📋 Overview**

Hệ thống Face Detection có các script khởi động riêng biệt để dễ quản lý:

- **`start_backend.py`** - Khởi động chỉ backend API
- **`start_frontend.py`** - Khởi động chỉ frontend server
- **`start_all.py`** - Khởi động cả backend và frontend
- **`stop_all.py`** - Dừng tất cả servers

## **🔧 Prerequisites**

### **1. Python Dependencies**
```bash
pip install fastapi uvicorn opencv-python face-recognition pillow numpy requests
```

### **2. Project Structure**
```
labs/face_detection/
├── src/
│   ├── api/
│   │   └── main.py
│   └── services/
│       ├── face_processing.py
│       ├── camera_service.py
│       └── simple_vector_db.py
├── fe/
│   └── index.html
├── start_backend.py
├── start_frontend.py
├── start_all.py
└── stop_all.py
```

## **🚀 Startup Options**

### **Option 1: Start Backend Only**
```bash
cd labs/face_detection
python start_backend.py
```

**Features:**
- ✅ Health check backend
- ✅ Kill existing processes
- ✅ Check dependencies
- ✅ Monitor server output
- ✅ Auto-restart on errors

**URLs:**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### **Option 2: Start Frontend Only**
```bash
cd labs/face_detection
python start_frontend.py
```

**Features:**
- ✅ Check backend health first
- ✅ Kill existing processes
- ✅ Check frontend files
- ✅ Auto-open browser
- ✅ Monitor server output

**URLs:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

### **Option 3: Start Complete System**
```bash
cd labs/face_detection
python start_all.py
```

**Features:**
- ✅ Start both backend and frontend
- ✅ Health check both services
- ✅ Monitor both servers
- ✅ Graceful shutdown
- ✅ Threaded monitoring

**URLs:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## **🛑 Stopping Servers**

### **Stop All Servers**
```bash
cd labs/face_detection
python stop_all.py
```

### **Manual Stop**
```bash
# Kill processes on specific ports
lsof -ti :8000 | xargs kill -9  # Backend
lsof -ti :3000 | xargs kill -9  # Frontend
```

## **🔍 Troubleshooting**

### **Common Issues**

#### **1. Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill processes
python stop_all.py
```

#### **2. Missing Dependencies**
```bash
# Install required packages
pip install fastapi uvicorn opencv-python face-recognition pillow numpy requests
```

#### **3. Backend Not Starting**
```bash
# Check if in correct directory
pwd  # Should be in labs/face_detection

# Check project structure
ls -la src/api/main.py
ls -la src/services/
```

#### **4. Frontend Not Starting**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check frontend files
ls -la fe/index.html
```

### **Debug Commands**

#### **Check Backend Health**
```bash
curl -s http://localhost:8000/health | jq .
```

#### **Check Frontend**
```bash
curl -s http://localhost:3000 | head -10
```

#### **Check Processes**
```bash
ps aux | grep uvicorn
ps aux | grep "http.server"
```

## **📊 System Status**

### **Backend Status**
- **Port**: 8000
- **Health Endpoint**: `/health`
- **API Docs**: `/docs`
- **Logs**: Real-time in console

### **Frontend Status**
- **Port**: 3000
- **Static Files**: `fe/` directory
- **Auto-reload**: Manual refresh needed
- **Logs**: Real-time in console

## **🎯 Usage Examples**

### **Development Mode**
```bash
# Terminal 1: Start backend
python start_backend.py

# Terminal 2: Start frontend
python start_frontend.py
```

### **Production Mode**
```bash
# Start everything at once
python start_all.py
```

### **Testing Mode**
```bash
# Start backend for API testing
python start_backend.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/faces/list
```

## **🔧 Advanced Configuration**

### **Custom Ports**
Edit the scripts to change ports:
```python
# In start_backend.py
self.port = 8001  # Change backend port

# In start_frontend.py  
self.port = 3001  # Change frontend port
```

### **Custom Hosts**
```python
# In scripts
self.host = "127.0.0.1"  # Local only
self.host = "0.0.0.0"    # All interfaces
```

### **Environment Variables**
```bash
# Set custom ports
export BACKEND_PORT=8001
export FRONTEND_PORT=3001

# Run with custom config
BACKEND_PORT=8001 FRONTEND_PORT=3001 python start_all.py
```

## **📝 Logs and Monitoring**

### **Backend Logs**
- Real-time API requests
- Face detection results
- Database operations
- Error messages

### **Frontend Logs**
- HTTP requests
- Static file serving
- Error messages

### **System Logs**
- Process startup/shutdown
- Health check results
- Port conflicts
- Dependency checks

## **✅ Success Indicators**

### **Backend Success**
```
✅ Backend server is running successfully!
🌐 API URL: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

### **Frontend Success**
```
✅ Frontend server is running successfully!
🌐 Frontend URL: http://localhost:3000
🔗 Backend API: http://localhost:8000
```

### **Complete System Success**
```
🎉 Complete system is running successfully!
🌐 Frontend URL: http://localhost:3000
🔗 Backend API: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

## **🚀 Quick Start**

```bash
# 1. Navigate to project
cd labs/face_detection

# 2. Start complete system
python start_all.py

# 3. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs

# 4. Stop when done
# Press Ctrl+C or run: python stop_all.py
```

**🎉 Happy Face Detection!** 
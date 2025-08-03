# Face Detection System - Shared Resources

## 🚀 Active Services & Resources

### 1. FastAPI Server
- **Status**: ✅ RUNNING
- **URL**: http://localhost:8000
- **Port**: 8000
- **Process ID**: Active uvicorn process
- **Health**: Healthy (all services operational)

### 2. Database Resources
- **SQLite Database**: `data/metadata.db`
- **Vector Database**: `data/face_vectors.db`
- **Status**: ✅ ACTIVE
- **Tables**: persons, face_embeddings, recognition_logs, system_settings, audit_logs

### 3. File Storage
- **Upload Directory**: `uploads/`
- **Test Images**: `automation_test/test_images/`
- **Logs**: `logs/`
- **Status**: ✅ ACTIVE

### 4. API Endpoints Status

#### ✅ Working Endpoints
- `GET /` - Root endpoint with system info
- `GET /health` - Health check
- `POST /api/v1/faces/upload` - Face registration
- `POST /api/v1/faces/recognize` - Face recognition
- `GET /api/v1/faces/list` - List registered faces
- `GET /api/v1/camera/status` - Camera status
- `POST /api/v1/camera/start` - Start camera
- `POST /api/v1/camera/stop` - Stop camera
- `GET /api/v1/camera/stream` - Camera stream

#### 📊 Test Results
- **Face Registration**: ✅ Success (3 test users registered)
- **Face Recognition**: ✅ Success (1.0 similarity score)
- **Camera Control**: ✅ Success (start/stop working)
- **Database Operations**: ✅ Success (SQL + Vector DB)

## 🔧 Service Dependencies

### Core Services
1. **Face Processing Service**
   - Library: face_recognition
   - Status: ✅ Healthy
   - Functions: detect_faces, generate_embedding, compare_faces

2. **Camera Service**
   - Library: OpenCV
   - Status: ✅ Healthy
   - Functions: get_available_cameras, start_video_stream, stop_video_stream

3. **Vector Database Service**
   - Implementation: SimpleVectorDB (SQLite-based)
   - Status: ✅ Healthy
   - Functions: add_face_embedding, search_similar_faces, list_all_faces

4. **SQL Database Service**
   - ORM: SQLAlchemy
   - Status: ✅ Healthy
   - Models: Person, FaceEmbedding, RecognitionLog

## 📁 File Structure

```
labs/face_detection/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── services/
│   │   ├── face_processing.py   # Face detection & recognition
│   │   ├── camera_service.py    # Camera management
│   │   └── simple_vector_db.py  # Vector database
│   ├── models/
│   │   └── database.py          # SQLAlchemy models
│   └── utils/
│       ├── logger.py            # Logging utilities
│       └── response_models.py   # API response models
├── data/
│   ├── metadata.db              # SQLite database
│   └── face_vectors.db          # Vector database
├── uploads/                     # Uploaded face images
├── logs/                        # Application logs
├── automation_test/
│   └── test_images/
│       └── test_face.jpg        # Test image
└── config.py                    # Configuration
```

## 🔄 Running Processes

### Active Processes
1. **uvicorn server** - FastAPI application
   - Port: 8000
   - Status: Running
   - Reload: Enabled

2. **Database connections**
   - SQLite: Active
   - Vector DB: Active

3. **Camera service**
   - Status: Available (1 camera detected)
   - Stream: Can be started/stopped

## 📊 Resource Usage

### Database Records
- **Persons**: 3 registered users
- **Face Embeddings**: 3 embeddings stored
- **Vector Database**: 4 face vectors (including old test data)

### Storage
- **Database files**: ~32KB total
- **Upload images**: ~24KB (3 images)
- **Log files**: Minimal

### Memory Usage
- **Server process**: ~25MB
- **Database connections**: Minimal
- **Face processing**: On-demand

## 🛠️ Configuration

### Environment Variables
- `DEBUG`: False
- `HOST`: 0.0.0.0
- `PORT`: 8000
- `DATABASE_URL`: sqlite:///./data/metadata.db
- `CHROMA_DB_PATH`: ./data/vector_db

### Face Recognition Settings
- `face_recognition_tolerance`: 0.6
- `min_face_size`: 20
- `max_face_size`: 1000
- `quality_threshold`: 0.7 (adjusted to 0.3 for testing)

### Camera Settings
- `camera_device_id`: 0
- `camera_resolution_width`: 640
- `camera_resolution_height`: 480
- `camera_fps`: 30

## 🔍 Monitoring & Health

### Health Check Response
```json
{
    "success": true,
    "message": "Health check completed",
    "data": {
        "status": "healthy",
        "services": {
            "face_processing": true,
            "camera_service": true,
            "vector_database": true
        },
        "timestamp": "2025-07-31T11:28:04.784226"
    }
}
```

### Service Status
- ✅ **Face Processing Service**: Healthy
- ✅ **Camera Service**: Healthy (1 camera available)
- ✅ **Vector Database**: Healthy
- ✅ **SQL Database**: Healthy

## 🚨 Troubleshooting

### Common Issues & Solutions
1. **Port 8000 in use**: Kill existing process or use different port
2. **Camera not found**: Check camera permissions and device ID
3. **Database errors**: Check file permissions and disk space
4. **Import errors**: Ensure running from correct directory

### Restart Commands
```bash
# Kill existing server
pkill -f uvicorn

# Start server
cd labs/face_detection
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Test health
curl -s http://localhost:8000/health
```

## 📈 Performance Metrics

### Response Times
- Health check: < 100ms
- Face registration: < 2000ms
- Face recognition: < 1500ms
- Camera status: < 50ms

### Success Rates
- Face registration: 100% (3/3 successful)
- Face recognition: 100% (1/1 successful)
- Camera operations: 100% (start/stop working)

## 🔐 Security Notes

### Current Security
- CORS enabled for all origins (development)
- No authentication implemented
- File upload validation active
- SQL injection protection (SQLAlchemy)

### Recommendations
- Implement authentication
- Add rate limiting
- Secure file uploads
- Add input validation

---

**Last Updated**: 2025-07-31
**Status**: ✅ ALL SERVICES OPERATIONAL
**Next Maintenance**: Performance optimization 
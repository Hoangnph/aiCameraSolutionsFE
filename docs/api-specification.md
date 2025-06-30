# API Specification - People Counting Dashboard

## Tổng quan API

API được xây dựng trên FastAPI với các endpoint RESTful và WebSocket cho real-time communication.

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.peoplecounting.com/api/v1
```

## Authentication

### JWT Token Authentication

```http
Authorization: Bearer <jwt_token>
```

### Token Refresh

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "string"
}
```

## API Endpoints

### 1. Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "string"
  }
}
```

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer <token>
```

### 2. Cameras

#### Get All Cameras
```http
GET /cameras
Authorization: Bearer <token>
```

**Response:**
```json
{
  "cameras": [
    {
      "id": 1,
      "name": "Main Entrance",
      "location": "Building A",
      "stream_url": "rtsp://camera1/stream",
      "status": "online",
      "settings": {
        "detection_sensitivity": 0.8,
        "counting_zones": []
      },
      "statistics": {
        "total_people_in": 1234,
        "total_people_out": 1189,
        "current_occupancy": 45,
        "last_update": "2024-01-01T12:00:00Z"
      }
    }
  ]
}
```

#### Get Camera by ID
```http
GET /cameras/{camera_id}
Authorization: Bearer <token>
```

#### Add Camera
```http
POST /cameras
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string",
  "location": "string",
  "stream_url": "string",
  "settings": {
    "detection_sensitivity": 0.8,
    "counting_zones": []
  }
}
```

#### Update Camera
```http
PUT /cameras/{camera_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string",
  "location": "string",
  "stream_url": "string",
  "settings": {}
}
```

#### Delete Camera
```http
DELETE /cameras/{camera_id}
Authorization: Bearer <token>
```

#### Get Camera Stream
```http
GET /cameras/{camera_id}/stream
Authorization: Bearer <token>
```

### 3. Analytics

#### Get Real-time Data
```http
GET /analytics/realtime
Authorization: Bearer <token>
```

**Response:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "cameras": [
    {
      "camera_id": 1,
      "people_in": 1234,
      "people_out": 1189,
      "current_count": 45,
      "occupancy": 0.75,
      "confidence": 0.95
    }
  ],
  "total": {
    "people_in": 1234,
    "people_out": 1189,
    "current_count": 45,
    "occupancy": 0.75
  }
}
```

#### Get Historical Data
```http
GET /analytics/historical
Authorization: Bearer <token>
Query Parameters:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- camera_ids: comma-separated IDs
- time_range: hourly|daily|weekly|monthly
```

**Response:**
```json
{
  "data": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "camera_id": 1,
      "people_in": 45,
      "people_out": 12,
      "current_count": 33,
      "occupancy": 0.55
    }
  ],
  "summary": {
    "total_people_in": 1234,
    "total_people_out": 1189,
    "peak_occupancy": 67,
    "average_occupancy": 38
  }
}
```

#### Get Peak Hours Report
```http
GET /analytics/peak-hours
Authorization: Bearer <token>
Query Parameters:
- date: YYYY-MM-DD
- camera_ids: comma-separated IDs
```

**Response:**
```json
{
  "date": "2024-01-01",
  "peak_hours": [
    {
      "hour": 8,
      "people_in": 234,
      "people_out": 45,
      "net_flow": 189,
      "occupancy": 0.85
    }
  ],
  "recommendations": [
    "Peak hours: 8:00-9:00 AM",
    "Consider additional staff during peak hours"
  ]
}
```

#### Get People Count Report
```http
GET /analytics/people-count
Authorization: Bearer <token>
Query Parameters:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- camera_ids: comma-separated IDs
```

**Response:**
```json
{
  "report": {
    "id": "report_123",
    "title": "People Count Report",
    "generated_at": "2024-01-01T12:00:00Z",
    "time_range": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "data": {
      "current_count": 45,
      "total_in": 1234,
      "total_out": 1189,
      "peak_occupancy": 67,
      "average_occupancy": 38,
      "hourly_data": [
        {
          "hour": 8,
          "people_in": 234,
          "people_out": 45,
          "current_count": 189
        }
      ]
    }
  }
}
```

#### Export Report
```http
GET /analytics/export
Authorization: Bearer <token>
Query Parameters:
- report_type: people-count|peak-hours
- format: pdf|excel
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- camera_ids: comma-separated IDs
```

### 4. Alerts

#### Get Notifications
```http
GET /alerts/notifications
Authorization: Bearer <token>
Query Parameters:
- unread_only: boolean
- limit: number
```

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "type": "camera_offline",
      "severity": "high",
      "title": "Camera Offline",
      "message": "Camera Main Entrance is offline",
      "camera_id": 1,
      "is_read": false,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### Mark Alert as Read
```http
PUT /alerts/{alert_id}/read
Authorization: Bearer <token>
```

#### Get Alert History
```http
GET /alerts/history
Authorization: Bearer <token>
Query Parameters:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- type: string
- severity: low|medium|high|critical
```

### 5. Settings

#### Get User Profile
```http
GET /settings/profile
Authorization: Bearer <token>
```

#### Update User Profile
```http
PUT /settings/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string"
}
```

#### Get System Settings
```http
GET /settings/system
Authorization: Bearer <token>
```

#### Update System Settings
```http
PUT /settings/system
Authorization: Bearer <token>
Content-Type: application/json

{
  "detection_sensitivity": 0.8,
  "alert_enabled": true,
  "data_retention_days": 30
}
```

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Events

#### Subscribe to Camera
```javascript
ws.send(JSON.stringify({
  event: 'subscribe:camera',
  data: { camera_id: 1 }
}));
```

#### Subscribe to Analytics
```javascript
ws.send(JSON.stringify({
  event: 'subscribe:analytics',
  data: {}
}));
```

#### Unsubscribe from Camera
```javascript
ws.send(JSON.stringify({
  event: 'unsubscribe:camera',
  data: { camera_id: 1 }
}));
```

### Incoming Events

#### Camera Count Update
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.event === 'camera:count') {
    console.log('Count update:', data.data);
  }
};
```

**Data Structure:**
```json
{
  "event": "camera:count",
  "data": {
    "camera_id": 1,
    "timestamp": "2024-01-01T12:00:00Z",
    "people_in": 1234,
    "people_out": 1189,
    "current_count": 45,
    "occupancy": 0.75,
    "confidence": 0.95
  }
}
```

#### Camera Alert
```json
{
  "event": "camera:alert",
  "data": {
    "alert_id": 1,
    "type": "camera_offline",
    "severity": "high",
    "title": "Camera Offline",
    "message": "Camera Main Entrance is offline",
    "camera_id": 1,
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

#### Analytics Update
```json
{
  "event": "analytics:update",
  "data": {
    "timestamp": "2024-01-01T12:00:00Z",
    "total_people_in": 1234,
    "total_people_out": 1189,
    "current_count": 45,
    "occupancy": 0.75
  }
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTH_REQUIRED` | 401 | Authentication required |
| `INVALID_TOKEN` | 401 | Invalid or expired token |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `INTERNAL_ERROR` | 500 | Internal server error |

### Example Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "username": "Username is required",
      "email": "Invalid email format"
    }
  }
}
```

## Rate Limiting

- **Authentication endpoints**: 5 requests per minute
- **API endpoints**: 100 requests per minute per user
- **WebSocket connections**: 10 connections per user

## Pagination

For endpoints that return lists, pagination is supported:

```http
GET /cameras?page=1&limit=10
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

## Data Types

### TimeRange
```typescript
interface TimeRange {
  start: string; // ISO 8601 date string
  end: string;   // ISO 8601 date string
}
```

### Camera
```typescript
interface Camera {
  id: number;
  name: string;
  location: string;
  stream_url: string;
  status: 'online' | 'offline' | 'maintenance';
  settings: CameraSettings;
  statistics: CameraStatistics;
  created_at: string;
}
```

### Alert
```typescript
interface Alert {
  id: number;
  type: 'camera_offline' | 'system_error' | 'high_traffic' | 'maintenance';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  message: string;
  camera_id?: number;
  is_read: boolean;
  created_at: string;
}
``` 
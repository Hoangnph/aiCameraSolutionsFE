import asyncio
import json
import logging
from typing import Dict, Set, Optional
from datetime import datetime
import redis.asyncio as redis
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            'camera_updates': set(),
            'alerts': set(),
            'analytics': set(),
            'system_status': set()
        }
        self.redis_client: Optional[redis.Redis] = None

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)
        logger.info(f"Client connected to {channel}. Total connections: {len(self.active_connections[channel])}")

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
        logger.info(f"Client disconnected from {channel}. Total connections: {len(self.active_connections.get(channel, set()))}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await self.disconnect(websocket, 'all')

    async def broadcast(self, message: str, channel: str):
        if channel not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[channel]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.add(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection, channel)

    async def broadcast_camera_update(self, camera_id: str, data: dict):
        """Broadcast camera count updates"""
        message = {
            'type': 'camera_update',
            'camera_id': camera_id,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(json.dumps(message), 'camera_updates')

    async def broadcast_alert(self, alert_type: str, message: str, severity: str = 'info'):
        """Broadcast system alerts"""
        alert = {
            'type': 'alert',
            'alert_type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(json.dumps(alert), 'alerts')

    async def broadcast_analytics(self, analytics_data: dict):
        """Broadcast analytics updates"""
        message = {
            'type': 'analytics_update',
            'data': analytics_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(json.dumps(message), 'analytics')

    async def broadcast_system_status(self, status_data: dict):
        """Broadcast system status updates"""
        message = {
            'type': 'system_status',
            'data': status_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(json.dumps(message), 'system_status')

    async def setup_redis_subscriber(self):
        """Setup Redis subscriber for cross-service communication"""
        if not self.redis_client:
            self.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
        
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('camera_updates', 'alerts', 'analytics', 'system_status')
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    channel = message['channel']
                    await self.broadcast(json.dumps(data), channel)
                except Exception as e:
                    logger.error(f"Error processing Redis message: {e}")

# Global WebSocket manager instance
manager = WebSocketManager()

# FastAPI app
app = FastAPI(title="AI Camera WebSocket Service", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection and start background tasks"""
    try:
        manager.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
        await manager.redis_client.ping()
        logger.info("Connected to Redis")
        
        # Start Redis subscriber in background
        asyncio.create_task(manager.setup_redis_subscriber())
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup connections"""
    if manager.redis_client:
        await manager.redis_client.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "connections": {
            channel: len(connections) 
            for channel, connections in manager.active_connections.items()
        }
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    metrics_data = {
        "websocket_connections_total": sum(len(connections) for connections in manager.active_connections.values()),
        "websocket_connections_by_channel": {
            channel: len(connections) 
            for channel, connections in manager.active_connections.items()
        }
    }
    return metrics_data

@app.websocket("/ws/camera-updates/{client_id}")
async def websocket_camera_updates(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for camera updates"""
    await manager.connect(websocket, 'camera_updates')
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('type') == 'ping':
                    await manager.send_personal_message(json.dumps({'type': 'pong'}), websocket)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from client {client_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, 'camera_updates')
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, 'camera_updates')

@app.websocket("/ws/alerts/{client_id}")
async def websocket_alerts(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for alerts"""
    await manager.connect(websocket, 'alerts')
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('type') == 'ping':
                    await manager.send_personal_message(json.dumps({'type': 'pong'}), websocket)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from client {client_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, 'alerts')
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, 'alerts')

@app.websocket("/ws/analytics/{client_id}")
async def websocket_analytics(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for analytics"""
    await manager.connect(websocket, 'analytics')
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('type') == 'ping':
                    await manager.send_personal_message(json.dumps({'type': 'pong'}), websocket)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from client {client_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, 'analytics')
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, 'analytics')

@app.websocket("/ws/system-status/{client_id}")
async def websocket_system_status(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for system status"""
    await manager.connect(websocket, 'system_status')
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('type') == 'ping':
                    await manager.send_personal_message(json.dumps({'type': 'pong'}), websocket)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from client {client_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, 'system_status')
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, 'system_status')

# API endpoints for other services to send updates
@app.post("/api/v1/broadcast/camera-update")
async def broadcast_camera_update(camera_id: str, data: dict):
    """API endpoint for broadcasting camera updates"""
    await manager.broadcast_camera_update(camera_id, data)
    return {"status": "broadcasted"}

@app.post("/api/v1/broadcast/alert")
async def broadcast_alert(alert_type: str, message: str, severity: str = 'info'):
    """API endpoint for broadcasting alerts"""
    await manager.broadcast_alert(alert_type, message, severity)
    return {"status": "alert_sent"}

@app.post("/api/v1/broadcast/analytics")
async def broadcast_analytics(analytics_data: dict):
    """API endpoint for broadcasting analytics"""
    await manager.broadcast_analytics(analytics_data)
    return {"status": "analytics_broadcasted"}

@app.post("/api/v1/broadcast/system-status")
async def broadcast_system_status(status_data: dict):
    """API endpoint for broadcasting system status"""
    await manager.broadcast_system_status(status_data)
    return {"status": "status_broadcasted"}

if __name__ == "__main__":
    uvicorn.run(
        "websocket_service:app",
        host="0.0.0.0",
        port=3003,
        reload=False,
        log_level="info"
    ) 
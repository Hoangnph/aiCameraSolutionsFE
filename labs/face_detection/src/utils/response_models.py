"""
Response models for Face Detection System API
Defines standardized response structures for all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SuccessResponse(BaseModel):
    """Standard success response model"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error: str
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class FaceRegistrationResponse(BaseModel):
    """Response model for face registration"""
    success: bool
    message: str
    data: Dict[str, Any] = Field(
        description="Registration details including person_id, face_id, confidence, etc."
    )
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class FaceRecognitionResponse(BaseModel):
    """Response model for face recognition"""
    success: bool
    message: str
    data: Dict[str, Any] = Field(
        description="Recognition results including person details, confidence, matches"
    )
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class CameraStatusResponse(BaseModel):
    """Response model for camera status"""
    success: bool
    message: str
    data: Dict[str, Any] = Field(
        description="Camera status including is_running, resolution, fps, etc."
    )
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class PersonInfo(BaseModel):
    """Person information model"""
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: str

class FaceInfo(BaseModel):
    """Face information model"""
    id: str
    person_id: str
    confidence: float
    face_location: List[int]
    image_path: str
    created_at: str

class RecognitionMatch(BaseModel):
    """Face recognition match model"""
    person_id: str
    name: str
    confidence: float
    similarity: float

class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    services: Dict[str, bool]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class UploadResponse(BaseModel):
    """File upload response model"""
    filename: str
    size: int
    content_type: str
    uploaded_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class StreamResponse(BaseModel):
    """Stream response model"""
    stream_url: str
    status: str
    resolution: Optional[str] = None
    fps: Optional[int] = None

class AnalyticsResponse(BaseModel):
    """Analytics response model"""
    total_faces: int
    total_people: int
    recognition_accuracy: float
    processing_time_avg: float
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

class SystemInfoResponse(BaseModel):
    """System information response model"""
    version: str
    status: str
    uptime: str
    memory_usage: Dict[str, float]
    cpu_usage: float
    active_connections: int
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat()) 
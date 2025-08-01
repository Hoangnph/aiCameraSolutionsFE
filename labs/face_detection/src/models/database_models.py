"""
Database models for Face Detection System
Defines SQLAlchemy models for storing person and face information.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Person(Base):
    """Person model for storing individual information"""
    __tablename__ = "persons"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to faces
    faces = relationship("FaceRecord", back_populates="person", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class FaceRecord(Base):
    """Face record model for storing face embeddings and metadata"""
    __tablename__ = "face_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    person_id = Column(String(36), ForeignKey("persons.id"), nullable=False, index=True)
    embedding = Column(JSON, nullable=False)  # Store face embedding as JSON array
    face_location = Column(JSON, nullable=False)  # Store face coordinates as JSON
    confidence = Column(Float, nullable=False, default=0.0)
    image_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to person
    person = relationship("Person", back_populates="faces")
    
    def __repr__(self):
        return f"<FaceRecord(id={self.id}, person_id={self.person_id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "person_id": self.person_id,
            "embedding": self.embedding,
            "face_location": self.face_location,
            "confidence": self.confidence,
            "image_path": self.image_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class RecognitionLog(Base):
    """Log model for tracking face recognition events"""
    __tablename__ = "recognition_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    person_id = Column(String(36), ForeignKey("persons.id"), nullable=True, index=True)
    confidence = Column(Float, nullable=False, default=0.0)
    similarity = Column(Float, nullable=False, default=0.0)
    image_path = Column(String(500), nullable=True)
    recognized_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    
    # Relationship to person
    person = relationship("Person")
    
    def __repr__(self):
        return f"<RecognitionLog(id={self.id}, person_id={self.person_id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "person_id": self.person_id,
            "confidence": self.confidence,
            "similarity": self.similarity,
            "image_path": self.image_path,
            "recognized_at": self.recognized_at.isoformat() if self.recognized_at else None,
            "processing_time": self.processing_time
        }

class SystemLog(Base):
    """System log model for tracking system events"""
    __tablename__ = "system_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)  # Additional log details
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class CameraSession(Base):
    """Camera session model for tracking camera usage"""
    __tablename__ = "camera_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_name = Column(String(255), nullable=False)
    camera_id = Column(String(100), nullable=True)
    resolution = Column(String(50), nullable=True)
    fps = Column(Integer, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    total_frames = Column(Integer, default=0)
    total_recognitions = Column(Integer, default=0)
    status = Column(String(20), default="active", nullable=False)  # active, stopped, error
    
    def __repr__(self):
        return f"<CameraSession(id={self.id}, session_name='{self.session_name}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "session_name": self.session_name,
            "camera_id": self.camera_id,
            "resolution": self.resolution,
            "fps": self.fps,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "total_frames": self.total_frames,
            "total_recognitions": self.total_recognitions,
            "status": self.status
        }

class Analytics(Base):
    """Analytics model for storing system performance metrics"""
    __tablename__ = "analytics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    details = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, metric_name='{self.metric_name}')>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metric_unit": self.metric_unit,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "details": self.details
        } 
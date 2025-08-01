"""
Database models for Face Detection System
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import uuid

from config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

class Person(Base):
    """Person model for storing user information"""
    __tablename__ = "persons"
    
    person_id = Column(String, primary_key=True, default=lambda: f"p_{uuid.uuid4().hex[:8]}")
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    department = Column(String(50), nullable=True)
    position = Column(String(50), nullable=True)
    registration_date = Column(DateTime, default=func.now())
    status = Column(String(20), default="active")  # active, inactive, deleted
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    face_embeddings = relationship("FaceEmbedding", back_populates="person", cascade="all, delete-orphan")
    recognition_logs = relationship("RecognitionLog", back_populates="person")
    
    def __repr__(self):
        return f"<Person(person_id='{self.person_id}', name='{self.name}')>"

class FaceEmbedding(Base):
    """Face embedding model for storing face vectors"""
    __tablename__ = "face_embeddings"
    
    embedding_id = Column(String, primary_key=True, default=lambda: f"emb_{uuid.uuid4().hex[:8]}")
    person_id = Column(String, ForeignKey("persons.person_id"), nullable=False)
    embedding_data = Column(Text, nullable=False)  # JSON string of embedding vector
    quality_score = Column(Float, nullable=True)
    model_version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    person = relationship("Person", back_populates="face_embeddings")
    
    def __repr__(self):
        return f"<FaceEmbedding(embedding_id='{self.embedding_id}', person_id='{self.person_id}')>"

class RecognitionLog(Base):
    """Recognition log model for storing recognition history"""
    __tablename__ = "recognition_logs"
    
    log_id = Column(String, primary_key=True, default=lambda: f"log_{uuid.uuid4().hex[:8]}")
    person_id = Column(String, ForeignKey("persons.person_id"), nullable=True)
    confidence_score = Column(Float, nullable=False)
    face_location = Column(Text, nullable=True)  # JSON string of face location
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    person = relationship("Person", back_populates="recognition_logs")
    
    def __repr__(self):
        return f"<RecognitionLog(log_id='{self.log_id}', person_id='{self.person_id}')>"

class SystemSetting(Base):
    """System settings model"""
    __tablename__ = "system_settings"
    
    setting_key = Column(String(100), primary_key=True)
    setting_value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemSetting(setting_key='{self.setting_key}')>"

class AuditLog(Base):
    """Audit log model for tracking system activities"""
    __tablename__ = "audit_logs"
    
    log_id = Column(String, primary_key=True, default=lambda: f"audit_{uuid.uuid4().hex[:8]}")
    user_id = Column(String(100), nullable=True)
    operation = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)  # JSON string of operation details
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<AuditLog(log_id='{self.log_id}', operation='{self.operation}')>"

# Database utility functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)

def init_default_settings():
    """Initialize default system settings"""
    db = SessionLocal()
    try:
        default_settings = [
            {
                "setting_key": "face_recognition_tolerance",
                "setting_value": "0.6",
                "description": "Threshold for face recognition"
            },
            {
                "setting_key": "min_face_size",
                "setting_value": "20",
                "description": "Minimum face size for detection"
            },
            {
                "setting_key": "max_face_size",
                "setting_value": "1000",
                "description": "Maximum face size for detection"
            },
            {
                "setting_key": "quality_threshold",
                "setting_value": "0.7",
                "description": "Minimum quality score for registration"
            },
            {
                "setting_key": "log_retention_days",
                "setting_value": "30",
                "description": "Number of days to keep recognition logs"
            },
            {
                "setting_key": "max_embeddings_per_person",
                "setting_value": "5",
                "description": "Maximum embeddings per person"
            }
        ]
        
        for setting_data in default_settings:
            existing = db.query(SystemSetting).filter(
                SystemSetting.setting_key == setting_data["setting_key"]
            ).first()
            
            if not existing:
                setting = SystemSetting(**setting_data)
                db.add(setting)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Pydantic models for API
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PersonBase(BaseModel):
    """Base person model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None, max_length=50)

class PersonCreate(PersonBase):
    """Person creation model"""
    pass

class PersonUpdate(BaseModel):
    """Person update model"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, pattern="^(active|inactive|deleted)$")

class PersonResponse(PersonBase):
    """Person response model"""
    person_id: str
    registration_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FaceEmbeddingBase(BaseModel):
    """Base face embedding model"""
    quality_score: Optional[float] = Field(None, ge=0, le=1)
    model_version: str = Field(default="1.0", max_length=20)

class FaceEmbeddingCreate(FaceEmbeddingBase):
    """Face embedding creation model"""
    person_id: str
    embedding_data: str  # JSON string of embedding vector

class FaceEmbeddingResponse(FaceEmbeddingBase):
    """Face embedding response model"""
    embedding_id: str
    person_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecognitionLogBase(BaseModel):
    """Base recognition log model"""
    confidence_score: float = Field(..., ge=0, le=1)
    face_location: Optional[str] = Field(None)  # JSON string

class RecognitionLogCreate(RecognitionLogBase):
    """Recognition log creation model"""
    person_id: Optional[str] = None

class RecognitionLogResponse(RecognitionLogBase):
    """Recognition log response model"""
    log_id: str
    person_id: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True

class SystemSettingBase(BaseModel):
    """Base system setting model"""
    setting_value: str
    description: Optional[str] = None

class SystemSettingCreate(SystemSettingBase):
    """System setting creation model"""
    setting_key: str = Field(..., max_length=100)

class SystemSettingResponse(SystemSettingBase):
    """System setting response model"""
    setting_key: str
    updated_at: datetime
    
    class Config:
        from_attributes = True 
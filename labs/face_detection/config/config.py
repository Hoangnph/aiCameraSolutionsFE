"""
Configuration module for Face Detection System
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Face Detection System"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Database
    database_url: str = Field(
        default="sqlite:///./data/metadata.db",
        env="DATABASE_URL"
    )
    chroma_db_path: str = Field(
        default="./data/vector_db",
        env="CHROMA_DB_PATH"
    )
    
    # Face Recognition
    face_recognition_tolerance: float = Field(default=0.6, env="FACE_RECOGNITION_TOLERANCE")
    min_face_size: int = Field(default=20, env="MIN_FACE_SIZE")
    max_face_size: int = Field(default=1000, env="MAX_FACE_SIZE")
    quality_threshold: float = Field(default=0.7, env="QUALITY_THRESHOLD")
    max_embeddings_per_person: int = Field(default=5, env="MAX_EMBEDDINGS_PER_PERSON")
    
    # Camera
    camera_device_id: int = Field(default=0, env="CAMERA_DEVICE_ID")
    camera_resolution_width: int = Field(default=640, env="CAMERA_RESOLUTION_WIDTH")
    camera_resolution_height: int = Field(default=480, env="CAMERA_RESOLUTION_HEIGHT")
    camera_fps: int = Field(default=30, env="CAMERA_FPS")
    
    # Storage
    upload_path: str = Field(default="./uploads", env="UPLOAD_PATH")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    allowed_extensions: list = Field(default=["jpg", "jpeg", "png"], env="ALLOWED_EXTENSIONS")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=1440, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # 24 hours
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_path: str = Field(default="./logs", env="LOG_PATH")
    
    # API
    api_prefix: str = "/api/v1"
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=8001, env="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        settings.upload_path,
        settings.log_path,
        "./data",
        "./logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Configuration for different environments
class Config:
    """Configuration class for different environments"""
    
    @staticmethod
    def get_database_config() -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "url": settings.database_url,
            "echo": settings.debug,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True
        }
    
    @staticmethod
    def get_chroma_config() -> Dict[str, Any]:
        """Get ChromaDB configuration"""
        return {
            "persist_directory": settings.chroma_db_path,
            "anonymized_telemetry": False
        }
    
    @staticmethod
    def get_face_recognition_config() -> Dict[str, Any]:
        """Get face recognition configuration"""
        return {
            "tolerance": settings.face_recognition_tolerance,
            "min_face_size": settings.min_face_size,
            "max_face_size": settings.max_face_size,
            "quality_threshold": settings.quality_threshold,
            "max_embeddings_per_person": settings.max_embeddings_per_person
        }
    
    @staticmethod
    def get_camera_config() -> Dict[str, Any]:
        """Get camera configuration"""
        return {
            "device_id": settings.camera_device_id,
            "resolution": (settings.camera_resolution_width, settings.camera_resolution_height),
            "fps": settings.camera_fps
        }
    
    @staticmethod
    def get_storage_config() -> Dict[str, Any]:
        """Get storage configuration"""
        return {
            "upload_path": settings.upload_path,
            "max_file_size": settings.max_file_size,
            "allowed_extensions": settings.allowed_extensions
        }
    
    @staticmethod
    def get_security_config() -> Dict[str, Any]:
        """Get security configuration"""
        return {
            "secret_key": settings.secret_key,
            "algorithm": settings.algorithm,
            "access_token_expire_minutes": settings.access_token_expire_minutes
        }

# Initialize directories
ensure_directories() 
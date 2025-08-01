"""
Logger utility for Face Detection System
Provides consistent logging configuration across all components.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import json
from typing import Optional, Dict, Any

class CustomFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record):
        """Format log record with structured data"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "json"
) -> logging.Logger:
    """
    Setup logger with consistent configuration
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Log format ("json" or "text")
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    if log_format == "json":
        formatter = CustomFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance by name
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **kwargs
):
    """
    Log message with additional context
    
    Args:
        logger: Logger instance
        level: Log level
        message: Log message
        **kwargs: Additional context fields
    """
    extra_fields = kwargs
    log_method = getattr(logger, level.lower())
    log_method(message, extra={"extra_fields": extra_fields})

class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    def __init__(self, logger_name: Optional[str] = None):
        """Initialize logger for the class"""
        if logger_name is None:
            logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        self.logger = get_logger(logger_name)
    
    def log_info(self, message: str, **kwargs):
        """Log info message with context"""
        log_with_context(self.logger, "INFO", message, **kwargs)
    
    def log_warning(self, message: str, **kwargs):
        """Log warning message with context"""
        log_with_context(self.logger, "WARNING", message, **kwargs)
    
    def log_error(self, message: str, **kwargs):
        """Log error message with context"""
        log_with_context(self.logger, "ERROR", message, **kwargs)
    
    def log_debug(self, message: str, **kwargs):
        """Log debug message with context"""
        log_with_context(self.logger, "DEBUG", message, **kwargs)
    
    def log_critical(self, message: str, **kwargs):
        """Log critical message with context"""
        log_with_context(self.logger, "CRITICAL", message, **kwargs)

# Default logger setup
def setup_default_logging():
    """Setup default logging configuration"""
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Setup root logger
    root_logger = setup_logger(
        "face_detection",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=logs_dir / "face_detection.log"
    )
    
    # Setup component-specific loggers
    setup_logger("face_detection.api", log_file=logs_dir / "api.log")
    setup_logger("face_detection.services", log_file=logs_dir / "services.log")
    setup_logger("face_detection.models", log_file=logs_dir / "models.log")
    setup_logger("face_detection.utils", log_file=logs_dir / "utils.log")
    
    return root_logger

# Performance logging decorator
def log_performance(logger_name: str = "face_detection.performance"):
    """
    Decorator to log function performance
    
    Args:
        logger_name: Logger name for performance logging
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                perf_logger = get_logger(logger_name)
                perf_logger.info(
                    f"Function {func.__name__} completed successfully",
                    function=func.__name__,
                    execution_time=execution_time,
                    status="success"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                perf_logger = get_logger(logger_name)
                perf_logger.error(
                    f"Function {func.__name__} failed",
                    function=func.__name__,
                    execution_time=execution_time,
                    error=str(e),
                    status="error"
                )
                raise
        
        return wrapper
    return decorator

# Error logging decorator
def log_errors(logger_name: str = "face_detection.errors"):
    """
    Decorator to log errors with context
    
    Args:
        logger_name: Logger name for error logging
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_logger = get_logger(logger_name)
                error_logger.error(
                    f"Error in {func.__name__}",
                    function=func.__name__,
                    error=str(e),
                    error_type=type(e).__name__,
                    args=str(args),
                    kwargs=str(kwargs)
                )
                raise
        return wrapper
    return decorator 
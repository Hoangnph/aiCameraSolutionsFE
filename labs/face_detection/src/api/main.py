"""
FastAPI Application for Face Detection System
Main application file with all API endpoints for face registration, recognition, and real-time processing.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
import asyncio
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import io
import face_recognition

# Import local modules
from ..services.face_processing import FaceProcessingService
from ..services.camera_service import CameraService
from ..services.simple_vector_db import SimpleVectorDB
from ..models.database import Person, FaceEmbedding, get_db, create_tables, init_default_settings
from ..utils.logger import setup_logger
from ..utils.response_models import (
    FaceRegistrationResponse,
    FaceRecognitionResponse,
    CameraStatusResponse,
    ErrorResponse,
    SuccessResponse
)

# Setup logging
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Face Detection System API",
    description="API for face registration, recognition, and real-time processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
face_service = FaceProcessingService()
camera_service = CameraService()
vector_db = SimpleVectorDB()

# Mount static files for uploaded images
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        logger.info("Starting Face Detection System API...")
        
        # Initialize database tables
        create_tables()
        init_default_settings()
        logger.info("Database tables initialized successfully")
        
        # Vector database is already initialized in constructor
        logger.info("Vector database initialized successfully")
        
        # Initialize face processing service
        await face_service.initialize()
        logger.info("Face processing service initialized successfully")
        
        # Initialize camera service
        await camera_service.initialize()
        logger.info("Camera service initialized successfully")
        
        logger.info("Face Detection System API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        logger.info("Shutting down Face Detection System API...")
        
        # Cleanup camera service
        await camera_service.cleanup()
        logger.info("Camera service cleaned up successfully")
        
        # Cleanup face processing service
        await face_service.cleanup()
        logger.info("Face processing service cleaned up successfully")
        
        # Cleanup vector database
        vector_db.cleanup()
        logger.info("Vector database cleaned up successfully")
        
        logger.info("Face Detection System API shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

@app.get("/", response_model=SuccessResponse)
async def root():
    """Root endpoint with system information"""
    return SuccessResponse(
        message="Face Detection System API",
        data={
            "version": "1.0.0",
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "docs": "/docs",
                "health": "/health",
                "upload": "/api/v1/faces/upload",
                "register": "/api/v1/faces/register",
                "recognize": "/api/v1/faces/recognize",
                "camera": "/api/v1/camera/status",
                "stream": "/api/v1/camera/stream"
            }
        }
    )

@app.get("/health", response_model=SuccessResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check service health
        services_status = {
            "face_processing": face_service.is_healthy(),
            "camera_service": camera_service.is_healthy(),
            "vector_database": vector_db.is_healthy()
        }
        
        overall_health = all(services_status.values())
        
        return SuccessResponse(
            message="Health check completed",
            data={
                "status": "healthy" if overall_health else "unhealthy",
                "services": services_status,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.post("/api/v1/faces/upload", response_model=FaceRegistrationResponse)
async def upload_face_image(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None)
):
    """
    Upload and process face image for registration
    
    Args:
        file: Image file (JPEG, PNG)
        name: Person's name
        email: Person's email (optional)
        phone: Person's phone (optional)
        notes: Additional notes (optional)
    
    Returns:
        FaceRegistrationResponse with registration details
    """
    try:
        logger.info(f"🔍 DEBUG: Starting face upload for person: {name}")
        logger.debug(f"🔍 DEBUG: File info - filename: {file.filename}, content_type: {file.content_type}, size: {file.size}")
        logger.debug(f"🔍 DEBUG: Form data - name: {name}, email: {email}, phone: {phone}, notes: {notes}")
        
        # Validate file type
        logger.debug(f"🔍 DEBUG: Validating file type - content_type: {file.content_type}")
        if not file.content_type or not file.content_type.startswith('image/'):
            logger.error(f"❌ DEBUG: Invalid file type - {file.content_type}")
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.debug("✅ DEBUG: File type validation passed")
        
        # Read and validate image
        logger.debug("🔍 DEBUG: Reading image file")
        image_data = await file.read()
        logger.debug(f"🔍 DEBUG: Image data size: {len(image_data)} bytes")
        
        logger.debug("🔍 DEBUG: Opening image with PIL")
        image = Image.open(io.BytesIO(image_data))
        logger.debug(f"🔍 DEBUG: Image format: {image.format}, size: {image.size}, mode: {image.mode}")
        
        # Convert to OpenCV format
        logger.debug("🔍 DEBUG: Converting to OpenCV format")
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        logger.debug(f"🔍 DEBUG: OpenCV image shape: {cv_image.shape}")
        
        # Process face detection and embedding with lower quality threshold for testing
        logger.debug("🔍 DEBUG: Starting face processing")
        original_threshold = face_service.quality_threshold
        face_service.quality_threshold = 0.3  # Lower threshold for testing
        logger.debug(f"🔍 DEBUG: Quality threshold set to: {face_service.quality_threshold}")
        
        face_data = face_service.process_image_for_registration(cv_image)
        face_service.quality_threshold = original_threshold  # Restore original threshold
        
        logger.debug(f"🔍 DEBUG: Face processing result: {face_data}")
        
        if not face_data or not face_data.get('success'):
            error_msg = face_data.get('error', 'No face detected in image') if face_data else 'No face detected in image'
            logger.error(f"❌ DEBUG: Face processing failed - {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        logger.debug("✅ DEBUG: Face processing successful")
        
        # Get the best embedding and quality score
        best_embedding = face_data['best_embedding']
        best_quality_score = face_data['best_quality_score']
        best_face_location = face_data['face_locations'][np.argmax(face_data['quality_scores'])]
        
        logger.debug(f"🔍 DEBUG: Best embedding shape: {len(best_embedding)}, quality score: {best_quality_score}")
        logger.debug(f"🔍 DEBUG: Best face location: {best_face_location}")
        
        # Save image to uploads directory
        logger.debug("🔍 DEBUG: Saving image to uploads directory")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"face_{timestamp}.jpg"
        image_path = f"uploads/{image_filename}"
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the image
        cv2.imwrite(image_path, cv_image)
        logger.debug(f"✅ DEBUG: Image saved to: {image_path}")
        
        # Get database session
        logger.debug("🔍 DEBUG: Getting database session")
        db = next(get_db())
        try:
            # Create person record
            logger.debug("🔍 DEBUG: Creating person record")
            person = Person(
                name=name,
                email=email,
                phone=phone,
                department=None,
                position=None,
                status="active"
            )
            db.add(person)
            db.flush()  # Get the ID
            logger.debug(f"✅ DEBUG: Person created with ID: {person.person_id}")
            
            # Create face embedding record
            logger.debug("🔍 DEBUG: Creating face embedding record")
            face_embedding = FaceEmbedding(
                person_id=person.person_id,
                embedding_data=json.dumps(best_embedding),
                quality_score=best_quality_score,
                model_version="1.0"
            )
            db.add(face_embedding)
            
            # Commit to database
            logger.debug("🔍 DEBUG: Committing to database")
            db.commit()
            
            # Get the embedding ID after commit
            embedding_id = face_embedding.embedding_id
            logger.debug(f"✅ DEBUG: Face embedding created with ID: {embedding_id}")
            
            # Save to vector database
            logger.debug("🔍 DEBUG: Saving to vector database")
            vector_db.add_face_embedding(
                embedding=best_embedding,
                metadata={
                    'person_id': person.person_id,
                    'name': person.name,
                    'email': person.email,
                    'phone': person.phone,
                    'notes': notes,
                    'embedding_id': embedding_id,
                    'image_path': image_path,
                    'quality_score': best_quality_score,
                    'upload_timestamp': timestamp
                }
            )
            logger.debug("✅ DEBUG: Saved to vector database")
            
            logger.info(f"✅ DEBUG: Face registered successfully for person: {name}")
            
            return FaceRegistrationResponse(
                success=True,
                message="Face registered successfully",
                data={
                    "person_id": person.person_id,
                    "name": person.name,
                    "email": person.email,
                    "phone": person.phone,
                    "embedding_id": embedding_id,
                    "image_path": image_path,
                    "quality_score": best_quality_score,
                    "face_count": len(face_data['face_locations']),
                    "upload_timestamp": timestamp
                },
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"❌ DEBUG: Database error during face registration: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ DEBUG: Face upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Face upload failed: {str(e)}")

@app.post("/api/v1/faces/recognize", response_model=FaceRecognitionResponse)
async def recognize_face(
    file: UploadFile = File(...),
    threshold: float = Form(0.6)
):
    """
    Recognize face from uploaded image
    
    Args:
        file: Image file (JPEG, PNG)
        threshold: Recognition confidence threshold (default: 0.6)
    
    Returns:
        FaceRecognitionResponse with recognition results
    """
    try:
        logger.info("🔍 DEBUG: Starting face recognition request")
        logger.debug(f"🔍 DEBUG: File info - filename: {file.filename}, content_type: {file.content_type}, size: {file.size}")
        logger.debug(f"🔍 DEBUG: Threshold: {threshold}")
        
        # Validate file type
        logger.debug(f"🔍 DEBUG: Validating file type - content_type: {file.content_type}")
        if not file.content_type or not file.content_type.startswith('image/'):
            logger.error(f"❌ DEBUG: Invalid file type - {file.content_type}")
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.debug("✅ DEBUG: File type validation passed")
        
        # Read and validate image
        logger.debug("🔍 DEBUG: Reading image file")
        image_data = await file.read()
        logger.debug(f"🔍 DEBUG: Image data size: {len(image_data)} bytes")
        
        logger.debug("🔍 DEBUG: Opening image with PIL")
        image = Image.open(io.BytesIO(image_data))
        logger.debug(f"🔍 DEBUG: Image format: {image.format}, size: {image.size}, mode: {image.mode}")
        
        # Convert to OpenCV format
        logger.debug("🔍 DEBUG: Converting to OpenCV format")
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        logger.debug(f"🔍 DEBUG: OpenCV image shape: {cv_image.shape}")
        
        # Process face detection and embedding
        logger.debug("🔍 DEBUG: Starting face detection and embedding")
        face_data = face_service.process_image_for_recognition(cv_image, [])
        logger.debug(f"🔍 DEBUG: Face processing result: {face_data}")
        
        if not face_data or not face_data.get('success'):
            error_msg = face_data.get('error', 'No face detected in image') if face_data else 'No face detected in image'
            logger.error(f"❌ DEBUG: Face processing failed - {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        logger.debug("✅ DEBUG: Face processing successful")
        
        if not face_data.get('faces'):
            logger.debug("🔍 DEBUG: No faces detected in image")
            return FaceRecognitionResponse(
                success=True,
                message="No faces detected in image",
                data={
                    "recognized": False,
                    "matches": [],
                    "confidence": 0.0
                }
            )
        
        # Get the first face result
        face_result = face_data['faces'][0]
        logger.debug(f"🔍 DEBUG: Face result: {face_result}")
        
        if not face_result.get('embedding'):
            logger.error("❌ DEBUG: Failed to generate embedding for detected face")
            raise HTTPException(status_code=400, detail="Failed to generate embedding for detected face")
        
        logger.debug(f"✅ DEBUG: Generated embedding with shape: {len(face_result['embedding'])}")
        
        # Search for matching face in vector database
        logger.debug(f"🔍 DEBUG: Searching for similar faces with threshold: {threshold}")
        matches = vector_db.search_similar_faces(
            embedding=face_result['embedding'],
            threshold=threshold,
            limit=5
        )
        
        if not matches:
            return FaceRecognitionResponse(
                success=True,
                message="No matching face found",
                data={
                    "recognized": False,
                    "matches": [],
                    "confidence": 0.0
                }
            )
        
        # Get best match
        best_match = matches[0]
        
        # Safely get metadata fields with defaults
        metadata = best_match.get('metadata', {})
        
        return FaceRecognitionResponse(
            success=True,
            message="Face recognized successfully",
            data={
                "recognized": True,
                "person": {
                    "id": metadata.get('person_id'),
                    "name": metadata.get('name', 'Unknown'),
                    "email": metadata.get('email'),
                    "phone": metadata.get('phone'),
                    "notes": metadata.get('notes')  # This field might not exist in database
                },
                "confidence": best_match['similarity'],
                "matches": [
                    {
                        "name": match['metadata'].get('name', 'Unknown'),
                        "confidence": match['similarity']
                    }
                    for match in matches[:3]
                ]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Face recognition failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Face recognition failed: {str(e)}")

@app.post("/api/v1/faces/detect")
async def detect_faces(file: UploadFile = File(...)):
    """
    Detect faces in image and return bounding boxes
    """
    try:
        # Validate file
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        image_data = await file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Detect faces
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Convert face locations to bounding boxes
        faces = []
        for i, (top, right, bottom, left) in enumerate(face_locations):
            face_info = {
                "id": i,
                "bounding_box": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left,
                    "width": right - left,
                    "height": bottom - top
                },
                "confidence": 0.9,  # Placeholder confidence
                "quality_score": 0.8  # Placeholder quality score
            }
            faces.append(face_info)
        
        return {
            "success": True,
            "message": f"Detected {len(faces)} faces",
            "data": {
                "faces": faces,
                "total_faces": len(faces),
                "image_size": {
                    "width": image.shape[1],
                    "height": image.shape[0]
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Face detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Face detection failed: {str(e)}")

@app.get("/api/v1/camera/status", response_model=CameraStatusResponse)
async def get_camera_status():
    """Get current camera status"""
    try:
        status = camera_service.get_camera_status()
        
        return CameraStatusResponse(
            success=True,
            message="Camera status retrieved successfully",
            data=status
        )
        
    except Exception as e:
        logger.error(f"Failed to get camera status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get camera status")

@app.post("/api/v1/camera/start")
async def start_camera(camera_request: dict):
    """Start camera service"""
    try:
        camera_id = camera_request.get('camera_id', 0)
        logger.info(f"Starting camera {camera_id}")
        
        # Force cleanup any existing camera
        camera_service.force_cleanup_camera(camera_id)
        
        # Check if camera is available
        if not camera_service.is_camera_available(camera_id):
            raise HTTPException(status_code=400, detail=f"Camera {camera_id} is not available")
        
        # Start camera service
        success = camera_service.start_video_stream(camera_id)
        
        if success:
            logger.info(f"Camera {camera_id} started successfully")
            return SuccessResponse(
                message="Camera started successfully",
                data={"status": "started"}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to start camera")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start camera: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start camera")

@app.post("/api/v1/camera/stop")
async def stop_camera():
    """Stop camera service"""
    try:
        logger.info("Stopping camera service")
        
        # Force cleanup all cameras
        camera_service.force_cleanup_camera(0)
        camera_service.force_cleanup_camera(1)
        
        logger.info("Camera service stopped successfully")
        return SuccessResponse(
            message="Camera stopped successfully",
            data={"status": "stopped"}
        )
        
    except Exception as e:
        logger.error(f"Failed to stop camera: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to stop camera")

@app.get("/api/v1/camera/stream")
async def get_camera_stream():
    """Get real-time camera stream with face recognition"""
    try:
        async def generate_frames():
            """Generate video frames with face recognition overlay"""
            # Get frame generator
            frame_generator = camera_service.get_frame_generator()
            
            for frame in frame_generator:
                if frame is not None:
                    # Process frame for face recognition
                    recognition_results = await face_service.process_frame(frame)
                    
                    # Draw recognition results on frame
                    processed_frame = await face_service.draw_recognition_results(
                        frame, recognition_results
                    )
                    
                    # Encode frame as JPEG
                    _, buffer = cv2.imencode('.jpg', processed_frame)
                    frame_bytes = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                await asyncio.sleep(0.033)  # ~30 FPS
        
        return StreamingResponse(
            generate_frames(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
        
    except Exception as e:
        logger.error(f"Failed to get camera stream: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get camera stream")

@app.get("/api/v1/faces/{face_id}/image")
async def get_face_image(face_id: str):
    """Get face image by ID"""
    try:
        # Get face data from database
        face_data = vector_db.get_face_by_id(face_id)
        if not face_data:
            raise HTTPException(status_code=404, detail="Face not found")
        
        # Get image path from metadata
        image_path = face_data.get('metadata', {}).get('image_path')
        if not image_path:
            raise HTTPException(status_code=404, detail="Face image not found")
        
        # Check if file exists
        full_path = os.path.join(os.getcwd(), image_path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Face image file not found")
        
        # Return image file
        from fastapi.responses import FileResponse
        return FileResponse(full_path, media_type="image/jpeg")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get face image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get face image")

@app.get("/api/v1/faces/list")
async def list_registered_faces():
    """List all registered faces"""
    try:
        faces = vector_db.list_all_faces()
        
        # Add image URLs to each face
        for face in faces:
            face['image_url'] = f"/api/v1/faces/{face['id']}/image"
        
        return SuccessResponse(
            message="Faces retrieved successfully",
            data={"faces": faces}
        )
        
    except Exception as e:
        logger.error(f"Failed to list faces: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list faces")

@app.delete("/api/v1/faces/{face_id}")
async def delete_face(face_id: str):
    """Delete a registered face"""
    try:
        vector_db.delete_face(face_id)
        
        return SuccessResponse(
            message="Face deleted successfully",
            data={"face_id": face_id}
        )
        
    except Exception as e:
        logger.error(f"Failed to delete face: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete face")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
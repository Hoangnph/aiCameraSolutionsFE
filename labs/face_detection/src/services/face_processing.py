"""
Face processing service using face_recognition library
"""
import cv2
import numpy as np
import face_recognition
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
import io
import base64
from loguru import logger
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from config.config import settings

class FaceProcessingService:
    """Service for face detection and recognition"""
    
    def __init__(self):
        """Initialize face processing service"""
        self.tolerance = settings.face_recognition_tolerance
        self.min_face_size = settings.min_face_size
        self.max_face_size = settings.max_face_size
        self.quality_threshold = settings.quality_threshold
        
        logger.info("Face processing service initialized")
    
    async def initialize(self):
        """Initialize the face processing service"""
        try:
            # Test face recognition library
            test_image = np.zeros((100, 100, 3), dtype=np.uint8)
            face_recognition.face_locations(test_image)
            logger.info("Face processing service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize face processing service: {str(e)}")
            raise
    
    async def cleanup(self):
        """Cleanup the face processing service"""
        try:
            logger.info("Face processing service cleaned up successfully")
        except Exception as e:
            logger.error(f"Failed to cleanup face processing service: {str(e)}")
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Simple health check
            return True
        except Exception as e:
            logger.error(f"Face processing service health check failed: {str(e)}")
            return False
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image
        
        Args:
            image: Input image as numpy array (RGB format)
        
        Returns:
            List of face locations (top, right, bottom, left)
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Check if it's BGR (OpenCV format)
                if image.dtype == np.uint8:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    image_rgb = image
            else:
                image_rgb = image
            
            # Detect faces
            face_locations = face_recognition.face_locations(image_rgb)
            
            # Filter by size
            filtered_locations = []
            for top, right, bottom, left in face_locations:
                face_width = right - left
                face_height = bottom - top
                
                if (self.min_face_size <= face_width <= self.max_face_size and 
                    self.min_face_size <= face_height <= self.max_face_size):
                    filtered_locations.append((top, right, bottom, left))
            
            logger.info(f"Detected {len(filtered_locations)} faces in image")
            return filtered_locations
            
        except Exception as e:
            logger.error(f"Failed to detect faces: {str(e)}")
            return []
    
    def generate_embedding(self, image: np.ndarray, face_location: Tuple[int, int, int, int]) -> Optional[List[float]]:
        """
        Generate face embedding for given face location
        
        Args:
            image: Input image as numpy array
            face_location: Face location (top, right, bottom, left)
        
        Returns:
            Face embedding as 128-dimensional vector or None
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                if image.dtype == np.uint8:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    image_rgb = image
            else:
                image_rgb = image
            
            # Generate embedding
            embeddings = face_recognition.face_encodings(image_rgb, [face_location])
            
            if embeddings:
                embedding = embeddings[0].tolist()
                logger.info(f"Generated embedding with {len(embedding)} dimensions")
                return embedding
            else:
                logger.warning("Failed to generate embedding for face location")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            return None
    
    def assess_face_quality(self, image: np.ndarray, face_location: Tuple[int, int, int, int]) -> float:
        """
        Assess quality of face image
        
        Args:
            image: Input image as numpy array
            face_location: Face location (top, right, bottom, left)
        
        Returns:
            Quality score between 0 and 1
        """
        try:
            top, right, bottom, left = face_location
            
            # Extract face region
            face_image = image[top:bottom, left:right]
            
            if face_image.size == 0:
                return 0.0
            
            # Calculate quality metrics
            quality_score = 0.0
            
            # 1. Face size score (larger faces are better)
            face_width = right - left
            face_height = bottom - top
            size_score = min(face_width * face_height / (self.max_face_size ** 2), 1.0)
            quality_score += size_score * 0.3
            
            # 2. Aspect ratio score (square-ish faces are better)
            aspect_ratio = face_width / face_height if face_height > 0 else 1.0
            aspect_score = 1.0 - abs(aspect_ratio - 1.0) * 0.5
            quality_score += max(aspect_score, 0.0) * 0.2
            
            # 3. Brightness score
            if len(face_image.shape) == 3:
                gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_face = face_image
            
            mean_brightness = np.mean(gray_face)
            brightness_score = 1.0 - abs(mean_brightness - 128) / 128
            quality_score += max(brightness_score, 0.0) * 0.3
            
            # 4. Contrast score
            contrast = np.std(gray_face)
            contrast_score = min(contrast / 50.0, 1.0)
            quality_score += contrast_score * 0.2
            
            # Normalize to [0, 1]
            quality_score = max(0.0, min(1.0, quality_score))
            
            logger.info(f"Face quality score: {quality_score:.3f}")
            return quality_score
            
        except Exception as e:
            logger.error(f"Failed to assess face quality: {str(e)}")
            return 0.0
    
    def compare_faces(self, known_embeddings: List[List[float]], query_embedding: List[float]) -> List[bool]:
        """
        Compare query face with known faces
        
        Args:
            known_embeddings: List of known face embeddings
            query_embedding: Query face embedding
        
        Returns:
            List of boolean matches
        """
        try:
            if not known_embeddings or not query_embedding:
                return []
            
            # Convert to numpy arrays
            known_array = np.array(known_embeddings)
            query_array = np.array([query_embedding])
            
            # Compare faces
            matches = face_recognition.compare_faces(
                known_array, 
                query_array[0], 
                tolerance=self.tolerance
            )
            
            logger.info(f"Compared query face with {len(known_embeddings)} known faces")
            return matches
            
        except Exception as e:
            logger.error(f"Failed to compare faces: {str(e)}")
            return []
    
    def calculate_face_distance(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate distance between two face embeddings
        
        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
        
        Returns:
            Distance between embeddings (lower is more similar)
        """
        try:
            # Convert to numpy arrays
            emb1_array = np.array([embedding1])
            emb2_array = np.array([embedding2])
            
            # Calculate distance
            distance = face_recognition.face_distance(emb1_array, embedding2)[0]
            
            return float(distance)
            
        except Exception as e:
            logger.error(f"Failed to calculate face distance: {str(e)}")
            return 1.0
    
    def process_image_for_registration(
        self, 
        image: np.ndarray
    ) -> Dict[str, Any]:
        """
        Process image for face registration
        
        Args:
            image: Input image as numpy array
        
        Returns:
            Dictionary with processing results
        """
        try:
            # Detect faces
            face_locations = self.detect_faces(image)
            
            if not face_locations:
                return {
                    "success": False,
                    "error": "No faces detected in image",
                    "face_locations": [],
                    "embeddings": [],
                    "quality_scores": []
                }
            
            # Generate embeddings and assess quality
            embeddings = []
            quality_scores = []
            
            for face_location in face_locations:
                embedding = self.generate_embedding(image, face_location)
                quality_score = self.assess_face_quality(image, face_location)
                
                if embedding:
                    embeddings.append(embedding)
                    quality_scores.append(quality_score)
                else:
                    logger.warning(f"Failed to generate embedding for face at {face_location}")
            
            # Check if we have any valid embeddings
            if not embeddings:
                return {
                    "success": False,
                    "error": "Failed to generate embeddings for detected faces",
                    "face_locations": face_locations,
                    "embeddings": embeddings,
                    "quality_scores": quality_scores
                }
            
            # Check quality threshold
            valid_embeddings = []
            valid_quality_scores = []
            valid_locations = []
            
            for i, (embedding, quality_score) in enumerate(zip(embeddings, quality_scores)):
                if quality_score >= self.quality_threshold:
                    valid_embeddings.append(embedding)
                    valid_quality_scores.append(quality_score)
                    valid_locations.append(face_locations[i])
                else:
                    logger.warning(f"Face quality {quality_score:.3f} below threshold {self.quality_threshold}")
            
            if not valid_embeddings:
                return {
                    "success": False,
                    "error": f"No faces meet quality threshold {self.quality_threshold}",
                    "face_locations": face_locations,
                    "embeddings": embeddings,
                    "quality_scores": quality_scores
                }
            
            return {
                "success": True,
                "face_locations": valid_locations,
                "embeddings": valid_embeddings,
                "quality_scores": valid_quality_scores,
                "best_embedding": valid_embeddings[np.argmax(valid_quality_scores)],
                "best_quality_score": max(valid_quality_scores)
            }
            
        except Exception as e:
            logger.error(f"Failed to process image for registration: {str(e)}")
            return {
                "success": False,
                "error": f"Processing error: {str(e)}",
                "face_locations": [],
                "embeddings": [],
                "quality_scores": []
            }
    
    def process_image_for_recognition(
        self, 
        image: np.ndarray,
        known_embeddings: List[List[float]]
    ) -> Dict[str, Any]:
        """
        Process image for face recognition
        
        Args:
            image: Input image as numpy array
            known_embeddings: List of known face embeddings
        
        Returns:
            Dictionary with recognition results
        """
        try:
            # Detect faces
            face_locations = self.detect_faces(image)
            
            if not face_locations:
                return {
                    "success": True,
                    "faces": [],
                    "message": "No faces detected"
                }
            
            # Process each face
            face_results = []
            
            for face_location in face_locations:
                embedding = self.generate_embedding(image, face_location)
                
                if embedding:
                    # Compare with known embeddings
                    matches = self.compare_faces(known_embeddings, embedding)
                    
                    # Calculate distances
                    distances = []
                    for known_emb in known_embeddings:
                        distance = self.calculate_face_distance(embedding, known_emb)
                        distances.append(distance)
                    
                    # Find best match
                    if distances:
                        min_distance = min(distances)
                        best_match_index = distances.index(min_distance)
                        similarity = 1.0 - min_distance
                        
                        face_results.append({
                            "face_location": face_location,
                            "embedding": embedding,
                            "best_match_index": best_match_index if matches[best_match_index] else None,
                            "similarity": similarity,
                            "distance": min_distance,
                            "matched": matches[best_match_index] if best_match_index < len(matches) else False
                        })
                    else:
                        face_results.append({
                            "face_location": face_location,
                            "embedding": embedding,
                            "best_match_index": None,
                            "similarity": 0.0,
                            "distance": 1.0,
                            "matched": False
                        })
                else:
                    logger.warning(f"Failed to generate embedding for face at {face_location}")
            
            return {
                "success": True,
                "faces": face_results
            }
            
        except Exception as e:
            logger.error(f"Failed to process image for recognition: {str(e)}")
            return {
                "success": False,
                "error": f"Recognition error: {str(e)}",
                "faces": []
            }
    
    def encode_image_to_base64(self, image: np.ndarray) -> str:
        """
        Encode image to base64 string
        
        Args:
            image: Input image as numpy array
        
        Returns:
            Base64 encoded image string
        """
        try:
            # Convert to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            logger.error(f"Failed to encode image to base64: {str(e)}")
            return ""
    
    def decode_base64_to_image(self, base64_string: str) -> Optional[np.ndarray]:
        """
        Decode base64 string to image
        
        Args:
            base64_string: Base64 encoded image string
        
        Returns:
            Image as numpy array or None
        """
        try:
            # Remove data URL prefix if present
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            image_data = base64.b64decode(base64_string)
            
            # Convert to numpy array
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Failed to decode base64 image: {str(e)}")
            return None

    async def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame for face recognition
        
        Args:
            frame: Input frame as numpy array
        
        Returns:
            Recognition results dictionary
        """
        try:
            # Detect faces in frame
            face_locations = self.detect_faces(frame)
            
            if not face_locations:
                return {
                    'success': True,
                    'faces_detected': 0,
                    'recognitions': []
                }
            
            # Get known embeddings from vector database
            from .simple_vector_db import SimpleVectorDB
            vector_db = SimpleVectorDB()
            known_faces = vector_db.list_all_faces()
            
            if not known_faces:
                return {
                    'success': True,
                    'faces_detected': len(face_locations),
                    'recognitions': []
                }
            
            # Extract known embeddings
            known_embeddings = []
            known_names = []
            for face in known_faces:
                embedding_data = face.get('embedding')
                if embedding_data:
                    known_embeddings.append(embedding_data)
                    known_names.append(face.get('metadata', {}).get('name', 'Unknown'))
            
            # Process each detected face
            recognitions = []
            for i, face_location in enumerate(face_locations):
                # Generate embedding for detected face
                embedding = self.generate_embedding(frame, face_location)
                
                if embedding is None:
                    continue
                
                # Compare with known faces
                matches = self.compare_faces(known_embeddings, embedding)
                
                # Find best match
                best_match_index = None
                best_distance = float('inf')
                
                for j, match in enumerate(matches):
                    if match:
                        distance = self.calculate_face_distance(known_embeddings[j], embedding)
                        if distance < best_distance:
                            best_distance = distance
                            best_match_index = j
                
                # Create recognition result
                recognition_result = {
                    'face_id': i,
                    'location': face_location,
                    'recognized': best_match_index is not None,
                    'name': known_names[best_match_index] if best_match_index is not None else 'Unknown',
                    'confidence': 1.0 - best_distance if best_match_index is not None else 0.0,
                    'distance': best_distance if best_match_index is not None else float('inf')
                }
                
                recognitions.append(recognition_result)
            
            return {
                'success': True,
                'faces_detected': len(face_locations),
                'recognitions': recognitions
            }
            
        except Exception as e:
            logger.error(f"Failed to process frame: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'faces_detected': 0,
                'recognitions': []
            }

    async def draw_recognition_results(self, frame: np.ndarray, recognition_results: Dict[str, Any]) -> np.ndarray:
        """
        Draw recognition results on frame
        
        Args:
            frame: Input frame as numpy array
            recognition_results: Results from process_frame
        
        Returns:
            Frame with recognition results drawn
        """
        try:
            # Create a copy of the frame
            result_frame = frame.copy()
            
            if not recognition_results.get('success', False):
                return result_frame
            
            recognitions = recognition_results.get('recognitions', [])
            
            for recognition in recognitions:
                location = recognition.get('location')
                if not location:
                    continue
                
                top, right, bottom, left = location
                name = recognition.get('name', 'Unknown')
                confidence = recognition.get('confidence', 0.0)
                recognized = recognition.get('recognized', False)
                
                # Choose color based on recognition status
                if recognized:
                    color = (0, 255, 0)  # Green for recognized
                else:
                    color = (0, 0, 255)  # Red for unrecognized
                
                # Draw bounding box
                cv2.rectangle(result_frame, (left, top), (right, bottom), color, 2)
                
                # Draw name and confidence
                label = f"{name}: {confidence:.2%}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                
                # Draw label background
                cv2.rectangle(result_frame, 
                            (left, top - label_size[1] - 10), 
                            (left + label_size[0], top), 
                            color, -1)
                
                # Draw label text
                cv2.putText(result_frame, label, 
                           (left, top - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            return result_frame
            
        except Exception as e:
            logger.error(f"Failed to draw recognition results: {str(e)}")
            return frame

# Global instance
face_processor = FaceProcessingService() 
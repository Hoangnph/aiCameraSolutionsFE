"""
Test core infrastructure components
"""
import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from config.config import settings
from src.models.database import create_tables, init_default_settings, SessionLocal
from src.services.simple_vector_db import SimpleVectorDatabaseService as VectorDatabaseService
from src.services.face_processing import FaceProcessingService
from src.services.camera_service import CameraService

class TestCoreInfrastructure:
    """Test class for core infrastructure components"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        # Create test directories
        os.makedirs("./data", exist_ok=True)
        os.makedirs("./uploads", exist_ok=True)
        os.makedirs("./logs", exist_ok=True)
        
        # Create test database
        create_tables()
        init_default_settings()
        
        yield
        
        # Cleanup
        if os.path.exists("./data/metadata.db"):
            os.remove("./data/metadata.db")
        if os.path.exists("./data/vector_db"):
            import shutil
            shutil.rmtree("./data/vector_db", ignore_errors=True)
    
    def test_config_loading(self):
        """Test configuration loading"""
        assert settings.app_name == "Face Detection System"
        assert settings.face_recognition_tolerance == 0.6
        assert settings.quality_threshold == 0.7
        assert settings.camera_device_id == 0
        print("✅ Configuration loading test passed")
    
    def test_database_creation(self):
        """Test database creation and initialization"""
        # Test database connection
        db = SessionLocal()
        try:
            # Test that tables exist
            from src.models.database import Person, SystemSetting
            result = db.query(SystemSetting).first()
            assert result is not None
            print("✅ Database creation test passed")
        finally:
            db.close()
    
    def test_vector_database_service(self):
        """Test vector database service"""
        # Initialize service
        vector_db = VectorDatabaseService()
        
        # Test collection stats
        stats = vector_db.get_collection_stats()
        assert "total_embeddings" in stats
        assert "unique_persons" in stats
        print("✅ Vector database service test passed")
    
    def test_face_processing_service(self):
        """Test face processing service"""
        # Initialize service
        face_processor = FaceProcessingService()
        
        # Create test image with face
        test_image = self._create_test_image_with_face()
        
        # Test face detection
        face_locations = face_processor.detect_faces(test_image)
        assert isinstance(face_locations, list)
        print("✅ Face processing service test passed")
    
    def test_camera_service(self):
        """Test camera service"""
        # Initialize service
        camera_service = CameraService()
        
        # Test getting available cameras
        cameras = camera_service.get_available_cameras()
        assert isinstance(cameras, list)
        print("✅ Camera service test passed")
    
    def test_face_embedding_generation(self):
        """Test face embedding generation"""
        face_processor = FaceProcessingService()
        
        # Create test image
        test_image = self._create_test_image_with_face()
        
        # Detect faces
        face_locations = face_processor.detect_faces(test_image)
        
        if face_locations:
            # Generate embedding
            embedding = face_processor.generate_embedding(test_image, face_locations[0])
            assert embedding is not None
            assert len(embedding) == 128
            print("✅ Face embedding generation test passed")
        else:
            print("⚠️ No faces detected in test image")
    
    def test_face_quality_assessment(self):
        """Test face quality assessment"""
        face_processor = FaceProcessingService()
        
        # Create test image
        test_image = self._create_test_image_with_face()
        
        # Detect faces
        face_locations = face_processor.detect_faces(test_image)
        
        if face_locations:
            # Assess quality
            quality_score = face_processor.assess_face_quality(test_image, face_locations[0])
            assert 0.0 <= quality_score <= 1.0
            print("✅ Face quality assessment test passed")
        else:
            print("⚠️ No faces detected in test image")
    
    def test_vector_database_operations(self):
        """Test vector database operations"""
        vector_db = VectorDatabaseService()
        
        # Test adding embedding
        test_embedding = [0.1] * 128  # 128-dimensional test vector
        test_metadata = {
            "person_id": "test_person",
            "name": "Test Person",
            "quality_score": 0.9
        }
        
        success = vector_db.add_embedding("test_emb_001", test_embedding, test_metadata)
        assert success is True
        
        # Test searching
        results = vector_db.search_similar_faces(test_embedding, n_results=5)
        assert isinstance(results, list)
        
        # Test getting embeddings by person
        embeddings = vector_db.get_embeddings_by_person("test_person")
        assert len(embeddings) > 0
        
        print("✅ Vector database operations test passed")
    
    def test_camera_frame_capture(self):
        """Test camera frame capture"""
        camera_service = CameraService()
        
        # Test frame capture (if camera available)
        frame = camera_service.capture_frame()
        
        if frame is not None:
            assert isinstance(frame, np.ndarray)
            assert len(frame.shape) == 3  # Should be 3D (height, width, channels)
            print("✅ Camera frame capture test passed")
        else:
            print("⚠️ No camera available for frame capture test")
    
    def test_image_processing_pipeline(self):
        """Test complete image processing pipeline"""
        face_processor = FaceProcessingService()
        
        # Create test image
        test_image = self._create_test_image_with_face()
        
        # Test registration pipeline
        registration_result = face_processor.process_image_for_registration(test_image)
        assert isinstance(registration_result, dict)
        assert "success" in registration_result
        
        print("✅ Image processing pipeline test passed")
    
    def test_face_comparison(self):
        """Test face comparison functionality"""
        face_processor = FaceProcessingService()
        
        # Create test embeddings
        embedding1 = [0.1] * 128
        embedding2 = [0.1] * 128  # Similar embedding
        embedding3 = [0.9] * 128  # Different embedding
        
        # Test comparison
        matches = face_processor.compare_faces([embedding1, embedding3], embedding2)
        assert isinstance(matches, list)
        assert len(matches) == 2
        
        # Test distance calculation
        distance = face_processor.calculate_face_distance(embedding1, embedding2)
        assert isinstance(distance, float)
        assert distance >= 0.0
        
        print("✅ Face comparison test passed")
    
    def test_camera_service_filters(self):
        """Test camera service filters"""
        camera_service = CameraService()
        
        # Create test frame
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test filters
        filters = ["grayscale", "blur", "sharpen"]
        for filter_name in filters:
            filtered_frame = camera_service.apply_filters(test_frame, [filter_name])
            assert isinstance(filtered_frame, np.ndarray)
            assert filtered_frame.shape == test_frame.shape
        
        print("✅ Camera service filters test passed")
    
    def test_vector_database_backup_restore(self):
        """Test vector database backup and restore"""
        vector_db = VectorDatabaseService()
        
        # Add test data
        test_embedding = [0.1] * 128
        test_metadata = {"person_id": "test_backup", "name": "Test Backup"}
        vector_db.add_embedding("backup_test_001", test_embedding, test_metadata)
        
        # Test backup
        backup_path = "./data/test_backup.json"
        success = vector_db.backup_collection(backup_path)
        assert success is True
        assert os.path.exists(backup_path)
        
        # Test restore
        restore_success = vector_db.restore_collection(backup_path)
        assert restore_success is True
        
        # Cleanup
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        print("✅ Vector database backup/restore test passed")
    
    def _create_test_image_with_face(self):
        """Create a test image with a simple face-like pattern"""
        # Create a simple test image (this won't have real faces but will test the pipeline)
        image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Add a simple face-like rectangle (for testing purposes)
        cv2.rectangle(image, (200, 150), (400, 350), (255, 255, 255), -1)
        cv2.circle(image, (300, 200), 30, (0, 0, 0), -1)  # Left eye
        cv2.circle(image, (350, 200), 30, (0, 0, 0), -1)  # Right eye
        cv2.ellipse(image, (325, 280), (50, 30), 0, 0, 180, (0, 0, 0), -1)  # Mouth
        
        return image

def run_automation_tests():
    """Run all automation tests"""
    print("🚀 Starting Core Infrastructure Automation Tests...")
    
    # Create test instance
    test_instance = TestCoreInfrastructure()
    
    # Run setup
    test_instance.setup()
    
    # Run tests
    tests = [
        test_instance.test_config_loading,
        test_instance.test_database_creation,
        test_instance.test_vector_database_service,
        test_instance.test_face_processing_service,
        test_instance.test_camera_service,
        test_instance.test_face_embedding_generation,
        test_instance.test_face_quality_assessment,
        test_instance.test_vector_database_operations,
        test_instance.test_camera_frame_capture,
        test_instance.test_image_processing_pipeline,
        test_instance.test_face_comparison,
        test_instance.test_camera_service_filters,
        test_instance.test_vector_database_backup_restore
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {str(e)}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Core Infrastructure tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    run_automation_tests() 
#!/usr/bin/env python3
"""
Simple test script for Face Detection System
Tests basic functionality without starting the full server.
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.services.face_processing import FaceProcessingService
        print("✅ FaceProcessingService imported successfully")
    except Exception as e:
        print(f"❌ Failed to import FaceProcessingService: {e}")
        return False
    
    try:
        from src.services.camera_service import CameraService
        print("✅ CameraService imported successfully")
    except Exception as e:
        print(f"❌ Failed to import CameraService: {e}")
        return False
    
    try:
        from src.services.simple_vector_db import SimpleVectorDB
        print("✅ SimpleVectorDB imported successfully")
    except Exception as e:
        print(f"❌ Failed to import SimpleVectorDB: {e}")
        return False
    
    try:
        from src.utils.logger import setup_logger
        print("✅ Logger utilities imported successfully")
    except Exception as e:
        print(f"❌ Failed to import logger utilities: {e}")
        return False
    
    return True

def test_services():
    """Test service initialization"""
    print("\nTesting service initialization...")
    
    try:
        from src.services.face_processing import FaceProcessingService
        face_service = FaceProcessingService()
        print("✅ FaceProcessingService initialized")
    except Exception as e:
        print(f"❌ Failed to initialize FaceProcessingService: {e}")
        return False
    
    try:
        from src.services.camera_service import CameraService
        camera_service = CameraService()
        print("✅ CameraService initialized")
    except Exception as e:
        print(f"❌ Failed to initialize CameraService: {e}")
        return False
    
    try:
        from src.services.simple_vector_db import SimpleVectorDB
        vector_db = SimpleVectorDB("test_vectors.db")
        print("✅ SimpleVectorDB initialized")
        
        # Test basic operations
        stats = vector_db.get_statistics()
        print(f"✅ Vector DB statistics: {stats}")
        
        # Cleanup test database
        import os
        if os.path.exists("test_vectors.db"):
            os.remove("test_vectors.db")
        
    except Exception as e:
        print(f"❌ Failed to initialize SimpleVectorDB: {e}")
        return False
    
    return True

def test_face_recognition():
    """Test face recognition functionality"""
    print("\nTesting face recognition...")
    
    try:
        import numpy as np
        import face_recognition
        
        # Create a simple test image
        test_image = np.zeros((300, 300, 3), dtype=np.uint8)
        
        # Test face detection
        face_locations = face_recognition.face_locations(test_image)
        print(f"✅ Face detection works (found {len(face_locations)} faces)")
        
        # Test face encoding (should work even with no faces)
        face_encodings = face_recognition.face_encodings(test_image)
        print(f"✅ Face encoding works (generated {len(face_encodings)} encodings)")
        
    except Exception as e:
        print(f"❌ Face recognition test failed: {e}")
        return False
    
    return True

def test_api_import():
    """Test API import"""
    print("\nTesting API import...")
    
    try:
        from src.api.main import app
        print("✅ FastAPI app imported successfully")
        
        # Test basic app properties
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        
    except Exception as e:
        print(f"❌ Failed to import API: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Face Detection System - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Service Tests", test_services),
        ("Face Recognition Tests", test_face_recognition),
        ("API Import Tests", test_api_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
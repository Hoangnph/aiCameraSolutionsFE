"""
Setup script for Face Detection System
"""
import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Install core dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "./data",
        "./uploads", 
        "./logs",
        "./src/models",
        "./src/services",
        "./src/utils",
        "./src/api",
        "./tests/unit",
        "./tests/integration",
        "./automation_test"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")

def setup_database():
    """Setup database and initialize tables"""
    print("🗄️ Setting up database...")
    
    try:
        # Import and setup database
        sys.path.append(str(Path(__file__).parent / "src"))
        
        from src.models.database import create_tables, init_default_settings
        
        create_tables()
        init_default_settings()
        
        print("✅ Database setup completed")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test core imports
        import cv2
        import numpy as np
        import face_recognition
        import chromadb
        import fastapi
        import streamlit
        
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def run_basic_tests():
    """Run basic functionality tests"""
    print("🔍 Running basic tests...")
    
    try:
        # Test configuration
        from config import settings
        assert settings.app_name == "Face Detection System"
        print("✅ Configuration test passed")
        
        # Test database connection
        from src.models.database import SessionLocal
        db = SessionLocal()
        db.close()
        print("✅ Database connection test passed")
        
        # Test vector database
        from src.services.vector_database import VectorDatabaseService
        vector_db = VectorDatabaseService()
        stats = vector_db.get_collection_stats()
        print("✅ Vector database test passed")
        
        # Test face processing
        from src.services.face_processing import FaceProcessingService
        face_processor = FaceProcessingService()
        print("✅ Face processing test passed")
        
        # Test camera service
        from src.services.camera_service import CameraService
        camera_service = CameraService()
        print("✅ Camera service test passed")
        
        print("🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Face Detection System...")
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Step 3: Test imports
    if not test_imports():
        print("❌ Setup failed at import testing")
        return False
    
    # Step 4: Setup database
    if not setup_database():
        print("❌ Setup failed at database setup")
        return False
    
    # Step 5: Run basic tests
    if not run_basic_tests():
        print("❌ Setup failed at basic tests")
        return False
    
    print("\n🎉 Face Detection System setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python automation_test/test_core_infrastructure.py")
    print("2. Start API: python main.py")
    print("3. Start Frontend: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
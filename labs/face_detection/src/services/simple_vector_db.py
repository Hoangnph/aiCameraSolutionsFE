"""
Simple Vector Database Service
A lightweight vector database implementation using SQLite and numpy for face embeddings.
"""

import sqlite3
import numpy as np
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import pickle
from datetime import datetime
import logging

from ..utils.logger import LoggerMixin

logger = logging.getLogger(__name__)

class SimpleVectorDB(LoggerMixin):
    """Simple vector database for face embeddings using SQLite and numpy"""
    
    def __init__(self, db_path: str = "data/face_vectors.db"):
        """Initialize the vector database"""
        super().__init__()
        self.db_path = db_path
        self.connection = None
        self.initialize_database()
    
    async def initialize(self):
        """Initialize the vector database"""
        try:
            # Database is already initialized in constructor
            logger.info("Vector database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {str(e)}")
            raise
    
    async def cleanup(self):
        """Cleanup the vector database"""
        try:
            self.cleanup()
            logger.info("Vector database cleaned up successfully")
        except Exception as e:
            logger.error(f"Failed to cleanup vector database: {str(e)}")
    
    def initialize_database(self):
        """Initialize the database and create tables"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Connect to database
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            
            # Create tables
            self._create_tables()
            
            self.log_info("Simple vector database initialized successfully")
            
        except Exception as e:
            self.log_error(f"Failed to initialize vector database: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Create embeddings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS face_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                embedding_data BLOB NOT NULL,
                metadata TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster searches
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON face_embeddings(created_at)
        """)
        
        self.connection.commit()
    
    def add_face_embedding(self, embedding: np.ndarray, metadata: Dict[str, Any]) -> str:
        """Add a face embedding to the database"""
        try:
            # Convert embedding to bytes
            embedding_bytes = pickle.dumps(embedding)
            
            # Convert metadata to JSON
            metadata_json = json.dumps(metadata)
            
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO face_embeddings (embedding_data, metadata)
                VALUES (?, ?)
            """, (embedding_bytes, metadata_json))
            
            embedding_id = str(cursor.lastrowid)
            self.connection.commit()
            
            self.log_info(f"Added face embedding with ID: {embedding_id}")
            return embedding_id
            
        except Exception as e:
            self.log_error(f"Failed to add face embedding: {str(e)}")
            raise
    
    def search_similar_faces(
        self, 
        embedding: np.ndarray, 
        threshold: float = 0.6, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar faces using cosine similarity"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM face_embeddings")
            rows = cursor.fetchall()
            
            similarities = []
            
            for row in rows:
                # Load embedding from bytes
                stored_embedding = pickle.loads(row['embedding_data'])
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(embedding, stored_embedding)
                
                if similarity >= threshold:
                    metadata = json.loads(row['metadata'])
                    similarities.append({
                        'id': row['id'],
                        'similarity': float(similarity),
                        'metadata': metadata
                    })
            
            # Sort by similarity (highest first) and limit results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            self.log_error(f"Failed to search similar faces: {str(e)}")
            return []
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            # Normalize vectors
            vec1_norm = vec1 / np.linalg.norm(vec1)
            vec2_norm = vec2 / np.linalg.norm(vec2)
            
            # Calculate cosine similarity
            similarity = np.dot(vec1_norm, vec2_norm)
            return float(similarity)
            
        except Exception as e:
            self.log_error(f"Failed to calculate cosine similarity: {str(e)}")
            return 0.0
    
    def get_face_by_id(self, face_id: str) -> Optional[Dict[str, Any]]:
        """Get face embedding by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM face_embeddings WHERE id = ?", (face_id,))
            row = cursor.fetchone()
            
            if row:
                embedding = pickle.loads(row['embedding_data'])
                metadata = json.loads(row['metadata'])
                
                return {
                    'id': row['id'],
                    'embedding': embedding,
                    'metadata': metadata,
                    'created_at': row['created_at']
                }
            
            return None
            
        except Exception as e:
            self.log_error(f"Failed to get face by ID: {str(e)}")
            return None
    
    def list_all_faces(self) -> List[Dict[str, Any]]:
        """List all face embeddings"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM face_embeddings ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            faces = []
            for row in rows:
                metadata = json.loads(row['metadata'])
                faces.append({
                    'id': row['id'],
                    'metadata': metadata,
                    'created_at': row['created_at']
                })
            
            return faces
            
        except Exception as e:
            self.log_error(f"Failed to list all faces: {str(e)}")
            return []
    
    def delete_face(self, face_id: str) -> bool:
        """Delete a face embedding by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM face_embeddings WHERE id = ?", (face_id,))
            self.connection.commit()
            
            deleted = cursor.rowcount > 0
            if deleted:
                self.log_info(f"Deleted face embedding with ID: {face_id}")
            else:
                self.log_warning(f"Face embedding with ID {face_id} not found")
            
            return deleted
            
        except Exception as e:
            self.log_error(f"Failed to delete face: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM face_embeddings")
            total_count = cursor.fetchone()['total']
            
            return {
                'total_faces': total_count,
                'database_path': self.db_path,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_error(f"Failed to get statistics: {str(e)}")
            return {}
    
    def clear_all_faces(self) -> bool:
        """Clear all face embeddings"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM face_embeddings")
            self.connection.commit()
            
            self.log_info("Cleared all face embeddings")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to clear all faces: {str(e)}")
            return False
    
    def is_healthy(self) -> bool:
        """Check if the database is healthy"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return True
        except Exception as e:
            self.log_error(f"Database health check failed: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup database connection"""
        try:
            if self.connection:
                self.connection.close()
                self.log_info("Database connection closed")
        except Exception as e:
            self.log_error(f"Failed to cleanup database: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup() 
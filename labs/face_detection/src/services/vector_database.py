"""
Simple vector database for face embeddings
"""
import numpy as np
import sqlite3
import json
from typing import List, Dict, Any, Optional
from loguru import logger
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import settings

class VectorDatabaseService:
    """Service for managing face embeddings in ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.chroma_db_path,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self._get_or_create_collection()
        logger.info("Vector database service initialized")
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection("face_embeddings")
            logger.info("Using existing face embeddings collection")
        except Exception:
            collection = self.client.create_collection(
                name="face_embeddings",
                metadata={
                    "description": "Face embeddings for recognition",
                    "embedding_dimension": 128,
                    "distance_metric": "cosine",
                    "model_version": "1.0"
                }
            )
            logger.info("Created new face embeddings collection")
        
        return collection
    
    def add_embedding(
        self, 
        embedding_id: str, 
        embedding: List[float], 
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Add face embedding to vector database
        
        Args:
            embedding_id: Unique identifier for embedding
            embedding: 128-dimensional face embedding vector
            metadata: Additional metadata (person_id, name, etc.)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert embedding to numpy array
            embedding_array = np.array(embedding, dtype=np.float32)
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding_array.tolist()],
                metadatas=[metadata],
                ids=[embedding_id]
            )
            
            logger.info(f"Added embedding {embedding_id} for person {metadata.get('person_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add embedding {embedding_id}: {str(e)}")
            return False
    
    def search_similar_faces(
        self, 
        query_embedding: List[float], 
        n_results: int = 5,
        threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Search for similar faces in database
        
        Args:
            query_embedding: Query face embedding
            n_results: Number of results to return
            threshold: Similarity threshold
        
        Returns:
            List of similar faces with metadata
        """
        try:
            # Convert to numpy array
            query_array = np.array(query_embedding, dtype=np.float32)
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_array.tolist()],
                n_results=n_results,
                include=["metadatas", "distances"]
            )
            
            # Process results
            similar_faces = []
            if results["ids"] and results["ids"][0]:
                for i, embedding_id in enumerate(results["ids"][0]):
                    distance = results["distances"][0][i]
                    metadata = results["metadatas"][0][i]
                    
                    # Calculate similarity score (1 - distance)
                    similarity = 1 - distance
                    
                    if similarity >= threshold:
                        similar_faces.append({
                            "embedding_id": embedding_id,
                            "similarity": similarity,
                            "distance": distance,
                            "metadata": metadata
                        })
            
            logger.info(f"Found {len(similar_faces)} similar faces")
            return similar_faces
            
        except Exception as e:
            logger.error(f"Failed to search similar faces: {str(e)}")
            return []
    
    def get_embeddings_by_person(self, person_id: str) -> List[Dict[str, Any]]:
        """
        Get all embeddings for a specific person
        
        Args:
            person_id: Person identifier
        
        Returns:
            List of embeddings for the person
        """
        try:
            results = self.collection.get(
                where={"person_id": person_id},
                include=["metadatas", "embeddings"]
            )
            
            embeddings = []
            for i, embedding_id in enumerate(results["ids"]):
                embeddings.append({
                    "embedding_id": embedding_id,
                    "embedding": results["embeddings"][i],
                    "metadata": results["metadatas"][i]
                })
            
            logger.info(f"Retrieved {len(embeddings)} embeddings for person {person_id}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to get embeddings for person {person_id}: {str(e)}")
            return []
    
    def delete_embedding(self, embedding_id: str) -> bool:
        """
        Delete embedding from database
        
        Args:
            embedding_id: Embedding identifier
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[embedding_id])
            logger.info(f"Deleted embedding {embedding_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete embedding {embedding_id}: {str(e)}")
            return False
    
    def delete_person_embeddings(self, person_id: str) -> bool:
        """
        Delete all embeddings for a person
        
        Args:
            person_id: Person identifier
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.collection.delete(where={"person_id": person_id})
            logger.info(f"Deleted all embeddings for person {person_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete embeddings for person {person_id}: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            
            # Get unique persons
            results = self.collection.get(include=["metadatas"])
            unique_persons = set()
            for metadata in results["metadatas"]:
                if "person_id" in metadata:
                    unique_persons.add(metadata["person_id"])
            
            stats = {
                "total_embeddings": count,
                "unique_persons": len(unique_persons),
                "collection_name": self.collection.name,
                "embedding_dimension": 128
            }
            
            logger.info(f"Collection stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}
    
    def update_embedding_metadata(
        self, 
        embedding_id: str, 
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Update metadata for an embedding
        
        Args:
            embedding_id: Embedding identifier
            metadata: New metadata
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # ChromaDB doesn't support direct metadata updates
            # We need to delete and re-add
            results = self.collection.get(
                ids=[embedding_id],
                include=["embeddings"]
            )
            
            if results["ids"]:
                # Delete old embedding
                self.collection.delete(ids=[embedding_id])
                
                # Add with new metadata
                self.collection.add(
                    embeddings=results["embeddings"],
                    metadatas=[metadata],
                    ids=[embedding_id]
                )
                
                logger.info(f"Updated metadata for embedding {embedding_id}")
                return True
            else:
                logger.warning(f"Embedding {embedding_id} not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update metadata for embedding {embedding_id}: {str(e)}")
            return False
    
    def get_all_embeddings(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Get all embeddings in collection
        
        Args:
            limit: Maximum number of embeddings to return
        
        Returns:
            List of all embeddings
        """
        try:
            results = self.collection.get(
                limit=limit,
                include=["metadatas", "embeddings"]
            )
            
            embeddings = []
            for i, embedding_id in enumerate(results["ids"]):
                embeddings.append({
                    "embedding_id": embedding_id,
                    "embedding": results["embeddings"][i],
                    "metadata": results["metadatas"][i]
                })
            
            logger.info(f"Retrieved {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to get all embeddings: {str(e)}")
            return []
    
    def backup_collection(self, backup_path: str) -> bool:
        """
        Backup collection to file
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get all embeddings
            embeddings = self.get_all_embeddings()
            
            # Save to file
            with open(backup_path, 'w') as f:
                json.dump(embeddings, f, indent=2)
            
            logger.info(f"Backed up collection to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to backup collection: {str(e)}")
            return False
    
    def restore_collection(self, backup_path: str) -> bool:
        """
        Restore collection from backup
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load backup
            with open(backup_path, 'r') as f:
                embeddings = json.load(f)
            
            # Clear existing collection
            self.collection.delete(where={})
            
            # Add embeddings from backup
            for embedding_data in embeddings:
                self.collection.add(
                    embeddings=[embedding_data["embedding"]],
                    metadatas=[embedding_data["metadata"]],
                    ids=[embedding_data["embedding_id"]]
                )
            
            logger.info(f"Restored collection from {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore collection: {str(e)}")
            return False

# Global instance
vector_db = VectorDatabaseService() 
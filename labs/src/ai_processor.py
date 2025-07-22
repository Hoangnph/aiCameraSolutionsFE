"""
AI Model Processor for People Counting
-------------------------------------
Module test AI model với video stream, mô phỏng detection/tracking.

Usage Example:
--------------
python ai_processor.py --stream <video_url_or_path>
"""
#!/usr/bin/env python3
"""
AI Model Processor for People Counting
Test AI model with video stream
"""

import cv2
import numpy as np
import time
import logging
import argparse
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class DetectionResult:
    """Result of people detection and counting"""
    people_count: int
    confidence: float
    processing_time: float
    frame_number: int
    timestamp: datetime
    bounding_boxes: List[Tuple[int, int, int, int]]

class CentroidTracker:
    """Simple centroid tracker for people counting"""
    
    def __init__(self, max_disappeared: int = 40, max_distance: int = 50):
        """
        Initialize the CentroidTracker.

        Args:
            max_disappeared (int): Maximum number of consecutive frames a trackable object can be marked as disappeared.
            max_distance (int): Maximum distance in pixels for a match to be considered valid.
        """
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    def register(self, centroid):
        """
        Register a new object.

        Args:
            centroid (Tuple[int, int]): The centroid (x, y) of the new object.
        """
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        """
        Deregister an object.

        Args:
            object_id (int): The ID of the object to deregister.
        """
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        """
        Update tracked objects.

        Args:
            rects (List[Tuple[int, int, int, int]]): List of bounding boxes (x, y, w, h) for the current frame.

        Returns:
            Dict[int, Tuple[int, int]]: Updated dictionary of object IDs and their centroids.
        """
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        input_centroids = np.array([self._get_centroid(rect) for rect in rects])
        
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            D = self._calculate_distances(object_centroids, input_centroids)
            
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                if D[row, col] > self.max_distance:
                    continue
                
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            
            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])
        
        return self.objects

    def _get_centroid(self, rect):
        """
        Calculate the centroid (x, y) from a bounding box (x, y, w, h).

        Args:
            rect (Tuple[int, int, int, int]): A tuple containing (x, y, w, h) of a bounding box.

        Returns:
            Tuple[int, int]: The centroid (x, y) of the bounding box.
        """
        if len(rect) == 4:
            x, y, w, h = rect
            return (x + w // 2, y + h // 2)
        else:
            return rect

    def _calculate_distances(self, centroids1, centroids2):
        """
        Calculate pairwise distances between two sets of centroids.

        Args:
            centroids1 (np.ndarray): Array of centroids (N, 2).
            centroids2 (np.ndarray): Array of centroids (M, 2).

        Returns:
            np.ndarray: Distance matrix (N, M) where each element is the Euclidean distance.
        """
        return np.linalg.norm(centroids1[:, None] - centroids2, axis=2)

class AIProcessor:
    """AI Model Processor for people counting"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the AIProcessor.

        Args:
            model_path (str): Path to the AI model file (optional for testing).
        """
        self.model_loaded = False
        self.net = None
        self.classes = [
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"
        ]
        self.confidence_threshold = 0.4
        self.skip_frames = 30
        self.tracker = CentroidTracker()
        self.total_frames = 0
        self.lock = threading.Lock()
        
        # Try to load model if path provided
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """
        Load the AI model (simplified version without actual model files).

        Args:
            model_path (str): Path to the AI model file.

        Returns:
            bool: True if model loaded successfully, False otherwise.
        """
        try:
            # For testing purposes, we'll simulate model loading
            logger.info("Loading AI model (simulated)")
            self.model_loaded = True
            logger.info("AI model loaded successfully (simulated)")
            return True
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            return False

    def process_frame(self, frame: np.ndarray) -> DetectionResult:
        """
        Process a single frame for people detection.

        Args:
            frame (np.ndarray): The input frame (BGR format).

        Returns:
            DetectionResult: A dataclass containing detection results.
        """
        if not self.model_loaded:
            # Simulate detection for testing
            return self._simulate_detection(frame)
        
        start_time = time.time()
        
        # Resize frame for processing
        frame = cv2.resize(frame, (500, int(500 * frame.shape[0] / frame.shape[1])))
        H, W = frame.shape[:2]
        
        # Simulate detection (replace with actual model inference)
        people_count = self._simulate_people_detection(frame)
        
        processing_time = time.time() - start_time
        
        with self.lock:
            self.total_frames += 1
        
        return DetectionResult(
            people_count=people_count,
            confidence=0.8,  # Simulated confidence
            processing_time=processing_time,
            frame_number=self.total_frames,
            timestamp=datetime.now(),
            bounding_boxes=[]  # Simulated bounding boxes
        )

    def _simulate_detection(self, frame: np.ndarray) -> DetectionResult:
        """
        Simulate people detection for testing.

        Args:
            frame (np.ndarray): The input frame (BGR format).

        Returns:
            DetectionResult: A dataclass containing detection results.
        """
        start_time = time.time()
        
        # Simple simulation based on frame brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        # Simulate people count based on brightness
        if brightness > 100:
            people_count = np.random.randint(1, 5)
        else:
            people_count = np.random.randint(0, 2)
        
        processing_time = time.time() - start_time
        
        with self.lock:
            self.total_frames += 1
        
        return DetectionResult(
            people_count=people_count,
            confidence=0.7 + np.random.random() * 0.2,
            processing_time=processing_time,
            frame_number=self.total_frames,
            timestamp=datetime.now(),
            bounding_boxes=[]
        )

    def _simulate_people_detection(self, frame: np.ndarray) -> int:
        """
        Simulate people detection logic.

        Args:
            frame (np.ndarray): The input frame (BGR format).

        Returns:
            int: The simulated number of people detected.
        """
        # Simple simulation - replace with actual model inference
        return np.random.randint(0, 5)

    def process_video_stream(self, stream_url: str, max_frames: int = 100) -> List[DetectionResult]:
        """
        Process video stream for people counting.

        Args:
            stream_url (str): The URL or path of the video stream.
            max_frames (int): Maximum number of frames to process.

        Returns:
            List[DetectionResult]: A list of DetectionResult dataclasses.
        """
        results = []
        
        try:
            cap = cv2.VideoCapture(stream_url)
            if not cap.isOpened():
                logger.error(f"Failed to open video stream: {stream_url}")
                return results
            
            frame_count = 0
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Failed to read frame from stream")
                    break
                
                try:
                    result = self.process_frame(frame)
                    results.append(result)
                    frame_count += 1
                    
                    # Log progress
                    if frame_count % 10 == 0:
                        logger.info(f"Processed {frame_count} frames, people count: {result.people_count}")
                
                except Exception as e:
                    logger.error(f"Error processing frame {frame_count}: {e}")
                    continue
            
            cap.release()
            logger.info(f"Completed processing {len(results)} frames")
        
        except Exception as e:
            logger.error(f"Error processing video stream: {e}")
        
        return results

def main():
    """
    Main function for command line usage.

    Returns:
        int: 0 for success, 1 for failure.
    """
    parser = argparse.ArgumentParser(description='AI Model Processor for People Counting')
    parser.add_argument('--stream', required=True, help='Video stream URL or file path')
    parser.add_argument('--model', help='AI model path (optional for testing)')
    parser.add_argument('--max-frames', type=int, default=100, help='Maximum frames to process')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create AI processor
    processor = AIProcessor(args.model)
    
    # Process stream
    print(f"Processing stream: {args.stream}")
    results = processor.process_video_stream(args.stream, args.max_frames)
    
    # Print results
    print(f"\n📊 Processing Results:")
    print(f"Frames Processed: {len(results)}")
    
    if results:
        avg_people = sum(r.people_count for r in results) / len(results)
        avg_confidence = sum(r.confidence for r in results) / len(results)
        avg_time = sum(r.processing_time for r in results) / len(results)
        
        print(f"Average People Count: {avg_people:.1f}")
        print(f"Average Confidence: {avg_confidence:.2f}")
        print(f"Average Processing Time: {avg_time:.3f}s")
        
        # Show last few results
        print(f"\nLast 5 Results:")
        for result in results[-5:]:
            print(f"  Frame {result.frame_number}: {result.people_count} people, "
                  f"confidence {result.confidence:.2f}, time {result.processing_time:.3f}s")
    
    return 0 if results else 1

if __name__ == "__main__":
    sys.exit(main()) 
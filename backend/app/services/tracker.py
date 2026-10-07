"""Vehicle tracker using ByteTrack from supervision."""

from typing import List, Dict, Optional, Tuple
import numpy as np
from supervision import ByteTrack


class VehicleTracker:
    """ByteTrack-based vehicle tracker for stable ID assignment."""
    
    def __init__(self, track_thresh: float = 0.5, track_buffer: int = 30, match_thresh: float = 0.8):
        """Initialize tracker.
        
        Args:
            track_thresh: Confidence threshold for tracking
            track_buffer: Number of frames to keep track alive without detection
            match_thresh: Matching threshold for associate detection
        """
        self.tracker = ByteTrack(
            track_thresh=track_thresh,
            track_buffer=track_buffer,
            match_thresh=match_thresh,
        )
    
    def update(self, boxes: List[List[float]], class_ids: List[int], class_names: List[str]) -> List[Dict]:
        """Update tracker with detections.
        
        Args:
            boxes: List of [x1, y1, x2, y2] bounding boxes
            class_ids: List of class IDs
            class_names: List of class names
        
        Returns:
            List of tracked vehicles with IDs and info
        """
        if not boxes:
            return []
        
        # Convert to numpy array for ByteTrack
        boxes_np = np.array(boxes)
        
        # Update tracker - passes boxes in xyxy format
        tracks = self.tracker.update(boxes_np)
        
        # Build result list
        vehicles = []
        for track in tracks:
            track_id = int(track[4])
            
            # Get bbox coordinates
            x1, y1, x2, y2 = float(track[0]), float(track[1]), float(track[2]), float(track[3])
            bbox = [x1, y1, x2, y2]
            
            # Find class info - use the most recent detection's class
            class_name = class_names[0] if class_names else "car"
            class_id = class_ids[0] if class_ids else 0
            
            vehicles.append({
                "id": track_id,
                "bbox": bbox,
                "class_name": class_name,
                "class_id": class_id,
            })
        
        return vehicles
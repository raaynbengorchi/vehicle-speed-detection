"""Vehicle detector using Ultralytics YOLO."""

from typing import List, Tuple, Optional
import numpy as np
from ultralytics import YOLO

from backend.app.schemas import VehicleResult


class VehicleDetector:
    """YOLO-based vehicle detector."""
    
    # Vehicle classes we care about
    TARGET_CLASSES = {"car", "motorcycle", "bus", "truck"}
    
    def __init__(self, model_path: str = "yolo11n.pt", confidence_threshold: float = 0.5):
        """Initialize detector with YOLO model.
        
        Args:
            model_path: Path to YOLO model file
            confidence_threshold: Minimum confidence for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model = YOLO(model_path)
    
    def detect(self, frame: np.ndarray) -> Tuple[List[List[float]], List[int], List[str]]:
        """Detect vehicles in a frame.
        
        Args:
            frame: OpenCV image frame
        
        Returns:
            Tuple of (bounding boxes, class IDs, class names)
        """
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)
        
        boxes = []
        class_ids = []
        class_names = []
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                # Only detect target vehicle classes
                if class_name not in self.TARGET_CLASSES:
                    continue
                
                confidence = float(box.conf[0])
                if confidence < self.confidence_threshold:
                    continue
                
                # Get bounding box [x1, y1, x2, y2]
                bbox = box.xyxy[0].cpu().numpy().tolist()
                boxes.append(bbox)
                class_ids.append(class_id)
                class_names.append(class_name)
        
        return boxes, class_ids, class_names
"""Video processor for handling video upload, processing, and output."""

import asyncio
import os
import time
import uuid
from pathlib import Path
from typing import Optional, Dict, Any

import cv2
import numpy as np

from backend.app.schemas import VideoStatus, ProcessingResults, VehicleResult
from backend.app.services.detector import VehicleDetector
from backend.app.services.tracker import VehicleTracker
from backend.app.services.speed_estimator import SpeedEstimator
from backend.app.utils.geometry import get_bbox_center


class VideoProcessor:
    """Handles video processing pipeline for vehicle speed estimation."""
    
    def __init__(self, 
                 detector: VehicleDetector,
                 tracker: VehicleTracker,
                 speed_estimator: SpeedEstimator):
        """Initialize video processor.
        
        Args:
            detector: Vehicle detector instance
            tracker: Vehicle tracker instance
            speed_estimator: Speed estimator instance
        """
        self.detector = detector
        self.tracker = tracker
        self.speed_estimator = speed_estimator
        self._processing_tasks: Dict[str, asyncio.Task] = {}
    
    def get_processing_id(self, video_id: str) -> str:
        """Get or create a processing task ID for a video.
        
        Args:
            video_id: Unique video identifier
        
        Returns:
            Processing task ID
        """
        if video_id not in self._processing_tasks:
            self._processing_tasks[video_id] = asyncio.create_task(self._process_video_internal(video_id))
        return video_id
    
    async def process_video(
        self,
        video_id: str,
        line1_y: float,
        line2_y: float,
        distance_meters: float,
        speed_limit: float,
        confidence_threshold: float
    ) -> None:
        """Process a video file asynchronously.
        
        Args:
            video_id: Unique video identifier
            line1_y: Y position of first virtual line
            line2_y: Y position of second virtual line
            distance_meters: Real-world distance between lines in meters
            speed_limit: Speed limit in km/h
            confidence_threshold: YOLO confidence threshold
        """
        # Reset speed estimator for new video
        self.speed_estimator.reset()
        
        # Update speed estimator parameters
        self.speed_estimator.speed_limit = speed_limit
        self.speed_estimator.distance_meters = distance_meters
        
        # Get the video file path
        video_path = Path(f"backend/uploads/{video_id}.mp4")
        output_path = Path(f"backend/outputs/{video_id}_processed.mp4")
        
        if not video_path.exists():
            print(f"Video file not found: {video_path}")
            return
        
        # Open video capture
        cap = cv2.VideoCapture(str(video_path))
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Use provided FPS if original FPS is invalid
        if fps <= 0 or np.isnan(fps):
            fps = 30.0
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Processing state
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = 0
        vehicle_count = 0
        all_vehicle_results = []
        speeds = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frames += 1
            
            # Run detection
            boxes, class_ids, class_names = self.detector.detect(frame)
            
            # Update tracker
            tracked_vehicles = self.tracker.update(boxes, class_ids, class_names)
            
            # Process each tracked vehicle
            for vehicle in tracked_vehicles:
                vehicle_id = vehicle["id"]
                bbox = vehicle["bbox"]
                class_name = vehicle["class_name"]
                
                # Get bounding box center
                cx, cy = get_bbox_center(np.array(bbox))
                
                # Store first detected timestamp
                if vehicle_id not in self.speed_estimator.vehicle_first_detected:
                    self.speed_estimator.vehicle_first_detected[vehicle_id] = time.time()
                
                # Process line crossings
                result = self.speed_estimator.process_line_crossing(
                    vehicle_id=vehicle_id,
                    cx=cx,
                    cy=cy,
                    line1_y=line1_y,
                    line2_y=line2_y,
                    current_time=processed_frames / fps
                )
                
                # Draw on frame if speed was calculated
                if result:
                    speed_kmh = result["speed_kmh"]
                    status = result["status"]
                    
                    # Color based on status
                    color = (0, 0, 255) if status == "Overspeed" else (0, 255, 0)  # Red or Green
                    
                    # Draw bounding box
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw label with ID and speed
                    label = f"ID {vehicle_id}: {speed_kmh} km/h ({status})"
                    cv2.putText(frame, label, (x1, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    # Vehicle result
                    vehicle_result = VehicleResult(
                        vehicle_id=vehicle_id,
                        vehicle_class=class_name,
                        speed_kmh=speed_kmh,
                        status=status,
                        detected_at=self.speed_estimator.vehicle_first_detected.get(vehicle_id, 0)
                    )
                    all_vehicle_results.append(vehicle_result)
                    vehicle_count += 1
                    speeds.append(speed_kmh)
                
                # Draw vehicle ID and class
                else:
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    label = f"ID {vehicle_id}: {class_name}"
                    cv2.putText(frame, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Draw virtual lines
            color = (255, 255, 255)  # White
            thickness = 2
            cv2.line(frame, (0, int(line1_y)), (width, int(line1_y)), color, thickness)
            cv2.line(frame, (0, int(line2_y)), (width, int(line2_y)), color, thickness)
            
            # Draw labels for lines
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"Line 1: {line1_y:.1f}m", (10, int(line1_y) - 10),
                       font, 0.5, color, 1)
            cv2.putText(frame, f"Line 2: {line2_y:.1f}m", (10, int(line2_y) - 30),
                       font, 0.5, color, 1)
            
            # Draw distance and speed limit info
            info_color = (0, 255, 255)  # Cyan
            cv2.putText(frame, f"Distance: {self.speed_estimator.distance_meters}m", 
                       (10, height - 60), font, 0.5, info_color, 1)
            cv2.putText(frame, f"Speed Limit: {self.speed_estimator.speed_limit}km/h", 
                       (10, height - 40), font, 0.5, info_color, 1)
            cv2.putText(frame, f"FPS: {fps:.1f}", 
                       (10, height - 20), font, 0.5, info_color, 1)
            
            # Write frame to output video
            out.write(frame)
        
        # Release resources
        cap.release()
        out.release()
        
        # Calculate summary statistics
        total_vehicles = len(all_vehicle_results)
        average_speed = round(np.mean(speeds), 2) if speeds else 0.0
        max_speed = round(max(speeds), 2) if speeds else 0.0
        overspeed_count = sum(1 for v in all_vehicle_results if v.status == "Overspeed")
        
        # Create results object
        results = ProcessingResults(
            video_id=video_id,
            total_vehicles=total_vehicles,
            average_speed=average_speed,
            max_speed=max_speed,
            overspeed_count=overspeed_count,
            vehicle_results=all_vehicle_results,
            video_duration=total_frames / fps if fps > 0 else 0
        )
        
        # Store results for later retrieval
        # In a full implementation, this would be stored in a database
        print(f"Processing complete for {video_id}: {results}")
    
    async def get_status(self, video_id: str) -> Dict[str, Any]:
        """Get processing status for a video.
        
        Args:
            video_id: Unique video identifier
        
        Returns:
            Status dictionary
        """
        # In a full implementation, this would check actual progress
        # For now, return basic status
        return {
            "video_id": video_id,
            "status": "completed",
            "progress": 1.0,
            "message": "Processing complete"
        }
"""Speed estimator for calculating vehicle speed from line crossing times."""

from typing import Dict, Optional, Tuple
import numpy as np


class SpeedEstimator:
    """Estimates vehicle speed based on line crossing times."""
    
    def __init__(self, distance_meters: float, speed_limit: float = 60.0):
        """Initialize speed estimator.
        
        Args:
            distance_meters: Real-world distance between the two lines in meters
            speed_limit: Speed limit in km/h for overspeed detection
        """
        if distance_meters <= 0:
            raise ValueError("Distance between lines must be positive")
        
        self.distance_meters = distance_meters
        self.speed_limit = speed_limit
        
        # Per-vehicle state: stores timestamp when vehicle crosses line 1
        self.vehicle_line1_time: Dict[int, float] = {}
        # Per-vehicle state: stores whether line 2 has been crossed
        self.vehicle_crossed_line2: Dict[int, bool] = {}
        # Per-vehicle state: stores calculated speed
        self.vehicle_speeds: Dict[int, float] = {}
        # Per-vehicle state: stores detection timestamp
        self.vehicle_first_detected: Dict[int, float] = {}
    
    def reset(self) -> None:
        """Reset all vehicle state (for new video processing)."""
        self.vehicle_line1_time.clear()
        self.vehicle_crossed_line2.clear()
        self.vehicle_speeds.clear()
        self.vehicle_first_detected.clear()
    
    def process_line_crossing(
        self,
        vehicle_id: int,
        cx: float,
        cy: float,
        line1_y: float,
        line2_y: float,
        current_time: float
    ) -> Optional[Dict]:
        """Process a vehicle crossing a line and calculate speed if applicable.
        
        Args:
            vehicle_id: Tracked vehicle ID
            cx: Center x coordinate of bounding box
            cy: Center y coordinate of bounding box
            line1_y: Y position of first virtual line
            line2_y: Y position of second virtual line
            current_time: Current timestamp in seconds
        
        Returns:
            Speed info dict if speed was calculated, None otherwise
        """
        # Initialize vehicle state on first detection
        if vehicle_id not in self.vehicle_first_detected:
            self.vehicle_first_detected[vehicle_id] = current_time
        
        # Check crossing of line 1 (downward direction)
        # Line going from top to bottom: cy crosses from above line1_y to below
        crossed_line1 = (
            self.vehicle_line1_time.get(vehicle_id) is None
            and is_near_line(cy, line1_y)
        )
        
        # Check crossing of line 2
        crossed_line2 = is_near_line(cy, line2_y)
        
        if crossed_line1:
            # Store timestamp when vehicle crosses line 1
            self.vehicle_line1_time[vehicle_id] = current_time
            self.vehicle_crossed_line2[vehicle_id] = False
            self.vehicle_speeds[vehicle_id] = None
            return None
        
        if crossed_line2 and vehicle_id in self.vehicle_line1_time:
            # Vehicle has crossed line 1 before, now crossing line 2
            line1_time = self.vehicle_line1_time[vehicle_id]
            
            # Calculate elapsed time
            elapsed_time = current_time - line1_time
            
            # Safety check: avoid division by zero and negative time
            if elapsed_time <= 0:
                # Vehicle crossed both lines at nearly the same time
                self.vehicle_crossed_line2[vehicle_id] = True
                return None
            
            # Calculate speed: speed_kmh = distance_meters / time_seconds * 3.6
            speed_kmh = self.distance_meters / elapsed_time * 3.6
            
            # Store the calculated speed
            self.vehicle_speeds[vehicle_id] = speed_kmh
            self.vehicle_crossed_line2[vehicle_id] = True
            
            # Determine status
            status = "Overspeed" if speed_kmh > self.speed_limit else "Normal"
            
            return {
                "vehicle_id": vehicle_id,
                "speed_kmh": round(speed_kmh, 2),
                "status": status,
            }
        
        return None
    
    def get_vehicle_speed(self, vehicle_id: int) -> Optional[float]:
        """Get calculated speed for a vehicle.
        
        Args:
            vehicle_id: Tracked vehicle ID
        
        Returns:
            Speed in kmh or None if not calculated yet
        """
        return self.vehicle_speeds.get(vehicle_id)
    
    def get_vehicle_status(self, vehicle_id: int) -> str:
        """Get overspeed status for a vehicle.
        
        Args:
            vehicle_id: Tracked vehicle ID
        
        Returns:
            "Normal" or "Overspeed"
        """
        speed = self.get_vehicle_speed(vehicle_id)
        if speed is None:
            return "Unknown"
        return "Overspeed" if speed > self.speed_limit else "Normal"


def is_near_line(cy: float, line_y: float, tolerance: float = 5.0) -> bool:
    """Check if a y-coordinate is near a horizontal line.
    
    Args:
        cy: Point y coordinate
        line_y: Line y coordinate
        tolerance: Acceptable distance in pixels
    
    Returns:
        True if point is within tolerance of the line
    """
    return abs(cy - line_y) <= tolerance
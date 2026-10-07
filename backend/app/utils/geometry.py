"""Geometry utilities for line crossing detection."""

import numpy as np


def point_line_distance(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate perpendicular distance from point to line segment.
    
    Args:
        px, py: Point coordinates
        x1, y1: Line start coordinates
        x2, y2: Line end coordinates
    
    Returns:
        Perpendicular distance from point to line
    """
    # Line vector
    dx = x2 - x1
    dy = y2 - y1
    
    # Point vector
    px_dx = px - x1
    py_dy = py - y1
    
    # Project point onto line
    if dx == 0 and dy == 0:
        # Line is a point
        return np.sqrt(px_dx**2 + py_dy**2)
    
    # t = dot product / length squared
    t = (px_dx * dx + py_dy * dy) / (dx**2 + dy**2)
    
    # Clamp t to [0, 1] to stay on segment
    t = max(0.0, min(1.0, t))
    
    # Closest point on segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    
    # Distance
    return np.sqrt((px - closest_x)**2 + (py - closest_y)**2)


def line_intersection_point(line1_start, line1_end, line2_start, line2_end):
    """Find intersection point of two lines.
    
    Returns None if lines are parallel or don't intersect.
    """
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if denom == 0:
        return None  # Parallel lines
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    # Intersection exists within both segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    
    return None


def is_point_on_horizontal_line(px: float, py: float, y_target: float, tolerance: float = 5.0) -> bool:
    """Check if a point is near a horizontal line at y_target.
    
    Args:
        px: Point x coordinate
        py: Point y coordinate
        y_target: Y coordinate of the horizontal line
        tolerance: Acceptable distance from the line in pixels
    
    Returns:
        True if point is within tolerance of the line
    """
    return abs(py - y_target) <= tolerance


def get_bbox_center(bbox: np.ndarray) -> tuple[float, float]:
    """Get the center point of a bounding box.
    
    Args:
        bbox: [x1, y1, x2, y2] format
    
    Returns:
        (cx, cy) center coordinates
    """
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return (cx, cy)
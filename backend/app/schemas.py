"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field, validator


# Video upload schema
class VideoUploadRequest(BaseModel):
    """Request to upload a video file."""
    pass


class VideoUploadResponse(BaseModel):
    """Response after video upload."""
    video_id: str = Field(description="Unique identifier for the uploaded video")
    filename: str = Field(description="Original filename")


# Video processing request
class VideoProcessRequest(BaseModel):
    """Request to start video processing."""
    line_1_y: float = Field(default=200.0, ge=0, description="Y position of first virtual line")
    line_2_y: float = Field(default=400.0, ge=0, description="Y position of second virtual line")
    distance_meters: float = Field(default=100.0, ge=0, description="Real-world distance between lines in meters")
    speed_limit: float = Field(default=60.0, ge=0, description="Speed limit in km/h")
    confidence_threshold: float = Field(default=0.5, ge=0, le=1, description="YOLO confidence threshold")


class VideoProcessRequestLine1Only(BaseModel):
    """Request with only line_1_y."""
    line_1_y: float = Field(default=200.0, ge=0, description="Y position of first virtual line")


# Video status schema
class VideoStatus(BaseModel):
    """Status of video processing."""
    video_id: str
    status: str = Field(description="Current processing status (processing, completed, error, completed)")
    progress: float = Field(default=0.0, ge=0, le=1, description="Processing progress 0-1")
    message: str = Field(default="", description="Optional status message")


# Processing result schemas
class VehicleResult(BaseModel):
    """Result for a single vehicle."""
    vehicle_id: int = Field(description="Tracking ID from ByteTrack")
    vehicle_class: str = Field(description="Vehicle class (car, motorcycle, bus, truck)")
    speed_kmh: float = Field(description="Estimated speed in km/h")
    status: str = Field(description="Normal or Overspeed")
    detected_at: float = Field(description="Timestamp when vehicle was first detected")


class ProcessingResults(BaseModel):
    """Complete processing results."""
    video_id: str
    total_vehicles: int = Field(default=0, description="Total number of vehicles detected")
    average_speed: float = Field(default=0.0, description="Average speed of all detected vehicles")
    max_speed: float = Field(default=0.0, description="Maximum speed recorded")
    overspeed_count: int = Field(default=0, description="Number of vehicles exceeding speed limit")
    vehicle_results: list[VehicleResult] = Field(default_factory=list, description="List of vehicle results")
    video_duration: float = Field(default=0.0, description="Processed video duration in seconds")


# API response schemas
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="API status")
    message: str = Field(default="API is running")


class VideoOutputResponse(BaseModel):
    """Response for video output endpoint."""
    video_id: str
    filename: str
    download_url: str
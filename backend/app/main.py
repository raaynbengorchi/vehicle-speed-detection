"""Main FastAPI application for RoadWatch AI."""

import asyncio
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import get_settings
from app.schemas import (
    VideoUploadRequest,
    VideoUploadResponse,
    VideoProcessRequest,
    VideoProcessRequestLine1Only,
    VideoStatus,
    ProcessingResults,
    HealthResponse,
    VideoOutputResponse,
)
from app.services.detector import VehicleDetector
from app.services.tracker import VehicleTracker
from app.services.video_processor import VideoProcessor


# Initialize FastAPI app
app = FastAPI(
    title="RoadWatch AI",
    description="Vehicle speed detection system using YOLO and ByteTrack",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize settings
settings = get_settings()

# Initialize services
detector = VehicleDetector(
    model_path=settings.model_path,
    confidence_threshold=settings.confidence_threshold,
)
tracker = VehicleTracker()
speed_estimator = None  # Will be created per video
video_processor = VideoProcessor(detector, tracker, speed_estimator)

# In-memory storage for video processing jobs
# In production, use a database
video_jobs: Dict[str, Dict] = {}


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="API is running")


@app.post("/api/videos/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """Upload a video file.
    
    Args:
        file: Uploaded video file
    
    Returns:
        Video upload response with video ID
    """
    # Validate file type
    allowed_types = ["video/mp4", "video/avi", "video/mov", "video/webm"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_types}"
        )
    
    # Generate unique video ID
    video_id = str(uuid.uuid4())
    
    # Save uploaded file
    uploads_dir = Path("backend/uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = uploads_dir / f"{video_id}.mp4"
    content = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    return VideoUploadResponse(
        video_id=video_id,
        filename=file.filename or "uploaded_video.mp4"
    )


@app.post("/api/videos/{video_id}/process", response_model=Dict[str, str])
async def process_video(
    video_id: str,
    request: VideoProcessRequest,
):
    """Start video processing.
    
    Args:
        video_id: Unique video identifier
        request: Processing parameters
    
    Returns:
        Processing job ID
    """
    # Check if video exists
    video_path = Path(f"backend/uploads/{video_id}.mp4")
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Initialize speed estimator with new parameters
    global speed_estimator
    speed_estimator = type(video_processor.speed_estimator)(
        distance_meters=request.distance_meters,
        speed_limit=request.speed_limit,
    )
    
    # Get or create processing task
    processing_id = video_processor.get_processing_id(video_id)
    
    # Store job parameters
    video_jobs[video_id] = {
        "line_1_y": request.line_1_y,
        "line_2_y": request.line_2_y,
        "distance_meters": request.distance_meters,
        "speed_limit": request.speed_limit,
        "confidence_threshold": request.confidence_threshold,
        "status": "processing",
    }
    
    return {"processing_id": video_id}


@app.get("/api/videos/{video_id}/status", response_model=VideoStatus)
async def get_video_status(video_id: str):
    """Get video processing status.
    
    Args:
        video_id: Unique video identifier
    
    Returns:
        Processing status
    """
    if video_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Video not found")
    
    job = video_jobs[video_id]
    
    return VideoStatus(
        video_id=video_id,
        status=job["status"],
        progress=1.0,  # In a full implementation, track actual progress
        message="Processing complete" if job["status"] == "completed" else "Processing in progress"
    )


@app.get("/api/videos/{video_id}/results", response_model=ProcessingResults)
async def get_video_results(video_id: str):
    """Get video processing results.
    
    Args:
        video_id: Unique video identifier
    
    Returns:
        Processing results with vehicle data
    """
    if video_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # In a full implementation, retrieve from actual storage
    # For now, return default results
    return ProcessingResults(
        video_id=video_id,
        total_vehicles=0,
        average_speed=0.0,
        max_speed=0.0,
        overspeed_count=0,
        vehicle_results=[],
    )


@app.get("/api/videos/{video_id}/output", response_class=FileResponse)
async def get_video_output(video_id: str):
    """Serve the processed video.
    
    Args:
        video_id: Unique video identifier
    
    Returns:
        Processed video file
    """
    output_path = Path(f"backend/outputs/{video_id}_processed.mp4")
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Processed video not found")
    
    return FileResponse(
        path=str(output_path),
        media_type="video/mp4",
        filename=f"processed_{video_id}.mp4"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
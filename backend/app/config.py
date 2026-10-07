"""Configuration settings for RoadWatch AI."""
"""Configuration settings for RoadWatch AI."""
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    # Video settings
    video_fps: float = Field(default=30.0, alias="VIDEO_FPS")
    # Speed settings
    speed_limit: float = Field(default=60.0, alias="SPEED_LIMIT")
    # Line settings
    line1_y: float = Field(default=200.0, alias="LINE1_Y")
    line2_y: float = Field(default=400.0, alias="LINE2_Y")
    # Detection settings
    confidence_threshold: float = Field(default=0.5, alias="CONFIDENCE_THRESHOLD")
    # Model settings
    model_path: str = Field(default="yolo11n.pt", alias="MODEL_PATH")


def get_settings() -> Settings:
    """Get settings instance from environment variables."""
    return Settings()
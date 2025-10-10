from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from datetime import datetime
from enum import Enum

class JobStatusEnum(str, Enum):
    """Job processing status"""
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    not_found = "not_found"

class ModelEnum(str, Enum):
    """Available AI enhancement models"""
    test = "test"
    waifu2x = "waifu2x"
    esrgan = "esrgan"

class ScaleEnum(int, Enum):
    """Available upscaling factors"""
    x2 = 2
    x4 = 4

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")

class RootResponse(BaseModel):
    """Root endpoint response"""
    message: str = Field(..., description="Welcome message")
    status: str = Field(..., description="Service status")

class EnhanceVideoResponse(BaseModel):
    """Response for video enhancement upload"""
    message: str = Field(..., description="Status message")
    job_id: str = Field(..., description="Unique job identifier for tracking")
    status: JobStatusEnum = Field(..., description="Current job status")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    model: ModelEnum = Field(..., description="AI model used for enhancement")
    scale: ScaleEnum = Field(..., description="Upscaling factor")

class JobStatusResponse(BaseModel):
    """Job status response"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatusEnum = Field(..., description="Current processing status")
    progress: float = Field(..., ge=0, le=100, description="Processing progress percentage")
    message: str = Field(..., description="Current status message")
    updated_at: Optional[str] = Field(None, description="Last update timestamp (ISO format)")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time (ISO format)")

class ModelInfo(BaseModel):
    """AI model information"""
    name: str = Field(..., description="Model display name")
    description: str = Field(..., description="Model description")
    scales: List[int] = Field(..., description="Supported upscaling factors")
    optimal_for: str = Field(..., description="Content type this model is optimized for")

class AvailableModelsResponse(BaseModel):
    """Available models response"""
    models: Dict[str, ModelInfo] = Field(..., description="Available AI enhancement models")
    default_model: str = Field(..., description="Default model name")
    default_scale: int = Field(..., description="Default upscaling factor")

class JobCancelResponse(BaseModel):
    """Job cancellation response"""
    message: str = Field(..., description="Cancellation confirmation message")

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: Union[str, Dict] = Field(..., description="Error details")

class VideoInfo(BaseModel):
    """Video file information"""
    duration: float = Field(..., description="Video duration in seconds")
    fps: float = Field(..., description="Frames per second")
    width: int = Field(..., description="Video width in pixels")
    height: int = Field(..., description="Video height in pixels")
    codec: str = Field(..., description="Video codec")
    bitrate: Optional[int] = Field(None, description="Video bitrate")

# Form data models for file uploads
class EnhanceVideoRequest(BaseModel):
    """Video enhancement request parameters"""
    model: ModelEnum = Field(ModelEnum.waifu2x, description="AI model to use for enhancement")
    scale: ScaleEnum = Field(ScaleEnum.x2, description="Upscaling factor")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "waifu2x",
                "scale": 2
            }
        }
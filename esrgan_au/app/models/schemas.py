from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class JobStatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    not_found = "not_found"

class ScaleEnum(int, Enum):
    x4 = 4

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")

class RootResponse(BaseModel):
    message: str = Field(..., description="Welcome message")
    status: str = Field(..., description="Service status")

class EnhanceVideoResponse(BaseModel):
    message: str = Field(..., description="Status message")
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatusEnum = Field(..., description="Current job status")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    scale: ScaleEnum = Field(..., description="Upscaling factor")

class JobStatusResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatusEnum = Field(..., description="Current processing status")
    progress: float = Field(..., ge=0, le=100, description="Processing progress percentage")
    message: str = Field(..., description="Current status message")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")

class JobCancelResponse(BaseModel):
    message: str = Field(..., description="Cancellation confirmation message")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error details")

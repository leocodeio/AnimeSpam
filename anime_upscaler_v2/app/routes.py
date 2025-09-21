from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse, FileResponse
import os
import uuid
import shutil
from pathlib import Path
import mimetypes
import logging
import json
import threading

logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

from .services.audio import AudioService
from .services.frames import FrameService
from .services.clarity import ClarityService
from .services.merge import MergeService
from .models.schemas import (
    JobStatusEnum, ModelEnum, ScaleEnum,
    EnhanceVideoResponse, JobStatusResponse, AvailableModelsResponse,
    JobCancelResponse, ErrorResponse, HealthResponse, RootResponse, ModelInfo
)

logger = logging.getLogger(__name__)

router = APIRouter()

TEMP_DIR = Path("temp")
UPLOAD_DIR = TEMP_DIR / "uploads"
PROCESSING_DIR = TEMP_DIR / "processing"
OUTPUT_DIR = TEMP_DIR / "output"

# Global job status tracking
JOB_STATUS = {}
JOB_LOCK = threading.Lock()

def update_job_status(job_id: str, status: str, progress: float = 0, message: str = ""):
    """Update job status in thread-safe manner"""
    with JOB_LOCK:
        if job_id not in JOB_STATUS:
            JOB_STATUS[job_id] = {}
        
        JOB_STATUS[job_id].update({
            "status": status,
            "progress": progress,
            "message": message,
            "updated_at": datetime.now().isoformat()
        })

def get_job_status_info(job_id: str) -> dict:
    """Get job status in thread-safe manner"""
    with JOB_LOCK:
        return JOB_STATUS.get(job_id, {"status": "not_found"})

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for dir_path in [UPLOAD_DIR, PROCESSING_DIR, OUTPUT_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_video_file(file: UploadFile) -> bool:
    """Validate uploaded file is a video"""
    logger.info(f"File validation - filename: {file.filename}, content_type: {file.content_type}")
    
    # Check file extension as backup
    if file.filename:
        file_ext = file.filename.lower().split('.')[-1]
        allowed_extensions = ['mp4', 'avi', 'mov', 'mkv', 'webm']
        if file_ext in allowed_extensions:
            logger.info(f"File validation passed by extension: {file_ext}")
            return True
    
    # Check content type
    if file.content_type:
        allowed_types = [
            "video/mp4", "video/avi", "video/mov", "video/mkv", 
            "video/webm", "video/quicktime", "video/x-msvideo"
        ]
        
        if file.content_type in allowed_types:
            logger.info(f"File validation passed by content_type: {file.content_type}")
            return True
    
    logger.warning(f"File validation failed - filename: {file.filename}, content_type: {file.content_type}")
    return False

async def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """Save uploaded file to destination"""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return destination
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

def cleanup_files(job_id: str):
    """Background task to cleanup temporary files after processing"""
    job_dir = PROCESSING_DIR / job_id
    output_dir = OUTPUT_DIR / job_id
    
    # Wait 24 hours before cleanup
    import time
    time.sleep(24 * 60 * 60)  # 24 hours
    
    # Clean up processing directory
    if job_dir.exists():
        shutil.rmtree(job_dir, ignore_errors=True)
    
    # Clean up output directory
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    
    # Remove from status tracking
    with JOB_LOCK:
        if job_id in JOB_STATUS:
            del JOB_STATUS[job_id]

async def enhance_video_pipeline(job_id: str, input_file: Path, model: str = "waifu2x", scale: int = 2):
    """
    Main video enhancement pipeline
    
    Args:
        job_id: Unique job identifier
        input_file: Path to input video file
        model: AI model to use for enhancement
        scale: Upscaling factor
    """
    try:
        job_dir = PROCESSING_DIR / job_id
        output_dir = OUTPUT_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize services
        audio_service = AudioService()
        frame_service = FrameService()
        clarity_service = ClarityService()
        merge_service = MergeService()
        
        update_job_status(job_id, "processing", 0, "Starting video enhancement pipeline")
        
        # Step 1: Get video information
        video_info = frame_service.get_video_info(input_file)
        if not video_info:
            update_job_status(job_id, "failed", 0, "Failed to analyze video file")
            return
        
        fps = video_info.get("fps", 24.0)
        logger.info(f"Video info: {video_info}")
        
        # Step 2: Extract audio
        update_job_status(job_id, "processing", 10, "Extracting audio track")
        audio_file = job_dir / "audio.wav"
        
        if not audio_service.extract_audio(input_file, audio_file):
            update_job_status(job_id, "failed", 10, "Failed to extract audio")
            return
        
        # Step 3: Extract frames
        update_job_status(job_id, "processing", 20, "Extracting video frames")
        frames_dir = job_dir / "frames"
        
        if not frame_service.extract_frames(input_file, frames_dir, fps=fps):
            update_job_status(job_id, "failed", 20, "Failed to extract frames")
            return
        
        # Step 4: Enhance frames with AI
        update_job_status(job_id, "processing", 30, f"Enhancing frames with {model}")
        enhanced_frames_dir = job_dir / "enhanced_frames"
        
        def progress_callback(progress, completed, failed):
            # Update progress from 30% to 80% during frame enhancement
            overall_progress = 30 + (progress * 0.5)
            update_job_status(
                job_id, 
                "processing", 
                overall_progress, 
                f"Enhanced {completed} frames, {failed} failed"
            )
        
        if not clarity_service.enhance_frames_batch(
            frames_dir, 
            enhanced_frames_dir, 
            model=model, 
            scale=scale,
            progress_callback=progress_callback
        ):
            update_job_status(job_id, "failed", 50, "Failed to enhance frames")
            return
        
        # Step 5: Merge enhanced frames with audio
        update_job_status(job_id, "processing", 80, "Merging enhanced video with audio")
        output_video = output_dir / "enhanced.mp4"
        
        if not merge_service.merge_frames_and_audio(
            enhanced_frames_dir,
            audio_file,
            output_video,
            fps=fps
        ):
            update_job_status(job_id, "failed", 80, "Failed to merge video and audio")
            return
        
        # Step 6: Optimize final video
        update_job_status(job_id, "processing", 90, "Optimizing final video")
        optimized_video = output_dir / "enhanced_optimized.mp4"
        
        if merge_service.optimize_video(output_video, optimized_video):
            # Replace original with optimized version
            output_video.unlink()
            optimized_video.rename(output_video)
        
        # Success!
        file_size = output_video.stat().st_size
        update_job_status(
            job_id, 
            "completed", 
            100, 
            f"Enhancement completed. Output file size: {file_size / 1024 / 1024:.1f} MB"
        )
        
        logger.info(f"Enhancement pipeline completed for job {job_id}")
        
    except Exception as e:
        logger.error(f"Enhancement pipeline failed for job {job_id}: {str(e)}")
        update_job_status(job_id, "failed", 0, f"Pipeline error: {str(e)}")

@router.post("/enhance_video/", 
            response_model=EnhanceVideoResponse,
            status_code=202,
            summary="Upload and enhance anime video",
            description="Upload a video file and start AI enhancement process",
            tags=["video-enhancement"],
            responses={
                202: {"model": EnhanceVideoResponse, "description": "Video upload successful, enhancement started"},
                400: {"model": ErrorResponse, "description": "Invalid file type or model parameters"},
                413: {"model": ErrorResponse, "description": "File too large (max 100MB)"},
                500: {"model": ErrorResponse, "description": "Server error during file processing"}
            })
async def enhance_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Video file to enhance (MP4, AVI, MOV, MKV, WebM - max 100MB)"),
    model: ModelEnum = Form(ModelEnum.waifu2x, description="AI model to use for enhancement"),
    scale: ScaleEnum = Form(ScaleEnum.x2, description="Upscaling factor")
):
    """
    Upload and enhance anime video
    
    Args:
        file: Video file to enhance
        model: AI model to use (waifu2x, esrgan)
        scale: Upscaling factor (2, 4)
    
    Returns:
        Job information for tracking enhancement progress
    """
    ensure_directories()
    
    # Validate file
    if not validate_video_file(file):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload a video file."
        )
    
    # Check file size (100MB limit)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > 100 * 1024 * 1024:  # 100MB
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 100MB."
        )
    
    # Validate model and scale
    clarity_service = ClarityService()
    available_models = clarity_service.get_available_models()
    
    if model not in available_models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model}' not available. Available models: {list(available_models.keys())}"
        )
    
    if scale not in available_models[model]["scales"]:
        raise HTTPException(
            status_code=400,
            detail=f"Scale {scale} not supported for model '{model}'. Supported scales: {available_models[model]['scales']}"
        )
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Create job directory
    job_dir = PROCESSING_DIR / job_id
    job_dir.mkdir(exist_ok=True)
    
    # Save uploaded file
    file_extension = Path(file.filename).suffix if file.filename else ".mp4"
    input_file = job_dir / f"input{file_extension}"
    
    try:
        await save_upload_file(file, input_file)
    except Exception as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    # Initialize job status
    update_job_status(job_id, "uploaded", 0, "Video uploaded successfully")
    
    # Start enhancement pipeline in background
    background_tasks.add_task(enhance_video_pipeline, job_id, input_file, model, scale)
    
    # Schedule cleanup after 24 hours
    background_tasks.add_task(cleanup_files, job_id)
    
    return EnhanceVideoResponse(
        message="Video upload successful, enhancement started",
        job_id=job_id,
        status=JobStatusEnum.uploaded,
        filename=file.filename or "unknown",
        file_size=file_size,
        model=model,
        scale=scale
    )

@router.get("/status/{job_id}",
           response_model=JobStatusResponse,
           summary="Get enhancement job status",
           description="Check the status and progress of a video enhancement job",
           tags=["job-management"],
           responses={
               200: {"model": JobStatusResponse, "description": "Job status retrieved successfully"},
               404: {"model": ErrorResponse, "description": "Job not found"}
           })
async def get_job_status(job_id: str):
    """Get enhancement job status"""
    job_dir = PROCESSING_DIR / job_id
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get current status
    status_info = get_job_status_info(job_id)
    
    if status_info["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Job status not found")
    
    # Add estimated completion time for processing jobs
    estimated_completion = None
    if status_info["status"] == "processing":
        # Rough estimation based on progress
        progress = status_info.get("progress", 0)
        if progress > 0:
            # Estimate remaining time (very rough)
            estimated_seconds = (100 - progress) * 2  # 2 seconds per percent
            estimated_completion = (datetime.now() + timedelta(seconds=estimated_seconds)).isoformat()
    
    return JobStatusResponse(
        job_id=job_id,
        status=JobStatusEnum(status_info["status"]),
        progress=status_info.get("progress", 0),
        message=status_info.get("message", ""),
        updated_at=status_info.get("updated_at"),
        estimated_completion=estimated_completion
    )

@router.get("/download/{job_id}",
           response_class=FileResponse,
           summary="Download enhanced video",
           description="Download the enhanced video file for a completed job",
           tags=["video-enhancement"],
           responses={
               200: {"description": "Enhanced video file", "content": {"video/mp4": {}}},
               202: {"model": ErrorResponse, "description": "Video is still being processed"},
               400: {"model": ErrorResponse, "description": "Video enhancement failed"},
               404: {"model": ErrorResponse, "description": "Enhanced video not found"}
           })
async def download_enhanced_video(job_id: str):
    """Download enhanced video"""
    output_file = OUTPUT_DIR / job_id / "enhanced.mp4"
    
    if not output_file.exists():
        # Check job status
        status_info = get_job_status_info(job_id)
        if status_info["status"] == "processing":
            raise HTTPException(status_code=202, detail="Video is still being processed")
        elif status_info["status"] == "failed":
            raise HTTPException(status_code=400, detail="Video enhancement failed")
        else:
            raise HTTPException(status_code=404, detail="Enhanced video not found")
    
    # Return file for download
    return FileResponse(
        path=str(output_file),
        media_type="video/mp4",
        filename=f"enhanced_{job_id}.mp4"
    )

@router.get("/models/",
           response_model=AvailableModelsResponse,
           summary="Get available AI models",
           description="Get list of available AI enhancement models with their supported configurations",
           tags=["models"],
           responses={
               200: {"model": AvailableModelsResponse, "description": "Available models retrieved successfully"}
           })
async def get_available_models():
    """Get list of available AI enhancement models"""
    from .models.schemas import ModelInfo
    
    clarity_service = ClarityService()
    available_models_raw = clarity_service.get_available_models()
    
    # Transform the raw models data to match ModelInfo schema
    models = {}
    for model_name, model_data in available_models_raw.items():
        models[model_name] = ModelInfo(
            name=model_name.title(),  # Capitalize first letter
            description=model_data["description"],
            scales=model_data["scales"],
            optimal_for="anime" if "anime" in model_data["description"].lower() else "general"
        )
    
    # Determine default model - prefer waifu2x if available, otherwise use first available
    default_model = "waifu2x" if "waifu2x" in models else list(models.keys())[0] if models else "test"
    
    return AvailableModelsResponse(
        models=models,
        default_model=default_model,
        default_scale=2
    )

@router.delete("/job/{job_id}",
              response_model=JobCancelResponse,
              summary="Cancel enhancement job",
              description="Cancel a running enhancement job and cleanup associated files",
              tags=["job-management"],
              responses={
                  200: {"model": JobCancelResponse, "description": "Job cancelled successfully"},
                  404: {"model": ErrorResponse, "description": "Job not found"}
              })
async def cancel_job(job_id: str):
    """Cancel enhancement job and cleanup files"""
    job_dir = PROCESSING_DIR / job_id
    output_dir = OUTPUT_DIR / job_id
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update status to cancelled
    update_job_status(job_id, "cancelled", 0, "Job cancelled by user")
    
    # Clean up directories
    if job_dir.exists():
        shutil.rmtree(job_dir, ignore_errors=True)
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    
    return JobCancelResponse(message=f"Job {job_id} cancelled and cleaned up")
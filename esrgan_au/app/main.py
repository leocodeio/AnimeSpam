from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
from pathlib import Path
import logging
import json
from datetime import datetime

from .models.schemas import (
    JobStatusEnum, ScaleEnum, EnhanceVideoResponse, 
    JobStatusResponse, RootResponse, HealthResponse,
    JobCancelResponse, ErrorResponse
)
from .services.audio import AudioService
from .services.frames import FrameService
from .services.clarity import ClarityService
from .services.merge import MergeService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
logger.info("Starting ESRGAN Anime Upscaler API")

app = FastAPI(
    title="ESRGAN Anime Upscaler",
    description="Real-ESRGAN powered anime video upscaling API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = Path("temp")
UPLOAD_DIR = TEMP_DIR / "uploads"
PROCESSING_DIR = TEMP_DIR / "processing"
COMPLETED_DIR = TEMP_DIR / "completed"

for directory in [UPLOAD_DIR, PROCESSING_DIR, COMPLETED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

jobs_db = {}
jobs_lock = {}

@app.get("/", response_model=RootResponse, tags=["system"])
async def root():
    return RootResponse(message="ESRGAN Anime Upscaler API", status="running")

@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health_check():
    return HealthResponse(status="healthy", service="esrgan-anime-upscaler")

def process_video(job_id: str, input_path: Path, scale: int):
    try:
        job_dir = PROCESSING_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        jobs_db[job_id]["status"] = JobStatusEnum.processing
        jobs_db[job_id]["progress"] = 5.0
        jobs_db[job_id]["message"] = "Extracting audio"
        
        audio_service = AudioService()
        frames_service = FrameService()
        clarity_service = ClarityService()
        merge_service = MergeService()
        
        video_path = job_dir / "input.mp4"
        shutil.copy(input_path, video_path)
        
        video_info = frames_service.get_video_info(video_path)
        logger.info(f"Video info: {video_info}")
        
        audio_path = job_dir / "audio.wav"
        audio_service.extract_audio(video_path, audio_path)
        
        jobs_db[job_id]["progress"] = 10.0
        jobs_db[job_id]["message"] = "Extracting frames"
        
        frames_dir = job_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        frames_service.extract_frames(video_path, frames_dir)
        
        jobs_db[job_id]["progress"] = 20.0
        jobs_db[job_id]["message"] = "Enhancing frames with Real-ESRGAN"
        
        enhanced_dir = job_dir / "enhanced_frames"
        enhanced_dir.mkdir(exist_ok=True)
        
        clarity_service.enhance_frames_batch(
            input_dir=frames_dir,
            output_dir=enhanced_dir,
            scale=scale,
            model="esrgan",
            max_workers=1
        )
        
        jobs_db[job_id]["progress"] = 90.0
        jobs_db[job_id]["message"] = "Merging enhanced frames"
        
        output_path = COMPLETED_DIR / f"{job_id}.mp4"
        merge_service.merge_frames_and_audio(
            frames_dir=enhanced_dir,
            audio_file=audio_path,
            output_video=output_path,
            fps=video_info.get("fps", 24)
        )
        
        jobs_db[job_id]["status"] = JobStatusEnum.completed
        jobs_db[job_id]["progress"] = 100.0
        jobs_db[job_id]["message"] = "Video enhancement completed"
        jobs_db[job_id]["output_path"] = str(output_path)
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        jobs_db[job_id]["status"] = JobStatusEnum.failed
        jobs_db[job_id]["message"] = f"Processing failed: {str(e)}"

@app.post("/enhance", response_model=EnhanceVideoResponse, status_code=202, tags=["video-enhancement"])
async def enhance_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Video file to enhance"),
    scale: ScaleEnum = Form(ScaleEnum.x4, description="Upscaling factor (2 or 4)")
):
    MAX_FILE_SIZE = 100 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")
    
    job_id = str(uuid.uuid4())
    upload_path = UPLOAD_DIR / f"{job_id}{file_ext}"
    
    file_size = 0
    with open(upload_path, "wb") as buffer:
        while chunk := await file.read(8192):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                upload_path.unlink()
                raise HTTPException(status_code=413, detail="File too large (max 100MB)")
            buffer.write(chunk)
    
    jobs_db[job_id] = {
        "status": JobStatusEnum.uploaded,
        "progress": 0.0,
        "message": "Video uploaded, queued for processing",
        "filename": file.filename,
        "file_size": file_size,
        "scale": scale,
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(process_video, job_id, upload_path, scale.value)
    
    return EnhanceVideoResponse(
        message="Video uploaded successfully",
        job_id=job_id,
        status=JobStatusEnum.uploaded,
        filename=file.filename,
        file_size=file_size,
        scale=scale
    )

@app.get("/status/{job_id}", response_model=JobStatusResponse, tags=["job-management"])
async def get_job_status(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        updated_at=job.get("created_at")
    )

@app.get("/download/{job_id}", tags=["job-management"])
async def download_video(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    
    if job["status"] != JobStatusEnum.completed:
        raise HTTPException(status_code=400, detail=f"Job not completed. Current status: {job['status']}")
    
    output_path = Path(job.get("output_path", ""))
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        path=str(output_path),
        media_type="video/mp4",
        filename=f"enhanced_{job_id}.mp4"
    )

@app.delete("/job/{job_id}", response_model=JobCancelResponse, tags=["job-management"])
async def cancel_job(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    jobs_db[job_id]["status"] = JobStatusEnum.cancelled
    jobs_db[job_id]["message"] = "Job cancelled by user"
    
    return JobCancelResponse(message=f"Job {job_id} cancelled successfully")

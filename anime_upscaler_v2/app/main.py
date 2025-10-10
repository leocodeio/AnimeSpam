from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from .routes import router
from .models.schemas import RootResponse, HealthResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Starting Anime Upscaler V2 API - Logging initialized")

app = FastAPI(
    title="Anime Upscaler V2",
    description="""
    # Anime Upscaler V2 API
    
    High-quality anime video enhancement API with FPS smoothing and AI upscaling.
    
    ## Features
    
    * **Video Enhancement**: Upload anime videos for AI-powered upscaling
    * **Multiple Models**: Support for Waifu2x and Real-ESRGAN models
    * **Asynchronous Processing**: Background processing with real-time status updates
    * **Download Results**: Download enhanced videos when processing is complete
    
    ## Workflow
    
    1. **Upload**: Use `/enhance_video/` to upload a video file
    2. **Monitor**: Use `/status/{job_id}` to track processing progress
    3. **Download**: Use `/download/{job_id}` to get the enhanced video
    
    ## Models Available
    
    * **waifu2x**: Optimized for anime/cartoon content
    * **esrgan**: High-quality general purpose upscaling
    
    ## Supported Formats
    
    Input: MP4, AVI, MOV, MKV, WebM (max 100MB)
    Output: MP4 (optimized)
    """,
    version="2.0.0",
    contact={
        "name": "Anime Upscaler V2 Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.anime-upscaler.example.com",
            "description": "Production server"
        }
    ],
    openapi_tags=[
        {
            "name": "system",
            "description": "System health and information endpoints"
        },
        {
            "name": "video-enhancement",
            "description": "Video upload and enhancement operations"
        },
        {
            "name": "job-management", 
            "description": "Job status tracking and management"
        },
        {
            "name": "models",
            "description": "AI model information and configuration"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", 
         response_model=RootResponse,
         summary="API Root",
         description="Get basic API information and status",
         tags=["system"])
async def root():
    return RootResponse(message="Anime Upscaler V2 API", status="running")

@app.get("/health",
         response_model=HealthResponse,
         summary="Health Check",
         description="Check if the API service is running and healthy",
         tags=["system"])
async def health_check():
    return HealthResponse(status="healthy", service="anime-upscaler-v2")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
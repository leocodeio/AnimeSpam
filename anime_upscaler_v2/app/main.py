from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from .routes import router

app = FastAPI(
    title="Anime Upscaler V2",
    description="High-quality anime video enhancement API with FPS smoothing and AI upscaling",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Anime Upscaler V2 API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "anime-upscaler-v2"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
import pytest
import asyncio
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_available_models():
    """Test models endpoint"""
    response = client.get("/models/")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "default_model" in data
    assert "default_scale" in data

def test_invalid_job_status():
    """Test status endpoint with invalid job ID"""
    response = client.get("/status/invalid-job-id")
    assert response.status_code == 404

def test_invalid_download():
    """Test download endpoint with invalid job ID"""
    response = client.get("/download/invalid-job-id")
    assert response.status_code == 404

def test_upload_invalid_file():
    """Test upload with invalid file type"""
    # Create a fake text file
    fake_file = {"file": ("test.txt", "not a video", "text/plain")}
    response = client.post("/enhance_video/", files=fake_file)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_upload_no_file():
    """Test upload without file"""
    response = client.post("/enhance_video/")
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_video_info_service():
    """Test video info extraction service"""
    from app.services.frames import FrameService
    
    # This test would need a real video file
    # For now, just test service initialization
    service = FrameService()
    assert service is not None

@pytest.mark.asyncio 
async def test_audio_service():
    """Test audio service initialization"""
    from app.services.audio import AudioService
    
    service = AudioService()
    assert service is not None

@pytest.mark.asyncio
async def test_clarity_service():
    """Test clarity service and model availability"""
    from app.services.clarity import ClarityService
    
    service = ClarityService()
    available_models = service.get_available_models()
    
    # Should return dict even if no models available
    assert isinstance(available_models, dict)

@pytest.mark.asyncio
async def test_merge_service():
    """Test merge service initialization"""
    from app.services.merge import MergeService
    
    service = MergeService()
    assert service is not None

if __name__ == "__main__":
    pytest.main([__file__])
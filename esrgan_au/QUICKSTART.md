# Quick Start Guide

## Setup (5 minutes)

```bash
# 1. Verify files are in place
./verify_setup.sh

# 2. Install API dependencies
pip install -r requirements.txt

# 3. Setup Real-ESRGAN (creates venv, installs PyTorch, etc.)
./setup_realesrgan.sh

# 4. Verify setup again
./verify_setup.sh
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Test

1. Open http://localhost:8000/docs
2. Click "POST /upscale" → "Try it out"
3. Upload a video file
4. Click "Execute"
5. Download the upscaled video

## Architecture

```
Video Input
    ↓
[Frame Extraction] ← FFmpeg
    ↓
[ESRGAN 4x Enhancement] ← Real-ESRGAN (RealESRGAN_x4plus_anime_6B)
    ↓
[Video Merge] ← FFmpeg + Audio
    ↓
Enhanced Video Output
```

## API Endpoints

### POST /upscale
Upload video for 4x upscaling

**Request:**
- `file`: Video file (multipart/form-data)
- `model`: "esrgan" (default)
- `scale`: 4 (default)

**Response:**
- Enhanced video file (MP4)

### GET /models
List available models

**Response:**
```json
{
  "esrgan": {
    "description": "High-quality anime upscaling using Real-ESRGAN",
    "scales": [4],
    "requirements": ["python3"]
  }
}
```

### GET /health
Health check

**Response:**
```json
{
  "status": "healthy"
}
```

## Example Usage

### cURL

```bash
curl -X POST "http://localhost:8000/upscale" \
  -F "file=@input.mp4" \
  -F "model=esrgan" \
  -F "scale=4" \
  -o output.mp4
```

### Python

```python
import requests

url = "http://localhost:8000/upscale"
files = {"file": open("input.mp4", "rb")}
data = {"model": "esrgan", "scale": 4}

response = requests.post(url, files=files, data=data)

with open("output.mp4", "wb") as f:
    f.write(response.content)
```

### JavaScript

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('model', 'esrgan');
formData.append('scale', 4);

fetch('http://localhost:8000/upscale', {
  method: 'POST',
  body: formData
})
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.mp4';
    a.click();
  });
```

## Performance

- **Processing time**: ~5 seconds per frame (GPU) / ~30 seconds (CPU)
- **GPU memory**: ~2GB for 1080p frames
- **Tile size**: 256 (adjustable in clarity.py)

## Troubleshooting

### "Real-ESRGAN virtual environment not found"
Run: `./setup_realesrgan.sh`

### "CUDA out of memory"
Reduce tile size in `app/services/clarity.py`:
```python
"--tile", "128"  # Instead of 256
```

### "FFmpeg not found"
Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### API not responding
Check logs:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## Production Tips

1. **Use a reverse proxy** (nginx/caddy) for SSL and rate limiting
2. **Set max file size** in nginx/proxy
3. **Monitor disk space** (temp files can accumulate)
4. **Use GPU** for production (CPU is too slow)
5. **Consider queue system** for concurrent requests (Celery/Redis)

## File Locations

- **Input videos**: Uploaded via API (stored in temp/)
- **Extracted frames**: temp/<job_id>/frames/
- **Enhanced frames**: temp/<job_id>/enhanced/
- **Output videos**: temp/<job_id>/output/
- **Model weights**: sources/Real-ESRGAN/weights/
- **Logs**: stdout (configure logging in app/main.py)

## Resource Requirements

- **Disk**: ~2GB for dependencies + temp space for videos
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: CUDA-capable (NVIDIA) with 4GB+ VRAM
- **CPU**: 4+ cores for frame processing

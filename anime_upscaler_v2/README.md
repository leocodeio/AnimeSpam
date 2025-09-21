# AnimeSpam v2 - AI-Powered Video Enhancement API

AnimeSpam v2 is a FastAPI-based microservice for enhancing anime videos using AI upscaling models. It provides a complete pipeline for video processing, frame enhancement, and audio preservation.

## 🚀 Features

- **AI-Powered Enhancement**: Support for multiple AI models (Waifu2x, Real-ESRGAN)
- **Video Processing Pipeline**: Automated extraction, enhancement, and merging
- **Async Processing**: Background task processing with job tracking
- **Multiple Formats**: Support for various video formats (MP4, AVI, MOV, MKV, WebM)
- **Quality Preservation**: Maintains original audio and frame rate
- **Scalable Architecture**: Microservice design with Docker support

## 📁 File Structure

```
anime_upscaler_v2/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes.py               # API endpoints and pipeline orchestration
│   ├── services/               # Core processing services
│   │   ├── audio.py           # Audio extraction and merging
│   │   ├── frames.py          # Frame extraction and video assembly
│   │   ├── clarity.py         # AI enhancement integration
│   │   └── merge.py           # Video/audio merging and optimization
│   └── models/                # AI model configurations (future)
├── tests/                     # Unit and integration tests
├── docs/                      # Documentation and specifications
├── temp/                      # Temporary processing directories
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- FFmpeg
- Docker (optional)
- AI Models (Waifu2x, Real-ESRGAN) - optional but recommended

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Install AI enhancement tools (optional)
# Waifu2x
wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20220728/waifu2x-ncnn-vulkan-20220728-ubuntu.zip
unzip waifu2x-ncnn-vulkan-20220728-ubuntu.zip
sudo mv waifu2x-ncnn-vulkan-20220728-ubuntu/waifu2x-ncnn-vulkan /usr/local/bin/

# Real-ESRGAN
pip install realesrgan
```

### Python Setup

```bash
# Clone repository
git clone <repository-url>
cd anime_upscaler_v2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Docker Setup

```bash
# Build container
docker build -t anime-upscaler-v2 .

# Run container
docker run -p 8000:8000 -v $(pwd)/temp:/app/temp anime-upscaler-v2
```

## 🚀 Usage

### Starting the Server

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Upload and Enhance Video
```bash
POST /enhance_video/
```

Upload a video file for AI enhancement:

```bash
curl -X POST "http://localhost:8000/enhance_video/" \
     -F "file=@video.mp4" \
     -F "model=waifu2x" \
     -F "scale=2"
```

**Parameters:**
- `file`: Video file (MP4, AVI, MOV, MKV, WebM) - max 100MB
- `model`: AI model (`waifu2x`, `esrgan`) - default: `waifu2x`
- `scale`: Upscaling factor (2, 4) - default: `2`

**Response:**
```json
{
  "message": "Video upload successful, enhancement started",
  "job_id": "uuid-string",
  "status": "uploaded",
  "filename": "video.mp4",
  "file_size": 15728640,
  "model": "waifu2x",
  "scale": 2
}
```

#### Check Job Status
```bash
GET /status/{job_id}
```

Track enhancement progress:

```bash
curl "http://localhost:8000/status/uuid-string"
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "progress": 65.5,
  "message": "Enhanced 1500 frames, 0 failed",
  "updated_at": "2023-12-07T10:30:00",
  "estimated_completion": "2023-12-07T10:35:00"
}
```

**Status Values:**
- `uploaded`: File uploaded, waiting to start
- `processing`: Enhancement in progress
- `completed`: Enhancement finished
- `failed`: Enhancement failed
- `cancelled`: Job cancelled by user

#### Download Enhanced Video
```bash
GET /download/{job_id}
```

Download the enhanced video:

```bash
curl -O "http://localhost:8000/download/uuid-string"
```

#### Get Available Models
```bash
GET /models/
```

List available AI enhancement models:

```bash
curl "http://localhost:8000/models/"
```

**Response:**
```json
{
  "models": {
    "waifu2x": {
      "description": "Fast anime upscaling using Anime4K",
      "scales": [2, 3, 4],
      "requirements": ["waifu2x-ncnn-vulkan"]
    },
    "esrgan": {
      "description": "High-quality upscaling using Real-ESRGAN",
      "scales": [2, 4],
      "requirements": ["realesrgan"]
    }
  },
  "default_model": "waifu2x",
  "default_scale": 2
}
```

#### Cancel Job
```bash
DELETE /job/{job_id}
```

Cancel a running job and cleanup files:

```bash
curl -X DELETE "http://localhost:8000/job/uuid-string"
```

## 🔄 Enhancement Pipeline

The video enhancement process follows these steps:

1. **Video Analysis**: Extract metadata (resolution, FPS, duration)
2. **Audio Extraction**: Separate audio track using FFmpeg
3. **Frame Extraction**: Convert video to individual frames
4. **AI Enhancement**: Upscale frames using selected AI model
5. **Video Assembly**: Reconstruct video from enhanced frames
6. **Audio Merging**: Combine enhanced video with original audio
7. **Optimization**: Compress final video for optimal file size

## 🎯 AI Models

### Waifu2x
- **Best for**: Anime/cartoon content
- **Speed**: Fast processing
- **Quality**: Good for anime-style images
- **Scales**: 2x, 3x, 4x

### Real-ESRGAN
- **Best for**: High-quality upscaling
- **Speed**: Slower processing
- **Quality**: Excellent for detailed content
- **Scales**: 2x, 4x

## 📊 Performance

### Processing Times (Approximate)
- **30-second video**: 2-5 minutes (Waifu2x), 5-10 minutes (Real-ESRGAN)
- **Memory usage**: 2-4GB during processing
- **Storage**: ~3x original file size during processing

### Optimization Tips
- Use Waifu2x for faster processing
- Limit video length to under 2 minutes for best experience
- Ensure sufficient disk space (3x video size)
- Use SSD storage for better performance

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_enhancement.py
```

## 🐳 Docker Deployment

```bash
# Build production image
docker build -t anime-upscaler-v2:latest .

# Run with volume mapping
docker run -d \
  --name anime-upscaler \
  -p 8000:8000 \
  -v /host/temp:/app/temp \
  anime-upscaler-v2:latest

# Docker Compose (optional)
version: '3.8'
services:
  anime-upscaler:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./temp:/app/temp
    environment:
      - LOG_LEVEL=INFO
```

## 🔧 Configuration

Environment variables:

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MAX_FILE_SIZE`: Maximum upload size in bytes (default: 100MB)
- `CLEANUP_DELAY`: Hours before temp file cleanup (default: 24)
- `MAX_WORKERS`: Parallel processing workers (default: 4)

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## 📝 License

See [LICENSE.md](../LICENCE.md) for license information.

## 🚀 Roadmap

- [ ] Web interface for easy video uploads
- [ ] Batch processing for multiple videos
- [ ] Additional AI models (Anime4K, SRCNN)
- [ ] GPU acceleration support
- [ ] Video preview thumbnails
- [ ] Progress webhooks
- [ ] User authentication
- [ ] Video compression options

## 📞 Support

For issues and questions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include logs and system information

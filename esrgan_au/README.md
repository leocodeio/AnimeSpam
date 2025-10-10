# ESRGAN AU - Standalone ESRGAN Upscaling API

A FastAPI-based service for 4x anime upscaling using Real-ESRGAN.

## Features

- 4x upscaling using Real-ESRGAN (RealESRGAN_x4plus_anime_6B model)
- Frame extraction and enhancement
- Audio preservation
- Video merging with upscaled frames
- RESTful API interface

## Setup

### 1. Install API dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Real-ESRGAN

Run the setup script to install Real-ESRGAN and its dependencies:

```bash
./setup_realesrgan.sh
```

This will:
- Create a virtual environment at `sources/Real-ESRGAN/.venv`
- Install PyTorch, BasicSR, and Real-ESRGAN
- Set up the model weights

### 3. Verify setup

Check that the model weights exist at:
```
sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth
```

## Running the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### POST /upscale
Upload a video file for 4x upscaling

**Parameters:**
- `file`: Video file (MP4, AVI, MKV, MOV)
- `model`: Always "esrgan" (default)
- `scale`: Always 4 (default)

**Returns:**
Enhanced video file

## Directory Structure

```
esrgan_au/
├── app/
│   ├── models/      # Pydantic schemas
│   ├── services/    # Core services (clarity, frames, audio, merge)
│   ├── main.py      # FastAPI app
│   └── routes.py    # API routes
├── sources/
│   └── Real-ESRGAN/ # Real-ESRGAN installation
│       ├── .venv/   # Virtual environment for Real-ESRGAN
│       └── weights/ # Model weights
├── requirements.txt
├── setup_realesrgan.sh
└── README.md
```

## Technical Details

- **Model**: RealESRGAN_x4plus_anime_6B
- **Scale**: 4x only
- **Input formats**: MP4, AVI, MKV, MOV
- **Output format**: MP4

## Differences from anime_upscaler_v2

This is a standalone version that:
- Only supports ESRGAN (no waifu2x, anime4k, or test models)
- Only supports 4x upscaling (no 2x)
- Has its own Real-ESRGAN installation (no external dependencies)
- Simplified and focused on production use

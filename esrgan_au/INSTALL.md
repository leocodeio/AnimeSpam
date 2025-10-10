# Installation Guide for ESRGAN AU

## Quick Start

```bash
# 1. Install API dependencies
pip install -r requirements.txt

# 2. Setup Real-ESRGAN (creates venv and installs dependencies)
./setup_realesrgan.sh

# 3. Start the API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Detailed Steps

### Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (recommended) or CPU
- ~2GB disk space for dependencies
- ~18MB for model weights (already included)

### 1. Install API Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI and Uvicorn (API framework)
- OpenCV, NumPy, Pillow (video/image processing)
- Pydantic (data validation)

### 2. Setup Real-ESRGAN

The `setup_realesrgan.sh` script automates the Real-ESRGAN installation:

```bash
./setup_realesrgan.sh
```

This script:
1. Creates a virtual environment at `sources/Real-ESRGAN/.venv`
2. Installs PyTorch with CUDA 11.8 support
3. Installs BasicSR (image restoration framework)
4. Installs Real-ESRGAN
5. Verifies model weights exist

**Manual Setup (if script fails):**

```bash
cd sources/Real-ESRGAN

# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Install PyTorch (adjust CUDA version as needed)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install BasicSR
cd BasicSR
pip install -e .
cd ..

# Install Real-ESRGAN
pip install -e .

deactivate
```

### 3. Verify Installation

Check that the virtual environment and model weights exist:

```bash
# Check venv
ls sources/Real-ESRGAN/.venv/bin/python3

# Check model weights
ls -lh sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth
```

### 4. Start the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Troubleshooting

### CUDA Not Available

If you don't have a CUDA-capable GPU, install CPU-only PyTorch:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Note: CPU processing will be significantly slower.

### Model Weights Missing

If the model weights are missing, download them:

```bash
cd sources/Real-ESRGAN/weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/RealESRGAN_x4plus_anime_6B.pth
```

### Import Errors

Make sure the Real-ESRGAN virtual environment is set up correctly:

```bash
sources/Real-ESRGAN/.venv/bin/python3 -c "import realesrgan; print('OK')"
```

### Permission Denied on setup_realesrgan.sh

Make the script executable:

```bash
chmod +x setup_realesrgan.sh
```

## GPU Configuration

### CUDA Version

The setup script installs PyTorch with CUDA 11.8. To use a different version:

```bash
# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# For CPU only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Verify GPU

```bash
sources/Real-ESRGAN/.venv/bin/python3 -c "import torch; print(torch.cuda.is_available())"
```

## Production Deployment

### Using systemd

Create `/etc/systemd/system/esrgan-au.service`:

```ini
[Unit]
Description=ESRGAN AU API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/esrgan_au
ExecStart=/path/to/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable esrgan-au
sudo systemctl start esrgan-au
```

### Using Docker

A Dockerfile can be created for containerized deployment. The key considerations:
- Base image with CUDA support (nvidia/cuda:11.8.0-runtime-ubuntu22.04)
- Copy sources/Real-ESRGAN/ including weights
- Install dependencies in container
- Expose port 8000

## Performance Tuning

- **Batch size**: Controlled via API max_workers parameter
- **GPU memory**: Adjust tile size in clarity.py (default: 256)
- **CPU workers**: Set max_workers=1 for CPU to avoid memory issues

## Updating

To update Real-ESRGAN or its dependencies:

```bash
cd sources/Real-ESRGAN
source .venv/bin/activate
pip install --upgrade torch torchvision basicsr realesrgan
deactivate
```

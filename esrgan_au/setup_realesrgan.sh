#!/bin/bash

# Setup script for Real-ESRGAN in esrgan_au

set -e

echo "Setting up Real-ESRGAN for esrgan_au..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REALESRGAN_DIR="$SCRIPT_DIR/sources/Real-ESRGAN"

# Check if Real-ESRGAN directory exists
if [ ! -d "$REALESRGAN_DIR" ]; then
    echo "Error: Real-ESRGAN directory not found at $REALESRGAN_DIR"
    exit 1
fi

# Create virtual environment in Real-ESRGAN directory
cd "$REALESRGAN_DIR"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyTorch (adjust based on your CUDA version)
echo "Installing PyTorch..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install BasicSR
echo "Installing BasicSR..."
cd BasicSR
pip install -e .
cd ..

# Install Real-ESRGAN
echo "Installing Real-ESRGAN..."
pip install -e .

# Install additional dependencies
echo "Installing additional dependencies..."
pip install opencv-python numpy Pillow

# Check if model weights exist
if [ -f "weights/RealESRGAN_x4plus_anime_6B.pth" ]; then
    echo "Model weights found!"
else
    echo "Warning: Model weights not found at weights/RealESRGAN_x4plus_anime_6B.pth"
    echo "Please download the weights manually"
fi

echo "Setup complete!"
echo "Virtual environment created at: $REALESRGAN_DIR/.venv"

deactivate

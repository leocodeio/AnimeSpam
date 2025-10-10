#!/bin/bash

# Verification script for esrgan_au standalone setup

echo "=== ESRGAN AU Setup Verification ==="
echo ""

SUCCESS=0
FAILED=0

check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
        ((SUCCESS++))
    else
        echo "✗ $1 (MISSING)"
        ((FAILED++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
        ((SUCCESS++))
    else
        echo "✗ $1/ (MISSING)"
        ((FAILED++))
    fi
}

echo "Checking directory structure..."
check_dir "sources/Real-ESRGAN"
check_dir "sources/Real-ESRGAN/realesrgan"
check_dir "sources/Real-ESRGAN/BasicSR"
check_dir "sources/Real-ESRGAN/weights"

echo ""
echo "Checking critical files..."
check_file "sources/Real-ESRGAN/inference_realesrgan.py"
check_file "sources/Real-ESRGAN/setup.py"
check_file "sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth"

echo ""
echo "Checking application files..."
check_file "app/services/clarity.py"
check_file "app/main.py"
check_file "requirements.txt"

echo ""
echo "Checking documentation..."
check_file "README.md"
check_file "INSTALL.md"
check_file "CHANGES.md"
check_file "STATUS.md"

echo ""
echo "Checking setup script..."
check_file "setup_realesrgan.sh"

if [ -x "setup_realesrgan.sh" ]; then
    echo "✓ setup_realesrgan.sh is executable"
    ((SUCCESS++))
else
    echo "✗ setup_realesrgan.sh is not executable (run: chmod +x setup_realesrgan.sh)"
    ((FAILED++))
fi

echo ""
echo "Checking model weights size..."
if [ -f "sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth" ]; then
    SIZE=$(stat -f%z "sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth" 2>/dev/null || stat -c%s "sources/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth" 2>/dev/null)
    SIZE_MB=$((SIZE / 1024 / 1024))
    
    if [ $SIZE_MB -gt 15 ]; then
        echo "✓ Model weights size: ${SIZE_MB}MB (valid)"
        ((SUCCESS++))
    else
        echo "✗ Model weights size: ${SIZE_MB}MB (too small, may be corrupted)"
        ((FAILED++))
    fi
fi

echo ""
echo "Checking Real-ESRGAN virtual environment..."
if [ -d "sources/Real-ESRGAN/.venv" ]; then
    echo "✓ Virtual environment exists"
    ((SUCCESS++))
    
    if [ -f "sources/Real-ESRGAN/.venv/bin/python3" ]; then
        echo "✓ Python3 binary found in venv"
        ((SUCCESS++))
    else
        echo "✗ Python3 binary not found in venv"
        ((FAILED++))
    fi
else
    echo "✗ Virtual environment not found (run: ./setup_realesrgan.sh)"
    ((FAILED++))
fi

echo ""
echo "=== Summary ==="
echo "Passed: $SUCCESS"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All checks passed! Ready to test."
    echo ""
    echo "Next steps:"
    echo "  1. Install API dependencies: pip install -r requirements.txt"
    if [ ! -d "sources/Real-ESRGAN/.venv" ]; then
        echo "  2. Setup Real-ESRGAN: ./setup_realesrgan.sh"
    fi
    echo "  3. Start API: uvicorn app.main:app --host 0.0.0.0 --port 8000"
    exit 0
else
    echo "⚠️  Some checks failed. Please review the errors above."
    exit 1
fi

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and install Waifu2x (optional, for AI enhancement)
RUN wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20220728/waifu2x-ncnn-vulkan-20220728-ubuntu.zip \
    && unzip waifu2x-ncnn-vulkan-20220728-ubuntu.zip \
    && mv waifu2x-ncnn-vulkan-20220728-ubuntu/waifu2x-ncnn-vulkan /usr/local/bin/ \
    && chmod +x /usr/local/bin/waifu2x-ncnn-vulkan \
    && rm -rf waifu2x-ncnn-vulkan-20220728-ubuntu* || true

# Copy application code
COPY app/ ./app/

# Create temp directories
RUN mkdir -p temp/uploads temp/processing temp/output

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
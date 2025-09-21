# Anime Upscaler V2 - Development Guide

## Phase 1 – Prototype Tasks

### Project Structure Guidelines

```
anime_upscaler_v2/
├── app/
│   ├── main.py          # FastAPI app initialization
│   ├── routes.py        # API endpoints
│   ├── services/        # Core business logic
│   │   ├── audio.py     # Audio extraction/handling
│   │   ├── frames.py    # Frame extraction + FPS management
│   │   ├── clarity.py   # AI enhancement (Anime4K/ESRGAN)
│   │   └── merge.py     # Video reconstruction
│   └── models/          # ML model management
├── temp/                # Temporary processing files
│   ├── uploads/         # Uploaded videos
│   ├── frames/          # Extracted frames
│   ├── frames_enhanced/ # AI-enhanced frames
│   └── audio/           # Extracted audio files
├── output/              # Final processed videos
└── models/              # Pre-trained AI models
```

## Implementation Do's and Don'ts

### ✅ DO's
- Use async/await for all I/O operations
- Implement proper error handling and logging
- Create temporary directories dynamically
- Clean up temp files after processing
- Use FFmpeg for all video/audio operations
- Validate input file formats and sizes
- Implement progress tracking for long operations
- Use environment variables for configuration
- Test with small video samples first
- Document all API endpoints

### ❌ DON'Ts
- Don't store large files in memory
- Don't hardcode file paths
- Don't skip input validation
- Don't ignore FFmpeg error codes
- Don't block the main thread with CPU-intensive tasks
- Don't leave temp files after processing
- Don't expose internal error details to API
- Don't process extremely large files without limits

## Phase 1 Implementation Tasks

### Task 1: Input Handling
**Priority: High**

#### Subtasks:
1.1. Setup FastAPI application structure
- [ ] Initialize FastAPI app in `main.py`
- [ ] Configure CORS and middleware
- [ ] Setup basic error handling
- [ ] Add request/response models

1.2. Implement `/enhance_video/` endpoint
- [ ] Create POST endpoint in `routes.py`
- [ ] Accept multipart/form-data uploads
- [ ] Validate file format (mp4, avi, mov, mkv)
- [ ] Validate file size limits (max 500MB for prototype)
- [ ] Generate unique job IDs for tracking

1.3. File storage management
- [ ] Create `temp/uploads/` directory structure
- [ ] Save uploaded video with unique filename
- [ ] Store metadata (original filename, size, duration)
- [ ] Return job ID and status

### Task 2: Audio Extraction
**Priority: High**

#### Subtasks:
2.1. FFmpeg integration setup
- [ ] Install and configure FFmpeg dependency
- [ ] Create audio extraction utility in `audio.py`
- [ ] Handle FFmpeg subprocess calls safely
- [ ] Implement error handling for audio extraction

2.2. Audio processing implementation
- [ ] Extract audio to AAC format (`audio.aac`)
- [ ] Store audio file path in job metadata
- [ ] Preserve original audio quality
- [ ] Handle videos without audio tracks

### Task 3: Frame Extraction
**Priority: High**

#### Subtasks:
3.1. Frame extraction setup
- [ ] Create frame extraction logic in `frames.py`
- [ ] Setup `temp/frames/` directory per job
- [ ] Implement FFmpeg frame extraction
- [ ] Use naming pattern: `frame_%04d.png`

3.2. Metadata collection
- [ ] Extract original video FPS
- [ ] Count total frames
- [ ] Store frame dimensions
- [ ] Calculate video duration
- [ ] Save metadata to JSON file

### Task 4: FPS Smoothing (24 fps target)
**Priority: Medium**

#### Subtasks:
4.1. FPS analysis and planning
- [ ] Analyze input video FPS
- [ ] Calculate frame interpolation requirements
- [ ] Implement frame duplication for upsampling
- [ ] Implement frame skipping for downsampling

4.2. Basic interpolation implementation
- [ ] Use FFmpeg frame blending for simple interpolation
- [ ] Generate 24 fps frame sequence
- [ ] Maintain smooth motion appearance
- [ ] Store interpolated frames separately

4.3. Advanced interpolation (Optional)
- [ ] Research RIFE integration
- [ ] Research DAIN integration
- [ ] Implement AI-based frame interpolation
- [ ] Compare quality vs processing time

### Task 5: Clarity Enhancement
**Priority: High**

#### Subtasks:
5.1. Anime4K integration
- [ ] Setup Anime4K model in `clarity.py`
- [ ] Implement frame-by-frame enhancement
- [ ] Handle different input resolutions
- [ ] Optimize processing performance

5.2. Enhancement pipeline
- [ ] Process frames in batches
- [ ] Implement progress tracking
- [ ] Save enhanced frames to `frames_enhanced/`
- [ ] Maintain frame ordering and naming

5.3. Alternative models (Optional)
- [ ] Integrate ESRGAN for comparison
- [ ] Test Waifu2x implementation
- [ ] Create model selection parameter
- [ ] Benchmark performance differences

### Task 6: Video Assembly
**Priority: High**

#### Subtasks:
6.1. Frame-to-video conversion
- [ ] Implement video reconstruction in `merge.py`
- [ ] Use FFmpeg to combine enhanced frames
- [ ] Set output video to 24 fps
- [ ] Maintain original video codec settings

6.2. Audio-video synchronization
- [ ] Merge reconstructed video with extracted audio
- [ ] Ensure audio-video sync at 24 fps
- [ ] Handle audio timing adjustments
- [ ] Save final output to `output/enhanced.mp4`

6.3. Output optimization
- [ ] Implement video compression settings
- [ ] Maintain quality vs file size balance
- [ ] Add metadata to output video
- [ ] Generate preview thumbnails

### Task 7: Cleanup and Response
**Priority: Medium**

#### Subtasks:
7.1. Cleanup implementation
- [ ] Remove temp files after successful processing
- [ ] Implement cleanup on error conditions
- [ ] Schedule cleanup for failed jobs
- [ ] Preserve output files with expiration

7.2. API response handling
- [ ] Return job completion status
- [ ] Provide download link for enhanced video
- [ ] Include processing statistics
- [ ] Add error details for failed jobs

7.3. Status tracking
- [ ] Implement job status endpoint
- [ ] Provide processing progress updates
- [ ] Store job history and logs
- [ ] Add job cancellation capability

## Configuration Requirements

### Environment Variables
```bash
FFMPEG_PATH=/usr/bin/ffmpeg
MAX_FILE_SIZE=524288000  # 500MB
TEMP_DIR=./temp
OUTPUT_DIR=./output
MODEL_PATH=./models
CLEANUP_INTERVAL=3600    # 1 hour
```

### Dependencies (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
opencv-python==4.8.1.78
numpy==1.24.3
Pillow==10.0.1
aiofiles==23.2.1
```

## Testing Strategy

### Unit Tests
- Test each service module independently
- Mock FFmpeg calls for faster testing
- Test error handling scenarios
- Validate file operations

### Integration Tests
- Test complete pipeline with sample videos
- Test different video formats and sizes
- Test edge cases (no audio, corrupt files)
- Performance testing with various file sizes

### Quality Assurance
- Visual quality comparison tools
- Automated video analysis
- Performance benchmarking
- Memory usage monitoring

## Success Metrics

### Phase 1 Goals
- [ ] Process 480p anime video to 24fps enhanced output
- [ ] Complete processing within 5x original video duration
- [ ] Maintain visual quality improvement
- [ ] Handle common video formats reliably
- [ ] Provide stable API with proper error handling
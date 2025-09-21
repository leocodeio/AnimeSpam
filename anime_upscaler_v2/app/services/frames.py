import subprocess
import os
from pathlib import Path
from typing import Optional, List
import logging
import json

logger = logging.getLogger(__name__)

class FrameService:
    """Service for extracting and processing video frames"""
    
    @staticmethod
    def get_video_info(video_file: Path) -> Optional[dict]:
        """
        Get video information using FFprobe
        
        Returns:
            dict: Video information or None if failed
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                "-select_streams", "v:0",
                str(video_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            data = json.loads(result.stdout)
            
            if data.get("streams"):
                stream = data["streams"][0]
                
                # Parse frame rate
                fps_str = stream.get("r_frame_rate", "24/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = float(num) / float(den)
                else:
                    fps = float(fps_str)
                
                return {
                    "width": int(stream.get("width", 0)),
                    "height": int(stream.get("height", 0)),
                    "fps": fps,
                    "duration": float(stream.get("duration", 0)),
                    "codec": stream.get("codec_name"),
                    "pixel_format": stream.get("pix_fmt"),
                    "frame_count": int(stream.get("nb_frames", 0))
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get video info: {str(e)}")
            return None
    
    @staticmethod
    def extract_frames(
        input_video: Path, 
        output_dir: Path, 
        fps: Optional[float] = None,
        format: str = "png"
    ) -> bool:
        """
        Extract frames from video
        
        Args:
            input_video: Path to input video file
            output_dir: Directory to save extracted frames
            fps: Target frame rate (None to keep original)
            format: Output image format (png, jpg)
        
        Returns:
            bool: True if extraction successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg",
                "-i", str(input_video),
                "-vsync", "0",  # Preserve original frame timing
            ]
            
            # Add frame rate filter if specified
            if fps:
                cmd.extend(["-vf", f"fps={fps}"])
            
            # Add output options
            cmd.extend([
                "-f", "image2",
                "-q:v", "2" if format == "jpg" else "1",  # Quality
                "-y",  # Overwrite output files
                str(output_dir / f"frame_%06d.{format}")
            ])
            
            logger.info(f"Extracting frames: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify frames were extracted
            frame_files = list(output_dir.glob(f"frame_*.{format}"))
            if frame_files:
                logger.info(f"Extracted {len(frame_files)} frames to {output_dir}")
                return True
            else:
                logger.error("No frames were extracted")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Frame extraction failed: {str(e)}")
            return False
    
    @staticmethod
    def get_frame_list(frames_dir: Path, format: str = "png") -> List[Path]:
        """
        Get sorted list of frame files
        
        Args:
            frames_dir: Directory containing frames
            format: Image format to look for
        
        Returns:
            List[Path]: Sorted list of frame file paths
        """
        frame_files = list(frames_dir.glob(f"frame_*.{format}"))
        frame_files.sort()  # Ensure proper ordering
        return frame_files
    
    @staticmethod
    def frames_to_video(
        frames_dir: Path,
        output_video: Path,
        fps: float = 24.0,
        format: str = "png",
        codec: str = "libx264"
    ) -> bool:
        """
        Convert frames back to video
        
        Args:
            frames_dir: Directory containing frames
            output_video: Path to output video file
            fps: Output frame rate
            format: Input frame format
            codec: Video codec to use
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_video.parent.mkdir(parents=True, exist_ok=True)
            
            # Verify frames exist
            frame_pattern = frames_dir / f"frame_%06d.{format}"
            if not list(frames_dir.glob(f"frame_*.{format}")):
                logger.error(f"No frames found in {frames_dir}")
                return False
            
            cmd = [
                "ffmpeg",
                "-framerate", str(fps),
                "-i", str(frame_pattern),
                "-c:v", codec,
                "-pix_fmt", "yuv420p",  # Ensure compatibility
                "-crf", "18",  # High quality
                "-preset", "medium",
                "-y",  # Overwrite output files
                str(output_video)
            ]
            
            logger.info(f"Creating video from frames: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify output file was created
            if output_video.exists() and output_video.stat().st_size > 0:
                logger.info(f"Video creation successful: {output_video}")
                return True
            else:
                logger.error("Video file was not created or is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Frames to video conversion failed: {str(e)}")
            return False
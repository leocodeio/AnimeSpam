import subprocess
import os
from pathlib import Path
from typing import Optional
import logging
import json

logger = logging.getLogger(__name__)

class MergeService:
    """Service for merging enhanced frames with audio to create final video"""
    
    @staticmethod
    def merge_frames_and_audio(
        frames_dir: Path,
        audio_file: Path,
        output_video: Path,
        fps: float = 24.0,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        quality: str = "high"
    ) -> bool:
        """
        Merge enhanced frames with extracted audio to create final video
        
        Args:
            frames_dir: Directory containing enhanced frames
            audio_file: Path to extracted audio file
            output_video: Path to output video file
            fps: Frame rate for output video
            video_codec: Video codec to use
            audio_codec: Audio codec to use
            quality: Quality preset (high, medium, fast)
            
        Returns:
            bool: True if merge successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_video.parent.mkdir(parents=True, exist_ok=True)
            
            # Verify frames exist
            frame_pattern = frames_dir / "frame_%06d.png"
            frame_files = list(frames_dir.glob("frame_*.png"))
            if not frame_files:
                frame_files = list(frames_dir.glob("frame_*.jpg"))
                frame_pattern = frames_dir / "frame_%06d.jpg"
            
            if not frame_files:
                logger.error(f"No frames found in {frames_dir}")
                return False
            
            # Verify audio file exists
            if not audio_file.exists():
                logger.error(f"Audio file not found: {audio_file}")
                return False
            
            # Set quality parameters based on preset
            quality_settings = {
                "high": {"crf": "18", "preset": "slow"},
                "medium": {"crf": "23", "preset": "medium"},
                "fast": {"crf": "28", "preset": "fast"}
            }
            
            settings = quality_settings.get(quality, quality_settings["medium"])
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg",
                "-framerate", str(fps),
                "-i", str(frame_pattern),
                "-i", str(audio_file),
                "-c:v", video_codec,
                "-c:a", audio_codec,
                "-crf", settings["crf"],
                "-preset", settings["preset"],
                "-pix_fmt", "yuv420p",  # Ensure compatibility
                "-map", "0:v:0",  # Map video from frames
                "-map", "1:a:0",  # Map audio from audio file
                "-shortest",      # Stop when shortest stream ends
                "-y",             # Overwrite output files
                str(output_video)
            ]
            
            logger.info(f"Merging frames and audio: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify output file was created
            if output_video.exists() and output_video.stat().st_size > 0:
                logger.info(f"Video merge successful: {output_video}")
                return True
            else:
                logger.error("Merged video file was not created or is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg merge error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Video merge failed: {str(e)}")
            return False
    
    @staticmethod
    def create_video_without_audio(
        frames_dir: Path,
        output_video: Path,
        fps: float = 24.0,
        video_codec: str = "libx264",
        quality: str = "high"
    ) -> bool:
        """
        Create video from frames without audio
        
        Args:
            frames_dir: Directory containing enhanced frames
            output_video: Path to output video file
            fps: Frame rate for output video
            video_codec: Video codec to use
            quality: Quality preset (high, medium, fast)
            
        Returns:
            bool: True if creation successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_video.parent.mkdir(parents=True, exist_ok=True)
            
            # Verify frames exist
            frame_pattern = frames_dir / "frame_%06d.png"
            frame_files = list(frames_dir.glob("frame_*.png"))
            if not frame_files:
                frame_files = list(frames_dir.glob("frame_*.jpg"))
                frame_pattern = frames_dir / "frame_%06d.jpg"
            
            if not frame_files:
                logger.error(f"No frames found in {frames_dir}")
                return False
            
            # Set quality parameters
            quality_settings = {
                "high": {"crf": "18", "preset": "slow"},
                "medium": {"crf": "23", "preset": "medium"},
                "fast": {"crf": "28", "preset": "fast"}
            }
            
            settings = quality_settings.get(quality, quality_settings["medium"])
            
            cmd = [
                "ffmpeg",
                "-framerate", str(fps),
                "-i", str(frame_pattern),
                "-c:v", video_codec,
                "-crf", settings["crf"],
                "-preset", settings["preset"],
                "-pix_fmt", "yuv420p",
                "-y",
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
            logger.error(f"Video creation failed: {str(e)}")
            return False
    
    @staticmethod
    def optimize_video(
        input_video: Path,
        output_video: Path,
        target_size_mb: Optional[float] = None,
        max_bitrate: Optional[str] = None
    ) -> bool:
        """
        Optimize video file size and quality
        
        Args:
            input_video: Path to input video file
            output_video: Path to optimized output video file
            target_size_mb: Target file size in MB
            max_bitrate: Maximum bitrate (e.g., "2M", "5000k")
            
        Returns:
            bool: True if optimization successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_video.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-i", str(input_video),
                "-c:v", "libx264",
                "-c:a", "aac"
            ]
            
            if target_size_mb:
                # Calculate bitrate for target file size
                # Get video duration first
                duration = MergeService._get_video_duration(input_video)
                if duration:
                    target_bitrate = int((target_size_mb * 8 * 1024) / duration)  # kbps
                    cmd.extend(["-b:v", f"{target_bitrate}k"])
            
            if max_bitrate:
                cmd.extend(["-maxrate", max_bitrate, "-bufsize", max_bitrate])
            
            cmd.extend([
                "-preset", "medium",
                "-crf", "23",
                "-y",
                str(output_video)
            ])
            
            logger.info(f"Optimizing video: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify output file was created
            if output_video.exists() and output_video.stat().st_size > 0:
                logger.info(f"Video optimization successful: {output_video}")
                return True
            else:
                logger.error("Optimized video file was not created or is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg optimization error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Video optimization failed: {str(e)}")
            return False
    
    @staticmethod
    def _get_video_duration(video_file: Path) -> Optional[float]:
        """Get video duration in seconds"""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                str(video_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            data = json.loads(result.stdout)
            duration = data.get("format", {}).get("duration")
            
            return float(duration) if duration else None
            
        except Exception as e:
            logger.error(f"Failed to get video duration: {str(e)}")
            return None
import subprocess
import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AudioService:
    """Service for extracting and processing audio from video files"""
    
    @staticmethod
    def extract_audio(input_video: Path, output_audio: Path, format: str = "wav") -> bool:
        """
        Extract audio from video file using FFmpeg
        
        Args:
            input_video: Path to input video file
            output_audio: Path to output audio file
            format: Audio format (wav, mp3, aac)
        
        Returns:
            bool: True if extraction successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_audio.parent.mkdir(parents=True, exist_ok=True)
            
            # FFmpeg command to extract audio
            cmd = [
                "ffmpeg",
                "-i", str(input_video),
                "-vn",  # No video
                "-acodec", "pcm_s16le" if format == "wav" else "libmp3lame",
                "-ar", "44100",  # Sample rate
                "-ac", "2",      # Stereo
                "-y",            # Overwrite output files
                str(output_audio)
            ]
            
            logger.info(f"Extracting audio: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify output file was created
            if output_audio.exists() and output_audio.stat().st_size > 0:
                logger.info(f"Audio extraction successful: {output_audio}")
                return True
            else:
                logger.error("Audio file was not created or is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Audio extraction failed: {str(e)}")
            return False
    
    @staticmethod
    def get_audio_info(video_file: Path) -> Optional[dict]:
        """
        Get audio information from video file
        
        Returns:
            dict: Audio information or None if failed
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                "-select_streams", "a:0",
                str(video_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            data = json.loads(result.stdout)
            
            if data.get("streams"):
                stream = data["streams"][0]
                return {
                    "codec": stream.get("codec_name"),
                    "duration": float(stream.get("duration", 0)),
                    "sample_rate": int(stream.get("sample_rate", 0)),
                    "channels": int(stream.get("channels", 0)),
                    "bit_rate": int(stream.get("bit_rate", 0))
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get audio info: {str(e)}")
            return None
    
    @staticmethod
    def merge_audio_video(video_file: Path, audio_file: Path, output_file: Path) -> bool:
        """
        Merge audio and video files
        
        Args:
            video_file: Path to video file (no audio)
            audio_file: Path to audio file
            output_file: Path to output file
        
        Returns:
            bool: True if merge successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-i", str(video_file),
                "-i", str(audio_file),
                "-c:v", "copy",  # Copy video stream
                "-c:a", "aac",   # Re-encode audio to AAC
                "-map", "0:v:0", # Map video from first input
                "-map", "1:a:0", # Map audio from second input
                "-y",            # Overwrite output files
                str(output_file)
            ]
            
            logger.info(f"Merging audio and video: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify output file was created
            if output_file.exists() and output_file.stat().st_size > 0:
                logger.info(f"Audio/video merge successful: {output_file}")
                return True
            else:
                logger.error("Merged file was not created or is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg merge error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Audio/video merge failed: {str(e)}")
            return False
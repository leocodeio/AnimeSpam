import subprocess
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
import logging
import concurrent.futures
import threading
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class ClarityService:
    """Service for AI-based video frame enhancement"""
    
    def __init__(self):
        self.supported_models = {
            "test": {
                "description": "Test mode - copies frames without enhancement (for testing)",
                "scales": [1, 2],
                "requirements": []
            },
            "anime4k": {
                "description": "Fast anime upscaling using Anime4K",
                "scales": [2, 3, 4],
                "requirements": ["mpv", "anime4k"]
            },
            "esrgan": {
                "description": "High-quality anime upscaling using Real-ESRGAN (RealESRGAN_x4plus_anime_6B)",
                "scales": [4],
                "requirements": ["python3"]
            },
            "waifu2x": {
                "description": "Anime-style image upscaling",
                "scales": [2, 4],
                "requirements": ["waifu2x-ncnn-vulkan"],
                "note": "4x is achieved by chaining two 2x passes"
            }
        }
        
        current_dir = Path(__file__).parent.parent.parent.parent
        self.realesrgan_path = current_dir / "anime_upscaler_v2" / "sources" / "Real-ESRGAN"
        self.realesrgan_venv = self.realesrgan_path / ".venv" / "bin" / "python3"
    
    def check_model_availability(self, model_name: str) -> bool:
        """
        Check if a specific AI model is available
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            bool: True if model is available, False otherwise
        """
        if model_name not in self.supported_models:
            return False
        
        if model_name == "esrgan":
            return self.realesrgan_venv.exists() and self.realesrgan_path.exists()
        
        model_info = self.supported_models[model_name]
        requirements = model_info.get("requirements", [])
        
        for requirement in requirements:
            if not self._check_command_exists(requirement):
                logger.warning(f"Missing requirement for {model_name}: {requirement}")
                return False
        
        return True
    
    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            result = subprocess.run(
                ["which", command],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available AI enhancement models
        
        Returns:
            dict: Available models with their information
        """
        available = {}
        for model_name, model_info in self.supported_models.items():
            if self.check_model_availability(model_name):
                available[model_name] = model_info
        
        return available
    
    def enhance_frame_waifu2x(self, input_frame: Path, output_frame: Path, scale: int = 2) -> bool:
        """
        Enhance single frame using Waifu2x
        
        Args:
            input_frame: Path to input frame
            output_frame: Path to output frame
            scale: Upscaling factor (2 or 4; 4x is achieved by chaining two 2x passes)
            
        Returns:
            bool: True if enhancement successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_frame.parent.mkdir(parents=True, exist_ok=True)
            
            # Get model path (relative to this file's location)
            current_dir = Path(__file__).parent.parent.parent
            model_path = current_dir / "sources" / "waifu2x-ncnn-vulkan-20220728-ubuntu" / "models-cunet"
            logger.info(f"Model path: {model_path}, exists: {model_path.exists()}")
            
            # For 4x scaling, apply 2x twice
            if scale == 4:
                # Create temporary file for intermediate result
                temp_frame = output_frame.parent / f"temp_{output_frame.name}"
                
                # First pass: 2x
                cmd1 = [
                    "waifu2x-ncnn-vulkan",
                    "-i", str(input_frame),
                    "-o", str(temp_frame),
                    "-s", "2",
                    "-n", "2",
                    "-m", str(model_path),
                    "-f", "png"
                ]
                
                result1 = subprocess.run(
                    cmd1,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Second pass: 2x on the intermediate result
                cmd2 = [
                    "waifu2x-ncnn-vulkan",
                    "-i", str(temp_frame),
                    "-o", str(output_frame),
                    "-s", "2",
                    "-n", "0",
                    "-m", str(model_path),
                    "-f", "png"
                ]
                
                result2 = subprocess.run(
                    cmd2,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Clean up temporary file
                if temp_frame.exists():
                    temp_frame.unlink()
                    
            else:
                # Single pass for 2x or other scales
                cmd = [
                    "waifu2x-ncnn-vulkan",
                    "-i", str(input_frame),
                    "-o", str(output_frame),
                    "-s", str(scale),
                    "-n", "2",
                    "-m", str(model_path),
                    "-f", "png"
                ]
                
                logger.info(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            # Verify output file was created
            if output_frame.exists() and output_frame.stat().st_size > 0:
                return True
            else:
                logger.error(f"Enhanced frame was not created: {output_frame}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Waifu2x error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Frame enhancement failed: {str(e)}")
            return False
    
    def enhance_frame_esrgan(self, input_frame: Path, output_frame: Path, scale: int = 4) -> bool:
        """
        Enhance single frame using Real-ESRGAN
        
        Args:
            input_frame: Path to input frame
            output_frame: Path to output frame
            scale: Upscaling factor (only 4x supported)
            
        Returns:
            bool: True if enhancement successful, False otherwise
        """
        try:
            output_frame.parent.mkdir(parents=True, exist_ok=True)
            
            if not self.realesrgan_venv.exists():
                logger.error(f"Real-ESRGAN virtual environment not found at {self.realesrgan_venv}")
                return False
            
            inference_script = self.realesrgan_path / "inference_realesrgan.py"
            if not inference_script.exists():
                logger.error(f"Real-ESRGAN inference script not found at {inference_script}")
                return False
            
            output_frame = output_frame.resolve()
            output_dir = output_frame.parent
            
            cmd = [
                str(self.realesrgan_venv),
                str(inference_script),
                "-n", "RealESRGAN_x4plus_anime_6B",
                "-i", str(input_frame.resolve()),
                "-o", str(output_dir),
                "-s", str(scale),
                "--fp32",
                "--tile", "256"
            ]
            
            logger.info(f"Running Real-ESRGAN: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.realesrgan_path),
                timeout=60
            )
            
            logger.info(f"Real-ESRGAN stdout: {result.stdout}")
            logger.info(f"Real-ESRGAN stderr: {result.stderr}")
            logger.info(f"Real-ESRGAN return code: {result.returncode}")
            
            if result.returncode != 0:
                logger.error(f"Real-ESRGAN error: {result.stderr}")
                return False
            
            output_filename = input_frame.stem + "_out" + input_frame.suffix
            actual_output = output_dir / output_filename
            
            if actual_output.exists() and actual_output != output_frame:
                actual_output.rename(output_frame)
            
            if output_frame.exists() and output_frame.stat().st_size > 0:
                return True
            else:
                logger.error(f"Enhanced frame was not created: {output_frame}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Real-ESRGAN processing timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Real-ESRGAN error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Frame enhancement failed: {str(e)}")
            return False
    
    def _enhance_frame_test(self, input_frame: Path, output_frame: Path, scale: int = 1) -> bool:
        """
        Test mode: Simply copy frames without enhancement
        
        Args:
            input_frame: Path to input frame
            output_frame: Path to output frame
            scale: Ignored in test mode
            
        Returns:
            bool: True if copy successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_frame.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy frame without modification
            import shutil
            shutil.copy2(str(input_frame), str(output_frame))
            
            # Verify output file was created
            if output_frame.exists() and output_frame.stat().st_size > 0:
                logger.debug(f"Test mode: copied frame {input_frame} -> {output_frame}")
                return True
            else:
                logger.error(f"Test mode: failed to copy frame: {output_frame}")
                return False
                
        except Exception as e:
            logger.error(f"Test mode frame copy failed: {str(e)}")
            return False
    
    def enhance_frames_batch(
        self,
        input_dir: Path,
        output_dir: Path,
        model: str = "waifu2x",
        scale: int = 2,
        max_workers: int = 4,
        progress_callback: Optional[Callable] = None
    ) -> bool:
        """
        Enhance multiple frames in parallel
        
        Args:
            input_dir: Directory containing input frames
            output_dir: Directory to save enhanced frames
            model: AI model to use
            scale: Upscaling factor
            max_workers: Number of parallel workers
            progress_callback: Function to call with progress updates
            
        Returns:
            bool: True if all frames enhanced successfully, False otherwise
        """
        try:
            # Get list of frame files
            frame_files = sorted(list(input_dir.glob("frame_*.png")))
            if not frame_files:
                frame_files = sorted(list(input_dir.glob("frame_*.jpg")))
            
            if not frame_files:
                logger.error(f"No frame files found in {input_dir}")
                return False
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Select enhancement function
            if model == "test":
                enhance_func = self._enhance_frame_test
            elif model == "waifu2x":
                enhance_func = self.enhance_frame_waifu2x
            elif model == "esrgan":
                enhance_func = self.enhance_frame_esrgan
            else:
                logger.error(f"Unsupported model: {model}")
                return False
            
            # Process frames in parallel
            completed = 0
            failed = 0
            
            def enhance_single_frame(frame_path):
                nonlocal completed, failed
                
                output_path = output_dir / frame_path.name
                success = enhance_func(frame_path, output_path, scale)
                
                if success:
                    completed += 1
                else:
                    failed += 1
                    logger.error(f"Failed to enhance frame: {frame_path}")
                
                # Call progress callback if provided
                if progress_callback:
                    progress = (completed + failed) / len(frame_files) * 100
                    progress_callback(progress, completed, failed)
                
                return success
            
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(enhance_single_frame, frame) for frame in frame_files]
                
                # Wait for all tasks to complete
                concurrent.futures.wait(futures)
            
            logger.info(f"Frame enhancement completed: {completed} successful, {failed} failed")
            
            return failed == 0
            
        except Exception as e:
            logger.error(f"Batch frame enhancement failed: {str(e)}")
            return False
    
    def estimate_processing_time(self, frame_count: int, model: str = "waifu2x") -> float:
        """
        Estimate processing time for given number of frames
        
        Args:
            frame_count: Number of frames to process
            model: AI model to use
            
        Returns:
            float: Estimated time in seconds
        """
        # Base processing times per frame (in seconds)
        base_times = {
            "test": 0.1,
            "waifu2x": 2.0,
            "esrgan": 5.0,
            "anime4k": 0.5
        }
        
        base_time = base_times.get(model, 2.0)
        return frame_count * base_time

if ! [ -d "animeupscale" ]; then
    mkdir animeupscale
    cd animeupscale

    # Clone the Real-ESRGAN repository
    git clone https://github.com/xinntao/Real-ESRGAN.git
    cd Real-ESRGAN

    # Install Real-ESRGAN
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."

    # Install dependencies
    git clone https://github.com/xinntao/BasicSR.git
    cd BasicSR
    pip install -r requirements.txt
    python setup.py develop
    cd ..

    # pip install basicsr
    # facexlib and gfpgan are for face enhancement
    pip install facexlib
    pip install gfpgan

    # build realesrgan
    pip install -r requirements.txt
    python setup.py develop
    echo "Real-ESRGAN installation completed."

    cd ../..
fi

# Check if the virtual environment exists
if ! [ -d "animeupscale/Real-ESRGAN/.venv" ]; then
    echo "Virtual environment not found. Please run the script again."
    exit 1
fi

# Activate the virtual environment
source animeupscale/Real-ESRGAN/.venv/bin/activate

# extract frames from the video
ffmpeg -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/inputs/upload.mp4 /home/leo/Desktop/leo-ext/self/production/AnimeSpam/inputs/input_frames/upload_%04d.png

# extract the audio from the video
ffmpeg -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/inputs/upload.mp4 -q:a 0 -map a /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/audio.mp3

# upscale the frames
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/inputs/input_frames -o /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/output_frames
 
# join the frames
ffmpeg -framerate 24 -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/output_frames/upload_%04d_out.png -c:v libx264 -pix_fmt yuv420p /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/output_no_aud.mp4

# join the audio
ffmpeg -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/output_no_aud.mp4 -i /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/audio.mp3 -c:v copy -c:a aac -strict experimental -shortest /home/leo/Desktop/leo-ext/self/production/AnimeSpam/outputs/output.mp4
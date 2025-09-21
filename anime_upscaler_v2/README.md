# AnimeSpam v2

AnimeSpam v2 is a new implementation of the AnimeSpam website.

## File Structure

anime_upscaler_v2/
│── app/
│ ├── main.py # FastAPI app
│ ├── routes.py # API endpoints
│ ├── services/  
│ │ ├── audio.py # audio extraction
│ │ ├── frames.py # frame extraction + fps fix
│ │ ├── clarity.py # Anime4K / ESRGAN / Waifu2x
│ │ ├── merge.py # merge frames + audio
│ └── models/ # pretrained ML models
│── tests/
│── docs/ # PRD, TDD, API docs
│── requirements.txt
│── Dockerfile

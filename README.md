# Farmer Voice Assistant (Voice-in/out, Multilingual)

Features:
- Voice input → text (Vosk STT) → intent handling → text → voice output (gTTS)
- Multilingual via googletrans (ta/hi/te/mr/kn/bn/ml/gu/pa/en)
- Future crop price forecast (toy linear model from sample CSV)
- Crop yield prediction from soil params (RandomForest on sample CSV)
- Real-time weather (OpenWeatherMap One Call)

## Prereqs
- Python 3.10+, Node 18+, FFmpeg on PATH
- OpenWeatherMap API key
- Vosk model folder (e.g., `vosk-model-small-en-us-0.15`) downloaded from https://alphacephei.com/vosk/models

## Quick Run
1. Copy `.env.example` → `.env`, add your OpenWeather API key, set `VOSK_MODEL_PATH` to your downloaded model folder.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -U pip
   pip install -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 8000

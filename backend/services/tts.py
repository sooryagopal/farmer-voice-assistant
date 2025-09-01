import base64
from gtts import gTTS
import io

def synthesize_speech(text, lang='en'):
    """Synthesizes text into base64 encoded audio."""
    try:
        tts = gTTS(text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return base64.b64encode(fp.read()).decode('utf-8')
    except Exception as e:
        print(f"TTS error: {e}")
        return None

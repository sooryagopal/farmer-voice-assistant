import speech_recognition as sr
import io

def transcribe_audio(audio_file):
    """Transcribes an audio file into text."""
    recognizer = sr.Recognizer()
    audio_data = io.BytesIO(audio_file.read())
    try:
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
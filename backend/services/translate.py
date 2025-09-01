# File: backend/services/translate.py
# Uses googletrans-py library
from googletrans import Translator

def translate_text(text, src, dest):
    """Translates text from source to destination language."""
    try:
        translator = Translator()
        translation = translator.translate(text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
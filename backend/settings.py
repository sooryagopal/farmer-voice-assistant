import os
from dotenv import load_dotenv
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "a059a98053d92438b7aa60d78975ad41")

# File paths for data and models
CROP_PRICE_MODEL_PATH = "models/price_model.pkl"
YIELD_MODEL_PATH = "models/yield_model.pkl"

# Supported languages for translation
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    # Add more languages as needed
}
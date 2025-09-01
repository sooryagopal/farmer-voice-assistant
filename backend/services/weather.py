# File: backend/services/weather.py
# Uses OpenWeatherMap API
import requests
from settings import OPENWEATHERMAP_API_KEY

def get_weather_report(city, api_key):
    """Fetches real-time weather data for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] == 200:
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            return {
                "city": data["name"],
                "temperature": main["temp"],
                "humidity": main["humidity"],
                "description": weather_desc
            }
        else:
            return None
    except Exception as e:
        print(f"Weather API error: {e}")
        return None
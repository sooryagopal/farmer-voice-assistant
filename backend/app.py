import os
import json
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.nlu import identify_intent
from services.price_forecast import train_price_model, predict_crop_price
from services.yield_predict import train_yield_model, predict_crop_yield
from services.weather import get_weather_report
from services.stt import transcribe_audio
from services.tts import synthesize_speech
from services.translate import translate_text
from settings import OPENWEATHERMAP_API_KEY, LANGUAGES, CROP_PRICE_MODEL_PATH, YIELD_MODEL_PATH

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# --- Model Training and Loading on Application Startup ---
def initialize_models():
    """Trains and saves ML models if they don't exist, then loads them."""
    print("Initializing ML models...")
    if not os.path.exists(os.path.dirname(CROP_PRICE_MODEL_PATH)):
        os.makedirs(os.path.dirname(CROP_PRICE_MODEL_PATH))

    if not os.path.exists(CROP_PRICE_MODEL_PATH):
        print("Training new crop price prediction model...")
        train_price_model(os.path.join(os.path.dirname(__file__), 'data', 'crop_prices.csv'), CROP_PRICE_MODEL_PATH)
    else:
        print("Loading existing crop price model.")

    if not os.path.exists(YIELD_MODEL_PATH):
        print("Training new crop yield prediction model...")
        train_yield_model(os.path.join(os.path.dirname(__file__), 'data', 'soil_yield.csv'), YIELD_MODEL_PATH)
    else:
        print("Loading existing crop yield model.")
    print("Models initialized successfully.")

# Run model initialization once at startup
with app.app_context():
    initialize_models()

@app.route('/api/voice', methods=['POST'])
def handle_voice_query():
    """
    Main API endpoint to handle voice input, process it, and return a voice response.
    """
    try:
        # Check if the request contains audio data and language info
        if 'audio' not in request.files or 'language' not in request.form:
            return jsonify({'error': 'Missing audio file or language parameter'}), 400

        audio_file = request.files['audio']
        user_lang = request.form['language']
        
        print(f"Received audio from user in language: {user_lang}")

        # Step 1: Speech-to-Text (STT)
        user_text = transcribe_audio(audio_file)
        if not user_text:
            return jsonify({'error': 'Could not transcribe speech'}), 500

        print(f"Transcribed text: {user_text}")

        # Step 2: Translate user text to English for internal logic
        if user_lang != 'en':
            translated_text = translate_text(user_text, src=user_lang, dest='en')
        else:
            translated_text = user_text
        
        print(f"Translated text (English): {translated_text}")

        # Step 3: Natural Language Understanding (NLU) - Identify intent
        intent, details = identify_intent(translated_text)
        print(f"Identified intent: {intent}, with details: {details}")

        response_text = "I'm sorry, I didn't understand that. Please try again."

        # Step 4: Act on the identified intent
        if intent == 'weather_report':
            location = details.get('location', 'Erode, Tamil Nadu')
            weather_data = get_weather_report(location, OPENWEATHERMAP_API_KEY)
            if weather_data:
                response_text = f"The current weather in {weather_data['city']} is {weather_data['description']} with a temperature of {weather_data['temperature']} degrees Celsius. The humidity is {weather_data['humidity']} percent."
            else:
                response_text = f"Sorry, I couldn't fetch the weather for {location}."

        elif intent == 'crop_price_forecast':
            crop = details.get('crop', 'rice')
            # The model is trained on a single dummy crop, so we'll use a placeholder.
            predicted_price = predict_crop_price(np.array([[2025]]))
            response_text = f"Based on my analysis, the forecasted price for {crop} is approximately ${predicted_price:.2f} per kg."

        elif intent == 'crop_yield_prediction':
            crop = details.get('crop', 'rice')
            location = details.get('location', 'Erode, Tamil Nadu')
            soil_params = details.get('soil', {'N': 90, 'P': 42, 'K': 43}) # Dummy values
            # The model is trained on a single dummy dataset.
            predicted_yield = predict_crop_yield(np.array([[soil_params['N'], soil_params['P'], soil_params['K']]]))
            response_text = f"Based on the soil parameters, the predicted yield for {crop} in {location} is approximately {predicted_yield:.2f} kg per hectare."

        print(f"Generated English response: {response_text}")

        # Step 5: Translate the response back to the user's language
        if user_lang != 'en':
            final_response = translate_text(response_text, src='en', dest=user_lang)
        else:
            final_response = response_text
        
        print(f"Translated final response: {final_response}")

        # Step 6: Text-to-Speech (TTS) and return audio
        audio_data = synthesize_speech(final_response)
        
        return jsonify({
            'response_audio': audio_data, # Base64 encoded audio
            'response_text': final_response,
            'source_text': user_text
        }), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500
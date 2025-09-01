# File: backend/services/price_forecast.py
# Basic ML model for crop price forecasting
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_price_model(data_path, model_path):
    """Trains a simple linear regression model for price forecasting."""
    try:
        df = pd.read_csv(data_path)
        X = df[['Year']]
        y = df['Price']
        model = LinearRegression()
        model.fit(X, y)
        joblib.dump(model, model_path)
        print("Price model trained and saved successfully.")
    except Exception as e:
        print(f"Error training price model: {e}")

def predict_crop_price(data):
    """Loads the model and predicts crop price."""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'price_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
        
    model = joblib.load(model_path)
    return model.predict(data)[0]
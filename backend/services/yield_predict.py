# File: backend/services/yield_predict.py
# Basic ML model for crop yield prediction
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_yield_model(data_path, model_path):
    """Trains a simple Random Forest Regressor for yield prediction."""
    try:
        df = pd.read_csv(data_path)
        X = df[['N', 'P', 'K']] # Nitrogen, Phosphorus, Potassium
        y = df['Yield']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, model_path)
        print("Yield model trained and saved successfully.")
    except Exception as e:
        print(f"Error training yield model: {e}")

def predict_crop_yield(data):
    """Loads the model and predicts crop yield."""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'yield_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
        
    model = joblib.load(model_path)
    return model.predict(data)[0]
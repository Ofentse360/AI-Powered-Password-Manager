"""
ML Prediction Service for Password Strength Evaluation

Loads the trained model and service predictions
"""

import joblib
import pandas as pd
import numpy as np 
import string
from pathlib import Path


# Define path to the saved model 
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "password_strength_v1.joblib"

class PasswordStrengthModel:
    """Wrapper for the trained Random Forest Model"""
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the .joblib file. Handles errors if the model hasnt been trained 
        yet.
        """

        try:
            if MODEL_PATH.exists():
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ ML Model loaded successfully from {MODEL_PATH}")
            else:
                print(f"⚠️ Warning: ML Model not found at {MODEL_PATH}")
                print("   Run 'python -m backend.app.ml.train' to generate it.")
        except Exception as e:
            print(f"❌ Error loading ML model: {e}")

    
    def _extract_features(self, password: str):
        """
        Must match the logic in train.py EXACTLY.
        """
        features = [
            len(password),                                      # Length
            sum(c.isdigit() for c in password),                 # Digits
            sum(c.isupper() for c in password),                 # Uppercase
            sum(c.islower() for c in password),                 # Lowercase
            sum(c in string.punctuation for c in password),     # Special chars
            len(set(password))                                  # Unique chars
        ]
        # Reshape for scikit-learn (1 sample, many features)
        return np.array(features).reshape(1, -1)
    

    def predict(self, password: str) -> dict:
            """
            Predicts strength.
            Returns: {score: float (0-1), label: str}
            """
            if not self.model:
                return {"score": 0.0, "label": "Model Not Loaded", "error": True}

            # 1. Prepare data
            features = self._extract_features(password)
            
            # 2. Predict Probability (Get the confidence score)
            # returns [[prob_class_0, prob_class_1]]
            probs = self.model.predict_proba(features)[0] 
            strength_score = probs[1] # Probability of being "Strong" (Class 1)

            # 3. Determine Label
            label = "Strong" if strength_score > 0.5 else "Weak"
            
            return {
                "score": float(strength_score), # e.g., 0.85
                "label": label,                 # "Strong"
                "error": False
            }

# Export instance
password_strength_model = PasswordStrengthModel()

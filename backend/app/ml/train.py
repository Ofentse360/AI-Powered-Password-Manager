"""
ML Training Script
Generates synthetic password data and trains a Random Forest model.
"""
import joblib
import pandas as pd
import numpy as np
import string
import secrets
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

# Defines where we save the trained model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "password_strength_v1.joblib"

def extract_features(password: str):
    """
    Converts a text password into numerical features.
    """
    return [
        len(password),                                      # Total Length
        sum(c.isdigit() for c in password),                 # Count of numbers
        sum(c.isupper() for c in password),                 # Count of Uppercase
        sum(c.islower() for c in password),                 # Count of Lowercase
        sum(c in string.punctuation for c in password),     # Count of Special chars
        len(set(password))                                  # Count of Unique chars
    ]

def generate_synthetic_data(n_samples=2000):
    """
    Creates a fake dataset of 'Weak' (0) and 'Strong' (1) passwords.
    """
    data = []
    labels = []
    
    # 1. Generate WEAK passwords
    for _ in range(n_samples // 2):
        length = secrets.randbelow(5) + 4 
        pwd = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        data.append(extract_features(pwd))
        labels.append(0) # 0 = Weak
        
    # 2. Generate STRONG passwords
    for _ in range(n_samples // 2):
        length = secrets.randbelow(9) + 12
        chars = string.ascii_letters + string.digits + string.punctuation
        pwd = ''.join(secrets.choice(chars) for _ in range(length))
        data.append(extract_features(pwd))
        labels.append(1) # 1 = Strong
        
    return np.array(data), np.array(labels)

if __name__ == "__main__":
    print("🤖 Generating synthetic training data...")
    X, y = generate_synthetic_data()
    
    print("🧠 Training Random Forest model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Ensure directory exists
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the model
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Model saved to: {MODEL_PATH}")
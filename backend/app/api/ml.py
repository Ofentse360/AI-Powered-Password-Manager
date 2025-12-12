"""
Machine Learning API Endpoints
"""
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.ml.password_strength import password_strength_model

router = APIRouter()

# --- Schemas ---
class MLRequest(BaseModel):
    password: str

class MLResponse(BaseModel):
    score: float    # 0.0 to 1.0
    label: str      # "Weak" or "Strong"
    message: str

@router.post("/predict", response_model=MLResponse)
def predict_strength(request: MLRequest = Body(...)):
    """
    Analyze password using the Random Forest ML model.
    Returns a score (0-1) indicating confidence in strength.
    """
    result = password_strength_model.predict(request.password)
    
    if result.get("error"):
        return {
            "score": 0.0,
            "label": "Error",
            "message": "ML Model is not active. Please contact admin."
        }
        
    # Create a nice message for the UI
    score_pct = int(result["score"] * 100)
    if result["score"] > 0.8:
        msg = "🚀 Strong! This password is excellent."
    elif result["score"] > 0.5:
        msg = "⚠️ Moderate. It's okay, but could be better."
    else:
        msg = "❌ Weak. Our AI thinks this is easy to guess."

    return {
        "score": result["score"],
        "label": result["label"],
        "message": f"{msg} (AI Confidence: {score_pct}%)"
    }
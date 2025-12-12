"""
Password Generator API Endpoints
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.generator import password_generator

router = APIRouter()

# --- Response Schema ---
class GeneratedPassword(BaseModel):
    password: str
    length: int
    complexity_score: str # Simple label like "High", "Medium"

@router.get("/generate", response_model=GeneratedPassword)
def generate_password(
    length: int = Query(16, ge=8, le=64), # ge=GreaterOrEqual, le=LessOrEqual
    uppercase: bool = True,
    digits: bool = True,
    special: bool = True
):
    """
    Generate a cryptographically secure random password.
    Parameters can be passed in the URL (e.g., ?length=20&special=false).
    """
    # 1. Generate the password using our core utility
    pwd = password_generator.generate(
        length=length,
        use_upper=uppercase,
        use_digits=digits,
        use_special=special
    )
    
    # 2. Determine a basic complexity label for the UI
    score = "High"
    if length < 12:
        score = "Medium"
    if length < 10 or (not digits and not special):
        score = "Low"
        
    return {
        "password": pwd,
        "length": len(pwd),
        "complexity_score": score
    }
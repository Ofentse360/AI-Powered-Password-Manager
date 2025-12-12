"""
Docstring for AI-Powered-Password-Manager.backend.app.api.security

Securty Tools API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.breach_checker import breach_checker 

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.score_service import score_service

router = APIRouter()

class HealthScoreResponse(BaseModel):
    score: int
    total_passwords: int
    weak_count: int
    reused_count: int
    message: str

# Request Schema 

class PasswordCheckRequest(BaseModel):
    password: str

# Response Schema
class BreachResponse(BaseModel):
    is_breached: bool
    breach_count: int
    message: str

@router.post("/check-password", reponse_model=BreachResponse)
async def check_password_breach(
    request: PasswordCheckRequest = Body(...)
):
    
    """Check If password exists in breach databases
    Uses K-Anonymity for pravacy (never send full password)
    """
    
# Verify against HIBP
    count = await breach_checker.check_password_breach(request.password)
    
    if count > 0:
        return {
            "is_breached": True,
            "breach_count": count,
            "message": f"⚠️ This password has appeared in {count} known data breaches. Do not use it!"
        }

    return {
        "is_breached": False,
        "breach_count": 0,
        "message": "✅ This password was NOT found in known data breaches."}


@router.get("/score", response_model=HealthScoreResponse)
def get_vault_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Requires Login!
):
    """
    Calculate the current health score of the user's password vault.
    Checks for password reuse and weak passwords.
    """
    return score_service.calculate_health_score(db=db, user_id=current_user.id)
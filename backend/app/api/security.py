"""
Docstring for AI-Powered-Password-Manager.backend.app.api.security

Securty Tools API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel

from app.services.breach_checker import breach_checker 

router = APIRouter()

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

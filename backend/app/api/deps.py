"""
API Dependencies (The "Bouncer")
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database.session import get_db
from app.core.jwt import decode_access_token
from app.services.user_service import user_service
from app.models.user import User
from app.config import settings

# 1. The OAuth2 Scheme
# This tells FastAPI that the token is sent in the Authorization header:
# "Authorization: Bearer <token>"
# The "tokenUrl" parameter points to our login endpoint so the Docs UI knows where to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Validates the token and retrieves the current logged-in user.
    If anything is wrong (expired token, fake user), it throws an error.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 2. Decode the Token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
        
    # 3. Get the User from DB
    user = user_service.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
        
    return user
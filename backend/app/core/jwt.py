"""
JWT Token handling utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT access token.
    
    Args:
        data: The dictionary of data to encode in the token (e.g., user_id).
        expires_delta: How long until the token expires.
        
    Returns:
        A string containing the encoded JWT.
    """
    # 1. Make a copy so we don't mutate the original input
    to_encode = data.copy()
    
    # 2. Calculate expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to the setting in config.py (usually 30 mins)
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 3. Add expiration claim ('exp') to the payload
    to_encode.update({"exp": expire})
    
    # 4. Encode the token using our Secret Key and Algorithm (HS256)
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodes and validates a JWT token.
    Returns the payload dictionary if valid, None if expired/invalid.
    Handles:
    - Expired tokens
    - Invalid signatures
    - Malformed tokens
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
        return None
    except jwt.JWTClaimsError:
        print("❌ Invalid token claims")
        return None
    except JWTError as e:
        print(f"❌ Invalid token: {e}")
        return None
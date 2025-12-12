"""
Pydantic schemas for authentication
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# --- 1. User Registration Request Body (Input) ---
class UserRegister(BaseModel):
    """
    Schema for a new user registration request.
    """
    # Ensures the username is between 3 and 50 characters
    username: str = Field(..., min_length=3, max_length=50)
    
    # EmailStr enforces valid email format
    email: EmailStr
    
    # Master password field (will be hashed immediately)
    master_password: str = Field(..., min_length=12, max_length=100)



# --- 2. User Login Request Body (Input) ---
class UserLogin(BaseModel):
    """
    Schema for user login request (uses username or email).
    """
    username: str
    master_password: str


# --- 3. Token Data (Output/Internal) ---
class Token(BaseModel):
    """
    Schema for the response after successful login.
    """
    access_token: str
    token_type: str = "bearer"

# --- 4. Token Payload Data (Internal) ---
class TokenData(BaseModel):
    """
    Schema for the data stored inside the JWT token (payload).
    """
    user_id: Optional[int] = None
    username: Optional[str] = None


# --- 5. User Response Schema (Output) ---
class UserResponse(BaseModel):
    """
    Schema for sending user data back to the client.
    Crucially, this excludes the password!
    """
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        # This tells Pydantic to read the data even if it's not a dict,
        # but a SQLAlchemy model (which is what our DB returns).
        from_attributes = True
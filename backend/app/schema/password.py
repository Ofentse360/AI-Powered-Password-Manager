"""
Pydantic schemas for password entries
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# --- 1. Shared Properties ---
# These are fields common to creating, reading, and updating.
class PasswordBase(BaseModel):
    service: str            # e.g., "Netflix"
    username: str           # e.g., "my_email@gmail.com"
    category: Optional[str] = None

# --- 2. Request Schema (Input) ---
# What the user sends when creating a new entry.
class PasswordCreate(PasswordBase):
    password: str           # The PLAIN TEXT password to be encrypted

# --- 3. Request Schema (Update) ---
# What the user sends when editing (all optional).
class PasswordUpdate(BaseModel):
    service: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None # User might want to change the password
    category: Optional[str] = None

# --- 4. Response Schema (Output) ---
# What we send back to the user.
class PasswordResponse(PasswordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    # We include a field for the decrypted password, but it's optional.
    # In a list view, we might leave this None for security (shoulder surfing).
    password: Optional[str] = None 

    class Config:
        from_attributes = True
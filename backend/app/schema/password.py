"""
Pydantic schemas for password entries
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# --- 1. Shared Properties ---
# These are fields common to creating, reading, and updating.
class PasswordBase(BaseModel):
    service: str = Field(..., min_length=1, max_length=100)      # e.g., "Netflix"
    username: str = Field(..., min_length=1, max_length=255)     # e.g., "my_email@gmail.com"
    category: Optional[str] = Field(None, max_length=50)         # e.g., "Social", "Work"

# --- 2. Request Schema (Input) ---
# What the user sends when creating a new entry.
class PasswordCreate(PasswordBase):
    password: str = Field(..., min_length=1, max_length=1000)    # The PLAIN TEXT password to be encrypted

# --- 3. Request Schema (Update) ---
# What the user sends when editing (all optional).
class PasswordUpdate(BaseModel):
    service: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=1, max_length=1000)  # User might want to change the password
    category: Optional[str] = Field(None, max_length=50)

# --- 4. Response Schema (List View) ---
# What we send back when listing passwords - EXCLUDES decrypted password for security
class PasswordListResponse(PasswordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- 5. Response Schema (Detail View) ---
# What we send back when viewing a single password - INCLUDES decrypted password
class PasswordResponse(PasswordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    # Include a field for the decrypted password (only in detail view)
    password: Optional[str] = None 

    class Config:
        from_attributes = True
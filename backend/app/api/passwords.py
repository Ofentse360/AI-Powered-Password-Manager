"""
Password Management API Endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schema.password import PasswordCreate, PasswordUpdate, PasswordResponse
from app.services.password_service import password_service
from app.api.deps import get_current_user # Import the Bouncer!
from app.core.security import encryption_manager

router = APIRouter()

# --- 1. Create a Password ---
@router.post("/", response_model=PasswordResponse, status_code=status.HTTP_201_CREATED)
def create_password(
    password_in: PasswordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Require login
):
    """
    Store a new encrypted password.
    """
    return password_service.create_password(
        db=db, 
        password_in=password_in, 
        user_id=current_user.id
    )

# --- 2. List All Passwords ---
@router.get("/", response_model=List[PasswordResponse])
def read_passwords(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all password entries for the current user.
    NOTE: This does NOT return the decrypted password field for security.
    """
    return password_service.get_passwords(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit
    )

# --- 3. Get One Password (Decrypted) ---
@router.get("/{password_id}", response_model=PasswordResponse)
def read_password(
    password_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific password entry.
    CRITICAL: This decrypts the password and sends it to the user.
    """
    password_entry = password_service.get_password(
        db=db, 
        password_id=password_id, 
        user_id=current_user.id
    )
    
    if not password_entry:
        raise HTTPException(status_code=404, detail="Password entry not found")
        
    # Decrypt specifically for this "View" action
    decrypted_pass = encryption_manager.decrypt(password_entry.encrypted_password)
    
    # Attach it to the response object (Pydantic will pick it up)
    password_entry.password = decrypted_pass
    
    return password_entry

# --- 4. Update Password ---
@router.put("/{password_id}", response_model=PasswordResponse)
def update_password(
    password_id: int,
    password_in: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a password entry.
    """
    password_entry = password_service.get_password(
        db=db, 
        password_id=password_id, 
        user_id=current_user.id
    )
    
    if not password_entry:
        raise HTTPException(status_code=404, detail="Password entry not found")
        
    return password_service.update_password(
        db=db, 
        db_password=password_entry, 
        password_in=password_in
    )

# --- 5. Delete Password ---
@router.delete("/{password_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_password(
    password_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a password entry.
    """
    success = password_service.delete_password(
        db=db, 
        password_id=password_id, 
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Password entry not found")
        
    return None
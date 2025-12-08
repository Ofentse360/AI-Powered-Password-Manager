"""
Authentication API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Import our system components
from app.database.session import get_db
from app.services.user_service import user_service
from app.schemas.auth import UserRegister, UserResponse

# Create the router (like a mini-app for auth routes)
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    1. Checks if email is already taken.
    2. Checks if username is already taken.
    3. Creates the user securely.
    """
    
    # 1. Check for duplicate email
    user_email = user_service.get_user_by_email(db, email=user_in.email)
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Check for duplicate username
    user_username = user_service.get_user_by_username(db, username=user_in.username)
    if user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
        
    # 3. Create the user
    new_user = user_service.create_user(db=db, user_in=user_in)
    
    return new_user
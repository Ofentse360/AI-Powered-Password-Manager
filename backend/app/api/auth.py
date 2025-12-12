"""
Authentication API Endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

# Import our system components
from app.database.session import get_db
from app.services.user_services import user_service
from app.core.jwt import create_access_token
from app.schema.auth import UserRegister, UserResponse, Token
from app.config import settings
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



@router.post("/token",response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    1. Verify username and password.
    2. Create JWT token with expiration.
    3. Return token and token type.
    """
    
    # 1. Authenticate user
    user = user_service.authenticate_user(
        db, 
        username=form_data.username, 
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    # 3. Return the token
    return {"access_token": access_token, "token_type": "bearer"}

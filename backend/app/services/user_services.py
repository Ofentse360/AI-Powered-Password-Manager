"""
User services - Business logic for user management
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.auth import UserRegister
from app.core.hashing import hasher

class UserService:
    """Services class for managing CRUD operations """
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Fetch a user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(db: Session, username: str):
        """Fetch a user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user_in: UserRegister):
        """
        Create a new user in the database.
        
        1. Hashes the master password using Bcrypt.
        2. Creates the User database object.
        3. Saves it to the database.
        """
        # 1. Hash the password using our security utility
        hashed_password = hasher.get_password_hash(user_in.master_password)
        
        # 2. Create the User model instance
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password
            # is_active and is_superuser default to standard values defined in the Model
        )
        
        # 3. Add to the session and commit (save)
        db.add(db_user)
        db.commit()
        
        # Refresh to get the ID and default values (like created_at) from the DB
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, master_password: str):
        """
        Authenticate a user by username and master password.
        
        Returns the User object if authentication is successful, else None.
        """
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not hasher.verify_master_password(master_password):
            return None
        return user
"""
Password Service - Business logic for password management
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.password_entry import PasswordEntry
from app.schema.password import PasswordCreate, PasswordUpdate
from app.core.security import encryption_manager

class PasswordService:
    """
    Service class for managing password entries (CRUD).
    Handles transparent encryption and decryption with error handling.
    """

    @staticmethod
    def get_password(db: Session, password_id: int, user_id: int) -> Optional[PasswordEntry]:
        """
        Fetch a single password entry by ID.
        Ensures the entry belongs to the requesting user.
        
        NOTE: This returns the raw DB entry (encrypted). 
        Decryption happens explicitly when needed.
        """
        return db.query(PasswordEntry).filter(
            PasswordEntry.id == password_id,
            PasswordEntry.user_id == user_id
        ).first()

    @staticmethod
    def decrypt_password(encrypted_password: str) -> Optional[str]:
        """
        Safely decrypt a password with error handling.
        Returns None if decryption fails (corrupted data or wrong key).
        """
        try:
            return encryption_manager.decrypt(encrypted_password)
        except Exception as e:
            print(f"❌ Decryption error: {e}")
            return None

    @staticmethod
    def get_passwords(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[PasswordEntry]:
        """
        Fetch all password entries for a user.
        Returns encrypted data - decryption happens in API layer if needed.
        """
        return db.query(PasswordEntry).filter(
            PasswordEntry.user_id == user_id
        ).offset(skip).limit(limit).all()

    @staticmethod
    def create_password(db: Session, password_in: PasswordCreate, user_id: int) -> PasswordEntry:
        """
        Create a new password entry.
        
        CRITICAL: Encrypts the plain text password before saving.
        Raises Exception if encryption or DB save fails.
        """
        try:
            # 1. Encrypt the plain text password
            encrypted_blob = encryption_manager.encrypt(password_in.password)
            
            # 2. Create the database model
            db_password = PasswordEntry(
                service=password_in.service,
                username=password_in.username,
                category=password_in.category,
                encrypted_password=encrypted_blob, # Store ciphertext
                user_id=user_id # Link to the logged-in user
            )
            
            # 3. Save to DB
            db.add(db_password)
            db.commit()
            db.refresh(db_password)
            
            # 4. Attach the plain password temporarily so the response schema can see it
            # (This acts like a virtual property for the immediate response)
            db_password.password = password_in.password
            
            return db_password
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create password entry: {str(e)}")

    @staticmethod
    def update_password(
        db: Session, 
        db_password: PasswordEntry, 
        password_in: PasswordUpdate
    ) -> PasswordEntry:
        """
        Update a password entry with error handling.
        """
        try:
            # Convert schema to dict, excluding fields that weren't sent
            update_data = password_in.model_dump(exclude_unset=True)
            
            # Special handling if the user is changing the password
            if "password" in update_data:
                # Encrypt the NEW password
                encrypted_blob = encryption_manager.encrypt(update_data["password"])
                # Update the specific DB field
                db_password.encrypted_password = encrypted_blob
                # Remove 'password' from update_data so we don't try to save it to a non-existent column
                del update_data["password"]
                
            # Update other fields (service, username, etc.)
            for field, value in update_data.items():
                if value is not None:
                    setattr(db_password, field, value)
                
            db.add(db_password)
            db.commit()
            db.refresh(db_password)
            
            return db_password
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update password entry: {str(e)}")
    
    @staticmethod
    def delete_password(db: Session, password_id: int, user_id: int) -> bool:
        """
        Delete a password entry.
        Returns True if deletion successful, False if entry not found.
        """
        try:
            password_entry = db.query(PasswordEntry).filter(
                PasswordEntry.id == password_id,
                PasswordEntry.user_id == user_id
            ).first()
            
            if not password_entry:
                return False
            
            db.delete(password_entry)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"❌ Error deleting password: {e}")
            return False


# Export instance
password_service = PasswordService()
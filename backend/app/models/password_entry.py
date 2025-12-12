"""Database model for password entries.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Import Base From Session 
from app.database.session import Base

class PasswordEntry(Base):
    """SQLAlchemy model for password entries. Strores ecnrypted data"""
    __tablename__ = "password_entries"

    # 1. Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # 2. Descriptive fields
    service = Column(String, nullable=False)        # e.g., "Netflix", "Gmail"
    username = Column(String, nullable=False)       # The username for that service (e.g., "my@email.com")
    
    # 3. The Secret (Encrypted)
    # This stores the huge gibberish string returned by Fernet
    encrypted_password = Column(String, nullable=False) 
    
    # Optional category (e.g., "Social", "Work")
    category = Column(String, nullable=True)

    # 4. Link to the User (The Foreign Key)
    # This says: "This entry belongs to the user with this ID"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 5. Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"<PasswordEntry(service={self.service}, username={self.username}, user_id={self.user_id})>"
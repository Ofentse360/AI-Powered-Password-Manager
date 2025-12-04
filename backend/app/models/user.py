"""
Docstring for AI-Powered-Password-Manager.backend.app.models.user
User model definitions and database interactions
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlachemy.orm import relationship

from app.database.session import Base

from app.core.hashing import hasher


class User(Base):
    """User model representing a registered user in the system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True,index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Securtiy Fieds
    # NOTE: This is the hashed master password
    hashed_master_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    passwords = relationship("PasswordEntry", back_populates="owner")


    def verify_master_password(self, master_password: str) -> bool:
        """
        Verifies the provided master password against the stored hash
        """

        return hasher.verify_password(master_password, self.hashed_master_password)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
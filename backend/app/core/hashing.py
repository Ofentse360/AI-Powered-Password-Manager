"""
Core hashing utilities - Master password hashing with bcrypt
"""
from passlib.context import CryptContext

# Define the hashing context for Bcrypt
# Schemes tells passlib which algorithms to use. We use bcrypt as it's strong.
# deprecated='auto' will automatically manage deprecated hash formats.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    """Handles hashing and verification of plain text passwords."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain text password against a stored hashed password.
        
        Args:
            plain_password: The password provided by the user (e.g., during login).
            hashed_password: The hashed password stored in the database.
        
        Returns:
            True if the password matches the hash, False otherwise.
        """
        # Bcrypt is designed to handle this comparison securely
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generates a secure hash for a plain text password.
        
        Args:
            password: The password to hash (e.g., the Master Password during registration).
            
        Returns:
            The securely generated hash string.
        """
        return pwd_context.hash(password)

# Export the instance for easy import in other modules
hasher = Hasher()



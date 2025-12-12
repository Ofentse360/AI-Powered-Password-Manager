"""
Application Configuration
Loads environment variables from the .env file.
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "AI Password Manager"
    APP_VERSION: str = "0.1.0"
    
    # Database
    # Default to local SQLite if not set
    DATABASE_URL: str = "sqlite:///./data/passwords.db"
    
    # Security - Encryption (Fernet)
    # This MUST be a valid base64 key (generate with fernet.generate_key())
    ENCRYPTION_KEY: str
    
    # Security - JWT (Login)
    # This acts as the salt for hashing tokens
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Pydantic Configuration
    class Config:
        # Tells Pydantic to read the .env file in the root directory
        # We go up two levels: app -> backend -> root
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Create the global settings object
settings = Settings()
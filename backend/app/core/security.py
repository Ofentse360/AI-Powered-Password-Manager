"""
Core security utilities - encryption and decryption
"""

from cryptography.fernet import Fernet
from app.config import settings


class EncryptionManager:
    """Handles AES-256 encryption/decryption using Fernet"""
    
    def __init__(self):
        # NOTE: This key is loaded from the .env file via app.config.settings
        self.key = settings.ENCRYPTION_KEY.encode()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()
    
    # ... (generate_key static method)
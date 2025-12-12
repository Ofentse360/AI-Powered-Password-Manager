"""
Password Generator Utility
Uses cryptographically secure random number generation.
"""
import string
import secrets

class PasswordGenerator:
    """
    Generates strong, random passwords with customizable complexity.
    """
    
    @staticmethod
    def generate(
        length: int = 16, 
        use_upper: bool = True, 
        use_digits: bool = True, 
        use_special: bool = True
    ) -> str:
        """
        Create a random password.
        
        Args:
            length: Total length of password (min 8).
            use_upper: Include uppercase letters (A-Z).
            use_digits: Include numbers (0-9).
            use_special: Include symbols (!@#$).
            
        Returns:
            A string containing the generated password.
        """
        # 1. Define the base character set (always include lowercase)
        chars = string.ascii_lowercase
        
        # 2. Add other character sets based on flags
        if use_upper:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            # We select a safe subset of punctuation that usually works on all websites
            chars += "!@#$%^&*()-_=+"

        # 3. Ensure length is safe
        if length < 8:
            length = 8
            
        # 4. Generate the password using 'secrets' (Secure!)
        # secrets.choice() is better than random.choice() for security
        return "".join(secrets.choice(chars) for _ in range(length))

# Export instance
password_generator = PasswordGenerator()
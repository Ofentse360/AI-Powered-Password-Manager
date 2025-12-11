"""
Breach Checker Service (Pwned Integratin)
Uses K-Anonymity model to securely check passwords.

"""

import hashlib
import httpx
import logging 

#Logger is configured to use what is happening
logger = logging.getLogger(__name__)

class BreachChecker:
    """Service to check credentials against public breach databases using K-Anonymity."""
    HIBP_PASSWORD_API =  "https://api.pwnedpasswords.com/range/"

    @staticmethod
    def _sha1_hash(password: str) -> str:
        """Helper to get SHA-1 hash of a string (uppercase)."""
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest()
        return sha1.upper()

    
    async def check_password_breach(self, password: str) -> int:
        """Check if a password has been breached using HIBP API.
        Returns the Number of Times it has been seen"""

        #1. Hash the Password
        full_hash = self._sha1_hash(password)

        #2. Split: First 5 chars (prefix) and the rest (suffix)
        prefix = full_hash[:5]
        suffix = full_hash[5:]

        #3. Query the HIBP API with the prefix
        url = f"{self.HIBP_PASSWORD_API}{prefix}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()

                #4. Process the response (list of suffixes)
                # The API retirns lines like: "SUFFIX:COUNT" "1E4C9"
                hashes = (line.split(":") for line in response.text.splitlines())

                #5. Check if our suffix is in the returned list

                for h_suffix, count in hashes:
                    if  h_suffix == suffix:
                        logger.warning(f"Password found in breach database {count} times.")
                        return int(count)  
            
            return 0 # Not found

        except httpx.RequestError as e:
            logger.error(f"Network error checking breach API: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error in breach checker: {e}")
            return 0
        
# Export Instance
breach_checker = BreachChecker()
 


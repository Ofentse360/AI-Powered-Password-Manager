"""
Security Score Service
Analyzes the user's vault to calculate a health score.
"""
from sqlalchemy.orm import Session
from collections import Counter

from app.models.password_entry import PasswordEntry
from app.core.security import encryption_manager

class ScoreService:
    """
    Logic for calculating vault health.
    """
    
    @staticmethod
    def calculate_health_score(db: Session, user_id: int) -> dict:
        """
        Analyze all passwords for a user and return detailed stats.
        """
        # 1. Fetch all passwords for the user
        entries = db.query(PasswordEntry).filter(PasswordEntry.user_id == user_id).all()
        
        total_passwords = len(entries)
        if total_passwords == 0:
            return {
                "score": 0,
                "total_passwords": 0,
                "weak_count": 0,
                "reused_count": 0,
                "message": "Vault is empty."
            }
            
        # 2. Decrypt and Analyze (In Memory)
        plain_passwords = []
        weak_count = 0
        
        for entry in entries:
            try:
                # Decrypt
                plain = encryption_manager.decrypt(entry.encrypted_password)
                plain_passwords.append(plain)
                
                # Simple strength check (Phase 4 rules)
                # (In Phase 5, we will replace this with the ML model!)
                if len(plain) < 10:
                    weak_count += 1
            except Exception:
                # If decryption fails for some reason, skip
                continue
                
        # 3. Check for Reuse
        # Counter creates a map: {'pass123': 2, 'secure': 1}
        counts = Counter(plain_passwords)
        reused_passwords = [pwd for pwd, count in counts.items() if count > 1]
        reused_count = len(reused_passwords)
        
        # 4. Calculate Score (Start at 100, deduct penalties)
        score = 100
        
        # Penalty: 10 points for every reused password (capped at 50)
        reuse_penalty = min(reused_count * 10, 50)
        score -= reuse_penalty
        
        # Penalty: 5 points for every weak password (capped at 50)
        weak_penalty = min(weak_count * 5, 50)
        score -= weak_penalty
        
        # Determine Message
        if score >= 80:
            msg = "Excellent! Your vault is very secure."
        elif score >= 50:
            msg = "Good, but you have some weak or reused passwords."
        else:
            msg = "Critical! High risk of reused or weak passwords."
            
        return {
            "score": score,
            "total_passwords": total_passwords,
            "weak_count": weak_count,
            "reused_count": reused_count,
            "message": msg
        }

# Export instance
score_service = ScoreService()
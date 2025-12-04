"""
Database initialization module.
"""

from app.database.session import Base, engine
from app.models import User # all models are imported

def init_database():
    """Create all database tables defined in the app."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database successfully initialized with all tables.")
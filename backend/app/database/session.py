"""
Docstring for AI-Powered-Password-Manager.backend.app.database.session

Database session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 1. Define connection arguments safely
# PostgreSQL crashes if it sees "check_same_thread", so we only add it for SQLite.
connect_args = {}

if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}

# 2. Create the SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args  # Uses the variable we just defined
)

# 3. Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for declarative models
Base = declarative_base()

# 5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
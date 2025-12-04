"""
Docstring for AI-Powered-Password-Manager.backend.app.database.session

Database session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 1. Create the SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 2. Create Session Factory
SessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base class for declarative models
Base = declarative_base()

#4. Dependency to get DB session
def get_db():
    """Yields a database session for use in request handling."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
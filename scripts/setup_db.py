"""
Database initialization script
"""
import sys
import os
from pathlib import Path

# Get the path to the current file (scripts/setup_db.py)
current_file = Path(__file__).resolve()

# Get the project root (the parent of 'scripts')
project_root = current_file.parent.parent

# Define the backend path
backend_path = project_root / "backend"

# Add it to the system path so imports work
sys.path.insert(0, str(backend_path))
# ------------------------

# Now we can import from 'app' as if we were inside the backend folder
from backend.app.database.init_db import init_database

def main():
    """Initialize the database"""
    print("🔧 Initializing database...")
    
    # Create the 'data' directory if it doesn't exist yet
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    try:
        init_database()
        print("✅ Database initialized successfully!")
        print(f"📍 Location: {data_dir / 'passwords.db'}")
    except Exception as e:
        print(f"❌ Error creating database: {e}")

if __name__ == "__main__":
    main()
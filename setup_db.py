import os
import sqlite3
from pathlib import Path
from config import Config

def setup_database():
    """
    Setup SQLite database - much simpler than MySQL setup!
    With SQLite, the database file is created automatically when first accessed,
    so we just need to make sure the directory exists.
    """
    # Get the database path from config
    db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Connect to create the file if it doesn't exist
    try:
        # Extract just the file path from the URI
        if os.path.isabs(db_path):
            # Absolute path
            file_path = db_path
        else:
            # Relative path - make it absolute
            base_dir = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(base_dir, db_path)
        
        conn = sqlite3.connect(file_path)
        conn.close()
        print(f"SQLite database initialized at: {file_path}")
        return True
    except Exception as e:
        print(f"Error setting up SQLite database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database() 
import pymysql
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

def setup_database():
    # Extract database info from DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url or 'mysql+pymysql://' not in db_url:
        print("Error: DATABASE_URL environment variable not set or not in the correct format.")
        print("Expected format: mysql+pymysql://username:password@host/database_name")
        return False
    
    # Parse the URL - handle query parameters
    db_info = db_url.replace('mysql+pymysql://', '')
    
    # Split at @ to separate auth from host
    auth_part, rest = db_info.split('@', 1)
    
    # Extract username and password
    username, password = auth_part.split(':', 1)
    
    # Handle host and database name, accounting for query parameters
    host_db_part = rest.split('/', 1)
    host = host_db_part[0]
    
    # Extract database name, removing any query parameters
    db_with_params = host_db_part[1]
    db_name = db_with_params.split('?')[0]
    
    try:
        # Connect to MySQL server (without specifying a database)
        conn = pymysql.connect(
            host=host,
            user=username,
            password=password,
            # Add auth_plugin parameter to handle MySQL 8+ authentication
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
        )
        
        cursor = conn.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database() 
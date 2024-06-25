import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(r'.env')

# Retrieve database connection details from environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Construct the database URI using environment variables
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    
    # Disable SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """Configuration class for testing."""
    TESTING = True
    
    # Use the same database URI as the base config; modify if a different testing database is needed
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    
    # Disable CSRF protection in forms during testing
    WTF_CSRF_ENABLED = False

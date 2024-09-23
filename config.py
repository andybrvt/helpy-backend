# config.py
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

#load from .env
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # If not found in the .env, use a default value
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Same here, default to 'HS256' if not set

# JWT expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Example: 30 minutes

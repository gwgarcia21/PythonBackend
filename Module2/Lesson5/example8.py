# .env file (DO NOT COMMIT THIS TO GIT)
# DATABASE_URL="postgresql://user:password@host:port/dbname"
# SECRET_KEY="your-production-secret-key-that-is-long-and-random"

# main.py
import os
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv() # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-secret") # Fallback for dev, but not prod
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

print(f"Loaded SECRET_KEY (first 5 chars): {SECRET_KEY[:5]}...")
print(f"Loaded DATABASE_URL: {DATABASE_URL}")
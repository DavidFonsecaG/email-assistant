import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if not value:
        print(f"Missing required environment variable: {key}")
        sys.exit(1)
    return value
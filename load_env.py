import os
import sys
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("Error: .env file not found.")
        print("Please run setup_api_keys.py first to create the .env file.")
        return 1
    
    # Load variables from .env file
    with open(env_file, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    
    # Print loaded variables (masked for security)
    print("Loaded environment variables:")
    for key, value in os.environ.items():
        if key in ["WEATHER_API_KEY", "NEWS_API_KEY", "HUGGINGFACE_API_KEY"]:
            masked_value = f"{value[:5]}...{value[-5:]}" if len(value) > 10 else "***"
            print(f"{key}={masked_value}")
    
    return 0

if __name__ == "__main__":
    sys.exit(load_env()) 
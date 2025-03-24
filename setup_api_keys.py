import os
import sys
import json
from pathlib import Path

def setup_api_keys():
    """Set up API keys for the assistant"""
    print("===== API KEY SETUP =====")
    print("This script will help you set up the API keys needed for the assistant.")
    print("The keys will be saved to a .env file in the project directory.")
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    env_vars = {}
    
    if env_file.exists():
        print("Found existing .env file. Loading current values...")
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value
    
    # Weather API key
    print("\n----- OpenWeatherMap API Key -----")
    print("This is used for weather information.")
    print("You can get a free API key at: https://openweathermap.org/api")
    
    weather_api_key = env_vars.get("WEATHER_API_KEY", "")
    if weather_api_key:
        print(f"Current value: {weather_api_key[:5]}...{weather_api_key[-5:]}")
        change = input("Do you want to change it? (y/n): ").lower() == "y"
    else:
        change = True
    
    if change:
        weather_api_key = input("Enter your OpenWeatherMap API key: ").strip()
        env_vars["WEATHER_API_KEY"] = weather_api_key
    
    # News API key
    print("\n----- NewsAPI Key -----")
    print("This is used for fetching news headlines.")
    print("You can get a free API key at: https://newsapi.org/")
    
    news_api_key = env_vars.get("NEWS_API_KEY", "")
    if news_api_key:
        print(f"Current value: {news_api_key[:5]}...{news_api_key[-5:]}")
        change = input("Do you want to change it? (y/n): ").lower() == "y"
    else:
        change = True
    
    if change:
        news_api_key = input("Enter your NewsAPI key: ").strip()
        env_vars["NEWS_API_KEY"] = news_api_key
    
    # HuggingFace API key (from config.py)
    print("\n----- HuggingFace API Key -----")
    print("This is used for advanced NLP features.")
    print("You can get a free API key at: https://huggingface.co/")
    
    # Try to read from config.py
    huggingface_api_key = ""
    try:
        from config import HUGGINGFACE_API_KEY
        huggingface_api_key = HUGGINGFACE_API_KEY
    except:
        pass
    
    if not huggingface_api_key:
        huggingface_api_key = env_vars.get("HUGGINGFACE_API_KEY", "")
    
    if huggingface_api_key:
        print(f"Current value: {huggingface_api_key[:5]}...{huggingface_api_key[-5:]}")
        change = input("Do you want to change it? (y/n): ").lower() == "y"
    else:
        change = True
    
    if change:
        huggingface_api_key = input("Enter your HuggingFace API key: ").strip()
        env_vars["HUGGINGFACE_API_KEY"] = huggingface_api_key
    
    # Save to .env file
    print("\nSaving API keys to .env file...")
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("API keys saved successfully!")
    print("\nTo use these keys in your current terminal session, run:")
    print("On Windows (PowerShell):")
    for key, value in env_vars.items():
        print(f"$env:{key} = \"{value}\"")
    
    print("\nOn Windows (Command Prompt):")
    for key, value in env_vars.items():
        print(f"set {key}={value}")
    
    print("\nOn Linux/Mac:")
    for key, value in env_vars.items():
        print(f"export {key}={value}")
    
    return 0

if __name__ == "__main__":
    sys.exit(setup_api_keys()) 
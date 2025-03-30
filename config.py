"""
Configuration module for the Travel Planner application.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required API keys
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "SERPER_API_KEY",
    "WEATHER_API_KEY",
    "AMADEUS_API_KEY",
    "AMADEUS_API_SECRET"
]

# Check if all required environment variables are set
def check_env_vars():
    """
    Check if all required environment variables are set.
    
    Returns:
        tuple: (bool, list) - Success status and list of missing variables
    """
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    return len(missing_vars) == 0, missing_vars

# Set environment variables for libraries
def setup_env():
    """
    Set up environment variables for various libraries.
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    success, missing_vars = check_env_vars()
    
    if not success:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    
    # Set up OpenAI API key for llama_index
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    return True

# Application settings
APP_SETTINGS = {
    "title": "AI Travel Planner",
    "description": "Let AI research and plan your next trip!",
    "theme": "soft",  # Gradio theme
    "share": True,    # Whether to create a public link
}
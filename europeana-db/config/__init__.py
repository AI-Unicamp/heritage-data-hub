import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
EUROPEANA_API_KEY = os.getenv("API_KEY")

if not EUROPEANA_API_KEY:
    raise EnvironmentError("API key not found. Make sure it is set in the .env file.")

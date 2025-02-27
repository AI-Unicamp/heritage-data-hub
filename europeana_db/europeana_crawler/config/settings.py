import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# ✅ API Key (stored in an environment variable)
EUROPEANA_API_KEY = os.getenv("EUROPEANA_API_KEY")

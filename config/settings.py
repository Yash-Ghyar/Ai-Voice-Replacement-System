import os
from dotenv import load_dotenv

# Load environment variables from api.env if present
load_dotenv("api.env")

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "YOUR_API_KEY_HERE")

# Folder paths
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "assets/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

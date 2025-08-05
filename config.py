import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

# Required Config
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Optional Config
MONGO_URL = os.getenv("MONGO_URL")  # For user DB

# Download directory
DOWNLOAD_DIR = "downloads"

# Aria2 RPC config
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "madara123")  # Can override in .env
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", 6800))

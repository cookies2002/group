import os
from dotenv import load_dotenv

load_dotenv()  # Load values from .env file

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URL = os.getenv("MONGO_URL")

# Directory where files will be downloaded
DOWNLOAD_DIR = "downloads"

# Aria2 RPC settings
ARIA2_SECRET = "madara123"  # You can move this to .env if you prefer
ARIA2_HOST = "http://localhost"
ARIA2_PORT = 6800  # ✅ Make sure this matches with your aria2 daemon

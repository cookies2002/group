import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Telegram Bot Credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# MongoDB
MONGO_URL = os.getenv("MONGO_URL")

# Aria2c RPC Configuration
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", 6800))
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "madara123")

# File Directory
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

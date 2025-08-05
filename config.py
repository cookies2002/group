import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

MONGO_URL = os.getenv("MONGO_URL")  # MongoDB connection string

# Aria2 Configuration
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", "6800"))
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "madara123")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")

import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URL = os.getenv("MONGO_URL")

DOWNLOAD_DIR = "downloads"
ARIA2_SECRET = "madara123"
ARIA2_HOST = "http://localhost"
ARIA2_PORT = 6800  # ✅ Fix: Correct variable name

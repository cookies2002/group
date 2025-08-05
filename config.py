# config.py

import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

MONGO_URL = os.getenv("MONGO_URL")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "madara123")
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", "6800"))
MAX_TASKS_PER_USER = int(os.getenv("MAX_TASKS_PER_USER", 3))

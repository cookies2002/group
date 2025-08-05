import os
import asyncio
import time
import shutil
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, Document
from aria2p import API, Client as Aria2Client
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_URL,
    DOWNLOAD_DIR, ARIA2_SECRET, ARIA2_HOST, ARIA2_PORT
)

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

# Setup
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
aria2_client = Aria2Client(host=ARIA2_HOST, port=ARIA2_PORT, secret=ARIA2_SECRET)
aria2 = API(aria2_client)
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.leech

app = Client("leech-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
cooldowns = {}

def format_progress(download):
    try:
        total_length = 30
        done_length = int((download.completed_length / download.total_length) * total_length)
        bar = "█" * done_length + "░" * (total_length - done_length)
        return f"[{bar}] {download.progress_string()} ({download.download_speed_string()})"
    except:
        return "Fetching progress..."

@app.on_message(filters.command("leech") & filters.reply)
async def leech(_, message: Message):
    user = message.from_user
    now = time.time()

    # Anti-spam
    if user.id in cooldowns and now - cooldowns[user.id] < 180:
        return await message.reply("⏳ Please wait 3 minutes before your next leech.")
    cooldowns[user.id] = now

    reply = message.reply_to_message
    link = reply.text or reply.caption
    torrent_file = None

    # Support for uploaded .torrent files
    if reply.document and reply.document.file_name.endswith(".torrent"):
        torrent_path = os.path.join(DOWNLOAD_DIR, reply.document.file_name)
        await reply.download(file_name=torrent_path)
        torrent_file = torrent_path

    if not link and not torrent_file:
        return await message.reply("❌ No valid link or .torrent file found.")

    status = await message.reply("📥 Starting download...")
    try:
        if torrent_file:
            download = aria2.add_torrent(torrent_file, options={"dir": DOWNLOAD_DIR})
        else:
            download = aria2.add_uris([link], options={"dir": DOWNLOAD_DIR})

        while not download.is_complete and not download.is_removed:
            await asyncio.sleep(5)
            download = aria2.get_download(download.gid)
            try:
                await status.edit(f"📥 Downloading...\n{format_progress(download)}")
            except:
                pass

        filepath = download.files[0].path
        final_path = filepath

        # Multi-file: ZIP the folder
        if download.followed_by_ids or len(download.files) > 1:
            folder = os.path.dirname(filepath)
            zip_name = f"{folder}.zip"
            final_path = os.path.join(DOWNLOAD_DIR, zip_name)
            shutil.make_archive(folder, 'zip', folder)

        file_size = os.path.getsize(final_path)
        if file_size > MAX_FILE_SIZE:
            return await status.edit("❌ File too large to send (Telegram bot limit is 2GB).")

        await status.edit("📤 Uploading file to your DM...")
        await app.send_document(user.id, final_path, caption="Here's your file 🎁")
        await status.edit("✅ Sent to your DM!")

        # Log to MongoDB
        await db.logs.insert_one({
            "user_id": user.id,
            "username": user.username,
            "filename": os.path.basename(final_path),
            "size": file_size,
            "time": datetime.utcnow(),
            "from_group": message.chat.title if message.chat else None
        })

    except Exception as e:
        await status.edit("❌ Something went wrong.")
        await app.send_message(OWNER_ID, f"⚠️ Error for {user.id}:\n{str(e)}")
    finally:
        # Cleanup
        try:
            if download.is_complete:
                if os.path.isdir(filepath):
                    shutil.rmtree(os.path.dirname(filepath), ignore_errors=True)
                if os.path.exists(final_path):
                    os.remove(final_path)
            if torrent_file and os.path.exists(torrent_file):
                os.remove(torrent_file)
        except:
            pass

@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply(
        "👋 Welcome! Reply to a magnet, link, or torrent file with /leech in a group, "
        "and I’ll download and DM the file to you."
    )

if __name__ == "__main__":
    os.system("bash aria.sh &")
    app.run()
    

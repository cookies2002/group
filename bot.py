import os
import asyncio
import time
import shutil
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from aria2p import API, Client as Aria2Client
from motor.motor_asyncio import AsyncIOMotorClient

# Environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URL = os.getenv("MONGO_URL")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Aria2 & MongoDB setup
aria_client = Aria2Client(host="http://localhost", port=6800, secret="madara123")
aria2 = API(aria2_client=aria_client)
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.leech

# Pyrogram client
app = Client("leech-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Cooldown tracker
cooldowns = {}

@app.on_message(filters.command("leech") & filters.reply)
async def leech(_, message: Message):
    user = message.from_user

    # Anti-spam
    now = time.time()
    if user.id in cooldowns and now - cooldowns[user.id] < 180:
        return await message.reply("⏳ Please wait 3 minutes between leeches.")
    cooldowns[user.id] = now

    # Get link from reply
    reply = message.reply_to_message
    link = reply.text or reply.caption
    if not link:
        return await message.reply("❌ No valid link found.")

    status = await message.reply("📥 Downloading started...")
    download = aria2.add_uris([link], options={"dir": DOWNLOAD_DIR})

    # Progress loop
    while not download.is_complete:
        await asyncio.sleep(5)
        download = aria2.get_download(download.gid)
        progress = f"{download.progress_string()} | {download.download_speed_string()}"
        try:
            await status.edit(f"📥 Downloading...\n{progress}")
        except:
            pass

    filepath = download.files[0].path
    final_path = filepath

    # Multi-file support
    if download.followed_by_ids:
        folder = os.path.dirname(filepath)
        zip_name = f"{folder}.zip"
        final_path = os.path.join(DOWNLOAD_DIR, zip_name)
        shutil.make_archive(folder, 'zip', folder)

    # Upload
    await status.edit("📤 Uploading file to your DM...")
    try:
        await app.send_document(user.id, final_path, caption="Here's your file 🎁")
        await status.edit("✅ Sent to your DM!")

        # Log to DB
        await db.logs.insert_one({
            "user_id": user.id,
            "username": user.username,
            "filename": os.path.basename(final_path),
            "size": os.path.getsize(final_path),
            "time": datetime.now()
        })

    except Exception as e:
        await status.edit(f"❌ Error sending file: {e}")
    finally:
        # Cleanup
        try:
            if os.path.isdir(filepath):
                shutil.rmtree(os.path.dirname(filepath))
            if os.path.exists(final_path):
                os.remove(final_path)
        except:
            pass

@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply("👋 Welcome! Use /leech on a magnet or link (by replying to it in a group). I’ll download and DM it to you!")

if __name__ == "__main__":
    os.system("bash aria.sh &")
    app.run()
    

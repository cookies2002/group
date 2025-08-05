import os
import asyncio
import time
import shutil
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message
from aria2p import API, Client as Aria2Client
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_URL,
    DOWNLOAD_DIR, ARIA2_SECRET, ARIA2_HOST, ARIA2_PORT
)

# Setup
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
aria2_client = Aria2Client(host=ARIA2_HOST, port=ARIA2_PORT, secret=ARIA2_SECRET)
aria2 = API(aria2_client)
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.leech

app = Client("leech-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
cooldowns = {}

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
    if not link:
        return await message.reply("❌ No valid link found in reply.")

    status = await message.reply("📥 Starting download...")
    try:
        download = aria2.add_uris([link], options={"dir": DOWNLOAD_DIR})

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

        # Multi-file: ZIP the folder
        if download.followed_by_ids:
            folder = os.path.dirname(filepath)
            zip_name = f"{folder}.zip"
            final_path = os.path.join(DOWNLOAD_DIR, zip_name)
            shutil.make_archive(folder, 'zip', folder)

        await status.edit("📤 Uploading...")
        await app.send_document(user.id, final_path, caption="Here's your file 🎁")
        await status.edit("✅ Sent to your DM!")

        await db.logs.insert_one({
            "user_id": user.id,
            "username": user.username,
            "filename": os.path.basename(final_path),
            "size": os.path.getsize(final_path),
            "time": datetime.utcnow()
        })

    except Exception as e:
        await status.edit(f"❌ Error: {e}")

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
    await message.reply(
        "👋 Welcome! Reply to a magnet/torrent/link with /leech in a group, "
        "and I'll download and DM the file to you."
    )

if __name__ == "__main__":
    os.system("bash aria.sh &")
    app.run()
    

import os
import shutil
import asyncio
import time
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aria2p import API, Client as Aria2Client
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_URL,
    DOWNLOAD_DIR, ARIA2_SECRET, ARIA2_HOST, ARIA2_PORT
)

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
COOLDOWN_SECONDS = 180  # 3 mins cooldown

# Setup
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
aria2_client = Aria2Client(host=ARIA2_HOST, port=ARIA2_PORT, secret=ARIA2_SECRET)
aria2 = API(aria2_client)
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.leech
cooldowns = {}

app = Client("leech-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def format_progress(download):
    try:
        total_length = 30
        done_length = int((download.completed_length / download.total_length) * total_length)
        bar = "█" * done_length + "░" * (total_length - done_length)
        return f"[{bar}] {download.progress_string()} ({download.download_speed_string()})"
    except:
        return "⏳ Fetching progress..."

@app.on_message(filters.command("leech") & filters.reply)
async def leech_handler(_, message: Message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized to use this bot.")

    now = time.time()
    if user.id in cooldowns and now - cooldowns[user.id] < COOLDOWN_SECONDS:
        wait = int(COOLDOWN_SECONDS - (now - cooldowns[user.id]))
        return await message.reply(f"⏳ Please wait {wait} seconds before using /leech again.")
    cooldowns[user.id] = now

    reply = message.reply_to_message
    link = reply.text or reply.caption
    torrent_file_path = None

    if reply.document and reply.document.file_name.endswith(".torrent"):
        torrent_file_path = os.path.join(DOWNLOAD_DIR, reply.document.file_name)
        await reply.download(file_name=torrent_file_path)

    if not link and not torrent_file_path:
        return await message.reply("❌ No valid link or .torrent file found.")

    status = await message.reply("📥 Downloading started...")
    download = None

    try:
        if torrent_file_path:
            download = aria2.add_torrent(torrent_file_path, options={
                "dir": DOWNLOAD_DIR,
                "bt-tracker": "udp://tracker.openbittorrent.com:80,udp://tracker.opentrackr.org:1337"
            })
        else:
            # Optional: validate the URL before adding it
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.head(link, timeout=10) as resp:
                    if resp.status >= 400:
                        await status.edit("❌ Download failed! Invalid or expired source.")
                        return

            download = aria2.add_uris([link], options={
                "dir": DOWNLOAD_DIR,
                "user-agent": "Mozilla/5.0",
                "referer": link
            })

        start_time = time.time()

        while True:
            await asyncio.sleep(5)
            download = aria2.get_download(download.gid)

            if download.is_complete:
                break
            elif download.status == "error":
                await status.edit("❌ Download failed! Invalid or expired source.")
                return
            elif download.status == "removed":
                await status.edit("❌ Download was removed.")
                return
            elif time.time() - start_time > 600:
                await status.edit("⚠️ Download timeout after 10 mins. Cancelled.")
                aria2.remove([download], force=True, files=True)
                return

            try:
                await status.edit(f"📥 Downloading...\n{format_progress(download)}")
            except:
                pass

        filepath = download.files[0].path
        final_path = filepath

        if download.followed_by_ids or len(download.files) > 1:
            folder = os.path.dirname(filepath)
            zip_name = os.path.basename(folder.rstrip("/")) + ".zip"
            final_path = os.path.join(DOWNLOAD_DIR, zip_name)
            shutil.make_archive(folder, 'zip', folder)

        file_size = os.path.getsize(final_path)
        if file_size > MAX_FILE_SIZE:
            await status.edit("❌ File too large for Telegram (limit: 2GB).")
            return

        await status.edit("📤 Uploading to your DM...")
        await app.send_document(user.id, final_path, caption="📦 Here's your file!")
        await status.edit("✅ File delivered in your DM!")

        await db.logs.insert_one({
            "user_id": user.id,
            "username": user.username,
            "filename": os.path.basename(final_path),
            "size": file_size,
            "time": datetime.utcnow(),
            "from_group": message.chat.title if message.chat else None
        })

    except Exception as e:
        await status.edit("❌ Error occurred during processing.")
        await app.send_message(OWNER_ID, f"⚠️ Error for {user.id}: `{str(e)}`")

    finally:
        try:
            if download and download.is_complete:
                if os.path.isdir(filepath):
                    shutil.rmtree(os.path.dirname(filepath), ignore_errors=True)
                elif os.path.exists(final_path):
                    os.remove(final_path)
            if torrent_file_path and os.path.exists(torrent_file_path):
                os.remove(torrent_file_path)
        except:
            pass

@app.on_message(filters.private & filters.command("start"))
async def start(_, message: Message):
    await message.reply(
        "👋 Welcome to the Leech Bot!\n\n"
        "📌 *How to use:*\n"
        "1. Send a magnet/link or .torrent file in any group\n"
        "2. Reply to it with `/leech`\n\n"
        "✅ Bot will download & send the file to your DM!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 View Logs", callback_data="logs")],
            [InlineKeyboardButton("💬 Support", url="https://t.me/YourSupportGroup")],
        ]),
        quote=True
    )

@app.on_callback_query(filters.regex("logs"))
async def logs_callback(client, callback_query):
    user_id = callback_query.from_user.id
    logs = await db.logs.find({"user_id": user_id}).sort("time", -1).to_list(5)
    if not logs:
        return await callback_query.answer("No logs found.", show_alert=True)

    text = "🧾 **Your Recent Logs:**\n"
    for log in logs:
        text += f"• `{log['filename']}` - {round(log['size'] / 1024 / 1024, 2)} MB\n"

    await callback_query.message.reply(text, quote=True)
    await callback_query.answer()

async def start_aria2():
    process = await asyncio.create_subprocess_shell(
        "bash aria.sh",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await process.communicate()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_aria2())
    app.run()
    

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from subprocess import run

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

app = Client("leech-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Start aria2c daemon
def start_aria2():
    run([
        "aria2c", "--enable-rpc", "--rpc-listen-all=true", "--rpc-allow-origin-all",
        f"--dir={DOWNLOAD_DIR}", "--max-connection-per-server=16", "--split=16",
        "--min-split-size=1M", "--max-concurrent-downloads=5"
    ])

@app.on_message(filters.command("leech") & filters.reply)
async def leech_file(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a magnet or link with /leech")

    user = message.from_user
    link = message.reply_to_message.text or message.reply_to_message.caption

    if not link:
        return await message.reply("No valid link found in reply")

    msg = await message.reply("Downloading...")
    filename = None

    try:
        cmd = ["aria2c", "--dir", DOWNLOAD_DIR, link, "--summary-interval=0"]
        result = run(cmd, capture_output=True)

        files = sorted(os.listdir(DOWNLOAD_DIR), key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
        if not files:
            return await msg.edit("Download failed.")

        filename = os.path.join(DOWNLOAD_DIR, files[0])
        await msg.edit("Uploading...")

        sent = await app.send_document(user.id, filename, caption="Here's your file")
        await msg.edit("✅ Sent to your DM")

    except Exception as e:
        await msg.edit(f"Error: {e}")
    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply("I'm a Group Leech Bot. Reply to a magnet/torrent/link with /leech")

if __name__ == "__main__":
    start_aria2()
    app.run()

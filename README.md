# 🚀 Madara Leech Bot

A powerful leech & upload Telegram bot using `Pyrogram`, `Aria2`, `MongoDB`. Supports direct downloads, torrent/magnet, file renaming, spam control, and progress updates.

---

## 🧠 Features

- File Leeching from URLs, Torrents, Magnets  
- Telegram File Uploading with Rename Support  
- MongoDB-based File Log (Permanent)  
- Progress Bar, Speed, ETA  
- Anti-Spam & User Restriction  
- Heroku & VPS Deploy Ready

---

## 🛠 Deploy to Heroku

Click the button below to deploy instantly to Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/cookies2002/group)

> 🔄 Replace `yourusername` with your actual GitHub username or repo link.

---

## 🔧 Required Variables

| Variable      | Description |
|---------------|-------------|
| `API_ID`      | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH`    | Telegram API HASH |
| `BOT_TOKEN`   | Token from [@BotFather](https://t.me/BotFather) |
| `OWNER_ID`    | Your Telegram numeric ID |
| `MONGODB_URI` | Your MongoDB URI (e.g. from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)) |

---

## ⚙️ Optional Variables

| Variable        | Description |
|-----------------|-------------|
| `USER_SESSION_STRING` | For uploader user session (optional) |
| `DOWNLOAD_DIR`  | Download directory path (default: `downloads`) |
| `ARIA_SECRET`   | Secret key for Aria2 RPC (default: `madara123`) |

---

## 🖥 Local Setup (Linux/Termux)

```bash
git clone https://github.com/yourusername/Madara-Leech-Bot
cd Madara-Leech-Bot
pip install -r requirements.txt
python3 bot.py

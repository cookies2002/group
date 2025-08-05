# 🚀 Group Leech Bot

A Heroku-ready Telegram bot that lets users reply with `/leech` to magnet/torrent/URL in a group. The bot downloads the file and sends it via DM.

## 📌 Features
- Fast download using aria2c
- Uploads file to user via DM
- Heroku compatible
- Private `/start` command

## ⚙️ Setup Instructions

### 1. Deploy to Heroku
```
heroku create your-bot-name
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set OWNER_ID=your_user_id
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
```

### 2. Push to Heroku
```
git init
git add .
git commit -m "Initial"
git push heroku master
```

### 3. Requirements
- Python 3.11+
- aria2 installed

## 📎 Credits
- Made by Marwin ❤️

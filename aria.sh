#!/bin/bash

mkdir -p downloads

aria2c --enable-rpc \
  --rpc-listen-all=true \
  --rpc-allow-origin-all \
  --rpc-listen-port=6800 \
  --dir=downloads \
  --max-connection-per-server=16 \
  --split=16 \
  --min-split-size=1M \
  --max-concurrent-downloads=5 \
  --rpc-secret=madara123 \
  --continue=true &
  
python3 bot.py

#!/bin/bash

# Create necessary directories
mkdir -p ~/.aria2
touch ~/.aria2/aria2.session

# Aria2c configuration
aria2c \
  --enable-rpc \
  --rpc-listen-all=true \
  --rpc-allow-origin-all \
  --rpc-secret=madara123 \
  --max-connection-per-server=10 \
  --continue=true \
  --input-file=~/.aria2/aria2.session \
  --save-session=~/.aria2/aria2.session \
  --dir=downloads \
  --max-concurrent-downloads=5 \
  --split=10 \
  --min-split-size=1M \
  --follow-torrent=mem \
  --seed-time=0 \
  --bt-save-metadata=true
  

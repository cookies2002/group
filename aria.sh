#!/bin/bash

# Madara Uchiha - Aria2 Daemon Starter
# Compatible with Termux / Ubuntu / Heroku

ARIA2_SECRET="madara123"
DOWNLOAD_DIR="downloads"
ARIA2_PORT=6800
ARIA2_LOG="aria2.log"

mkdir -p "$DOWNLOAD_DIR"

aria2c \
  --enable-rpc=true \
  --rpc-listen-port=$ARIA2_PORT \
  --rpc-secret="$ARIA2_SECRET" \
  --rpc-listen-all=true \
  --rpc-allow-origin-all=true \
  --dir="$DOWNLOAD_DIR" \
  --max-connection-per-server=10 \
  --continue=true \
  --input-file=aria2.session \
  --save-session=aria2.session \
  --max-concurrent-downloads=5 \
  --min-split-size=10M \
  --split=10 \
  --daemon=true \
  --log="$ARIA2_LOG" \
  --log-level=notice
  

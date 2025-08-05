#!/bin/bash

# ================================
# Start Aria2 with RPC Support
# ================================

# Directory to save downloads (fallback)
DOWNLOAD_DIR="${DOWNLOAD_DIR:-downloads}"
mkdir -p "$DOWNLOAD_DIR"

# Aria2 secret token (default: "mysecret" if not set in env)
ARIA2_SECRET="${ARIA2_SECRET:-mysecret}"

# RPC Port (default: 6800)
ARIA2_PORT="${ARIA2_PORT:-6800}"

# Tracker list (auto-optimized for better torrent speed)
TRACKERS=$(curl -fsSL https://trackerslist.com/all_aria2.txt | tr '\n' ',' | sed 's/,$//')

# Run Aria2 daemon
aria2c \
  --enable-rpc \
  --rpc-listen-all=false \
  --rpc-allow-origin-all=true \
  --rpc-listen-port="$ARIA2_PORT" \
  --rpc-secret="$ARIA2_SECRET" \
  --dir="$DOWNLOAD_DIR" \
  --max-connection-per-server=10 \
  --continue=true \
  --max-concurrent-downloads=5 \
  --split=10 \
  --min-split-size=1M \
  --follow-torrent=mem \
  --seed-time=0 \
  --bt-seed-unverified=true \
  --bt-save-metadata=true \
  --bt-tracker="${TRACKERS}" \
  --summary-interval=30
  

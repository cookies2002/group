#!/bin/bash

# Ensure aria2 starts with RPC, proper tracker support, and log for debug
aria2c \
  --enable-rpc \
  --rpc-listen-all=true \
  --rpc-listen-port=6800 \
  --rpc-secret=madara123 \
  --max-connection-per-server=10 \
  --rpc-allow-origin-all \
  --continue=true \
  --dir=downloads \
  --bt-tracker="udp://tracker.openbittorrent.com:80,udp://opentracker.i2p.rocks:6969/announce,udp://tracker.opentrackr.org:1337/announce,udp://9.rarbg.to:2710/announce" \
  --daemon=true \
  --log-level=notice \
  --log=aria2.log

echo "✅ Aria2 started"

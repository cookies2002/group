#!/bin/bash

# Start aria2 with RPC enabled
aria2c \
  --enable-rpc \
  --rpc-listen-all=false \
  --rpc-listen-port=6800 \
  --rpc-secret=madara123 \
  --max-connection-per-server=10 \
  --rpc-allow-origin-all \
  --dir=downloads \
  --continue=true \
  --daemon=true

echo "✅ Aria2 started"

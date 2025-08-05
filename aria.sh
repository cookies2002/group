#!/bin/bash
aria2c \
  --enable-rpc \
  --rpc-listen-all=false \
  --rpc-allow-origin-all \
  --rpc-secret="myaria2secret" \
  --rpc-listen-port=6800 \
  --max-connection-per-server=10 \
  --continue=true \
  --dir="./downloads" \
  --max-concurrent-downloads=5 \
  --split=10 \
  --min-split-size=5M
  

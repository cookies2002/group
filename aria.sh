#!/bin/bash

# ─── CONFIG START ────────────────────────────────────────────────

ARIA2_CONF="aria2.conf"
ARIA2_SESSION="aria2.session"
ARIA2_LOG="aria2.log"
ARIA2_PORT=6800
SECRET_TOKEN="your_secret_token"  # Optional: Use if you have RPC secret

# ─── CONFIG END ──────────────────────────────────────────────────

# ─── CREATE DEFAULT SESSION FILE IF NOT EXISTS ───────────────────

if [ ! -f "$ARIA2_SESSION" ]; then
    touch "$ARIA2_SESSION"
fi

# ─── CREATE DEFAULT CONFIG IF NOT EXISTS ─────────────────────────

if [ ! -f "$ARIA2_CONF" ]; then
    cat > "$ARIA2_CONF" <<EOF
dir=downloads
file-allocation=falloc
continue=true
max-concurrent-downloads=10
split=10
min-split-size=1M
max-connection-per-server=10
disable-ipv6=true
check-certificate=false

input-file=${ARIA2_SESSION}
save-session=${ARIA2_SESSION}
save-session-interval=30
log=${ARIA2_LOG}
log-level=notice

enable-rpc=true
rpc-listen-all=true
rpc-allow-origin-all=true
rpc-listen-port=${ARIA2_PORT}
rpc-secret=${SECRET_TOKEN}
EOF
fi

# ─── START ARIA2C WITH CONFIG ────────────────────────────────────

echo "Starting aria2c with config..."
aria2c --conf-path="${ARIA2_CONF}"

#!/bin/bash

aria2c --enable-rpc \
--rpc-listen-all=true \
--rpc-allow-origin-all \
--dir=downloads \
--max-connection-per-server=16 \
--split=16 \
--min-split-size=1M \
--max-concurrent-downloads=5

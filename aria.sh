#!/bin/bash

aria2c \
--enable-rpc \
--rpc-listen-all=true \
--rpc-allow-origin-all \
--rpc-secret=madara \
--max-connection-per-server=10 \
--min-split-size=10M \
--split=10 \
--dir=downloads \
--continue=true

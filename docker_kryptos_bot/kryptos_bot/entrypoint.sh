#!/bin/bash

# set env for license codebook
export KRYPTOS_BOT_CODEBOOK=THIS_IS_A_SECRET

# Validate ENV
if [ -z "$KRYPTOS_BOT_API_TOKEN" ]; then
  echo "[ERROR] KRYPTOS_BOT_API_TOKEN is not set."
  echo "Please run container again with '-e KRYPTOS_BOT_API_TOKEN=[YOUR_TELEGRAM_BOT_API_KEY]'"
  exit 1
fi

if [ -z "$KRYPTOS_API_HOST_IP" ]; then
  echo "[ERROR] KRYPTOS_API_HOST_IP is not set."
  echo "Please run container again with '-e KRYPTOS_API_HOST_IP=[KRYPTOS_API_CONTAINER_HOST_IP]'"
  exit 1
fi

# Start the first Python script (kryptos_bot.py) in the background
python kryptos_bot.py &

# Block Container shell
rm /usr/bin/*

# Wait for all background processes to finish
wait

#!/bin/bash

# set env for license codebook
export KRYPTOS_BOT_CODEBOOK=THIS_IS_SECRET

# Validate ENV
if [ -z "$KRYPTOS_BOT_API_TOKEN" ]; then
  echo "[ERROR] KRYPTOS_BOT_API_TOKEN is not set."
  echo "Please run container again with '-e KRYPTOS_BOT_API_TOKEN=[YOUR_TELEGRAM_BOT_API_KEY]'"
  exit 1
fi

# remove bash and sh
rm /usr/bin/sh /bin/sh

# get CMD arguments and execute: 2025.06.04
exec $@


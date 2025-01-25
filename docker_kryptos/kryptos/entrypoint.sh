#!/bin/bash

# Set Django secret token
export KRYPTOS_VERSION=1.0
export KRYPTOS_DIGITAL_SIGN=THIS_IS_A_SECRET
export KRYPTOS_DRF_API_TOKEN=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Validate ENV
if [ -z "$KRYPTOS_MONGODB_HOST" ]; then
  echo "[ERROR] KRYPTOS_MONGODB_HOST is not set."
  echo "Please run container again with '-e KRYPTOS_MONGODB_HOST=[MONGODB_CONTAINER_HOST_IP]'"
  exit 1
fi

if [ -z "$KRYPTOS_EMAIL_HOST_USER" ]; then
  echo "[ERROR] KRYPTOS_EMAIL_HOST_USER is not set."
  echo "Please run container again with '-e KRYPTOS_EMAIL_HOST_USER=[EMAIL_SMTP_USERNAME]'"
  echo "This container has a gmail SMTP as a default. If you want to use another SMTP Server, Please set 'KRYPTOS_EMAIL_HOST'"
  exit 1
fi

if [ -z "$KRYPTOS_EMAIL_HOST_PASSWORD" ]; then
  echo "[ERROR] KRYPTOS_EMAIL_HOST_PASSWORD is not set."
  echo "Please run container again with '-e KRYPTOS_EMAIL_HOST_PASSWORD=[EMAIL_SMTP_PASSWORD]'"
  exit 1
fi

# Start the second Python script (Django server) in the background
python manage.py runserver 0.0.0.0:8000 &

# Block Container shell
rm /usr/bin/*

# Wait for all background processes to finish
wait

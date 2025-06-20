"""
Django settings for cryptex project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

from mongoengine import (get_connection,
                         connect as mongodb_connect)
from django.utils.log import request_logger
from os import getenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# KRYPTOS_VERSION
KRYPTOS_VERSION: str = str(getenv("KRYPTOS_VERSION"))
KRYPTOS_DIGITAL_SIGN = str(getenv("KRYPTOS_DIGITAL_SIGN"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("KRYPTOS_DRF_API_TOKEN")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
HOSTNAME=getenv("HOSTNAME")
BOT_HOSTNAME="kryptos-bot"
ALLOWED_HOSTS = [HOSTNAME,]


# Application definition
INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine',                      # Mongo DB ORM Application
    'rest_framework',                   # Rest Framework Application for Django
    'rest_framework_mongoengine',       # Rest Framework Application for MongoDB
    'rest_framework_simplejwt',         # JWT Token Application
    'accounts',
    'admins',
    'documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kryptos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kryptos.wsgi.application'


# Database
while True:
    mongodb_connect(
        db="THIS_IS_SECRET",
        host="kryptos-db",
        port=int(getenv("KRYPTOS_MONGODB_PORT") or 27017),
        username="THIS_IS_SECRET",
        password="THIS_IS_SECRET",
        authentication_source="THIS_IS_SECRET",
        serverSelectionTimeoutMS=5000,  # searching db server timeout for 5 secs
        connectTimeoutMS=2000,          # connection timeout for 2 secs
        socketTimeoutMS=3000            # Waiting timeout for 3 secs
    )

    try:
        # check the connection.
        get_connection().admin.command("ping")
        request_logger.info(f"[INFO] Successfully connect to Database.")
        break

    except Exception as e:
        # fail log for db connection.
        request_logger.error(f"[ERROR] Fail to connect to Database. Retry...)")


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "accounts.validators.SimilarityPasswordValidator"},
    {"NAME": "accounts.validators.MinimumLengthPasswordValidator"},
    {"NAME": "accounts.validators.NumericPasswordValidator"},
    {"NAME": "accounts.validators.UpperPasswordValidator"},
    {"NAME": "accounts.validators.LowerPasswordValidator"},
    {"NAME": "accounts.validators.SpecialPasswordValidator"}
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = getenv("KRYPTOS_DRF_TIMEZONE") or "Asia/Tokyo"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


### Custom Settings ###
# JWT Config
SIMPLE_JWT:dict = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=3),
}

# Authenticate Backends
AUTHENTICATION_BACKENDS:list = ["accounts.backends.CustomUserBackend"]


# Kryptos Telegram bot' host container IP
KRYPTOS_BOT_HOST_IP: str = getenv("KRYPTOS_BOT_HOST_API")


# Google App Pass Email Sending
EMAIL_BACKEND = getenv("KRYPTOS_EMAIL_BACKEND") or "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = getenv("KRYPTOS_EMAIL_HOST") or "smtp.gmail.com"
EMAIL_HOST_USER = getenv("KRYPTOS_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("KRYPTOS_EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(getenv("KRYPTOS_EMAIL_PORT") or 587)
EMAIL_USE_TLS = getenv("KRYPTOS_EMAIL_USE_TLS") or True
EMAIL_USE_SSL = getenv("KRYPTOS_EMAIL_USE_SSL") or False


# CORS
CORS_ALLOWED_ORIGINS = [
    f"http://{HOSTNAME}:8000",
]

CORS_ALLOW_HEADERS = [
    "authorization",
]

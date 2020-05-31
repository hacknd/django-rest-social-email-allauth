# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import timedelta

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",

    # Packages Needed
    "social_django",
    "rest_framework",
    "rest_framework.authtoken",
    "knox",

    # Local Package
    "rest_social_email_auth"
]

SITE_ID = 1

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TLL': timedelta(hours=10),
    'USER_SERIALIZER': 'rest_social_email_auth.serializers.AccountSerializer',
    'AUTO_REFRESH': False,
    'TOKEN_LIMIT_PER_USER': None,
}


MIDDLEWARE = MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Custom Authentication Formula
    'rest_social_email_auth.backends.AuthBackend',
    #Discord OAuth2 Authentication
    'social_core.backends.discord.DiscordOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        }
    },
]

SECRET_KEY = '1q%7#a9-=(s_&qo)2m^arnjpwvf07j+8=+d8x8von%8u4x0io%'

STATIC_URL = '/static/'

AUTH_USER_MODEL = "rest_social_email_auth.User"

TEST_RUNNER = 'tests.runner.PytestTestRunner'


EMAIL_AUTH = {
    "EMAIL_VERIFICATION_URL": "https://example.com/verify/{key}",
    "PASSWORD_RESET_URL": "https://example.com/reset/{key}",
}
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

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

MIDDLEWARE = MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
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
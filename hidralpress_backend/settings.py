"""
Django settings for hidralpress_backend project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g24glhzyd!a56j$!+y6c@w&u1bk9cq-3+5w*pa)cj1bz0@-l2f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'True'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'imagekit',
    'hidralpress_backend',
    'imagens',
    # desenvolvimento
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # desenvolvimento
   'corsheaders.middleware.CorsMiddleware',
]

ALLOWED_HOSTS = [
    '192.168.0.6',
    '192.168.0.6:8000',
    'localhost',
    'saf.hidralpress.local',
    'localhost:3000',
    'hidralpress.ngrok.app',
]

ROOT_URLCONF = 'hidralpress_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hidralpress_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "saf2",
        "USER": "admin",
        "PASSWORD": "SAF@hidral",
        "HOST": "localhost",
        "PORT": "5432",
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL='/media/'
MEDIA_ROOT='aaa'

STORAGES = {
    "default": {
        "BACKEND": "hidralpress_backend.storages.MyFileSystemStorage",
        "OPTIONS": {
            # "location": "/hidralpress-prod",
            "location": "/mnt/c-prod"
        }
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = None

# BACK_URL = "http://192.168.0.6:8000"

# desenvolvimento
BACK_URL = "https://hidralpress.ngrok.app"

CORS_ORIGIN_ALLOW_ALL = True


CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = None

CSRF_TRUSTED_ORIGINS = [BACK_URL]

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'ngrok-skip-browser-warning',
]


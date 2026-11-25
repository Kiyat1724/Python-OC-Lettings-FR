"""Configuration Django du projet Orange County Lettings."""
import logging
import os
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


BASE_DIR = Path(__file__).resolve().parent.parent

# Conserver le type des identifiants des migrations existantes.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Configuration fournie par l'environnement.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Le débogage est désactivé si la variable est absente.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'DJANGO_ALLOWED_HOSTS',
        '127.0.0.1,localhost',
    ).split(',')
    if host.strip()
]


# Applications.
INSTALLED_APPS = [
    'oc_lettings_site.apps.OCLettingsSiteConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lettings.apps.LettingsConfig',
    'profiles.apps.ProfilesConfig',
]


# Traitement des requêtes et des réponses.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'oc_lettings_site.urls'


# Templates HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'oc_lettings_site.wsgi.application'


# Base de données SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'oc-lettings-site.sqlite3',
    }
}


# Validation des mots de passe.
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


# Langue et fuseau horaire.
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Fichiers statiques.
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Journalisation de l'application.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'oc_lettings': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Surveillance activée uniquement lorsqu'un DSN est fourni.
SENTRY_DSN = os.environ.get('SENTRY_DSN', '').strip()

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=os.environ.get('SENTRY_ENVIRONMENT', 'development'),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                breadcrumb_level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        data_collection={
            'user_info': False,
            'http_bodies': [],
            'cookies': {'mode': 'off'},
            'http_headers': {'request': {'mode': 'off'}},
            'url_query_params': {'mode': 'off'},
            'stack_frame_variables': {'mode': 'off'},
        },
    )

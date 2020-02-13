"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import environ
from .utils import build_component_list

PROJECT_NAME = '3MEGAWAT'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')
BSAE_FILES_PATH = os.path.join(BASE_DIR, 'files')
STATIC_ROOT = os.path.join(BSAE_FILES_PATH, 'static')
MEDIA_ROOT = os.path.join(BSAE_FILES_PATH, 'media')
sys.path.insert(2, APPS_DIR)

env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
env.read_env(
    env.path(
        'ENV_FILE_PATH',
        default=(environ.Path(__file__) - 2).path('.env')()
    )())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

BASE_MIDDLEWARE_CLASSES = {
    'django.middleware.security.SecurityMiddleware': 100,
    'django.contrib.sessions.middleware.SessionMiddleware': 200,
    'django.middleware.common.CommonMiddleware': 300,
    'django.middleware.csrf.CsrfViewMiddleware': 400,
    'django.contrib.auth.middleware.AuthenticationMiddleware': 500,
    'django.contrib.messages.middleware.MessageMiddleware': 600,
    'django.middleware.clickjacking.XFrameOptionsMiddleware': 700,
}

CUSTOM_MIDDLEWARE_CLASSES = {}

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# ------------------------------------------#
# Debug Toolbar
# ------------------------------------------#
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    CUSTOM_MIDDLEWARE_CLASSES.update({
        'debug_toolbar.middleware.DebugToolbarMiddleware':
            BASE_MIDDLEWARE_CLASSES['django.contrib.sessions.middleware.SessionMiddleware'] + 10000,
    })
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
# ------------------------------------------#
# Rest Framework
# ------------------------------------------#
INSTALLED_APPS += (
    'rest_framework',
    'rest_framework.authtoken',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# ------------------------------------------#

# Plant App
# ------------------------------------------#
INSTALLED_APPS += [
    'plant',
]
DATAPOINT_DATE_FORMAT_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Django Filter
# ------------------------------------------#
INSTALLED_APPS += [
    'django_filters',
]

# ------------------------------------------#
# Misc
# ------------------------------------------#
INSTALLED_APPS += [
    'django_extensions',
]

# ------------------------------------------#
# REDIS
# ------------------------------------------#
if os.getenv('REDIS_USER'):
    REDIS_FORMAT_URL = 'redis://{user}:{passwd}@{host}:{port}/0'
else:
    REDIS_FORMAT_URL = 'redis://{host}:{port}/0'

REDIS_URL = REDIS_FORMAT_URL.format(
    user=os.getenv('REDIS_USER', None),
    passwd=os.getenv('REDIS_PASS', None),
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', '16379')
)

# ------------------------------------------#
# CELERY
# ------------------------------------------#
CELERY_BROKER_TRANSPORT = os.getenv('CELERY_BROKER_TRANSPORT', 'redis')
if os.getenv('CELERY_BROKER_USER'):
    CELERY_FORMAT_URL = "{transport}://{user}:{passwd}@{host}:{port}/1"
else:
    CELERY_FORMAT_URL = "{transport}://{host}:{port}/1"

CELERY_BROKER_URL = CELERY_FORMAT_URL.format(
    transport=os.getenv('CELERY_BROKER_TRANSPORT', 'redis'),
    user=os.getenv('CELERY_BROKER_USER', None),
    passwd=os.getenv('CELERY_BROKER_PASS', None),
    host=os.getenv('CELERY_BROKER_HOST', 'localhost'),
    port=os.getenv('CELERY_BROKER_PORT', '16379')
)
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

#  -------------------------------------------#
# Don't change following section
# -------------------------------------------#

MIDDLEWARE = build_component_list(BASE_MIDDLEWARE_CLASSES, CUSTOM_MIDDLEWARE_CLASSES)

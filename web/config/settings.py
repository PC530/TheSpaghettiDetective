"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'django.contrib.humanize',
    'hijack',
    'compat',
    'simple_history',
    'widget_tweaks',
    'rest_framework',
    'bootstrap_pagination',
    'jstemplate',
    'pushbullet',
    'telebot',
    'app',  # app has to come before allauth for template override to work
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'api',
]

if os.environ.get('SOCIAL_LOGIN') == 'True':
    INSTALLED_APPS += [
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.telegram_bot.enable_webhooks'
]

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
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

HIJACK_ALLOW_GET_REQUESTS = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Request logging for debugging purpose

import logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_build')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Allauth

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET=True
ACCOUNT_EMAIL_VERIFICATION = os.environ.get('ACCOUNT_EMAIL_VERIFICATION', 'none')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1
SITE_USES_HTTPS = os.environ.get('SITE_USES_HTTPS') == 'True'

AUTH_USER_MODEL = 'app.User'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.PrinterAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        ),
}

# Sentry
if os.environ.get('SENTRY_DSN'):
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

# Extra js
EXTRA_JS = [s for s in os.environ.get('EXTRA_JS', '').split('|') if s]

# REDIS client
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')

# Email and SMS settings

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')
TWILIO_ENABLED = TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# settings export
SETTINGS_EXPORT = [
    'EXTRA_JS',
    'TWILIO_ENABLED',
    'ACCOUNT_EMAIL_VERIFICATION',
    'TELEGRAM_BOT_TOKEN',
]

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600*12}

# Channels layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

# Settings to store and serve uploaded images
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
INTERNAL_MEDIA_HOST = os.environ.get('INTERNAL_MEDIA_HOST')
PICS_CONTAINER = 'tsd-pics'
TIMELAPSE_CONTAINER = 'tsd-timelapses'

BUCKET_PREFIX = os.environ.get('BUCKET_PREFIX')
ML_API_HOST = os.environ.get('ML_API_HOST')
ML_API_TOKEN = os.environ.get('ML_API_TOKEN')

# Hyper parameters for prediction model
THRESHOLD_LOW = float(os.environ.get('THRESHOLD_LOW', '0.38'))   # Definitely not failing if ewm mean is below this level. =(0.4 - 0.02): 0.4 - optimal THRESHOLD_LOW in hyper params grid search; 0.02 - average of rolling_mean_short
THRESHOLD_HIGH = float(os.environ.get('THRESHOLD_HIGH', '0.78'))   # Definitely failing if ewm mean is above this level. =(0.8 - 0.02): 0.8 - optimal THRESHOLD_HIGH in hyper params grid search; 0.02 - average of rolling_mean_short
INIT_SAFE_FRAME_NUM = int(os.environ.get('INIT_SAFE_FRAME_NUM', 30))        # The number of frames at the beginning of the print that are considered "safe"
ROLLING_MEAN_SHORT_MULTIPLE = float(os.environ.get('ROLLING_MEAN_SHORT_MULTIPLE', 3.8))   # Print is failing is ewm mean is this many times over the short rolling mean
ESCALATING_FACTOR = float(os.environ.get('ESCALATING_FACTOR', 1.75))   # The multiplication factor to escalate "warning" to "error"

TIMELAPSE_MINIMUM_SECONDS = 5 if DEBUG else 300

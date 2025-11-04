import os
from pathlib import Path
import logging
import logging.config
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'billing',
    'membership',
    'services',
    'whatsapp_ads',
    
    # 'whatsapp',
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

ROOT_URLCONF = 'spa_admin.urls'

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

WSGI_APPLICATION = 'spa_admin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

CSRF_COOKIE_SECURE = False  # if you're only using local http



APP_LOGGING_LEVEL = "DEBUG"

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# ✅ Local: use file logging
if "manage.py" in sys.argv[0]:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": "%(asctime)s %(levelname)s %(message)s"},
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "app": {
                "level": APP_LOGGING_LEVEL,
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": os.path.join(BASE_DIR, "logs", "app.log"),
                "when": "D",
                "interval": 1,
                "backupCount": 3,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["app"],
                "level": APP_LOGGING_LEVEL,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["app"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

# ✅ Cloud: use Google Cloud Logging (only in production)
else:
    from google.cloud import logging as gcloud_logging
    client = gcloud_logging.Client()
    client.setup_logging()

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "app": {
                "class": "google.cloud.logging.handlers.CloudLoggingHandler",
                "client": client,
                "name": "DXE_App",
            },
        },
        "loggers": {
            "app": {"handlers": ["app"], "level": "DEBUG"},
            "django.request": {"handlers": ["app"], "level": "ERROR"},
        },
    }

logging.config.dictConfig(LOGGING)


# WhatsApp API Settings (configure these)
WHATSAPP_BUSINESS_ACCOUNT_ID = 'your_business_account_id'
WHATSAPP_PHONE_NUMBER_ID = 'your_phone_number_id'
WHATSAPP_ACCESS_TOKEN = 'your_access_token'
WHATSAPP_API_VERSION = 'v17.0'


# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
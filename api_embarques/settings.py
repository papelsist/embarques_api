"""
Django settings for api_embarques project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import json
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ii0&9pue56%44abdjt8ya+!b1pc3kszktofgxb-40q(vibqi6t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]


# Application definition


DJANGO_APPS = [
     "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles"
]

LOCAL_APPS = [
    'applications.authentication',
    'applications.reportes',
    'applications.embarques',
    'applications.ruteo',
    'applications.tableros',
    'applications.dashboards',
    'applications.knzl',
    'applications.core',
    'applications.localizacion_gps',
]

THIRD_PART_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
]

INSTALLED_APPS = DJANGO_APPS+ THIRD_PART_APPS + LOCAL_APPS 

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api_embarques.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_embarques.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'siipap',
        'USER': 'root',
        'PASSWORD': 'Paproot_83',
        'HOST': '10.10.1.121',
        #'USER': 'admin',
        #'PASSWORD': 'papelrx',
        #'HOST': '198.199.69.63',
        'PORT': 3306 ,
        'OPTIONS': {'ssl_mode': 'DISABLED'},
        #'OPTIONS': {'ssl': False},
    },
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
] 

AUTH_USER_MODEL = 'authentication.User'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True


CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,   
}

REST_FRAMEWORK = { 'DEFAULT_AUTHENTICATION_CLASSES':[
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication', ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
} 

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
} 



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT =os.path.join(BASE_DIR, 'media').replace('\\', '/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

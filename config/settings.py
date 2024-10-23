
# nohup xvfb-run -a gunicorn config.wsgi -t 36000 -w 3 > gunicorn.log 2>&1 &

import os
from pathlib import Path
import environ

env = environ.Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xcj7@)ijvx=jae0#2fq(*=6h%&i74#qfbjxl5w@a4y!2cvd=%r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool)

ALLOWED_HOSTS = ["*"]
BASE_URL = env('BASE_URL')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hrm_app',
    'users',
    'import_export',
    'tailwind',
    'django_browser_reload',
    'rest_framework',
    'corsheaders',
    'core',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'users.context_processor.base_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

engine = env('DATABASE_ENGING')
if engine == 'django.db.backends.mysql':
    print("RDS")
    DATABASES = {
        'default': {
            'ENGINE': engine,
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USERNAME'),
            'PASSWORD': env('DATABASE_PASSWORD').strip(),
            'HOST': env('DATABASE_HOST'),  # e.g., 'localhost' or an IP address
            'PORT': env('DATABASE_PORT'),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
else:
    print("sql")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "config/media")


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    'http://52.206.234.170',
    'https://52.206.234.170',
    "http://localhost:80",
    "http://localhost",
    "https://localhost",
    "http://127.0.0.1:8000",
    "http://207.148.10.92",
    "https://207.148.10.92",
    'http://localhost:8000',
    'http://ec2-34-226-12-37.compute-1.amazonaws.com',
    'https://ec2-34-226-12-37.compute-1.amazonaws.com',
    'http://hrm.nexiatech.org',
    'https://hrm.nexiatech.org'

]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)


CSRF_TRUSTED_ORIGINS = [
    'http://52.206.234.170',
    "http://localhost",
    "https://localhost",
    'https://52.206.234.170',
    "http://localhost:80",
    "http://207.148.10.92",
    "https://207.148.10.92",
    "http://127.0.0.1:8000",
    'http://ec2-34-226-12-37.compute-1.amazonaws.com',
    'https://ec2-34-226-12-37.compute-1.amazonaws.com',
    'http://hrm.nexiatech.org',
    'https://hrm.nexiatech.org'


]


DATA_UPLOAD_MAX_MEMORY_SIZE = 100000000000  # 1 GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 100000000000  # 1 GB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000000000000000000000

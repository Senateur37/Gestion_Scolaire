import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-x(4_by^k+j=wu$&k1zr6s2%i22f2=bl-&q2=^0uwys__%3x3b8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.onrender.com,.railway.app').split(',') if h.strip()]

CSRF_TRUSTED_ORIGINS = [
    origin.strip() 
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.onrender.com,https://*.railway.app,http://localhost,http://127.0.0.1').split(',') 
    if origin.strip()
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'crispy_forms',
    'crispy_tailwind',

    # Local apps
    "accounts",
    "students",
    "teachers",
    "academics",
    "grades",
    "attendance",
    "communication",
    "payments",
    "documents",
    "dashboards",
    "audit",
    "library",
    "transport",
    "hostel",
    "reports",
    "exams",
    "hr",
    "frontoffice",
    "inventory",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

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

ROOT_URLCONF = 'G_Scolaire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'G_Scolaire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

db_url = os.environ.get('DATABASE_URL', '').strip()
if db_url and db_url.startswith(('postgres://', 'postgresql://', 'sqlite://', 'mysql://')):
    DATABASES = {
        'default': dj_database_url.parse(
            db_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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


# Internationalisation — Français (Mali / Afrique de l'Ouest)
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'fr'         # Français neutre (pas lié à la France / Euro)
TIME_ZONE = 'Africa/Bamako'  # GMT+0 (Mali, Sénégal, Burkina Faso...)
USE_I18N = True
USE_L10N = False              # Désactivé pour éviter le format Euro automatique
USE_TZ = True

# Devise locale : Franc CFA — utilisé manuellement via le filtre {| fcfa }
CURRENCY_SYMBOL = 'FCFA'
CURRENCY_THOUSANDS_SEP = '\u202f'  # espace insécable

# Format de date en français (ex: 27 août 2025)
DATE_FORMAT = 'j F Y'
DATETIME_FORMAT = 'j F Y à H:i'
SHORT_DATE_FORMAT = 'd/m/Y'
FIRST_DAY_OF_WEEK = 1  # Lundi


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# Media files (Documents, uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Reverse Proxy SSL Header for Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

import os
from pathlib import Path
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = os.environ.get('SECRET_KEY', 'insecure-default-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'swahilifacile.onrender.com').split(',')

# Applications
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'utilisateurs.apps.UtilisateursConfig',
    'publications.apps.PublicationsConfig',
    'core.apps.CoreConfig',
    'messagerie.apps.MessagerieConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # nécessaire en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'swahili_facile.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.slider_publications',
            ],
        },
    },
]

WSGI_APPLICATION = 'swahili_facile.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )
}

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'utilisateurs.UtilisateurPerso'

# Langue et fuseau
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Kinshasa'
USE_I18N = True
USE_TZ = True

# Static & media
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Admin Swahili Facile",
    "site_header": "Swahili Facile",
    "site_brand": "SwahiliFacile",
    "login_logo": "images/logo.png",
    "login_logo_dark": "images/logo.png",
    "site_logo": "images/logo.png",
    "copyright": "Swahili Facile Ltd",
    "theme": "flatly",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "order_with_respect_to": ["publications", "utilisateurs", "messagerie", "auth"],
    "icons": {
        "publications": "fas fa-newspaper",
        "utilisateurs": "fas fa-users",
        "messagerie": "fas fa-comments",
        "auth.Group": "fas fa-users-cog",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
from pathlib import Path
from dotenv import load_dotenv  # Optional but recommended

# Load environment variables from .env file (for local development)
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Security Settings
# ========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-for-local-only')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'your-app-name.azurewebsites.net',  # Replace with your Azure App Service URL
    'victorious-ocean-05a3a040f.6.azurestaticapps.net',  # Your frontend URL
]

# ========================
# Application Definition
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    'storages',
    
    # Local
    'app1',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BlobProject.urls'

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

WSGI_APPLICATION = 'BlobProject.wsgi.application'

# ========================
# Database
# ========================
def get_db_config():
    """Configure database based on environment."""
    if 'AZURE_POSTGRESQL_CONNECTIONSTRING' in os.environ:
        conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
        return {
            'ENGINE': 'django.db.backends.postgresql',
            **{k: v for k, v in [pair.split('=') for pair in conn_str.split(' ')]},
            'OPTIONS': {'sslmode': 'require'},
            'CONN_MAX_AGE': 600,
        }
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

DATABASES = {'default': get_db_config()}

# ========================
# CORS & Security
# ========================
CORS_ALLOWED_ORIGINS = [
    'https://victorious-ocean-05a3a040f.6.azurestaticapps.net',
    'http://localhost:3000',  # For local frontend development
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS.append('http://*')

# ========================
# Azure Blob Storage
# ========================
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', 'devaccount')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', 'devkey')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'django')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_SSL = True

# ========================
# Static & Media Files
# ========================
# Static files (Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (Azure)
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/media/'

# ========================
# REST Framework
# ========================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Lock down in production
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

# ========================
# Production Security
# ========================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# Default Auto Field
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import os
 
from pathlib import Path
 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
# SECURITY WARNING: keep the secret key used in production secret!
 
# Get secret key from environment variable
 
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
 
# SECURITY WARNING: don't run with debug turned on in production!
 
# Set DEBUG based on environment variable - defaults to False for production safety
 
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
 
# Set your Azure web app URL here, or better, get from environment
 
ALLOWED_HOSTS = [
 
    os.environ.get('DJANGO_ALLOWED_HOST', '.azurewebsites.net'),
 
    'localhost',
 
    '127.0.0.1',
 
]
 
# Application definition
 
INSTALLED_APPS = [
 
    'django.contrib.admin',
 
    'django.contrib.auth',
 
    'django.contrib.contenttypes',
 
    'django.contrib.sessions',
 
    'django.contrib.messages',
 
    'django.contrib.staticfiles',
 
    'app1',
 
    'rest_framework',
 
    'storages',
 
    'corsheaders',  # Make sure this is installed
 
]
 
# Azure Blob Storage settings from environment variables
 
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
 
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
 
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'django')
 
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
 
MIDDLEWARE = [
 
    'corsheaders.middleware.CorsMiddleware',  # Keep CORS at the top
 
    'django.middleware.security.SecurityMiddleware',
 
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise for static files (if not using Azure for static)
 
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
 
# Database
 
# Use Azure PostgreSQL
 
try:
 
    # Get the connection string from environment variable
 
    CONNECTION = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
 
    # Parse the connection string into components
 
    CONNECTION_STR = {pair.split('=')[0]: pair.split('=')[1]
 
                     for pair in CONNECTION.split(' ')}
 
    DATABASES = {
 
        'default': {
 
            'ENGINE': 'django.db.backends.postgresql',
 
            'NAME': CONNECTION_STR.get('dbname'),
 
            'USER': CONNECTION_STR.get('user'),
 
            'PASSWORD': CONNECTION_STR.get('password'),
 
            'HOST': CONNECTION_STR.get('host'),
 
            'PORT': '5432',
 
            'OPTIONS': {'sslmode': 'require'},
 
            'CONN_MAX_AGE': 600,
 
        },
 
    }
 
except Exception as e:
 
    # Fallback for local development or if connection string is missing
 
    print(f"Error setting up database: {e}")
 
    print("Using SQLite as fallback")
 
    DATABASES = {
 
        'default': {
 
            'ENGINE': 'django.db.backends.sqlite3',
 
            'NAME': BASE_DIR / 'db.sqlite3',
 
        }
 
    }
 
# CORS settings - more restrictive for production
 
if DEBUG:
 
    CORS_ALLOW_ALL_ORIGINS = True
 
else:
 
    CORS_ALLOW_ALL_ORIGINS = False
 
    CORS_ALLOWED_ORIGINS = [
 
        # List your frontend origins here
 
        os.environ.get('FRONTEND_URL', 'https://victorious-ocean-05a3a040f.6.azurestaticapps.net'),
 
        'https://victorious-ocean-05a3a040f.6.azurestaticapps.net',  # For local development
 
    ]
 
CORS_ALLOW_METHODS = [
 
    'DELETE',
 
    'GET',
 
    'OPTIONS',
 
    'PATCH',
 
    'POST',
 
    'PUT',
 
]
 
CORS_ALLOW_HEADERS = [
 
    'accept',
 
    'accept-encoding',
 
    'authorization',
 
    'content-type',
 
    'dnt',
 
    'origin',
 
    'user-agent',
 
    'x-csrftoken',
 
    'x-requested-with',
 
]
 
# Password validation
 
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
 
# REST Framework settings
 
REST_FRAMEWORK = {
 
    'DEFAULT_PERMISSION_CLASSES': [
 
        'rest_framework.permissions.AllowAny',  # Consider changing this for production
 
    ],
 
}
 
# Internationalization
 
LANGUAGE_CODE = 'en-us'
 
TIME_ZONE = 'UTC'
 
USE_I18N = True
 
USE_TZ = True
 
# Static and Media Files with Azure Blob Storage
 
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
 
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
 
# Azure URLs
 
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/static/'
 
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/media/'
 
# Local static files (in addition to Azure)
 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
 
# Default primary key field type
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 
# Production security settings
 
if not DEBUG:
 
    # HTTPS settings
 
    SECURE_SSL_REDIRECT = True
 
    SECURE_HSTS_SECONDS = 31536000  # 1 year
 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
 
    SECURE_HSTS_PRELOAD = True
 
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
 
    # Cookie settings
 
    SESSION_COOKIE_SECURE = True
 
    CSRF_COOKIE_SECURE = True
 
    # Content security policy
 
    SECURE_REFERRER_POLICY = 'same-origin'
 
    SECURE_BROWSER_XSS_FILTER = True
 
    # Log settings for production
 
    LOGGING = {
 
        'version': 1,
 
        'disable_existing_loggers': False,
 
        'formatters': {
 
            'verbose': {
 
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
 
                'style': '{',
 
            },
 
        },
 
        'handlers': {
 
            'console': {
 
                'level': 'INFO',
 
                'class': 'logging.StreamHandler',
 
                'formatter': 'verbose'
 
            },
 
        },
 
        'loggers': {
 
            'django': {
 
                'handlers': ['console'],
 
                'level': 'INFO',
 
                'propagate': True,
 
            },
 
        },
 
    }
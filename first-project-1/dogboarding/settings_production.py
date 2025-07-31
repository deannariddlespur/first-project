import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Will be updated with your actual domain

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Use PostgreSQL on Railway with better connection handling
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=0,  # Disable connection pooling to avoid timeout issues
            conn_health_checks=False  # Disable health checks to reduce connection overhead
        )
    }
    print(f"✅ Using PostgreSQL database from DATABASE_URL")
else:
    # Fallback to SQLite for local development
    db_path = os.path.join(BASE_DIR, 'data', 'db.sqlite3')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }
    print(f"⚠️ Using SQLite database at: {db_path}")
    print("⚠️ WARNING: SQLite is not persistent on Railway!")
    print("⚠️ Please add PostgreSQL plugin to your Railway project.")

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (for uploaded photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add media file serving for production
# This allows uploaded files to be served in production
import django.conf.urls.static
from django.conf import settings

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
# Disable SSL redirect for Railway testing
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
} 
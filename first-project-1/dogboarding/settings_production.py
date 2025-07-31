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

# AWS S3 Configuration for Media Files
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'media'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# Use S3 for media files if AWS credentials are available
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # S3 for media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    print(f"✅ Using AWS S3 for media storage: {MEDIA_URL}")
else:
    # Fallback to local media storage (not persistent on Railway)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    print("⚠️ Using local media storage (not persistent on Railway)")
    print("⚠️ Set up AWS S3 environment variables for persistent media storage")

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
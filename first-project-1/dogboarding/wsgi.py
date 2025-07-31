"""
WSGI config for dogboarding project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_NAME'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')

# Initialize Django
django.setup()

# Auto-run migrations and setup on Railway
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_NAME'):
    try:
        from django.core.management import call_command
        from django.db import connection
        
        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='auth_user'
            """)
            table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("Running migrations and setup...")
            call_command('migrate')
            call_command('setup_production')
            print("Database setup complete!")
        else:
            print("Database tables already exist, skipping setup.")
            
    except Exception as e:
        print(f"Error during auto-setup: {e}")

application = get_wsgi_application()

#!/usr/bin/env python
"""
Startup script for Railway deployment.
This script runs before the main application to ensure the database is properly set up.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_NAME'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')

# Initialize Django
django.setup()

def setup_database():
    """Set up the database with migrations and initial data."""
    try:
        from django.core.management import call_command
        from django.db import connection
        
        print("Checking database setup...")
        
        # Check if auth_user table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='auth_user'
            """)
            table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("Running migrations...")
            call_command('migrate', verbosity=1)
            
            print("Running production setup...")
            call_command('setup_production', verbosity=1)
            
            print("Database setup complete!")
        else:
            print("Database tables already exist, skipping setup.")
            
    except Exception as e:
        print(f"Error during database setup: {e}")
        # Don't exit with error, let the app start anyway
        pass

if __name__ == '__main__':
    setup_database() 
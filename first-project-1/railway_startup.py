#!/usr/bin/env python
"""
Railway startup script for automatic database setup.
This script runs before the main application to ensure the database is properly configured.
"""

import os
import sys
import django
import time

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_railway():
    """Set up the application for Railway deployment."""
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
    
    # Initialize Django
    django.setup()
    
    print("🚀 Starting Railway deployment setup...")
    
    try:
        from django.core.management import call_command
        from django.db import connection
        from django.contrib.auth.models import User
        
        # Test database connection
        print("🔍 Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        # Check if we're using PostgreSQL
        db_engine = connection.settings_dict['ENGINE']
        print(f"📊 Database engine: {db_engine}")
        
        if 'postgresql' in db_engine:
            print("✅ Using PostgreSQL database")
        else:
            print("⚠️ Using SQLite database (not persistent on Railway)")
        
        # Check if tables exist
        print("🔍 Checking database tables...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'auth_user'
            """)
            table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("📦 Running Django migrations...")
            call_command('migrate', verbosity=1)
            
            print("👤 Creating admin user...")
            if not User.objects.filter(username='admin').exists():
                User.objects.create_user(
                    username='admin',
                    email='admin@dogboarding.com',
                    password='admin123456',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                print("✅ Admin user created: admin/admin123456")
            
            print("🏠 Creating sample kennels...")
            from core.models import Kennel
            kennel_sizes = [
                ('Small Kennel A', 'small', 'Cozy kennel for small dogs'),
                ('Small Kennel B', 'small', 'Cozy kennel for small dogs'),
                ('Medium Kennel A', 'medium', 'Comfortable kennel for medium dogs'),
                ('Medium Kennel B', 'medium', 'Comfortable kennel for medium dogs'),
                ('Large Kennel A', 'large', 'Spacious kennel for large dogs'),
                ('Large Kennel B', 'large', 'Spacious kennel for large dogs'),
            ]
            
            for name, size, description in kennel_sizes:
                Kennel.objects.get_or_create(
                    name=name,
                    defaults={
                        'size': size,
                        'description': description
                    }
                )
            print("✅ Sample kennels created")
            
            print("🎉 Database setup complete!")
        else:
            print("✅ Database tables already exist")
            
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        print("⚠️ Application will start anyway, but database may not be ready")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("🐕 Dog Boarding Railway Startup")
    print("=" * 50)
    
    success = setup_railway()
    
    if success:
        print("✅ Railway setup completed successfully!")
    else:
        print("⚠️ Railway setup had issues, but continuing...")
    
    print("=" * 50) 
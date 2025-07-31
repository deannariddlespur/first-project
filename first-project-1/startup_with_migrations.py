#!/usr/bin/env python3
"""
Startup script with migrations for Railway
"""
import os
import sys
import time
import subprocess
import threading
import urllib.request

def make_health_request():
    """Make a request to the health endpoint to keep container alive"""
    try:
        # Wait a moment for gunicorn to start
        time.sleep(8)
        
        # Get the port from environment
        port = os.environ.get('PORT', '8080')
        
        # Make request to health endpoint
        try:
            response = urllib.request.urlopen(f'http://localhost:{port}/health/', timeout=10)
            print(f"✅ Health check request successful: {response.getcode()}")
        except Exception as e:
            print(f"⚠️ Health check request failed: {e}")
        
        # Make request to homepage
        try:
            response = urllib.request.urlopen(f'http://localhost:{port}/', timeout=10)
            print(f"✅ Homepage request successful: {response.getcode()}")
        except Exception as e:
            print(f"⚠️ Homepage request failed: {e}")
        
    except Exception as e:
        print(f"⚠️ Health request warning: {e}")

def start_keep_alive():
    """Start keep alive in background"""
    thread = threading.Thread(target=make_health_request, daemon=True)
    thread.start()
    print("🔄 Keep alive thread started")

print("🚀 Starting Django application with migrations...")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')

# Import Django
import django
django.setup()

print("✅ Django setup complete")

# Start keep alive thread
start_keep_alive()

# Run migrations
print("🔄 Running database migrations...")
try:
    from django.core.management import call_command
    call_command('migrate')
    print("✅ Migrations completed successfully!")
    
    # Create admin user if it doesn't exist
    from django.contrib.auth.models import User
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
    else:
        print("✅ Admin user already exists")
    
    # Create sample kennels if they don't exist
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
    
except Exception as e:
    print(f"❌ Error during migrations: {e}")
    # Don't exit, continue with startup

print("🎯 Database setup complete!")

# Start gunicorn with proper error handling
print("🚀 Starting Gunicorn...")
try:
    # Use subprocess to start gunicorn
    cmd = [
        'gunicorn',
        'dogboarding.wsgi:application',
        '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
        '--workers', '1',
        '--timeout', '120',
        '--keep-alive', '2',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        '--log-file', '-'
    ]
    
    print(f"🎯 Starting command: {' '.join(cmd)}")
    os.execvp('gunicorn', cmd)
    
except Exception as e:
    print(f"❌ Error starting gunicorn: {e}")
    sys.exit(1) 
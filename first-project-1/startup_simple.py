#!/usr/bin/env python3
"""
Simple startup script for Railway
"""
import os
import sys
import time
import urllib.request
import threading

def make_immediate_request():
    """Make an immediate request to keep Railway happy"""
    try:
        # Wait for gunicorn to start
        time.sleep(3)
        
        # Get the port
        port = os.environ.get('PORT', '8080')
        
        # Make immediate requests
        try:
            response = urllib.request.urlopen(f'http://localhost:{port}/health/', timeout=5)
            print(f"✅ Immediate health check: {response.getcode()}")
        except:
            pass
            
        try:
            response = urllib.request.urlopen(f'http://localhost:{port}/', timeout=5)
            print(f"✅ Immediate homepage: {response.getcode()}")
        except:
            pass
            
    except Exception as e:
        print(f"⚠️ Immediate request warning: {e}")

# Start immediate request thread
thread = threading.Thread(target=make_immediate_request, daemon=True)
thread.start()

print("🚀 Starting with immediate traffic...")

# Run migrations first
print("🔄 Running migrations...")
os.system('python manage.py setup_railway')

# Test database connection
print("🔍 Testing database connection...")
try:
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
    import django
    django.setup()
    
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection test successful")
except Exception as e:
    print(f"❌ Database connection test failed: {e}")
    # Continue anyway - might be temporary issue

# Start gunicorn with better settings for Railway
print("🚀 Starting gunicorn...")
os.execvp('gunicorn', [
    'gunicorn', 
    'dogboarding.wsgi:application', 
    '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}', 
    '--workers=1', 
    '--timeout=300',
    '--keep-alive=5',
    '--max-requests=1000',
    '--max-requests-jitter=100',
    '--preload',
    '--log-file', '-'
]) 
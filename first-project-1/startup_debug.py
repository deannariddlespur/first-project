#!/usr/bin/env python3
"""
Startup debug script for Railway deployment
"""
import os
import sys
import time

print("🚀 Starting Railway debug script...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")
print(f"🔧 Environment variables:")
print(f"   - PORT: {os.environ.get('PORT', 'NOT SET')}")
print(f"   - DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
print(f"   - RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'NOT SET')}")

# Try to import Django
try:
    import django
    print(f"✅ Django version: {django.get_version()}")
except ImportError as e:
    print(f"❌ Django import error: {e}")
    sys.exit(1)

# Try to set up Django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup error: {e}")
    sys.exit(1)

# Try to check database
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection error: {e}")

print("🎯 Starting Gunicorn...")
print("=" * 50)

# Start gunicorn
os.execvp('gunicorn', [
    'gunicorn',
    'dogboarding.wsgi:application',
    '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
    '--log-file', '-',
    '--workers', '1',
    '--timeout', '120'
]) 
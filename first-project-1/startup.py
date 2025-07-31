#!/usr/bin/env python3
"""
Simple startup script for Railway
"""
import os
import sys
import time

print("🚀 Starting Django application...")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')

# Import Django
import django
django.setup()

print("✅ Django setup complete")

# Test database connection
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection verified")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

print("🎯 Starting Gunicorn...")

# Start gunicorn
os.execvp('gunicorn', [
    'gunicorn',
    'dogboarding.wsgi:application',
    '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
    '--workers', '1',
    '--timeout', '120',
    '--keep-alive', '2',
    '--log-file', '-'
]) 
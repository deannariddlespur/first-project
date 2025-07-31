#!/usr/bin/env python3
"""
Test script to verify Django app startup
"""
import os
import sys
import time
import requests

print("🧪 Testing Django app startup...")

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

# Test URL resolution
try:
    from django.urls import reverse
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/')
    
    # Test homepage URL
    home_url = reverse('home')
    print(f"✅ Homepage URL resolved: {home_url}")
    
    # Test health check URL
    health_url = reverse('health_check')
    print(f"✅ Health check URL resolved: {health_url}")
    
except Exception as e:
    print(f"❌ URL resolution failed: {e}")
    sys.exit(1)

print("🎯 All tests passed! Starting Gunicorn...")

# Start gunicorn
os.execvp('gunicorn', [
    'gunicorn',
    'dogboarding.wsgi:application',
    '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
    '--workers', '1',
    '--timeout', '120',
    '--log-file', '-'
]) 
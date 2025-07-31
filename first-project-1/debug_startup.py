#!/usr/bin/env python3
"""
Debug script to test Django startup
"""
import os
import sys
import time

print("🔍 Debugging Django startup...")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')

print("📁 Current directory:", os.getcwd())
print("🔧 Environment variables:")
print(f"   - PORT: {os.environ.get('PORT', 'NOT SET')}")
print(f"   - DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
print(f"   - RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'NOT SET')}")

# Test Django import
try:
    import django
    print(f"✅ Django version: {django.get_version()}")
except ImportError as e:
    print(f"❌ Django import error: {e}")
    sys.exit(1)

# Test Django setup
try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup error: {e}")
    sys.exit(1)

# Test database connection
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection error: {e}")
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
    print(f"❌ URL resolution error: {e}")
    sys.exit(1)

# Test template rendering
try:
    from django.template.loader import render_to_string
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/')
    
    # Test if templates can be loaded
    template_content = render_to_string('core/home.html', {}, request=request)
    print("✅ Template rendering successful")
    
except Exception as e:
    print(f"❌ Template rendering error: {e}")
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
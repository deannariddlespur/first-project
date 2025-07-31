#!/usr/bin/env python
import os
import django
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.core.management import call_command

print("🔄 Running Django migrations...")

try:
    # Run migrations
    call_command('migrate')
    print("✅ Migrations completed successfully!")
    
    # Show migration status
    call_command('showmigrations', 'core')
    
except Exception as e:
    print(f"❌ Error during migrations: {e}")
    # Don't exit - let the app continue
    pass

print("🎯 Startup script completed!") 
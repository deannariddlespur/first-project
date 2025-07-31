#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.core.management import call_command

print("🔄 Running Django migrations...")

try:
    # Run migrations
    call_command('migrate')
    print("✅ Migrations completed successfully!")
except Exception as e:
    print(f"❌ Error during migrations: {e}")

print("🔧 Fixing database schema...")

try:
    # Run database schema fix
    call_command('fix_database_schema')
    print("✅ Database schema fixed successfully!")
except Exception as e:
    print(f"❌ Error fixing database schema: {e}")

print("🎯 Startup script completed!") 
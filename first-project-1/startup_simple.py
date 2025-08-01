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

print("🔧 Fixing core_dailylog.photo column for PostgreSQL...")

try:
    # Run PostgreSQL fix for photo column
    call_command('fix_daily_log_photo_postgresql')
    print("✅ Photo column fix completed successfully!")
except Exception as e:
    print(f"❌ Error fixing photo column: {e}")

print("🎯 Startup script completed!") 
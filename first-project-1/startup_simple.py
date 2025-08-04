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

print("🔧 Adding missing columns directly with SQL...")
print("🔍 DEBUG: About to call add_columns_direct command...")

try:
    # Add missing columns directly with SQL
    call_command('add_columns_direct')
    print("✅ Missing columns added directly successfully!")
except Exception as e:
    print(f"❌ Error adding missing columns directly: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Fixing daily logs database columns...")

try:
    # Run the Django management command to fix daily log columns
    call_command('fix_daily_log_columns')
    print("✅ Daily logs database fix completed!")
except Exception as e:
    print(f"❌ Error fixing daily logs database: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🎯 Startup script completed!") 
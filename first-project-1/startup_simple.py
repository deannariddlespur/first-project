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

print("🔧 Force adding missing columns with verification...")
print("🔍 DEBUG: About to call force_add_columns_final command...")

try:
    # Force add missing columns with verification
    call_command('force_add_columns_final')
    print("✅ Missing columns force added and verified successfully!")
except Exception as e:
    print(f"❌ Error force adding missing columns: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🎯 Startup script completed!") 
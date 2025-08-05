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

print("🔧 Force adding photo column to DailyLog...")

try:
    # Import and run the force add script
    from force_add_photo_column import force_add_photo_column
    force_add_photo_column()
    print("✅ Force column addition completed!")
except Exception as e:
    print(f"❌ Error force adding columns: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Adding photo_url column to Railway database...")

try:
    # Add photo_url column to Railway database
    call_command('add_photo_url_railway')
    print("✅ photo_url column added successfully!")
except Exception as e:
    print(f"❌ Error adding photo_url column: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Force applying photo field length migration...")

try:
    # Force apply photo field length migration
    call_command('force_apply_photo_migration')
    print("✅ Photo field length migration applied successfully!")
except Exception as e:
    print(f"❌ Error applying photo field length migration: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Force fixing photo field length with direct SQL...")

try:
    # Force fix photo field length with direct SQL
    call_command('force_fix_photo_length')
    print("✅ Photo field length fixed with direct SQL!")
except Exception as e:
    print(f"❌ Error fixing photo field length with direct SQL: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Adding supabase_url column directly with SQL...")

try:
    # Add supabase_url column directly with SQL
    call_command('add_supabase_url_column')
    print("✅ supabase_url column added successfully!")
except Exception as e:
    print(f"❌ Error adding supabase_url column: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🔧 Fixing photo field length with PostgreSQL syntax...")

try:
    # Fix photo field length with PostgreSQL syntax
    call_command('fix_photo_length_postgresql')
    print("✅ Photo field length fixed with PostgreSQL syntax!")
except Exception as e:
    print(f"❌ Error fixing photo field length: {e}")
    print(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}")

print("🎯 Startup script completed!") 
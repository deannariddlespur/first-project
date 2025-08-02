#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

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

print("🔧 Fixing database columns...")

# Check database type and fix columns accordingly
try:
    db_engine = connection.settings_dict['ENGINE']
    print(f"📊 Using database: {db_engine}")
    
    if 'postgresql' in db_engine:
        print("🔧 Running PostgreSQL-specific column fixes...")
        try:
            call_command('fix_daily_log_photo_postgresql')
            print("✅ Photo column fix completed successfully!")
        except Exception as e:
            print(f"❌ Error fixing photo column: {e}")
        
        try:
            call_command('fix_dog_photo_base64_postgresql')
            print("✅ Photo base64 column fix completed successfully!")
        except Exception as e:
            print(f"❌ Error fixing photo base64 column: {e}")
    else:
        print("🔧 Running SQLite-specific column fixes...")
        # For SQLite, we'll use a different approach
        with connection.cursor() as cursor:
            # Check and add photo column to core_dailylog
            cursor.execute("PRAGMA table_info(core_dailylog)")
            columns = cursor.fetchall()
            photo_exists = any(col[1] == 'photo' for col in columns)
            
            if not photo_exists:
                cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100)")
                print("✅ Added photo column to core_dailylog table")
            else:
                print("⚠️ photo column already exists in core_dailylog table")
            
            # Check and add photo_base64 column to core_dog
            cursor.execute("PRAGMA table_info(core_dog)")
            columns = cursor.fetchall()
            photo_base64_exists = any(col[1] == 'photo_base64' for col in columns)
            
            if not photo_base64_exists:
                cursor.execute("ALTER TABLE core_dog ADD COLUMN photo_base64 TEXT")
                print("✅ Added photo_base64 column to core_dog table")
            else:
                print("⚠️ photo_base64 column already exists in core_dog table")
                
except Exception as e:
    print(f"❌ Error during column fixes: {e}")

print("🎯 Startup script completed!") 
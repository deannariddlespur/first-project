#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def check_and_fix_daily_logs():
    """Check and fix daily logs database issues"""
    print("🔍 Checking daily logs database...")
    
    try:
        with connection.cursor() as cursor:
            # Check if photo column exists in core_dailylog table (SQLite compatible)
            cursor.execute("PRAGMA table_info(core_dailylog)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'photo' in column_names:
                print("✅ photo column exists in core_dailylog table")
            else:
                print("❌ photo column missing from core_dailylog table")
                print("🔧 Adding photo column...")
                
                # Add the photo column
                cursor.execute("""
                    ALTER TABLE core_dailylog 
                    ADD COLUMN photo VARCHAR(100)
                """)
                print("✅ photo column added successfully")
            
            # Check if photo_base64 column exists in core_dog table (SQLite compatible)
            cursor.execute("PRAGMA table_info(core_dog)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'photo_base64' in column_names:
                print("✅ photo_base64 column exists in core_dog table")
            else:
                print("❌ photo_base64 column missing from core_dog table")
                print("🔧 Adding photo_base64 column...")
                
                # Add the photo_base64 column
                cursor.execute("""
                    ALTER TABLE core_dog 
                    ADD COLUMN photo_base64 TEXT
                """)
                print("✅ photo_base64 column added successfully")
                
    except Exception as e:
        print(f"❌ Error checking/fixing database: {e}")
        return False
    
    print("🎯 Daily logs database check completed!")
    return True

if __name__ == "__main__":
    success = check_and_fix_daily_logs()
    if success:
        print("✅ Database fix completed successfully!")
    else:
        print("❌ Database fix failed!")
        sys.exit(1) 
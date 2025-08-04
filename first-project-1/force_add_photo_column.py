#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.db import connection

def force_add_photo_column():
    """Force add photo column to DailyLog table"""
    print("🔧 Force adding photo column to DailyLog table...")
    
    try:
        with connection.cursor() as cursor:
            # Try to add the photo column directly
            cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100)")
            print("✅ photo column added successfully!")
            
    except Exception as e:
        print(f"⚠️ Column might already exist: {e}")
        
    try:
        with connection.cursor() as cursor:
            # Also add photo_base64 to core_dog
            cursor.execute("ALTER TABLE core_dog ADD COLUMN photo_base64 TEXT")
            print("✅ photo_base64 column added successfully!")
            
    except Exception as e:
        print(f"⚠️ photo_base64 column might already exist: {e}")
    
    print("🎯 Force column addition completed!")

if __name__ == "__main__":
    force_add_photo_column() 
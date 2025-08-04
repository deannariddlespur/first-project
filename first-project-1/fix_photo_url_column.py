#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/Users/deannariddlespur/Desktop/first-project/first-project-1')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.db import connection

def add_photo_url_column():
    """Add photo_url column to core_dog table"""
    try:
        with connection.cursor() as cursor:
            # Check if column exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_dog' AND column_name = 'photo_url'
            """)
            exists = cursor.fetchone()
            
            if not exists:
                print("📝 Adding photo_url column to database...")
                cursor.execute("""
                    ALTER TABLE core_dog 
                    ADD COLUMN photo_url VARCHAR(500) NULL
                """)
                print("✅ photo_url column added successfully!")
            else:
                print("✅ photo_url column already exists")
                
    except Exception as e:
        print(f"❌ Error adding photo_url column: {e}")

if __name__ == "__main__":
    add_photo_url_column() 
#!/usr/bin/env python
"""
Fix database by adding missing columns
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.db import connection

print("🔧 Fixing database schema...")

try:
    with connection.cursor() as cursor:
        # Add missing columns to core_dog table
        print("Adding photo_base64 column...")
        cursor.execute("""
            ALTER TABLE core_dog 
            ADD COLUMN photo_base64 TEXT;
        """)
        
        # Add missing columns to core_booking table
        print("Adding booking columns...")
        cursor.execute("""
            ALTER TABLE core_booking 
            ADD COLUMN total_amount DECIMAL(8,2) NULL,
            ADD COLUMN price_per_night DECIMAL(6,2) NULL;
        """)
        
        # Add missing columns to core_payment table
        print("Adding payment columns...")
        cursor.execute("""
            ALTER TABLE core_payment 
            ADD COLUMN payment_method VARCHAR(20) NULL,
            ADD COLUMN paid_date TIMESTAMP NULL;
        """)
        
        # Add missing columns to core_staffnote table
        print("Adding staff note columns...")
        cursor.execute("""
            ALTER TABLE core_staffnote 
            ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)
        
        print("✅ Database schema fixed successfully!")
        
except Exception as e:
    print(f"❌ Error fixing database: {e}")
    print("Some columns might already exist, which is okay.") 
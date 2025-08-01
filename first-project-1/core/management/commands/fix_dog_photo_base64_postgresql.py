from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Fix missing photo_base64 column in core_dog table for PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing core_dog.photo_base64 column for PostgreSQL...')
        
        try:
            with connection.cursor() as cursor:
                # Check if the photo_base64 column exists
                cursor.execute("""
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_dog' 
                    AND column_name = 'photo_base64'
                """)
                
                column_exists = cursor.fetchone()
                
                if not column_exists:
                    # Add the photo_base64 column
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_base64 TEXT
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo_base64 column to core_dog table')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ photo_base64 column already exists in core_dog table')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fixing photo_base64 column: {str(e)}')
            )
            raise 
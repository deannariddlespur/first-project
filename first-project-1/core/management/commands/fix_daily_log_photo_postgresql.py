from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Fix missing photo column in core_dailylog table for PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing core_dailylog.photo column for PostgreSQL...')
        
        try:
            with connection.cursor() as cursor:
                # Check if the photo column exists
                cursor.execute("""
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_dailylog' 
                    AND column_name = 'photo'
                """)
                
                column_exists = cursor.fetchone()
                
                if not column_exists:
                    # Add the photo column
                    cursor.execute("""
                        ALTER TABLE core_dailylog 
                        ADD COLUMN photo VARCHAR(100)
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo column to core_dailylog table')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ photo column already exists in core_dailylog table')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fixing photo column: {str(e)}')
            )
            raise 
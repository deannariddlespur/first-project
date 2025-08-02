from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Fix missing photo_base64 column in core_dog table for both SQLite and PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing core_dog.photo_base64 column...')
        
        try:
            with connection.cursor() as cursor:
                # Check database type
                db_engine = connection.settings_dict['ENGINE']
                
                if 'postgresql' in db_engine:
                    # PostgreSQL-specific check
                    cursor.execute("""
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dog' 
                        AND column_name = 'photo_base64'
                    """)
                else:
                    # SQLite-specific check
                    cursor.execute("PRAGMA table_info(core_dog)")
                    columns = cursor.fetchall()
                    column_exists = any(col[1] == 'photo_base64' for col in columns)
                    
                    if column_exists:
                        self.stdout.write(
                            self.style.WARNING('⚠️ photo_base64 column already exists in core_dog table')
                        )
                        return
                    else:
                        # Add the column for SQLite
                        cursor.execute("""
                            ALTER TABLE core_dog 
                            ADD COLUMN photo_base64 TEXT
                        """)
                        self.stdout.write(
                            self.style.SUCCESS('✅ Added photo_base64 column to core_dog table (SQLite)')
                        )
                        return
                
                # PostgreSQL path
                column_exists = cursor.fetchone()
                
                if not column_exists:
                    # Add the photo_base64 column
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_base64 TEXT
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo_base64 column to core_dog table (PostgreSQL)')
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
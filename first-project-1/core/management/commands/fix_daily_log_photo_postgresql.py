from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Fix missing photo column in core_dailylog table for both SQLite and PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing core_dailylog.photo column...')
        
        try:
            with connection.cursor() as cursor:
                # Check database type
                db_engine = connection.settings_dict['ENGINE']
                
                if 'postgresql' in db_engine:
                    # PostgreSQL-specific check
                    cursor.execute("""
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dailylog' 
                        AND column_name = 'photo'
                    """)
                else:
                    # SQLite-specific check
                    cursor.execute("PRAGMA table_info(core_dailylog)")
                    columns = cursor.fetchall()
                    column_exists = any(col[1] == 'photo' for col in columns)
                    
                    if column_exists:
                        self.stdout.write(
                            self.style.WARNING('⚠️ photo column already exists in core_dailylog table')
                        )
                        return
                    else:
                        # Add the column for SQLite
                        cursor.execute("""
                            ALTER TABLE core_dailylog 
                            ADD COLUMN photo VARCHAR(100)
                        """)
                        self.stdout.write(
                            self.style.SUCCESS('✅ Added photo column to core_dailylog table (SQLite)')
                        )
                        return
                
                # PostgreSQL path
                column_exists = cursor.fetchone()
                
                if not column_exists:
                    # Add the photo column
                    cursor.execute("""
                        ALTER TABLE core_dailylog 
                        ADD COLUMN photo VARCHAR(100)
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo column to core_dailylog table (PostgreSQL)')
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
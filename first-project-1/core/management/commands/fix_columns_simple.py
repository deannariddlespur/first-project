from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add missing columns using raw SQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Adding missing columns with raw SQL...')
        
        try:
            with connection.cursor() as cursor:
                # Add photo_base64 column to core_dog table
                try:
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_base64 TEXT
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo_base64 column to core_dog table')
                    )
                except Exception as e:
                    if 'already exists' in str(e) or 'duplicate column' in str(e):
                        self.stdout.write(
                            self.style.WARNING('⚠️ photo_base64 column already exists in core_dog table')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Error adding photo_base64 column: {e}')
                        )
                
                # Add photo column to core_dailylog table
                try:
                    cursor.execute("""
                        ALTER TABLE core_dailylog 
                        ADD COLUMN photo VARCHAR(100)
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo column to core_dailylog table')
                    )
                except Exception as e:
                    if 'already exists' in str(e) or 'duplicate column' in str(e):
                        self.stdout.write(
                            self.style.WARNING('⚠️ photo column already exists in core_dailylog table')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Error adding photo column: {e}')
                        )
                        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise 
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Force add missing columns and verify they exist'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Force adding missing columns with verification...')
        
        try:
            with connection.cursor() as cursor:
                # Force add photo_base64 column to core_dog table
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
                
                # Force add photo column to core_dailylog table
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
                
                # Verify the columns exist by querying them
                self.stdout.write('🔍 Verifying columns exist by querying them...')
                try:
                    # Test querying the photo_base64 column
                    cursor.execute("SELECT photo_base64 FROM core_dog LIMIT 1")
                    self.stdout.write(
                        self.style.SUCCESS('✅ Verified: photo_base64 column exists and is queryable')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ ERROR: photo_base64 column is NOT queryable: {e}')
                    )
                
                try:
                    # Test querying the photo column
                    cursor.execute("SELECT photo FROM core_dailylog LIMIT 1")
                    self.stdout.write(
                        self.style.SUCCESS('✅ Verified: photo column exists and is queryable')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ ERROR: photo column is NOT queryable: {e}')
                    )
                        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise 
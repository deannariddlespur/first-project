from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Force add missing columns to database tables'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Force adding missing columns...')
        
        try:
            with connection.cursor() as cursor:
                # Force add photo_base64 column to core_dog table
                try:
                    # First check if column exists
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dog' 
                        AND column_name = 'photo_base64'
                    """)
                    exists = cursor.fetchone()
                    
                    if not exists:
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
                        self.style.ERROR(f'❌ Error with photo_base64 column: {e}')
                    )
                
                # Force add photo column to core_dailylog table
                try:
                    # First check if column exists
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dailylog' 
                        AND column_name = 'photo'
                    """)
                    exists = cursor.fetchone()
                    
                    if not exists:
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
                        self.style.ERROR(f'❌ Error with photo column: {e}')
                    )
                
                # Verify the columns exist
                self.stdout.write('🔍 Verifying columns exist...')
                try:
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dog' 
                        AND column_name = 'photo_base64'
                    """)
                    if cursor.fetchone():
                        self.stdout.write(
                            self.style.SUCCESS('✅ Verified: photo_base64 column exists in core_dog')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR('❌ ERROR: photo_base64 column does NOT exist in core_dog')
                        )
                        
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dailylog' 
                        AND column_name = 'photo'
                    """)
                    if cursor.fetchone():
                        self.stdout.write(
                            self.style.SUCCESS('✅ Verified: photo column exists in core_dailylog')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR('❌ ERROR: photo column does NOT exist in core_dailylog')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error verifying columns: {e}')
                    )
                        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise 
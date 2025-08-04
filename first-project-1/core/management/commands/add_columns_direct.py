from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add missing columns directly using SQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Adding missing columns directly with SQL...')
        
        try:
            with connection.cursor() as cursor:
                # Add photo_base64 column to core_dog table
                try:
                    cursor.execute("ALTER TABLE core_dog ADD COLUMN IF NOT EXISTS photo_base64 TEXT")
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo_base64 column to core_dog table')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error adding photo_base64 column: {e}')
                    )
                
                # Add photo column to core_dailylog table
                try:
                    cursor.execute("ALTER TABLE core_dailylog ADD COLUMN IF NOT EXISTS photo VARCHAR(100)")
                    self.stdout.write(
                        self.style.SUCCESS('✅ Added photo column to core_dailylog table')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error adding photo column: {e}')
                    )
                
                # Test the exact query that's failing
                try:
                    cursor.execute("""
                        SELECT "core_dailylog"."id", "core_dailylog"."booking_id", 
                               "core_dailylog"."date", "core_dailylog"."feeding", 
                               "core_dailylog"."medication", "core_dailylog"."exercise", 
                               "core_dailylog"."notes", "core_dailylog"."photo" 
                        FROM "core_dailylog" ORDER BY "core_dailylog"."id" DESC
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ The exact failing query now works!')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ The exact failing query still fails: {e}')
                    )
                        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            raise 
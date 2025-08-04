from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Test if columns exist by running direct queries'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Testing if columns exist...')
        
        try:
            with connection.cursor() as cursor:
                # Test photo_base64 column in core_dog
                try:
                    cursor.execute("SELECT photo_base64 FROM core_dog LIMIT 1")
                    self.stdout.write(
                        self.style.SUCCESS('✅ photo_base64 column exists and is queryable in core_dog')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ photo_base64 column does NOT exist in core_dog: {e}')
                    )
                
                # Test photo column in core_dailylog
                try:
                    cursor.execute("SELECT photo FROM core_dailylog LIMIT 1")
                    self.stdout.write(
                        self.style.SUCCESS('✅ photo column exists and is queryable in core_dailylog')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ photo column does NOT exist in core_dailylog: {e}')
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
                        self.style.SUCCESS('✅ The exact failing query works!')
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
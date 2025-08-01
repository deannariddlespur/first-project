from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add missing photo column to core_dailylog table'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Check if the column already exists
                cursor.execute("PRAGMA table_info(core_dailylog)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'photo' not in columns:
                    # Add the photo column
                    cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100) NULL")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully added photo column to core_dailylog table')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Photo column already exists in core_dailylog table')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error adding photo column: {e}')
                ) 
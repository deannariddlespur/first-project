from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add photo_url column to Railway database'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Adding photo_url column to Railway database...")
        
        try:
            with connection.cursor() as cursor:
                # Check if column exists (SQLite compatible)
                cursor.execute("PRAGMA table_info(core_dog)")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns]
                
                if 'photo_url' not in column_names:
                    self.stdout.write("📝 Adding photo_url column...")
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_url TEXT
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ photo_url column added successfully!"))
                else:
                    self.stdout.write("✅ photo_url column already exists")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error adding photo_url column: {e}"))
            self.stdout.write(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}") 
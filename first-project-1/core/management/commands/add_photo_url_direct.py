from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add photo_url column directly to database'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Adding photo_url column directly to database...")
        
        try:
            with connection.cursor() as cursor:
                # Check if column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_dog' AND column_name = 'photo_url'
                """)
                exists = cursor.fetchone()
                
                if not exists:
                    self.stdout.write("📝 Adding photo_url column...")
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_url VARCHAR(500) NULL
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ photo_url column added successfully!"))
                else:
                    self.stdout.write("✅ photo_url column already exists")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error adding photo_url column: {e}"))
            self.stdout.write(f"🔍 DEBUG: Exception details: {type(e).__name__}: {str(e)}") 
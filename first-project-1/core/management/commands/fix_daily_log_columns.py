from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix missing photo column in DailyLog table'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing DailyLog photo column...")
        
        try:
            with connection.cursor() as cursor:
                # Check if photo column exists
                cursor.execute("PRAGMA table_info(core_dailylog)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                if 'photo' in column_names:
                    self.stdout.write(self.style.SUCCESS("✅ photo column already exists"))
                else:
                    self.stdout.write("❌ photo column missing, adding...")
                    cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100)")
                    self.stdout.write(self.style.SUCCESS("✅ photo column added successfully"))
                
                # Also check photo_base64 in core_dog
                cursor.execute("PRAGMA table_info(core_dog)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                if 'photo_base64' in column_names:
                    self.stdout.write(self.style.SUCCESS("✅ photo_base64 column already exists"))
                else:
                    self.stdout.write("❌ photo_base64 column missing, adding...")
                    cursor.execute("ALTER TABLE core_dog ADD COLUMN photo_base64 TEXT")
                    self.stdout.write(self.style.SUCCESS("✅ photo_base64 column added successfully"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            return
            
        self.stdout.write(self.style.SUCCESS("🎯 DailyLog columns fix completed!")) 
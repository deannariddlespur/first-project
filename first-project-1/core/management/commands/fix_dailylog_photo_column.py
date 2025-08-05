from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add missing photo column to DailyLog table'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Adding photo column to DailyLog table...")
        
        try:
            with connection.cursor() as cursor:
                # Check if we're using SQLite or PostgreSQL
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_dailylog'")
                tables = cursor.fetchall()
                
                if tables:
                    # SQLite database
                    self.stdout.write("✅ Using SQLite database")
                    
                    # Check if photo column exists
                    cursor.execute("PRAGMA table_info(core_dailylog)")
                    columns = [column[1] for column in cursor.fetchall()]
                    
                    if 'photo' not in columns:
                        cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(500)")
                        self.stdout.write("✅ Added photo column to core_dailylog table")
                    else:
                        self.stdout.write("✅ Photo column already exists")
                        
                else:
                    # PostgreSQL database
                    self.stdout.write("✅ Using PostgreSQL database")
                    
                    # Check if photo column exists
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'core_dailylog' AND column_name = 'photo'
                    """)
                    columns = cursor.fetchall()
                    
                    if not columns:
                        cursor.execute("ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(500)")
                        self.stdout.write("✅ Added photo column to core_dailylog table")
                    else:
                        self.stdout.write("✅ Photo column already exists")
                
                self.stdout.write("✅ DailyLog photo column fix completed!")
                
        except Exception as e:
            self.stdout.write(f"❌ Error fixing DailyLog photo column: {e}")
            self.stdout.write(f"🔍 Error type: {type(e)}") 
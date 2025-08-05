from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Force apply the photo field length migration'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Force applying photo field length migration...")
        
        try:
            with connection.cursor() as cursor:
                # Check current column definition
                cursor.execute("""
                    SELECT column_name, data_type, character_maximum_length 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_dog' AND column_name = 'photo'
                """)
                result = cursor.fetchone()
                
                if result:
                    column_name, data_type, max_length = result
                    self.stdout.write(f"🔍 Current photo column: {column_name}, type: {data_type}, max_length: {max_length}")
                    
                    if max_length and max_length < 500:
                        # Alter the column to increase max_length
                        cursor.execute("""
                            ALTER TABLE core_dog 
                            ALTER COLUMN photo TYPE VARCHAR(500)
                        """)
                        self.stdout.write("✅ Photo field length increased to 500")
                    else:
                        self.stdout.write("✅ Photo field already has sufficient length")
                else:
                    self.stdout.write("❌ Photo column not found")
                    
        except Exception as e:
            self.stdout.write(f"❌ Error applying migration: {e}")
            self.stdout.write(f"🔍 Error type: {type(e)}")
            
        # Also try to apply the Django migration directly
        try:
            from django.core.management import call_command
            self.stdout.write("🔄 Attempting to apply Django migration...")
            call_command('migrate', 'core', '0013_fix_photo_field_length')
            self.stdout.write("✅ Django migration applied successfully!")
        except Exception as e:
            self.stdout.write(f"❌ Django migration failed: {e}")
            self.stdout.write(f"🔍 Django migration error type: {type(e)}") 
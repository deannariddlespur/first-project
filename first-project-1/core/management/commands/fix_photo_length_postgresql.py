from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix photo field length using PostgreSQL syntax'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing photo field length with PostgreSQL syntax...")
        
        try:
            with connection.cursor() as cursor:
                # Check current length using PostgreSQL syntax
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
                        # Use PostgreSQL ALTER COLUMN syntax
                        self.stdout.write("🔄 Altering photo column to VARCHAR(500) with PostgreSQL syntax...")
                        cursor.execute("""
                            ALTER TABLE core_dog 
                            ALTER COLUMN photo TYPE VARCHAR(500)
                        """)
                        
                        # Verify the change
                        cursor.execute("""
                            SELECT column_name, data_type, character_maximum_length 
                            FROM information_schema.columns 
                            WHERE table_name = 'core_dog' AND column_name = 'photo'
                        """)
                        new_result = cursor.fetchone()
                        
                        if new_result:
                            new_column_name, new_data_type, new_max_length = new_result
                            self.stdout.write(f"✅ Photo column updated: {new_column_name}, type: {new_data_type}, max_length: {new_max_length}")
                        else:
                            self.stdout.write("❌ Could not verify column change")
                    else:
                        self.stdout.write("✅ Photo field already has sufficient length")
                else:
                    self.stdout.write("❌ Photo column not found")
                    
        except Exception as e:
            self.stdout.write(f"❌ Error fixing photo field length: {e}")
            self.stdout.write(f"🔍 Error type: {type(e)}") 
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add supabase_url column directly with SQL'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Adding supabase_url column directly with SQL...")
        
        try:
            with connection.cursor() as cursor:
                # Check if column already exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_dog' AND column_name = 'supabase_url'
                """)
                result = cursor.fetchone()
                
                if result:
                    self.stdout.write("✅ supabase_url column already exists")
                else:
                    # Add the column
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN supabase_url VARCHAR(1000) NULL
                    """)
                    self.stdout.write("✅ supabase_url column added successfully!")
                    
        except Exception as e:
            self.stdout.write(f"❌ Error adding supabase_url column: {e}")
            self.stdout.write(f"🔍 Error type: {type(e)}")
            
            # Try alternative approach for PostgreSQL
            try:
                self.stdout.write("🔄 Trying alternative PostgreSQL approach...")
                with connection.cursor() as cursor:
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN supabase_url VARCHAR(1000)
                    """)
                    self.stdout.write("✅ Alternative approach succeeded!")
            except Exception as e2:
                self.stdout.write(f"❌ Alternative approach also failed: {e2}") 
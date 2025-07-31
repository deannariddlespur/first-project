from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix database schema by adding missing columns'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing database schema...")

        try:
            with connection.cursor() as cursor:
                # Add missing columns to core_dog table
                self.stdout.write("Adding photo_base64 column...")
                try:
                    cursor.execute("""
                        ALTER TABLE core_dog 
                        ADD COLUMN photo_base64 TEXT;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ photo_base64 column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ photo_base64 column might already exist: {e}")
                
                # Add missing columns to core_booking table
                self.stdout.write("Adding booking columns...")
                try:
                    cursor.execute("""
                        ALTER TABLE core_booking 
                        ADD COLUMN total_amount DECIMAL(8,2) NULL;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ total_amount column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ total_amount column might already exist: {e}")
                
                try:
                    cursor.execute("""
                        ALTER TABLE core_booking 
                        ADD COLUMN price_per_night DECIMAL(6,2) NULL;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ price_per_night column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ price_per_night column might already exist: {e}")
                
                # Add missing columns to core_payment table
                self.stdout.write("Adding payment columns...")
                try:
                    cursor.execute("""
                        ALTER TABLE core_payment 
                        ADD COLUMN payment_method VARCHAR(20) NULL;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ payment_method column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ payment_method column might already exist: {e}")
                
                try:
                    cursor.execute("""
                        ALTER TABLE core_payment 
                        ADD COLUMN paid_date TIMESTAMP NULL;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ paid_date column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ paid_date column might already exist: {e}")
                
                # Add missing columns to core_staffnote table
                self.stdout.write("Adding staff note columns...")
                try:
                    cursor.execute("""
                        ALTER TABLE core_staffnote 
                        ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                    """)
                    self.stdout.write(self.style.SUCCESS("✅ created_at column added"))
                except Exception as e:
                    self.stdout.write(f"⚠️ created_at column might already exist: {e}")
                
            self.stdout.write(self.style.SUCCESS("✅ Database schema fixed successfully!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error fixing database: {e}")) 
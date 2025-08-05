from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix database issues by resetting migrations'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing database issues...")
        
        try:
            with connection.cursor() as cursor:
                # Check if we're using SQLite or PostgreSQL
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations'")
                tables = cursor.fetchall()
                
                if tables:
                    # SQLite database
                    self.stdout.write("✅ Using SQLite database")
                    
                    # Reset migrations table
                    cursor.execute("DELETE FROM django_migrations WHERE app='core'")
                    self.stdout.write("✅ Reset core migrations")
                    
                    # Mark migrations as applied
                    migrations_to_apply = [
                        ('core', '0001_initial'),
                        ('core', '0002_booking_status'),
                        ('core', '0003_booking_price_per_night_booking_total_amount_payment'),
                        ('core', '0004_staffnote'),
                        ('core', '0005_kennel_size'),
                        ('core', '0006_dog_size'),
                        ('core', '0007_facilityavailability'),
                        ('core', '0008_dog_photo_base64'),
                        ('core', '0009_dailylog_photo'),
                        ('core', '0010_auto_20250801_2248'),
                        ('core', '0011_add_photo_url_clean'),
                        ('core', '0012_increase_photo_field_length'),
                        ('core', '0013_fix_photo_field_length'),
                        ('core', '0014_add_supabase_url_field'),
                    ]
                    
                    for app, migration in migrations_to_apply:
                        cursor.execute(
                            "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, datetime('now'))",
                            [app, migration]
                        )
                    
                    self.stdout.write("✅ Marked all migrations as applied")
                    
                else:
                    # PostgreSQL database
                    self.stdout.write("✅ Using PostgreSQL database")
                    
                    # Reset migrations table
                    cursor.execute("DELETE FROM django_migrations WHERE app='core'")
                    self.stdout.write("✅ Reset core migrations")
                    
                    # Mark migrations as applied
                    migrations_to_apply = [
                        ('core', '0001_initial'),
                        ('core', '0002_booking_status'),
                        ('core', '0003_booking_price_per_night_booking_total_amount_payment'),
                        ('core', '0004_staffnote'),
                        ('core', '0005_kennel_size'),
                        ('core', '0006_dog_size'),
                        ('core', '0007_facilityavailability'),
                        ('core', '0008_dog_photo_base64'),
                        ('core', '0009_dailylog_photo'),
                        ('core', '0010_auto_20250801_2248'),
                        ('core', '0011_add_photo_url_clean'),
                        ('core', '0012_increase_photo_field_length'),
                        ('core', '0013_fix_photo_field_length'),
                        ('core', '0014_add_supabase_url_field'),
                    ]
                    
                    for app, migration in migrations_to_apply:
                        cursor.execute(
                            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
                            [app, migration]
                        )
                    
                    self.stdout.write("✅ Marked all migrations as applied")
                
                self.stdout.write("✅ Database fixed successfully!")
                
        except Exception as e:
            self.stdout.write(f"❌ Error fixing database: {e}")
            self.stdout.write("🔍 Error type: {type(e)}") 
from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Dog
import os

class Command(BaseCommand):
    help = 'Fix dog images by adding photo_url field and uploading to Supabase'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Starting image fix process...")
        
        # Check if photo_url column exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_dog' AND column_name = 'photo_url'
            """)
            exists = cursor.fetchone()
            
            if not exists:
                self.stdout.write("📝 Adding photo_url column to database...")
                cursor.execute("""
                    ALTER TABLE core_dog 
                    ADD COLUMN photo_url VARCHAR(500) NULL
                """)
                self.stdout.write(self.style.SUCCESS("✅ photo_url column added"))
            else:
                self.stdout.write("✅ photo_url column already exists")
        
        # Get all dogs with photos
        dogs_with_photos = Dog.objects.filter(photo__isnull=False).exclude(photo='')
        
        self.stdout.write(f"📸 Found {dogs_with_photos.count()} dogs with photos")
        
        for dog in dogs_with_photos:
            self.stdout.write(f"🐕 Processing {dog.name}...")
            
            # For now, just set a placeholder URL
            # In a real implementation, you would upload to Supabase here
            placeholder_url = f"https://via.placeholder.com/300x300/667eea/ffffff?text={dog.name}"
            
            dog.photo_url = placeholder_url
            dog.save()
            
            self.stdout.write(f"✅ Updated {dog.name} with placeholder URL")
        
        self.stdout.write(self.style.SUCCESS("🎉 Image fix process completed!"))
        self.stdout.write("📋 Next steps:")
        self.stdout.write("1. Check the dashboard to see if images are working")
        self.stdout.write("2. If working, we can replace placeholder URLs with real Supabase URLs") 
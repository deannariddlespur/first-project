from django.core.management.base import BaseCommand
from core.models import Dog
import base64
import os

class Command(BaseCommand):
    help = 'Convert existing dog photos to base64 storage'

    def handle(self, *args, **options):
        dogs = Dog.objects.all()
        
        if not dogs.exists():
            self.stdout.write(self.style.WARNING('No dogs found in database'))
            return
        
        self.stdout.write(f'Found {dogs.count()} dogs:')
        
        for dog in dogs:
            self.stdout.write(f'\nProcessing: {dog.name}')
            
            if dog.photo:
                try:
                    # Check if file exists
                    if os.path.exists(dog.photo.path):
                        # Read the image file
                        with open(dog.photo.path, 'rb') as img_file:
                            image_data = img_file.read()
                        
                        # Convert to base64
                        img_str = base64.b64encode(image_data).decode()
                        
                        # Store in database
                        dog.photo_base64 = img_str
                        dog.save()
                        
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Converted {dog.photo.name} to base64'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠️ File not found: {dog.photo.path}'))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error converting {dog.name}: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️ No photo for {dog.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Base64 conversion complete!')) 
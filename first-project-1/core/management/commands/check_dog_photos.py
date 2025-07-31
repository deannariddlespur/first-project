from django.core.management.base import BaseCommand
from core.models import Dog

class Command(BaseCommand):
    help = 'Check dog photos in the database'

    def handle(self, *args, **options):
        dogs = Dog.objects.all()
        
        if not dogs.exists():
            self.stdout.write(self.style.WARNING('No dogs found in database'))
            return
        
        self.stdout.write(f'Found {dogs.count()} dogs:')
        
        for dog in dogs:
            self.stdout.write(f'\nDog: {dog.name}')
            self.stdout.write(f'  Photo field: {dog.photo}')
            self.stdout.write(f'  Photo URL: {dog.get_photo_url()}')
            self.stdout.write(f'  Photo exists: {bool(dog.photo)}')
            
            if dog.photo:
                self.stdout.write(f'  Photo name: {dog.photo.name}')
                self.stdout.write(f'  Photo path: {dog.photo.path}')
                
                # Check if file actually exists
                import os
                if os.path.exists(dog.photo.path):
                    self.stdout.write(self.style.SUCCESS('  ✓ File exists on disk'))
                else:
                    self.stdout.write(self.style.ERROR('  ✗ File does not exist on disk')) 
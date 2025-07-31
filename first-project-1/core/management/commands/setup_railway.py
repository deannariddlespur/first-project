from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import Kennel

class Command(BaseCommand):
    help = 'Setup Railway deployment with migrations and initial data'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Running migrations...')
        
        try:
            # Run migrations
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed successfully!'))
            
            # Create admin user if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                User.objects.create_user(
                    username='admin',
                    email='admin@dogboarding.com',
                    password='admin123456',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(self.style.SUCCESS('✅ Admin user created: admin/admin123456'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ Admin user already exists'))
            
            # Create sample kennels if they don't exist
            kennel_sizes = [
                ('Small Kennel A', 'small', 'Cozy kennel for small dogs'),
                ('Small Kennel B', 'small', 'Cozy kennel for small dogs'),
                ('Medium Kennel A', 'medium', 'Comfortable kennel for medium dogs'),
                ('Medium Kennel B', 'medium', 'Comfortable kennel for medium dogs'),
                ('Large Kennel A', 'large', 'Spacious kennel for large dogs'),
                ('Large Kennel B', 'large', 'Spacious kennel for large dogs'),
            ]
            
            for name, size, description in kennel_sizes:
                Kennel.objects.get_or_create(
                    name=name,
                    defaults={
                        'size': size,
                        'description': description
                    }
                )
            self.stdout.write(self.style.SUCCESS('✅ Sample kennels created'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during setup: {e}'))
            raise 
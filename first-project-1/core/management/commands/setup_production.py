from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Kennel
from django.db import connection

class Command(BaseCommand):
    help = 'Set up production database with migrations and initial data'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Setting up production database...')
        
        # Check if we can connect to the database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('✅ Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            return

        # Create default kennels if they don't exist
        kennel_sizes = [
            ('Small Kennel A', 'small', 'Cozy kennel for small dogs'),
            ('Small Kennel B', 'small', 'Cozy kennel for small dogs'),
            ('Medium Kennel A', 'medium', 'Comfortable kennel for medium dogs'),
            ('Medium Kennel B', 'medium', 'Comfortable kennel for medium dogs'),
            ('Large Kennel A', 'large', 'Spacious kennel for large dogs'),
            ('Large Kennel B', 'large', 'Spacious kennel for large dogs'),
        ]
        
        created_count = 0
        for name, size, description in kennel_sizes:
            kennel, created = Kennel.objects.get_or_create(
                name=name,
                defaults={
                    'size': size,
                    'description': description,
                    'is_available': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'✅ Created kennel: {name}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} kennels'))
        
        # Check if admin user exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dogboarding.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123456')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created admin user (admin/admin123456)'))
        else:
            self.stdout.write('ℹ️ Admin user already exists')
        
        self.stdout.write(self.style.SUCCESS('🎉 Production database setup complete!'))
        self.stdout.write('📝 You can now:')
        self.stdout.write('   - Login as admin (admin/admin123456)')
        self.stdout.write('   - Access the admin dashboard')
        self.stdout.write('   - Create owner accounts')
        self.stdout.write('   - Start managing bookings!') 
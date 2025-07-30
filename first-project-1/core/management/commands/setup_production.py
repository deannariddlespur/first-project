from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from core.models import Owner, Kennel
from datetime import date

class Command(BaseCommand):
    help = 'Set up production database with initial users and data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up production database...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@dogboarding.com',
                password='admin123456',
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created admin user: {admin_user.username}')
            )
        else:
            self.stdout.write('ℹ️ Admin user already exists')
        
        # Create sample owner
        if not User.objects.filter(username='jane.doe').exists():
            owner_user = User.objects.create_user(
                username='jane.doe',
                email='jane@example.com',
                password='password123',
                first_name='Jane',
                last_name='Doe'
            )
            
            owner = Owner.objects.create(
                user=owner_user,
                phone='646-577-3608',
                address='123 Main Street, New York, NY'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created owner: {owner.user.username}')
            )
        else:
            self.stdout.write('ℹ️ Owner user already exists')
        
        # Create sample kennels
        kennel_data = [
            {'name': 'Kennel 001', 'description': 'Small kennel for small dogs', 'size': 'small'},
            {'name': 'Kennel 002', 'description': 'Medium kennel for medium dogs', 'size': 'medium'},
            {'name': 'Kennel 003', 'description': 'Large kennel for large dogs', 'size': 'large'},
            {'name': 'Kennel 004', 'description': 'Small kennel for small dogs', 'size': 'small'},
            {'name': 'Kennel 005', 'description': 'Medium kennel for medium dogs', 'size': 'medium'},
            {'name': 'Kennel 006', 'description': 'Large kennel for large dogs', 'size': 'large'},
        ]
        
        created_kennels = 0
        for kennel_info in kennel_data:
            if not Kennel.objects.filter(name=kennel_info['name']).exists():
                kennel = Kennel.objects.create(**kennel_info)
                created_kennels += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created kennel: {kennel.name} ({kennel.get_size_display()})')
                )
        
        if created_kennels == 0:
            self.stdout.write('ℹ️ All kennels already exist')
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created {created_kennels} kennels')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Production database setup complete!')
        )
        self.stdout.write('\n📋 Login Credentials:')
        self.stdout.write('👨‍💼 Admin: username=admin, password=admin123456')
        self.stdout.write('🏠 Owner: username=jane.doe, password=password123')
        self.stdout.write('\n🔗 URLs:')
        self.stdout.write('- Homepage: /')
        self.stdout.write('- Admin: /admin/')
        self.stdout.write('- Staff Login: /staff/login/')
        self.stdout.write('- Owner Login: /login/')
        self.stdout.write('- Owner Registration: /register/') 
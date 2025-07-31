#!/usr/bin/env python3
"""
Run Django migrations automatically
"""
import os
import sys
import django
from django.core.management import call_command

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings_production')

# Setup Django
django.setup()

print("🔄 Running Django migrations...")

try:
    # Run migrations
    call_command('migrate')
    print("✅ Migrations completed successfully!")
    
    # Create admin user if it doesn't exist
    from django.contrib.auth.models import User
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
        print("✅ Admin user created: admin/admin123456")
    else:
        print("✅ Admin user already exists")
    
    # Create sample kennels if they don't exist
    from core.models import Kennel
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
    print("✅ Sample kennels created")
    
except Exception as e:
    print(f"❌ Error during migrations: {e}")
    sys.exit(1)

print("🎯 Database setup complete!") 
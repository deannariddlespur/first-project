#!/usr/bin/env python
"""
Railway Database Setup Script
Run this to set up your Railway database manually
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def setup_database():
    """Set up the Railway database"""
    print("🚀 Setting up Railway database...")
    
    try:
        # Run migrations
        print("📦 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed")
        
        # Run our setup command
        print("🔧 Running production setup...")
        execute_from_command_line(['manage.py', 'setup_production'])
        print("✅ Production setup completed")
        
        print("\n🎉 Database setup complete!")
        print("📝 You can now:")
        print("   - Visit your Railway app")
        print("   - Login as admin (admin/admin123456)")
        print("   - Start using your dog boarding app!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try running this script again in a few minutes")

if __name__ == '__main__':
    setup_database() 
#!/usr/bin/env python
"""
Simple script to fix session table issue
Run this if you get access to Railway console
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("🔧 Fixing session table issue...")
    try:
        # Run migrations to create missing tables
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Session table fixed!")
        print("🎉 Your app should now work without session errors!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try running this script again") 
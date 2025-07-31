#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Running migrations on Railway...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrations completed!") 
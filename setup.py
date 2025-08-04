#!/usr/bin/env python3

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpi_monitor.settings')
    django.setup()

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created with password 'admin123'")

def main():
    setup_django()
    
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Creating superuser...")
    create_superuser()
    
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Setup completed!")

if __name__ == '__main__':
    main()
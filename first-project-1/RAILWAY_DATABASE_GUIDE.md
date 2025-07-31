# 🚀 Railway Database Setup Guide

A comprehensive guide for setting up PostgreSQL databases in Railway for Django applications.

## 📋 Table of Contents

1. [Adding PostgreSQL to Railway](#adding-postgresql-to-railway)
2. [Environment Variables](#environment-variables)
3. [Django Configuration](#django-configuration)
4. [Database Migrations](#database-migrations)
5. [Initial Data Setup](#initial-data-setup)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## 🗄️ Adding PostgreSQL to Railway

### Step 1: Access Your Railway Project
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your Django project
3. Click on your Django service

### Step 2: Add PostgreSQL Plugin
1. Click the **"+ Create"** button
2. Select **"Database"** from the dropdown
3. Choose **"PostgreSQL"**
4. Click **"Deploy"**

### Step 3: Verify Database Creation
- Railway will automatically create a PostgreSQL database
- The `DATABASE_URL` environment variable will be automatically set
- You can see the database in your project's service list

---

## 🔧 Environment Variables

### Automatic Variables (Set by Railway)
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### Manual Variables (Add if needed)
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app

# Database Settings (optional)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
```

### How to Add Variables
1. Go to your Django service in Railway
2. Click **"Variables"** tab
3. Click **"New Variable"**
4. Add key-value pairs as needed

---

## ⚙️ Django Configuration

### Production Settings (`settings_production.py`)
```python
import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Update with your domain

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Use PostgreSQL on Railway
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    print(f"✅ Using PostgreSQL database from DATABASE_URL")
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print(f"⚠️ Using SQLite database (not persistent on Railway)")

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security (disable for testing, enable for production)
SECURE_SSL_REDIRECT = False  # Set to True for production
SESSION_COOKIE_SECURE = False  # Set to True for production
CSRF_COOKIE_SECURE = False  # Set to True for production
```

### Requirements (`requirements.txt`)
```txt
Django==5.2.4
dj-database-url==2.1.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
whitenoise==6.9.0
```

### WSGI Configuration (`wsgi.py`)
```python
import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_NAME'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

application = get_wsgi_application()
```

---

## 🔄 Database Migrations

### Automatic Migration Script (`run_migrations.py`)
```python
#!/usr/bin/env python3
"""
Run Django migrations automatically
"""
import os
import sys
import django
from django.core.management import call_command

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings_production')

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
            email='admin@yourproject.com',
            password='admin123456',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        print("✅ Admin user created: admin/admin123456")
    else:
        print("✅ Admin user already exists")
    
except Exception as e:
    print(f"❌ Error during migrations: {e}")
    sys.exit(1)

print("🎯 Database setup complete!")
```

### Health Check Server (`health_server.py`)
```python
#!/usr/bin/env python3
"""
Simple health check server for Railway
"""
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'message': 'Your Django App is running',
                'timestamp': time.time()
            }
            self.wfile.write(str(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Your Django App</h1><p>Starting up...</p>')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🏥 Health check server listening on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    # Start health server in background
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    time.sleep(2)
    
    # Run migrations before starting Django
    print("🔄 Running database migrations...")
    try:
        os.system('python run_migrations.py')
        print("✅ Database setup complete!")
    except Exception as e:
        print(f"⚠️ Migration warning: {e}")
    
    # Start Django application
    print("🚀 Starting Django application...")
    os.execvp('gunicorn', [
        'gunicorn',
        'yourproject.wsgi:application',
        '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
        '--workers', '1',
        '--timeout', '120',
        '--log-file', '-'
    ])
```

### Procfile
```bash
web: python health_server.py
```

---

## 📊 Initial Data Setup

### Creating Sample Data
```python
# In your migration script or management command
from yourproject.models import YourModel

# Create sample data
sample_data = [
    {'name': 'Sample 1', 'description': 'Description 1'},
    {'name': 'Sample 2', 'description': 'Description 2'},
]

for data in sample_data:
    YourModel.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
```

### Admin User Creation
```python
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_user(
        username='admin',
        email='admin@yourproject.com',
        password='admin123456',
        first_name='Admin',
        last_name='User',
        is_staff=True,
        is_superuser=True
    )
```

---

## 📈 Monitoring & Maintenance

### Database Health Check
```python
def health_check(request):
    """Simple health check endpoint"""
    from django.http import JsonResponse
    import time
    
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': time.time()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }, status=500)
```

### URL Configuration
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    # ... other URLs
]
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "no such table: auth_user"
**Solution:** Run migrations
```bash
python manage.py migrate
```

#### 2. "ModuleNotFoundError: No module named 'dj_database_url'"
**Solution:** Add to requirements.txt
```txt
dj-database-url==2.1.0
```

#### 3. Container stops immediately
**Solution:** Use health check server
- Implement health check server
- Ensure immediate response to `/health/`
- Run migrations in background

#### 4. Database connection errors
**Solution:** Check environment variables
- Verify `DATABASE_URL` is set
- Check PostgreSQL plugin is added
- Ensure correct database credentials

#### 5. SSL redirect issues
**Solution:** Disable for testing
```python
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### Debug Commands
```bash
# Check environment variables
echo $DATABASE_URL

# Test database connection
python manage.py dbshell

# Run migrations manually
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 🏆 Best Practices

### 1. Environment Management
- Use separate settings files for development/production
- Never commit sensitive data to version control
- Use environment variables for all secrets

### 2. Database Security
- Use strong passwords for database users
- Enable SSL connections in production
- Regularly backup your database

### 3. Performance
- Use connection pooling (`conn_max_age`)
- Enable database health checks
- Monitor database performance

### 4. Deployment
- Always run migrations before starting the app
- Use health checks to ensure app is ready
- Implement graceful shutdown handling

### 5. Monitoring
- Set up logging for database operations
- Monitor database connection errors
- Track migration success/failure

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Django Database Documentation](https://docs.djangoproject.com/en/5.2/topics/db/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [dj-database-url Documentation](https://github.com/jacobian/dj-database-url)

---

## 🎯 Quick Start Checklist

- [ ] Add PostgreSQL plugin to Railway
- [ ] Verify `DATABASE_URL` environment variable
- [ ] Update Django settings for production
- [ ] Add required packages to requirements.txt
- [ ] Create health check endpoint
- [ ] Set up automatic migrations
- [ ] Test database connection
- [ ] Deploy and verify functionality

---

**Happy deploying! 🚀** 
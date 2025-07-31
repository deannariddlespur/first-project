# 🚀 Railway Database Setup Guide

## Complete Step-by-Step Guide to Set Up PostgreSQL in Railway

This guide will help you set up a stable PostgreSQL database in Railway to avoid connection issues and deployment problems.

---

## 📋 Prerequisites

- Railway account (free tier works fine)
- GitHub repository with your Django project
- Basic understanding of environment variables

---

## 🎯 Step 1: Create Railway Project

### 1.1 Go to Railway Dashboard
- Visit [railway.app](https://railway.app)
- Sign in with your GitHub account
- Click "New Project"

### 1.2 Choose Deployment Method
- Select "Deploy from GitHub repo"
- Choose your repository: `deannariddlespur/first-project`
- Railway will automatically detect it's a Django project

---

## 🗄️ Step 2: Add PostgreSQL Database

### 2.1 Add PostgreSQL Plugin
- In your Railway project dashboard
- Click "New" → "Database" → "PostgreSQL"
- Railway will create a new PostgreSQL database

### 2.2 Verify Database Creation
- You should see a new PostgreSQL service in your project
- Note the database name (usually something like `postgresql-12345`)

---

## ⚙️ Step 3: Configure Environment Variables

### 3.1 Access Environment Variables
- In your Railway project dashboard
- Click on your main Django service (not the database)
- Go to "Variables" tab

### 3.2 Set Required Variables
Add these environment variables:

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=dogboarding.settings_production
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False

# Database (Railway will auto-set this)
DATABASE_URL=postgresql://username:password@host:port/database

# Optional: Custom domain
RAILWAY_STATIC_URL=your-custom-domain.com
```

### 3.3 Get Database URL
- Click on your PostgreSQL service in Railway
- Go to "Connect" tab
- Copy the "Postgres Connection URL"
- Paste it as the `DATABASE_URL` value

---

## 🔧 Step 4: Update Django Settings

### 4.1 Verify Production Settings
Your `dogboarding/settings_production.py` should look like this:

```python
import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Update with your domain later

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=0,  # Disable connection pooling
            conn_health_checks=False  # Disable health checks
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
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### 4.2 Verify Requirements
Your `requirements.txt` should include:

```txt
Django==5.2.4
dj-database-url==2.1.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
whitenoise==6.9.0
```

---

## 🚀 Step 5: Deploy and Test

### 5.1 Push Your Code
```bash
git add .
git commit -m "Configure for Railway PostgreSQL"
git push origin main
```

### 5.2 Monitor Deployment
- Go to Railway dashboard
- Watch the deployment logs
- Look for these success messages:
  - ✅ "Migrations completed successfully"
  - ✅ "Database connection test successful"
  - ✅ "Starting gunicorn"

### 5.3 Test Your Application
- Click on your Railway URL
- Try accessing the admin panel: `/admin/`
- Test creating a booking

---

## 🔍 Step 6: Troubleshooting Common Issues

### 6.1 Database Connection Errors
**Problem**: `could not receive data from client: Connection reset by peer`

**Solution**:
- Ensure `conn_max_age=0` in settings
- Disable `conn_health_checks=False`
- Add retry logic in startup script

### 6.2 Migration Errors
**Problem**: `django.db.utils.OperationalError: relation "django_session" does not exist`

**Solution**:
- Ensure migrations run before app starts
- Check that `DATABASE_URL` is set correctly
- Verify PostgreSQL plugin is added

### 6.3 Static Files Not Loading
**Problem**: CSS/JS files return 404

**Solution**:
- Ensure `STATIC_ROOT` is set
- Use `whitenoise` for static file serving
- Run `python manage.py collectstatic` in startup

---

## 📊 Step 7: Monitoring and Maintenance

### 7.1 Check Database Health
- Go to PostgreSQL service in Railway
- Check "Metrics" tab for connection stats
- Monitor "Logs" for any errors

### 7.2 Backup Strategy
- Railway automatically backs up PostgreSQL
- Consider setting up additional backups
- Test restore procedures

### 7.3 Performance Monitoring
- Monitor database connection count
- Watch for slow queries
- Check memory usage

---

## 🎯 Best Practices

### ✅ Do This
- Use environment variables for all secrets
- Test database connections during startup
- Implement proper error handling
- Monitor logs regularly
- Keep dependencies updated

### ❌ Don't Do This
- Hardcode database credentials
- Use SQLite in production
- Ignore connection errors
- Skip database testing
- Forget to backup data

---

## 🚨 Emergency Procedures

### If Database is Down
1. Check Railway status page
2. Verify environment variables
3. Restart the service
4. Check PostgreSQL logs
5. Contact Railway support if needed

### If Migrations Fail
1. Check database connection
2. Verify `DATABASE_URL` format
3. Run migrations manually if needed
4. Check for conflicting migrations

---

## 📞 Getting Help

### Railway Support
- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status Page](https://status.railway.app/)

### Django Database Help
- [Django Database Documentation](https://docs.djangoproject.com/en/5.2/topics/db/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## ✅ Checklist

- [ ] Created Railway project
- [ ] Added PostgreSQL plugin
- [ ] Set environment variables
- [ ] Updated Django settings
- [ ] Verified requirements.txt
- [ ] Deployed and tested
- [ ] Monitored logs
- [ ] Created admin user
- [ ] Tested all functionality

---

## 🎉 Success Indicators

Your setup is working correctly when you see:
- ✅ All migrations complete successfully
- ✅ Database connection test passes
- ✅ Gunicorn starts without errors
- ✅ Admin panel accessible
- ✅ No "Connection reset by peer" errors during startup
- ✅ HTTP requests return 200 status codes

---

**Remember**: The key to avoiding database issues is proper configuration, monitoring, and following these best practices. This guide should help you set up a stable, production-ready database on Railway! 🚀 
# 🧹 Django Migration Best Practices

## **Why Clean Migrations Matter**
- Prevents deployment errors on Railway
- Avoids "duplicate column" and "column does not exist" errors
- Keeps database schema consistent
- Makes debugging easier

## **✅ DO's**

### **1. Plan Your Model Changes**
```python
# Before making changes, plan:
# - What fields are being added/removed
# - What data needs to be migrated
# - What dependencies exist
```

### **2. Use Descriptive Migration Names**
```bash
# Good names:
python manage.py makemigrations core --name=add_photo_url_field
python manage.py makemigrations core --name=remove_photo_base64_field
python manage.py makemigrations core --name=update_booking_status_choices

# Bad names:
python manage.py makemigrations core --name=fix
python manage.py makemigrations core --name=update
```

### **3. Test Migrations Locally First**
```bash
# Always test locally before pushing to Railway
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### **4. Use --empty for Complex Changes**
```bash
# For complex data migrations
python manage.py makemigrations core --empty --name=complex_data_migration
```

### **5. Check Migration State**
```bash
# Always check what migrations are applied
python manage.py showmigrations core
```

## **❌ DON'Ts**

### **1. Don't Create Multiple Migrations for Same Field**
```bash
# BAD: Multiple migrations for photo_url
0011_add_photo_url.py
0012_remove_photo_url.py  
0013_add_photo_url_back.py
0014_remove_photo_url_final.py

# GOOD: Single clean migration
0011_add_photo_url_clean.py
```

### **2. Don't Modify Applied Migrations**
- Never edit migrations that have been applied to production
- Create new migrations instead

### **3. Don't Ignore Migration Errors**
- Fix migration issues immediately
- Don't skip migrations with --fake unless you're sure

## **🛠️ Railway-Specific Best Practices**

### **1. Use Custom Management Commands for Schema Fixes**
```python
# In management/commands/fix_schema.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if column exists first
            cursor.execute("PRAGMA table_info(core_dog)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'photo_url' not in columns:
                cursor.execute("ALTER TABLE core_dog ADD COLUMN photo_url TEXT")
```

### **2. Handle SQLite vs PostgreSQL Differences**
```python
# SQLite compatible
cursor.execute("PRAGMA table_info(core_dog)")

# PostgreSQL compatible  
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'core_dog'")
```

### **3. Use Startup Scripts for Railway**
```python
# In startup_simple.py
def startup():
    call_command('migrate')
    call_command('fix_schema')  # Custom command
    call_command('collectstatic', '--noinput')
```

## **🔧 Migration Cleanup Process**

### **When You Have Migration Issues:**

1. **Identify the Problem**
   ```bash
   python manage.py showmigrations core
   python manage.py migrate --plan
   ```

2. **Clean Up Redundant Migrations**
   ```bash
   # Remove problematic migration files
   rm core/migrations/0012_problematic_migration.py
   rm core/migrations/0013_another_problematic.py
   ```

3. **Create Single Clean Migration**
   ```bash
   python manage.py makemigrations core --name=fix_schema_clean
   ```

4. **Test Locally**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Deploy to Railway**
   ```bash
   git add .
   git commit -m "Clean migration: fix schema issues"
   git push
   ```

## **📋 Migration Checklist**

Before creating a migration:
- [ ] Model changes are final
- [ ] No conflicting field names
- [ ] Dependencies are correct
- [ ] Migration name is descriptive
- [ ] Tested locally first

Before deploying:
- [ ] All migrations are clean
- [ ] No redundant migrations
- [ ] Migration state is consistent
- [ ] Custom commands handle edge cases

## **🚨 Emergency Fixes**

### **If Railway Has Migration Issues:**

1. **Temporarily Disable Problematic Features**
   ```python
   # Comment out problematic imports
   # from .supabase_storage import supabase_storage
   ```

2. **Use Custom Commands for Schema Fixes**
   ```python
   # In startup script
   call_command('add_photo_url_railway')
   ```

3. **Fake Migrations When Safe**
   ```bash
   python manage.py migrate core 0011_add_photo_url_clean --fake
   ```

## **🔄 Railway Migration Troubleshooting**

### **When Migrations Don't Apply on Railway:**

1. **Check Railway Logs First**
   - Look for `Applying core.XXXX_migration_name... OK`
   - If migration doesn't appear, it wasn't applied

2. **Use Direct SQL Commands**
   ```python
   # Create management command for direct SQL
   class Command(BaseCommand):
       def handle(self, *args, **options):
           with connection.cursor() as cursor:
               cursor.execute("ALTER TABLE core_dog ADD COLUMN new_field VARCHAR(500)")
   ```

3. **Add to Startup Script**
   ```python
   # In startup_simple.py
   try:
       call_command('your_direct_sql_command')
       print("✅ Direct SQL command executed successfully!")
   except Exception as e:
       print(f"❌ Direct SQL command failed: {e}")
   ```

4. **Verify Database Schema**
   ```python
   # Test endpoint to check schema
   def test_database_schema(request):
       with connection.cursor() as cursor:
           cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'core_dog'")
           columns = [row[0] for row in cursor.fetchall()]
           return JsonResponse({'columns': columns})
   ```

### **Common Railway Migration Issues:**

1. **"column does not exist" error**
   - **Solution**: Use direct SQL commands in startup script
   - **Prevention**: Always test migrations locally first

2. **"value too long" error**
   - **Solution**: Increase field max_length in migration
   - **Prevention**: Plan field lengths carefully

3. **Migration not applied**
   - **Solution**: Add direct SQL commands as backup
   - **Prevention**: Check Railway logs after deployment

### **Railway-Specific Best Practices:**

1. **Always include direct SQL commands as backup**
   ```python
   # In startup script
   call_command('migrate')  # Try Django migration first
   call_command('force_fix_schema')  # Direct SQL as backup
   ```

2. **Test schema changes immediately**
   ```python
   # Add test endpoint
   path('test-schema/', views.test_database_schema, name='test_schema')
   ```

3. **Use descriptive error messages**
   ```python
   print(f"🔍 Current photo column: {column_name}, type: {data_type}, max_length: {max_length}")
   ```

### **Image Upload Debugging Process:**

1. **First, check what's stored in database**
   ```python
   # Visit: /debug-dog-photos/
   # Look for: photo_starts_with_http: true/false
   ```

2. **If photos are stored locally (not as URLs)**
   - Supabase upload is failing
   - Test with: `/test-supabase-upload-debug/`
   - Check Supabase credentials and RLS policies

3. **If photos are stored as URLs but not displaying**
   - Check if URLs are accessible
   - Verify bucket permissions
   - Test direct URL access

4. **Common patterns from our experience:**
   - **Local paths**: `dog_photos/Screenshot_2025-08-05_at_6_Yw7waW6.28.49a.m..png` ❌
   - **Supabase URLs**: `https://tcnjduwxthistsdxajrs.supabase.co/storage/v1/object/public/dog-photos/...` ✅

### **Key Debug Endpoints to Always Include:**
- `/debug-dog-photos/` - Database inspection
- `/test-supabase-upload-debug/` - Upload testing
- `/test-photo-field-length/` - Schema verification

## **📚 Key Commands Reference**

```bash
# Check migration state
python manage.py showmigrations core

# Create migration
python manage.py makemigrations core --name=descriptive_name

# Apply migrations
python manage.py migrate

# Fake migration (use carefully)
python manage.py migrate core 0011_migration_name --fake

# Plan migrations
python manage.py migrate --plan

# Reset migrations (dangerous!)
python manage.py migrate core zero
```

---

**Remember:** Clean migrations save hours of debugging time! 🎯 
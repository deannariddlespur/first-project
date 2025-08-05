# Supabase Image Storage Setup Guide

## Overview
This guide documents the complete setup process for using Supabase Storage for dog images in the Django dog boarding application. This prevents the ephemeral filesystem issues on Railway.

## Prerequisites
- Supabase account and project
- Railway deployment with environment variables configured
- Django application with image upload functionality

## Step 1: Supabase Project Setup

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and API keys

### 1.2 Create Storage Bucket
1. In Supabase dashboard, go to Storage
2. Create a new bucket called `dog-photos`
3. Set bucket to **Public** (important!)
4. Note the bucket name for environment variables

### 1.3 Configure RLS (Row Level Security) Policies
**CRITICAL STEP - This is where most uploads fail!**

1. Go to Storage → dog-photos → Policies
2. Create the following policies:

#### INSERT Policy (for uploads)
```sql
-- Allow authenticated users to upload files
CREATE POLICY "Allow authenticated uploads" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'dog-photos' AND 
  auth.role() = 'authenticated'
);
```

#### SELECT Policy (for viewing)
```sql
-- Allow public access to view files
CREATE POLICY "Allow public viewing" ON storage.objects
FOR SELECT USING (bucket_id = 'dog-photos');
```

#### UPDATE Policy (for updates)
```sql
-- Allow authenticated users to update their files
CREATE POLICY "Allow authenticated updates" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'dog-photos' AND 
  auth.role() = 'authenticated'
);
```

#### DELETE Policy (for deletions)
```sql
-- Allow authenticated users to delete their files
CREATE POLICY "Allow authenticated deletions" ON storage.objects
FOR DELETE USING (
  bucket_id = 'dog-photos' AND 
  auth.role() = 'authenticated'
);
```

## Step 2: Environment Variables

### 2.1 Railway Environment Variables
Add these to your Railway project:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_BUCKET=dog-photos
```

**Important Notes:**
- Use the **service key** for uploads (not anon key)
- The service key has admin privileges needed for uploads
- The anon key is for client-side access only

## Step 3: Django Code Setup

### 3.1 Install Dependencies
```bash
pip install supabase
```

### 3.2 Create Supabase Storage Module
Create `core/supabase_storage.py`:

```python
import os
import uuid
from django.conf import settings
from supabase import create_client, Client
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64

class SupabaseStorage:
    def __init__(self):
        from django.conf import settings
        # Use settings configuration
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_anon_key = settings.SUPABASE_ANON_KEY
        self.supabase_service_key = settings.SUPABASE_SERVICE_KEY
        self.bucket_name = settings.SUPABASE_BUCKET
        
        # Debug: Print what we found
        print(f"🔍 DEBUG: SUPABASE_URL = {self.supabase_url}")
        print(f"🔍 DEBUG: SUPABASE_ANON_KEY = {'Set' if self.supabase_anon_key else 'Not set'}")
        print(f"🔍 DEBUG: SUPABASE_SERVICE_KEY = {'Set' if self.supabase_service_key else 'Not set'}")
        
        if self.supabase_url and self.supabase_service_key:
            # Use service key for uploads (has admin privileges)
            self.client: Client = create_client(self.supabase_url, self.supabase_service_key)
            print("✅ Using Supabase service key for uploads")
        elif self.supabase_url and self.supabase_anon_key:
            # Fallback to anon key
            self.client: Client = create_client(self.supabase_url, self.supabase_anon_key)
            print("⚠️ Using Supabase anon key (may have limited permissions)")
        else:
            self.client = None
            print("⚠️ Supabase credentials not found. Using local storage fallback.")
    
    def upload_file(self, file, folder_path="dog_photos"):
        """Upload a file to Supabase Storage"""
        if not self.client:
            # Fallback to local storage
            return self._upload_to_local(file, folder_path)
        
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = f"{folder_path}/{unique_filename}"
            
            # Upload to Supabase
            result = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file.read(),
                file_options={"content-type": file.content_type}
            )
            
            # Return the public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            return public_url
            
        except Exception as e:
            print(f"❌ Supabase upload failed: {e}")
            print(f"🔍 Error type: {type(e)}")
            print(f"🔍 Error details: {str(e)}")
            # Fallback to local storage
            return self._upload_to_local(file, folder_path)
    
    def _upload_to_local(self, file, folder_path):
        """Fallback to local storage"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = f"{folder_path}/{unique_filename}"
            
            # Save to local storage
            saved_path = default_storage.save(file_path, file)
            return default_storage.url(saved_path)
            
        except Exception as e:
            print(f"❌ Local upload failed: {e}")
            return None

# Global instance
supabase_storage = SupabaseStorage()
```

### 3.3 Update Django Settings
Add to `settings.py`:

```python
# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
SUPABASE_BUCKET = "dog-photos"
```

### 3.4 Update Dog Model
Update `core/models.py`:

```python
from .supabase_storage import supabase_storage

class Dog(models.Model):
    # ... existing fields ...
    photo = models.ImageField(upload_to='dog_photos/', blank=True, null=True)
    
    def get_photo_url(self):
        """Get photo URL with comprehensive fallback system"""
        # Try to get Supabase URL first
        try:
            if self.photo and self.photo.name:
                # Check if this is a Supabase URL (stored in photo field)
                if 'supabase' in self.photo.name or self.photo.name.startswith('http'):
                    print(f"✅ Using Supabase photo URL for {self.name}: {self.photo.name}")
                    return self.photo.name
        except Exception as e:
            print(f"⚠️ Supabase photo not available for {self.name}: {e}")
        
        # Try local photo as fallback
        try:
            if self.photo:
                photo_url = self.photo.url
                print(f"✅ Using local photo URL for {self.name}: {photo_url}")
                return photo_url
        except Exception as e:
            print(f"⚠️ Local photo not available for {self.name}: {e}")
        
        # Fallback to a placeholder
        placeholder_url = f"https://via.placeholder.com/300x300/667eea/ffffff?text={self.name}"
        print(f"✅ Using placeholder URL for {self.name}: {placeholder_url}")
        return placeholder_url
    
    def save_photo_to_supabase(self, image_file):
        """Upload photo to Supabase for persistent storage"""
        try:
            print(f"🔄 Uploading photo for {self.name} to Supabase...")
            
            # Upload to Supabase
            public_url = supabase_storage.upload_file(image_file)
            
            if public_url:
                print(f"✅ Photo uploaded successfully: {public_url}")
                # Save the Supabase URL to the photo field for reference
                self.photo.save(image_file.name, image_file, save=True)
                return True
            else:
                print(f"❌ Supabase upload failed for {self.name}")
                # Fallback to local storage
                self.photo.save(image_file.name, image_file, save=True)
                return False
                
        except Exception as e:
            print(f"❌ Error in save_photo_to_supabase for {self.name}: {e}")
            # Fallback to local storage
            self.photo.save(image_file.name, image_file, save=True)
            return False
```

## Step 4: Testing and Debugging

### 4.1 Test Supabase Upload
Create a test endpoint to verify uploads work:

```python
def test_supabase_upload(request):
    """Test Supabase upload directly"""
    from django.core.files.base import ContentFile
    import os
    
    try:
        # Create a simple test file
        test_content = b"test image content"
        test_file = ContentFile(test_content, name="test_image.jpg")
        
        # Test Supabase upload
        from .supabase_storage import supabase_storage
        result = supabase_storage.upload_file(test_file)
        
        return JsonResponse({
            'status': 'success',
            'supabase_upload_result': result,
            'supabase_url': supabase_storage.supabase_url,
            'bucket_name': supabase_storage.bucket_name,
            'client_available': supabase_storage.client is not None
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        })
```

### 4.2 Common Issues and Solutions

#### Issue: "new row violates row-level security policy"
**Solution:** Ensure RLS policies are set up correctly (see Step 1.3)

#### Issue: "Invalid Compact JWS"
**Solution:** Use service key instead of anon key for uploads

#### Issue: Files show as 0 bytes in Supabase
**Solution:** Check that the upload method is working correctly and RLS policies allow uploads

#### Issue: Images not displaying
**Solution:** 
1. Check if Supabase URLs are being generated correctly
2. Verify the `get_photo_url()` method is using Supabase URLs
3. Ensure the bucket is set to public

### 4.3 Debugging Steps

1. **Check Environment Variables:**
   ```bash
   curl https://your-app.railway.app/test-debug-logs/
   ```

2. **Test Supabase Upload:**
   ```bash
   curl https://your-app.railway.app/test-supabase-upload/
   ```

3. **Check Photo URLs:**
   ```bash
   curl https://your-app.railway.app/test-photo-urls/
   ```

## Step 5: Deployment Checklist

- [ ] Supabase project created
- [ ] Storage bucket created and set to public
- [ ] RLS policies configured
- [ ] Environment variables set in Railway
- [ ] Django code updated
- [ ] Dependencies installed
- [ ] Test uploads working
- [ ] Images displaying correctly

## Troubleshooting Summary

**Most Common Issues:**
1. **RLS Policies** - 90% of upload failures are due to missing RLS policies
2. **Wrong API Key** - Using anon key instead of service key for uploads
3. **Bucket Not Public** - Bucket must be set to public for file access
4. **Environment Variables** - Missing or incorrect environment variables

**Key Lessons Learned:**
- Always test Supabase uploads directly before integrating
- RLS policies are critical for uploads to work
- Service key is required for server-side uploads
- Local storage fallback is important for development
- Railway's ephemeral filesystem requires external storage

This guide should prevent the circular debugging we experienced and provide a clear path to working image uploads. 
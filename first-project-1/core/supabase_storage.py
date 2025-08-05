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
            
            # Set content type based on file extension
            content_type = "image/jpeg"  # Default for .jpg files
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ['.png']:
                content_type = "image/png"
            elif file_extension in ['.gif']:
                content_type = "image/gif"
            elif file_extension in ['.webp']:
                content_type = "image/webp"
            
            # Create a copy of the file content (Django files can only be read once)
            file_content = file.read()
            file.seek(0)  # Reset file pointer for potential future use
            
            # Upload to Supabase
            result = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}
            )
            
            # Return the public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            # Remove trailing ? if present (can cause browser issues)
            if public_url.endswith('?'):
                public_url = public_url[:-1]
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
    
    def delete_file(self, file_url):
        """Delete a file from Supabase Storage"""
        if not self.client:
            return False
        
        try:
            # Extract file path from URL
            if 'supabase' in file_url:
                # Supabase URL format
                file_path = file_url.split('/')[-1]
                self.client.storage.from_(self.bucket_name).remove([file_path])
                return True
            else:
                # Local file
                return default_storage.delete(file_url)
                
        except Exception as e:
            print(f"❌ File deletion failed: {e}")
            return False
    
    def get_file_url(self, file_path):
        """Get public URL for a file"""
        if not self.client:
            return default_storage.url(file_path)
        
        try:
            return self.client.storage.from_(self.bucket_name).get_public_url(file_path)
        except Exception as e:
            print(f"❌ Failed to get file URL: {e}")
            return default_storage.url(file_path)

# Global instance
supabase_storage = SupabaseStorage() 
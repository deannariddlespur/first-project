from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Test Supabase connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing Supabase Configuration...")
        
        # Check environment variables
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY')
        supabase_service_key = os.environ.get('SUPABASE_SERVICE_KEY')
        
        self.stdout.write(f"📋 Environment Variables:")
        self.stdout.write(f"   SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Not set'}")
        self.stdout.write(f"   SUPABASE_ANON_KEY: {'✅ Set' if supabase_anon_key else '❌ Not set'}")
        self.stdout.write(f"   SUPABASE_SERVICE_KEY: {'✅ Set' if supabase_service_key else '❌ Not set'}")
        
        if not all([supabase_url, supabase_anon_key, supabase_service_key]):
            self.stdout.write(self.style.ERROR("❌ Missing Supabase environment variables!"))
            self.stdout.write("Please check your Railway environment variables.")
            return
        
        # Test Supabase connection
        try:
            from supabase import create_client, Client
            
            # Test with service key (for uploads)
            client = create_client(supabase_url, supabase_service_key)
            
            # Try to list files in bucket
            try:
                files = client.storage.from_('dog-photos').list()
                self.stdout.write(self.style.SUCCESS(f"✅ Supabase connection successful!"))
                self.stdout.write(f"   Files in bucket: {len(files) if files else 0}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Bucket access failed: {e}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Supabase connection failed: {e}"))
            self.stdout.write("Please check your Supabase credentials.") 
#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogboarding.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import DailyLog, Booking, Dog, Owner

def test_daily_logs_access():
    """Test accessing daily logs admin page"""
    print("🔍 Testing daily logs admin access...")
    
    try:
        # Create a test client
        client = Client()
        
        # Try to access the daily logs admin page
        response = client.get('/admin/core/dailylog/')
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 500:
            print("❌ 500 Error detected!")
            print(f"📄 Response content: {response.content[:500]}...")
        elif response.status_code == 302:
            print("✅ 302 redirect (expected for unauthenticated)")
        else:
            print(f"📊 Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()

def test_daily_logs_model():
    """Test DailyLog model operations"""
    print("🔍 Testing DailyLog model...")
    
    try:
        # Try to query DailyLog model
        count = DailyLog.objects.count()
        print(f"✅ DailyLog count: {count}")
        
        # Try to get all DailyLog objects
        logs = list(DailyLog.objects.all()[:5])
        print(f"✅ Retrieved {len(logs)} DailyLog objects")
        
        # Check if photo field exists
        if hasattr(DailyLog, 'photo'):
            print("✅ DailyLog.photo field exists")
        else:
            print("❌ DailyLog.photo field missing")
            
    except Exception as e:
        print(f"❌ Exception during model test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_daily_logs_model()
    test_daily_logs_access() 
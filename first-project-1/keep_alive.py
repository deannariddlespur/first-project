#!/usr/bin/env python3
"""
Keep alive script for Railway
"""
import os
import sys
import time
import requests
import threading

def make_health_request():
    """Make a request to the health endpoint to keep container alive"""
    try:
        # Wait a moment for gunicorn to start
        time.sleep(5)
        
        # Get the port from environment
        port = os.environ.get('PORT', '8080')
        
        # Make request to health endpoint
        response = requests.get(f'http://localhost:{port}/health/', timeout=10)
        print(f"✅ Health check request successful: {response.status_code}")
        
        # Make request to homepage
        response = requests.get(f'http://localhost:{port}/', timeout=10)
        print(f"✅ Homepage request successful: {response.status_code}")
        
    except Exception as e:
        print(f"⚠️ Health request warning: {e}")

def start_keep_alive():
    """Start keep alive in background"""
    thread = threading.Thread(target=make_health_request, daemon=True)
    thread.start()
    print("🔄 Keep alive thread started")

if __name__ == '__main__':
    print("🚀 Starting keep alive script...")
    start_keep_alive()
    
    # Start the main application
    print("🎯 Starting main application...")
    os.execvp('python', ['python', 'startup_with_migrations.py']) 
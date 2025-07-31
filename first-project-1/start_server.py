#!/usr/bin/env python
"""
Simple server startup script for Railway.
This just starts the web server without any database operations.
"""

import os
import sys
import subprocess

print("🚀 Starting Dog Boarding System...")
print("✅ Health check: /health/")
print("✅ Emergency fix: /emergency-fix/")

# Get the port from environment
port = os.environ.get('PORT', '8080')

# Start gunicorn
cmd = [
    'gunicorn',
    'dogboarding.wsgi:application',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '1',
    '--timeout', '120',
    '--access-logfile', '-',
    '--error-logfile', '-'
]

print(f"Starting gunicorn on port {port}...")
subprocess.run(cmd) 
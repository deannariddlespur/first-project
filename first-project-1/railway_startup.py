#!/usr/bin/env python
"""
Railway startup script - simplified version.
This script just starts the web server without database setup.
Database setup should be done manually via the emergency fix page.
"""

import os
import sys

print("=" * 50)
print("🐕 Dog Boarding Railway Startup")
print("=" * 50)
print("✅ Starting web server...")
print("✅ Health check available at: /health/")
print("✅ Emergency database fix at: /emergency-fix/")
print("=" * 50) 
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
                'message': 'Dog Boarding System is running',
                'timestamp': time.time()
            }
            self.wfile.write(str(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Dog Boarding System</h1><p>Starting up...</p>')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress logging for cleaner output
        pass

def start_health_server():
    """Start a simple health check server"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🏥 Health check server listening on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    # Start health server in background
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Give health server time to start
    time.sleep(2)
    
    # Now start the main Django application
    print("🚀 Starting Django application...")
    os.execvp('gunicorn', [
        'gunicorn',
        'dogboarding.wsgi:application',
        '--bind', f'0.0.0.0:{os.environ.get("PORT", "8080")}',
        '--workers', '1',
        '--timeout', '120',
        '--log-file', '-'
    ]) 
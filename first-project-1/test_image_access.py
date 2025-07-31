#!/usr/bin/env python3
import requests
import os

def test_image_access():
    """Test if images are accessible via HTTP"""
    base_url = "http://localhost:8000"
    
    # Get list of image files
    media_dir = "first-project-1/media/dog_photos"
    if not os.path.exists(media_dir):
        print(f"Media directory not found: {media_dir}")
        return
    
    image_files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    print(f"Found {len(image_files)} image files:")
    
    for image_file in image_files:
        image_url = f"{base_url}/media/dog_photos/{image_file}"
        try:
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {image_file} - Accessible (Status: {response.status_code})")
                print(f"  Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
                print(f"  Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
            else:
                print(f"✗ {image_file} - Not accessible (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ {image_file} - Error: {e}")

if __name__ == "__main__":
    test_image_access() 
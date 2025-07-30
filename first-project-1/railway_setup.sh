#!/bin/bash
echo "Setting up production database..."
railway run python manage.py setup_production
echo "Setup complete!" 
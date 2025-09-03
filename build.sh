#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: run Django migrations
python manage.py migrate

# Optional: collect static files if using Django
# python manage.py collectstatic --noinput
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Initialize and migrate database
echo "Initializing database..."
python init_render_db.py

echo "Build completed successfully!"

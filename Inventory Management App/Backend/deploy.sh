#!/bin/bash
# ============================================================
# EC2 Deployment Script - Cloud Inventory Monitoring System
# Run this on your EC2 instance (Ubuntu 22.04 recommended)
# ============================================================

set -e  # Exit immediately on any error

echo "=============================="
echo " Updating system packages..."
echo "=============================="
sudo apt update && sudo apt upgrade -y

echo "=============================="
echo " Installing dependencies..."
echo "=============================="
sudo apt install -y python3 python3-pip python3-venv git pkg-config \
    libmysqlclient-dev default-libmysqlclient-dev build-essential

echo "=============================="
echo " Cloning project..."
echo "=============================="
# Replace with your actual repo URL
git clone https://github.com/your-group/inventory-system.git /home/ubuntu/inventory_system
cd /home/ubuntu/inventory_system

echo "=============================="
echo " Setting up virtual environment..."
echo "=============================="
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "=============================="
echo " Configuring environment variables..."
echo "=============================="
# Copy and edit your .env file
cp .env.example .env
echo ">>> IMPORTANT: Edit the .env file with your actual credentials <<<"
echo ">>> Run: nano .env"

echo "=============================="
echo " Running migrations..."
echo "=============================="
python manage.py migrate

echo "=============================="
echo " Collecting static files..."
echo "=============================="
python manage.py collectstatic --noinput

echo "=============================="
echo " Starting Gunicorn server..."
echo "=============================="
gunicorn inventory_system.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --daemon \
    --log-file /home/ubuntu/gunicorn.log \
    --access-logfile /home/ubuntu/gunicorn-access.log

echo "=============================="
echo " Deployment complete!"
echo " Backend running on port 8000"
echo "=============================="

#!/bin/bash

# RPI Django Monitoring System Installation Script
# For Kali Linux on Raspberry Pi Zero 2 W

set -e

echo "🚀 Starting RPI Django Monitoring System Installation..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install system monitoring tools
echo "📊 Installing system monitoring tools..."
sudo apt install -y htop iotop nethogs lm-sensors

# Install database
echo "🗄️ Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Install Redis for caching and real-time features
echo "🔄 Installing Redis..."
sudo apt install -y redis-server

# Install Nginx for production
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Install additional system tools
echo "🔧 Installing additional tools..."
sudo apt install -y git curl wget build-essential

# Create project directory
PROJECT_DIR="/opt/rpi_monitor"
echo "📁 Creating project directory at $PROJECT_DIR..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install django==4.2.7
pip install psycopg2-binary
pip install redis
pip install celery
pip install django-redis
pip install psutil
pip install requests
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install channels
pip install channels-redis
pip install django-extensions
pip install gunicorn
pip install whitenoise
pip install django-cors-headers
pip install djangorestframework
pip install django-filter
pip install pillow

# Setup PostgreSQL
echo "🗄️ Setting up PostgreSQL..."
sudo -u postgres createuser --interactive --pwprompt rpi_user || true
sudo -u postgres createdb rpi_monitor_db -O rpi_user || true

# Configure Redis
echo "🔄 Configuring Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Initialize sensors
echo "📡 Initializing sensors..."
sudo sensors-detect --auto || true

# Create systemd service files
echo "⚙️ Creating systemd services..."

# Django service
sudo tee /etc/systemd/system/rpi-monitor.service > /dev/null <<EOF
[Unit]
Description=RPI Monitor Django App
After=network.target

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 rpi_monitor.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Celery service
sudo tee /etc/systemd/system/rpi-celery.service > /dev/null <<EOF
[Unit]
Description=RPI Monitor Celery Worker
After=network.target

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/celery -A rpi_monitor worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/rpi-monitor > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/rpi-monitor /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R $USER:$USER $PROJECT_DIR

echo "✅ Installation completed!"
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_DIR"
echo "2. source venv/bin/activate"
echo "3. Run the Django project setup"
echo "4. python manage.py migrate"
echo "5. python manage.py createsuperuser"
echo "6. python manage.py collectstatic"
echo ""
echo "To start services:"
echo "sudo systemctl enable rpi-monitor rpi-celery nginx"
echo "sudo systemctl start rpi-monitor rpi-celery nginx"
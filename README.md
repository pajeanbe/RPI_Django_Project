# RPI Django Monitoring System

A comprehensive Django-based monitoring system designed for Raspberry Pi Zero 2 W running Kali Linux.

## Features

- **Real-time System Monitoring**: CPU, Memory, Disk, Temperature, Network interfaces
- **User Management**: Create and manage users with role-based permissions
- **Security Features**: IP whitelisting/blacklisting, security event logging, session management
- **Modern UI**: Bootstrap 5 responsive design with real-time charts
- **API Endpoints**: RESTful API for external integrations
- **Background Tasks**: Celery for periodic data collection
- **Production Ready**: Nginx, PostgreSQL, Redis integration

## Quick Installation

1. **Make the installation script executable:**
   ```bash
   chmod +x install.sh
   ```

2. **Run the installation script:**
   ```bash
   sudo ./install.sh
   ```

3. **Navigate to project directory:**
   ```bash
   cd /opt/rpi_monitor
   source venv/bin/activate
   ```

4. **Setup Django:**
   ```bash
   python setup.py
   ```

5. **Start services:**
   ```bash
   sudo systemctl enable rpi-monitor rpi-celery nginx
   sudo systemctl start rpi-monitor rpi-celery nginx
   ```

## Manual Installation

If you prefer manual installation:

1. **Install system dependencies:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv postgresql redis-server nginx
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup database:**
   ```bash
   sudo -u postgres createuser --interactive --pwprompt rpi_user
   sudo -u postgres createdb rpi_monitor_db -O rpi_user
   ```

4. **Configure environment variables:**
   ```bash
   export SECRET_KEY='your-secret-key'
   export DB_PASSWORD='your-db-password'
   ```

5. **Run Django setup:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

## Usage

1. **Access the web interface:**
   - Open browser to `http://your-pi-ip/`
   - Login with created superuser credentials

2. **Default superuser (if using setup.py):**
   - Username: `admin`
   - Password: `admin123`
   - **Change this immediately in production!**

3. **API Endpoints:**
   - `/api/metrics/` - System metrics
   - `/api/network/` - Network statistics
   - `/api/processes/` - Process information

## Security Considerations

- Change default passwords immediately
- Configure firewall rules
- Use HTTPS in production
- Regular security updates
- Monitor security logs

## Architecture

```
├── rpi_monitor/          # Main Django project
│   ├── monitoring/       # System monitoring app
│   ├── users/           # User management app
│   ├── security/        # Security features app
│   └── settings.py      # Django settings
├── templates/           # HTML templates
├── static/             # Static files
├── install.sh          # Installation script
└── requirements.txt    # Python dependencies
```

## Monitoring Features

- **CPU Usage**: Real-time CPU utilization
- **Memory Usage**: RAM consumption tracking
- **Disk Usage**: Storage utilization
- **Temperature**: CPU temperature monitoring
- **Network Traffic**: Interface statistics
- **Process Monitoring**: Top processes by CPU/Memory
- **Load Average**: System load metrics

## User Management

- Create/edit/delete users
- Role-based permissions
- Session management
- Account security features

## Security Features

- IP whitelisting/blacklisting
- Security event logging
- Failed login attempt tracking
- Session security
- CSRF protection
- XSS protection

## Development

1. **Run development server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Run Celery worker:**
   ```bash
   celery -A rpi_monitor worker --loglevel=info
   ```

3. **Run Celery beat:**
   ```bash
   celery -A rpi_monitor beat --loglevel=info
   ```

## Troubleshooting

- Check service status: `sudo systemctl status rpi-monitor`
- View logs: `sudo journalctl -u rpi-monitor -f`
- Database issues: Check PostgreSQL service
- Redis issues: Check Redis service

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

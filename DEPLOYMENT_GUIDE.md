# 🚀 Deployment Guide - Pharmacy Management System

## 📁 Project Structure for Deployment

```
pharmacy-system/
├── app.py                      # Main Flask application
├── database.py                 # Database schema
├── ai_predictor.py            # AI prediction engine
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
│
├── templates/                 # HTML templates (create this folder)
│   ├── index.html            # Main dashboard
│   ├── login.html            # Login page
│   └── register-org.html     # Organization registration
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── styles.css
│   │   └── login.css
│   └── js/
│       ├── script.js
│       └── login.js
│
├── scripts/                   # Utility scripts
│   └── migrate_to_multitenancy.py
│
├── docs/                      # Documentation
│   ├── MULTI_TENANCY_GUIDE.md
│   ├── DOWNLOAD_REPORTS_GUIDE.md
│   └── ...
│
└── pharmacy.db               # SQLite database (production: use PostgreSQL)
```

---

## 🔧 Pre-Deployment Setup

### 1. Move HTML Files to Templates Folder

```bash
# Create templates folder
mkdir templates

# Move HTML files
move index.html templates/
move login.html templates/
move register-org.html templates/
```

### 2. Update app.py to Use Templates

Change these lines in app.py:
```python
# OLD:
return send_from_directory('.', 'index.html')

# NEW:
from flask import render_template
return render_template('index.html')
```

### 3. Clean Up Test Files

Move to a `tests/` folder or delete:
- check_analytics_data.py
- check_medicine_data.py
- test_dashboard.py
- test_endpoints.py
- test_frontend.html
- test_login.py
- debug_frontend.html

### 4. Clean Up Fix Scripts

Move to `scripts/` folder:
- fix_admin_login.py
- fix_auth_headers.py
- fix_chart_functions.py
- fix_tofixed_errors.py
- optimize_database.py

---

## 🔐 Security Configuration

### 1. Change SECRET_KEY

In `app.py`, replace:
```python
app.config['SECRET_KEY'] = 'your-jwt-secret-key-change-in-production-12345678'
```

With a secure random key:
```python
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
# Or use environment variable:
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
```

### 2. Use Environment Variables

Create `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/pharmacy_db
FLASK_ENV=production
```

Update app.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

### 3. Update CORS Settings

For production, restrict CORS:
```python
# Development:
CORS(app, resources={r"/*": {"origins": "*"}})

# Production:
CORS(app, resources={r"/*": {"origins": ["https://yourdomain.com"]}})
```

---

## 🗄️ Database Migration

### For Production: Use PostgreSQL

1. Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

2. Update database.py:
```python
import psycopg2
from psycopg2.extras import RealDictCursor

class PharmacyDB:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
    
    def get_connection(self):
        return psycopg2.connect(self.db_url)
```

3. Migrate data:
```bash
# Export from SQLite
sqlite3 pharmacy.db .dump > pharmacy_dump.sql

# Import to PostgreSQL
psql -U username -d pharmacy_db < pharmacy_dump.sql
```

---

## 🌐 Deployment Options

### Option 1: Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create pharmacy-system
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python migrate_to_multitenancy.py
```

### Option 2: DigitalOcean App Platform

1. Connect GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Configure run command: `gunicorn app:app`

### Option 3: AWS EC2

1. Launch Ubuntu instance
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements.txt
```

3. Configure Nginx:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. Use systemd service:
```ini
[Unit]
Description=Pharmacy Management System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/pharmacy-system
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option 4: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=pharmacy_db
      - POSTGRES_USER=pharmacy_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 📦 Production Dependencies

Update `requirements.txt`:
```txt
Flask==3.0.0
Flask-CORS==4.0.0
PyJWT==2.8.0
gunicorn==21.2.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

---

## ✅ Pre-Deployment Checklist

### Security
- [ ] Change SECRET_KEY to secure random value
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS to specific domains
- [ ] Add rate limiting
- [ ] Implement CSRF protection
- [ ] Sanitize user inputs
- [ ] Use prepared statements (already done)

### Database
- [ ] Migrate to PostgreSQL for production
- [ ] Set up database backups
- [ ] Create database indexes for performance
- [ ] Test database migrations

### Performance
- [ ] Use Gunicorn with multiple workers
- [ ] Enable gzip compression
- [ ] Add caching headers for static files
- [ ] Optimize database queries
- [ ] Use CDN for static assets

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Add application monitoring (New Relic, DataDog)
- [ ] Configure health check endpoint
- [ ] Set up uptime monitoring

### Testing
- [ ] Test all API endpoints
- [ ] Test multi-tenancy isolation
- [ ] Test file uploads/downloads
- [ ] Load testing
- [ ] Security testing

---

## 🔍 Health Check Endpoint

Add to app.py:
```python
@app.route('/health')
def health_check():
    try:
        # Test database connection
        conn = db.get_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
```

---

## 📊 Monitoring & Logging

### Add Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('pharmacy.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Pharmacy system startup')
```

---

## 🚀 Deployment Commands

### Quick Deploy Script

Create `deploy.sh`:
```bash
#!/bin/bash

echo "🚀 Deploying Pharmacy Management System..."

# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python scripts/migrate_to_multitenancy.py

# Restart service
sudo systemctl restart pharmacy-system

echo "✅ Deployment complete!"
```

---

## 📝 Post-Deployment

1. **Test the application**
   - Login functionality
   - Multi-tenancy isolation
   - All CRUD operations
   - Report downloads

2. **Monitor logs**
   ```bash
   tail -f pharmacy.log
   ```

3. **Set up backups**
   ```bash
   # Daily database backup
   0 2 * * * pg_dump pharmacy_db > /backups/pharmacy_$(date +\%Y\%m\%d).sql
   ```

4. **Configure SSL**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 🆘 Troubleshooting

### Issue: 502 Bad Gateway
- Check if Gunicorn is running
- Check Nginx configuration
- Check application logs

### Issue: Database Connection Error
- Verify DATABASE_URL
- Check PostgreSQL is running
- Verify credentials

### Issue: Static Files Not Loading
- Check Nginx static file configuration
- Verify file permissions
- Check STATIC_URL settings

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Review this guide
3. Test locally first
4. Check server resources (CPU, memory, disk)

---

**Ready for Production!** 🎉

Follow this guide step by step for a successful deployment.

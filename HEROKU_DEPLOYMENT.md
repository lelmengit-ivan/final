# 🚀 Heroku Deployment Guide - Complete Step-by-Step

## ✅ Prerequisites

1. **Heroku Account**: Sign up at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli
3. **Git**: Make sure git is installed

---

## 📁 Files Created for Heroku

✅ `Procfile` - Tells Heroku how to run your app
✅ `runtime.txt` - Specifies Python version
✅ `requirements-heroku.txt` - Production dependencies
✅ `.gitignore` - Files to exclude from deployment

---

## 🚀 Quick Deploy (5 Steps)

### Step 1: Install Heroku CLI

**Windows:**
Download from: https://devcenter.heroku.com/articles/heroku-cli

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

This will open your browser to login.

### Step 3: Prepare Your App

```bash
# Copy Heroku requirements
copy requirements-heroku.txt requirements.txt

# Initialize git (if not already)
git init
git add .
git commit -m "Prepare for Heroku deployment"
```

### Step 4: Create Heroku App

```bash
# Create app (Heroku will generate a name)
heroku create

# Or create with custom name
heroku create your-pharmacy-app
```

### Step 5: Add PostgreSQL & Deploy

```bash
# Add PostgreSQL database
heroku addons:create heroku-postgresql:essential-0

# Set SECRET_KEY
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku main

# Run database migration
heroku run python migrate_to_multitenancy.py

# Open your app
heroku open
```

---

## 📝 Detailed Setup

### 1. Update app.py for Heroku

Add this at the top of `app.py`:

```python
import os

# Heroku configuration
if os.environ.get('DATABASE_URL'):
    # Heroku provides DATABASE_URL
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
    
# Use environment variable for SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Get port from environment (Heroku assigns this)
port = int(os.environ.get('PORT', 5000))
```

Update the bottom of `app.py`:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### 2. Update database.py for PostgreSQL

Replace the database.py content:

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

class PharmacyDB:
    def __init__(self):
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Heroku uses postgres:// but psycopg2 needs postgresql://
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            self.db_url = database_url
            self.use_postgres = True
        else:
            # Fallback to SQLite for local development
            self.db_name = 'pharmacy.db'
            self.use_postgres = False
    
    def get_connection(self):
        if self.use_postgres:
            return psycopg2.connect(self.db_url)
        else:
            import sqlite3
            return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Organizations table (multi-tenancy)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizations (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                subdomain TEXT UNIQUE,
                contact_email TEXT NOT NULL,
                contact_phone TEXT,
                address TEXT,
                subscription_plan TEXT DEFAULT 'free',
                subscription_status TEXT DEFAULT 'active',
                created_date TEXT,
                expiry_date TEXT,
                max_users INTEGER DEFAULT 5,
                settings TEXT
            )
        ''')
        
        # Continue with other tables...
        # (Copy the rest from your current database.py)
        
        conn.commit()
        conn.close()
```

### 3. Create .gitignore

```bash
# Python
__pycache__/
*.py[cod]
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.db
*.sqlite

# Environment
.env
.vscode/
.idea/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

---

## 🔐 Environment Variables

### Set Required Variables

```bash
# SECRET_KEY (required)
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# JWT expiration (optional)
heroku config:set JWT_EXPIRATION_HOURS=24

# CORS origins (optional)
heroku config:set ALLOWED_ORIGINS=https://your-app.herokuapp.com
```

### View All Variables

```bash
heroku config
```

### View Specific Variable

```bash
heroku config:get DATABASE_URL
```

---

## 🗄️ Database Setup

### Automatic Setup

Heroku automatically creates PostgreSQL database and sets `DATABASE_URL`.

### Run Migration

```bash
# After first deployment
heroku run python migrate_to_multitenancy.py
```

### Access Database

```bash
# Open PostgreSQL console
heroku pg:psql

# View database info
heroku pg:info

# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Real-time logs
heroku logs --tail

# Last 100 lines
heroku logs -n 100

# Filter by source
heroku logs --source app

# Filter by dyno
heroku logs --dyno web.1
```

### Monitor App

```bash
# Open dashboard
heroku open

# View metrics
heroku ps

# View addons
heroku addons
```

---

## 🔄 Updating Your App

### Deploy Updates

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push heroku main
```

### Restart App

```bash
heroku restart
```

### Run Commands

```bash
# Run Python script
heroku run python script.py

# Open Python shell
heroku run python

# Run migration
heroku run python migrate_to_multitenancy.py
```

---

## 🌐 Custom Domain

### Add Domain

```bash
# Add custom domain
heroku domains:add www.yourdomain.com

# View domains
heroku domains

# Get DNS target
heroku domains:wait www.yourdomain.com
```

### SSL Certificate

```bash
# Heroku provides free SSL
# Automatically enabled for custom domains
heroku certs:auto:enable
```

---

## 📈 Scaling

### View Current Dynos

```bash
heroku ps
```

### Scale Up

```bash
# Scale to 2 web dynos
heroku ps:scale web=2

# Scale to hobby dyno (better performance)
heroku dyno:type hobby
```

### Upgrade Database

```bash
# Upgrade to standard plan
heroku addons:create heroku-postgresql:standard-0
```

---

## 🐛 Troubleshooting

### Issue: "Application Error"

**Check logs:**
```bash
heroku logs --tail
```

**Common causes:**
- Missing dependencies in requirements.txt
- Database connection error
- Port binding issue

### Issue: "Module not found"

**Solution:**
```bash
# Make sure all dependencies are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push heroku main
```

### Issue: "Database connection failed"

**Solution:**
```bash
# Check DATABASE_URL is set
heroku config:get DATABASE_URL

# Restart app
heroku restart
```

### Issue: "Timeout error"

**Solution:**
- Optimize slow queries
- Add database indexes
- Upgrade dyno type

---

## ✅ Post-Deployment Checklist

### Test Your App

- [ ] Visit your Heroku URL
- [ ] Test login page
- [ ] Register new organization
- [ ] Login with credentials
- [ ] Test all dashboard features
- [ ] Test multi-tenancy (create 2 orgs)
- [ ] Test report downloads
- [ ] Check mobile responsiveness

### Security

- [ ] SECRET_KEY is set
- [ ] DATABASE_URL is secure
- [ ] HTTPS is enabled (automatic)
- [ ] CORS is configured
- [ ] No sensitive data in logs

### Performance

- [ ] App loads quickly
- [ ] Database queries are fast
- [ ] No timeout errors
- [ ] Logs show no errors

---

## 💰 Pricing

### Free Tier
- 550-1000 dyno hours/month
- Sleeps after 30 min inactivity
- 10,000 rows PostgreSQL

### Hobby ($7/month)
- Never sleeps
- Custom domains
- SSL included

### Standard ($25-50/month)
- Better performance
- More database rows
- Metrics & monitoring

---

## 🔄 Rollback

### View Releases

```bash
heroku releases
```

### Rollback to Previous Version

```bash
heroku rollback v123
```

---

## 📞 Useful Commands

```bash
# App info
heroku info

# Open app
heroku open

# Open dashboard
heroku dashboard

# View config
heroku config

# View addons
heroku addons

# View logs
heroku logs --tail

# Restart
heroku restart

# Run command
heroku run python script.py

# Database console
heroku pg:psql

# Create backup
heroku pg:backups:capture

# Scale
heroku ps:scale web=2
```

---

## 🎯 Complete Deployment Script

Save this as `deploy_heroku.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying to Heroku..."

# Copy Heroku requirements
cp requirements-heroku.txt requirements.txt

# Commit changes
git add .
git commit -m "Deploy to Heroku"

# Create Heroku app (if not exists)
if ! heroku apps:info > /dev/null 2>&1; then
    echo "Creating Heroku app..."
    heroku create
fi

# Add PostgreSQL (if not exists)
if ! heroku addons | grep -q "heroku-postgresql"; then
    echo "Adding PostgreSQL..."
    heroku addons:create heroku-postgresql:essential-0
fi

# Set SECRET_KEY (if not set)
if ! heroku config:get SECRET_KEY > /dev/null 2>&1; then
    echo "Setting SECRET_KEY..."
    heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
fi

# Deploy
echo "Deploying..."
git push heroku main

# Run migration
echo "Running migration..."
heroku run python migrate_to_multitenancy.py

# Open app
echo "✅ Deployment complete!"
heroku open
```

Make it executable:
```bash
chmod +x deploy_heroku.sh
./deploy_heroku.sh
```

---

## 🎉 Success!

Your pharmacy system is now live on Heroku!

**Next Steps:**
1. Test all features
2. Set up monitoring
3. Configure backups
4. Add custom domain (optional)
5. Share with users

**Your App URL:**
```
https://your-app-name.herokuapp.com
```

---

## 📚 Additional Resources

- Heroku Dev Center: https://devcenter.heroku.com
- Python on Heroku: https://devcenter.heroku.com/categories/python-support
- PostgreSQL on Heroku: https://devcenter.heroku.com/categories/postgres-basics

---

**Need Help?** Check logs with `heroku logs --tail`

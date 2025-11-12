# ✅ Deployment Checklist

## Pre-Deployment

### 1. Organize Files
```bash
python organize_for_deployment.py
```

This will:
- ✅ Create templates/ folder and move HTML files
- ✅ Create tests/ folder and move test files
- ✅ Move utility scripts to scripts/
- ✅ Create .env.example
- ✅ Update .gitignore
- ✅ Create Procfile and runtime.txt

### 2. Update app.py

Change HTML file serving:
```python
# Add at top
from flask import render_template

# Change these routes:
@app.route('/')
def index():
    return render_template('index.html')  # Changed from send_from_directory

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register-org')
def register_org_page():
    return render_template('register-org.html')
```

### 3. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and set:
# - SECRET_KEY (use: python -c "import secrets; print(secrets.token_hex(32))")
# - DATABASE_URL (for production)
# - ALLOWED_ORIGINS
```

### 4. Test Locally

```bash
# Install production dependencies
pip install -r requirements.prod.txt

# Run migration
python scripts/migrate_to_multitenancy.py

# Test the app
python app.py

# Visit http://localhost:5000
```

---

## Deployment Steps

### Option A: Heroku

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-pharmacy-app

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 5. Deploy
git add .
git commit -m "Prepare for deployment"
git push heroku main

# 6. Run migration
heroku run python scripts/migrate_to_multitenancy.py

# 7. Open app
heroku open
```

### Option B: DigitalOcean

1. Create new App
2. Connect GitHub repository
3. Set environment variables in dashboard
4. Deploy automatically on push

### Option C: AWS/VPS

```bash
# 1. SSH to server
ssh user@your-server-ip

# 2. Clone repository
git clone your-repo-url
cd pharmacy-system

# 3. Install dependencies
pip3 install -r requirements.prod.txt

# 4. Set up environment
cp .env.example .env
nano .env  # Edit values

# 5. Run migration
python3 scripts/migrate_to_multitenancy.py

# 6. Start with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Post-Deployment

### 1. Verify Deployment

- [ ] Can access login page
- [ ] Can register organization
- [ ] Can login
- [ ] Dashboard loads
- [ ] All tabs work
- [ ] Reports download
- [ ] Multi-tenancy works

### 2. Security

- [ ] HTTPS enabled
- [ ] SECRET_KEY changed
- [ ] CORS restricted
- [ ] Database secured
- [ ] Firewall configured

### 3. Monitoring

- [ ] Error logging set up
- [ ] Uptime monitoring
- [ ] Database backups
- [ ] Health check endpoint

### 4. Documentation

- [ ] Update README with production URL
- [ ] Document admin credentials
- [ ] Share with team

---

## Quick Commands

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Database Backup
```bash
# SQLite
cp pharmacy.db backups/pharmacy_$(date +%Y%m%d).db

# PostgreSQL
pg_dump pharmacy_db > backups/pharmacy_$(date +%Y%m%d).sql
```

### View Logs
```bash
# Heroku
heroku logs --tail

# Local
tail -f pharmacy.log
```

---

## Rollback Plan

If deployment fails:

```bash
# Heroku
heroku releases
heroku rollback v123

# Git
git revert HEAD
git push
```

---

## Support Contacts

- **Technical Issues**: Check DEPLOYMENT_GUIDE.md
- **Database Issues**: Check logs and connection string
- **Security Issues**: Review security checklist

---

**Status**: Ready for Deployment ✅

Last Updated: After multi-tenancy implementation

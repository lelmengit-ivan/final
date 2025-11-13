# 🔧 Deploy Backend API to Render

Complete step-by-step guide for deploying the Pharmacy Management System backend to Render.

## 📁 Backend Files

Your backend folder contains everything needed for deployment:
```
backend/
├── app.py                 # Flask application (all API routes)
├── database.py            # Database handler (PostgreSQL/SQLite)
├── ai_predictor.py        # AI stock predictions
├── init_render_db.py      # Database initialization script
├── requirements.txt       # Python dependencies
├── render.yaml            # Render configuration (optional)
├── build.sh               # Build script
├── .gitignore             # Git ignore rules
└── .renderignore          # Render ignore rules
```

## 🎯 What You'll Deploy

**Backend API with:**
- ✅ Flask REST API
- ✅ PostgreSQL database
- ✅ JWT authentication
- ✅ Multi-tenancy support
- ✅ AI predictions
- ✅ Automatic HTTPS
- ✅ Global CDN

## 🚀 Quick Deploy (6 Steps)

### Step 1: Prepare Code
```bash
# Ensure all changes are committed
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Render Account
1. Go to **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub** (recommended)
4. Authorize Render to access your repositories

### Step 3: Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - Name: `pharmacy-db`
   - Database: `pharmacy_db`
   - User: `pharmacy_user`
   - Region: Choose closest (Oregon, Frankfurt, Singapore)
   - Plan: **Free**
3. Click **"Create Database"**
4. Wait 2-3 minutes
5. **Copy "Internal Database URL"** (you'll need this!)

### Step 4: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - Name: `pharmacy-backend`
   - Root Directory: `backend` (or leave empty if deploying from root)
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn app:app`
   - Plan: **Free**

### Step 5: Add Environment Variables
Add these 3 variables:
- `PYTHON_VERSION` = `3.11.0`
- `SECRET_KEY` = Click "Generate"
- `DATABASE_URL` = Paste Internal Database URL from Step 3

### Step 6: Deploy & Test
- Click **"Create Web Service"**
- Wait 5-10 minutes
- Test: `https://your-url.onrender.com/api/login`

## 📋 Detailed Steps

### 1. Prerequisites

**Required:**
- ✅ GitHub account
- ✅ Code pushed to GitHub
- ✅ Render account (free)

**Files needed:**
- ✅ `app.py` - Flask application
- ✅ `database.py` - Database handler
- ✅ `requirements.txt` - Dependencies
- ✅ `render.yaml` - Configuration
- ✅ `build.sh` - Build script
- ✅ `init_render_db.py` - DB initialization

### 2. Create PostgreSQL Database

1. Login to Render Dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   ```
   Name: pharmacy-db
   Database: pharmacy_db
   User: pharmacy_user
   Region: Oregon (or closest to you)
   PostgreSQL Version: 16
   Plan: Free
   ```
4. Click **"Create Database"**
5. Wait 2-3 minutes
6. **Copy "Internal Database URL"**
   - Format: `postgresql://user:pass@host/db`
   - You'll need this for the web service

### 3. Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Connect your GitHub repository
4. Click **"Connect"**

### 4. Configure Web Service

#### Basic Settings:
```
Name: pharmacy-backend (or pharmacy-system)
Region: Same as database (IMPORTANT for performance!)
Branch: main
Root Directory: backend (if deploying from backend folder)
              OR leave empty (if deploying from root)
Runtime: Python 3
```

**Note:** If your files are in the root directory (not in `backend/` folder), leave Root Directory empty.

#### Build Settings:
```
Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

**Why these commands:**
- `chmod +x build.sh` - Makes build script executable
- `./build.sh` - Runs the build script (installs deps, inits DB)
- `gunicorn app:app` - Starts the Flask app with Gunicorn
- `--bind 0.0.0.0:$PORT` - Binds to Render's port (optional, Render handles this)

#### Instance Type:
```
Plan: Free
```

**Free Tier Includes:**
- 750 hours/month
- 512 MB RAM
- 0.1 CPU
- Sleeps after 15 min inactivity

### 5. Environment Variables

Scroll down and click **"Advanced"** to expand environment variables section.

Add these 3 required variables:

#### Variable 1: PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.11.0
```
**Purpose:** Specifies Python version for compatibility

#### Variable 2: SECRET_KEY
```
Key: SECRET_KEY
Value: [Click "Generate" button]
```
**Purpose:** Used for JWT token signing and session security

**Alternative:** Use any random string (min 32 characters):
```
your-secret-key-change-in-production-12345678
```

#### Variable 3: DATABASE_URL
```
Key: DATABASE_URL
Value: [Paste Internal Database URL from Step 2]
```
**Format:** `postgresql://user:password@host/database`
**Example:** `postgresql://pharmacy_user:abc123@dpg-xyz123/pharmacy_db`

**Important:** Use **Internal** Database URL (not External) for better performance.

#### Optional Variables:

**DEBUG** (not recommended for production)
```
Key: DEBUG
Value: False
```

**FLASK_ENV**
```
Key: FLASK_ENV
Value: production
```

### 6. Deploy

1. Review all settings
2. Click **"Create Web Service"**
3. Watch deployment logs

### 7. Monitor Deployment

Expected logs:
```
==> Cloning from GitHub...
==> Running build command...
==> Installing dependencies...
    Collecting Flask==3.0.0
    Collecting flask-cors==4.0.0
    Collecting PyJWT==2.8.0
    Collecting gunicorn==21.2.0
    Collecting psycopg2-binary==2.9.9
    Successfully installed...
==> Initializing database...
    Creating organizations table...
    Creating users table...
    Creating medicines table...
    Creating sales table...
    Creating suppliers table...
    Creating prescriptions table...
    ✅ Database initialized successfully!
    Organizations: 1
    Users: 1
    Default Login: admin@pharmacy.com / admin123
==> Build successful!
==> Starting server...
==> Your service is live at https://pharmacy-system-xyz.onrender.com
```

### 8. Get Your API URL

Once deployed:
```
🎉 https://pharmacy-system-abc123.onrender.com
```

Your API endpoints:
```
POST   /api/login
POST   /api/register
GET    /api/medicines
POST   /api/medicines
GET    /api/sales
POST   /api/sales
GET    /api/analytics/summary
... and more
```

### 9. Test Your API

#### Test 1: Health Check
```bash
curl https://your-url.onrender.com
```
Should return HTML (status 200)

#### Test 2: Login API
```bash
curl -X POST https://your-url.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```

Should return:
```json
{
  "message": "Login successful",
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@pharmacy.com",
    "role": "admin",
    "organization_id": 1,
    "organization_name": "Default Pharmacy"
  }
}
```

#### Test 3: Authenticated Request
```bash
# Get token from login response
TOKEN="your-token-here"

curl https://your-url.onrender.com/api/medicines \
  -H "Authorization: Bearer $TOKEN"
```

## 🔧 Configuration Files Explained

### requirements.txt
```txt
Flask==3.0.0              # Web framework
Flask-CORS==4.0.0         # Cross-Origin Resource Sharing
PyJWT==2.8.0              # JWT token authentication
gunicorn==21.2.0          # Production WSGI server
psycopg2-binary==2.9.9    # PostgreSQL adapter
python-dotenv==1.0.0      # Environment variables
```

**Why these versions:**
- Tested and stable
- Compatible with Python 3.11
- Security patches included

### render.yaml (Optional - for Blueprint deployment)
```yaml
services:
  - type: web
    name: pharmacy-backend
    env: python
    buildCommand: "chmod +x build.sh && ./build.sh"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: pharmacy-db
          property: connectionString

databases:
  - name: pharmacy-db
    databaseName: pharmacy_db
    user: pharmacy_user
```

**Note:** You don't need this file if deploying manually through Render dashboard.

### build.sh
```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python init_render_db.py

echo "Build completed successfully!"
```

**What it does:**
1. Installs all Python packages
2. Creates database tables
3. Creates default organization
4. Creates admin user

### init_render_db.py
This script:
- Creates all database tables
- Creates default organization (ID: 1)
- Creates admin user (admin@pharmacy.com / admin123)
- Handles both PostgreSQL and SQLite
- Safe to run multiple times (checks if data exists)

## 🔍 Troubleshooting

### Build Failed

**Error: "requirements.txt not found"**
```
Solution: Ensure file is in root or backend folder
Check: ls -la requirements.txt
```

**Error: "Module not found"**
```
Solution: Add missing module to requirements.txt
Example: Add "requests==2.31.0"
```

**Error: "Permission denied: build.sh"**
```
Solution: Build command includes chmod +x
Check: chmod +x build.sh && ./build.sh
```

### Database Connection Error

**Error: "could not connect to server"**
```
Solution:
1. Check DATABASE_URL is set
2. Verify database is running
3. Ensure same region as web service
4. Use Internal Database URL (not External)
```

**Error: "relation does not exist"**
```
Solution: Database tables not created
Fix: Run in Render Shell:
  python init_render_db.py
```

### Login Returns 500 Error

**Error: "Internal Server Error"**
```
Solution:
1. Check logs for Python errors
2. Verify database initialized
3. Run: python init_render_db.py
4. Check SECRET_KEY is set
```

### Service Keeps Restarting

**Check logs for:**
- Syntax errors in Python code
- Missing environment variables
- Database connection issues
- Port binding errors (Render handles this)

## 🔄 Update Deployment

When you make changes:

```bash
# 1. Make changes to code
# 2. Test locally
python app.py

# 3. Commit changes
git add .
git commit -m "Update feature"

# 4. Push to GitHub
git push
```

Render automatically:
1. Detects push
2. Starts new build
3. Runs build.sh
4. Deploys new version
5. Zero-downtime switch

## 📊 Monitoring

### Check Logs:
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. Watch real-time logs

### Check Metrics:
1. CPU usage
2. Memory usage
3. Request count
4. Response times

### Set Up Alerts:
1. Go to service settings
2. Notifications
3. Add email/Slack webhook

## 🔐 Security Best Practices

### Environment Variables:
```python
# In app.py
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

**Security Rules:**
- ✅ Never commit secrets to Git
- ✅ Use environment variables for sensitive data
- ✅ Rotate SECRET_KEY periodically
- ✅ Use strong database passwords
- ✅ Keep dependencies updated

### CORS Configuration:

**Development (allow all):**
```python
from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": "*"}})
```

**Production (specific origins - RECOMMENDED):**
```python
CORS(app, resources={r"/*": {
    "origins": [
        "https://pharmacy-frontend.onrender.com",
        "https://pharmacy-frontend.netlify.app",
        "https://yourdomain.com",
        "http://localhost:5000"  # for local testing
    ],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})
```

**Update CORS after deploying frontend:**
1. Get your frontend URL
2. Add it to origins list
3. Commit and push
4. Backend will auto-redeploy

### HTTPS & SSL:
- ✅ Automatic HTTPS on Render
- ✅ Free SSL certificate (Let's Encrypt)
- ✅ Auto-renewal every 90 days
- ✅ Force HTTPS redirect
- ✅ TLS 1.2+ only

### Database Security:
- ✅ Use Internal Database URL (not External)
- ✅ Database credentials auto-generated
- ✅ Encrypted connections
- ✅ Firewall protected
- ✅ Regular backups (paid tier)

### API Security:
- ✅ JWT token authentication
- ✅ Password hashing (SHA-256)
- ✅ Token expiration (24 hours)
- ✅ Role-based access control
- ✅ Organization isolation

## 📈 Performance

### Free Tier:
- Service sleeps after 15 minutes
- First request takes 30-60 seconds
- Subsequent requests are fast
- 750 hours/month

### Paid Tier ($7/month):
- Always-on (no sleep)
- Better performance
- More resources
- Priority support

### Optimization Tips:
1. Use database connection pooling
2. Cache frequent queries
3. Optimize database indexes
4. Use CDN for static files
5. Enable gzip compression

## 🗄️ Database Management

### Access Database:
1. Go to database in Render
2. Click "Connect"
3. Use provided connection string

### Backup Database:
```bash
# Manual backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

### Run Migrations:
```bash
# In Render Shell
python init_render_db.py
```

## 🔧 Advanced Configuration

### Custom Domain:
1. Go to service settings
2. Custom Domains
3. Add your domain
4. Update DNS records

### Environment-Specific Settings:
```python
import os

if os.environ.get('RENDER'):
    # Production settings
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
else:
    # Development settings
    DEBUG = True
    DATABASE_URL = 'sqlite:///pharmacy.db'
```

### Health Check Endpoint:
Add to `app.py`:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

## 📝 API Documentation

### Authentication:
```
POST /api/login
POST /api/register
GET  /api/check-auth
POST /api/logout
```

### Medicines:
```
GET    /api/medicines
POST   /api/medicines
PUT    /api/medicines/<id>
DELETE /api/medicines/<id>
```

### Sales:
```
GET    /api/sales
POST   /api/sales
GET    /api/sales/<id>
```

### Analytics:
```
GET /api/analytics/summary
GET /api/analytics/revenue
GET /api/predictions
```

### Organizations:
```
POST /api/organizations/register
GET  /api/organizations/<id>
```

## ✅ Deployment Checklist

**Before Deployment:**
- [ ] All code committed to GitHub
- [ ] requirements.txt complete
- [ ] render.yaml configured
- [ ] build.sh executable
- [ ] init_render_db.py ready
- [ ] No hardcoded secrets
- [ ] CORS configured

**After Deployment:**
- [ ] Service shows "Live"
- [ ] Database initialized
- [ ] Login API works
- [ ] All endpoints tested
- [ ] Logs checked
- [ ] Performance monitored

## 🆘 Support

**Render Documentation:**
- https://render.com/docs

**Community:**
- https://community.render.com

**Status:**
- https://status.render.com

**Contact:**
- support@render.com

## 🎯 Quick Commands

### Test API:
```bash
# Login
curl -X POST https://your-url.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'

# Get medicines (with token)
curl https://your-url.onrender.com/api/medicines \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Render Shell Commands:
```bash
# Initialize database
python init_render_db.py

# Check environment
env | grep DATABASE_URL

# Check Python version
python --version

# List files
ls -la

# Check logs
tail -f /var/log/render.log
```

## 📊 Default Credentials

After deployment, use these to login:
```
Email: admin@pharmacy.com
Password: admin123
Organization: Default Pharmacy
```

**⚠️ Change password immediately after first login!**

---

## 🎉 Success!

Your backend API is now live on Render!

**API Base URL:**
```
https://your-service-name.onrender.com/api
```

**Next Steps:**
1. Test all endpoints
2. Update frontend config.js with API URL
3. Deploy frontend
4. Monitor logs
5. Set up alerts

Happy deploying! 🚀


## 🎯 Post-Deployment Checklist

### Immediate Actions:
- [ ] Test API login endpoint
- [ ] Verify database initialized
- [ ] Check all tables created
- [ ] Test authenticated endpoints
- [ ] Change default admin password
- [ ] Update frontend API URL
- [ ] Configure CORS for frontend

### Monitoring:
- [ ] Check deployment logs
- [ ] Monitor error rates
- [ ] Track response times
- [ ] Set up alerts
- [ ] Review resource usage

### Security:
- [ ] Rotate SECRET_KEY periodically
- [ ] Update CORS origins
- [ ] Enable HTTPS only
- [ ] Review access logs
- [ ] Update dependencies

## 📊 Your Deployment Summary

**Backend API:** `https://your-backend.onrender.com`  
**Database:** PostgreSQL on Render  
**Authentication:** JWT tokens  
**Default User:** admin@pharmacy.com / admin123  
**Status:** ✅ Live and ready!

---

**Updated:** November 2025  
**Version:** 2.0  
**Status:** Production Ready 🚀

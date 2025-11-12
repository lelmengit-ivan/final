# 🚀 Vercel Deployment Guide

## ⚠️ Important Notes

### Limitations on Vercel
1. **Serverless Functions**: Vercel uses serverless functions, not traditional servers
2. **SQLite Not Recommended**: File-based databases don't work well on serverless
3. **Stateless**: Each request may hit a different server instance
4. **10-second timeout**: Functions must respond within 10 seconds

### Recommended Setup
For production on Vercel, you should:
- Use **PostgreSQL** (via Vercel Postgres or external service)
- Use **Vercel KV** for session storage
- Keep functions lightweight

---

## 📁 Files Created for Vercel

✅ `vercel.json` - Vercel configuration
✅ `api/index.py` - Serverless function entry point
✅ `.vercelignore` - Files to ignore
✅ `requirements-vercel.txt` - Minimal dependencies

---

## 🔧 Setup Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Prepare Your Project

#### Option A: Quick Deploy (SQLite - Development Only)

```bash
# Deploy directly
vercel
```

**Note**: SQLite won't persist data between deployments!

#### Option B: Production Setup (PostgreSQL)

**Step 1: Set up Vercel Postgres**

```bash
# In your Vercel dashboard:
# 1. Go to Storage
# 2. Create Postgres Database
# 3. Copy connection string
```

**Step 2: Update database.py**

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class PharmacyDB:
    def __init__(self):
        # Use Vercel Postgres connection string
        self.db_url = os.environ.get('POSTGRES_URL')
    
    def get_connection(self):
        return psycopg2.connect(self.db_url)
```

**Step 3: Add psycopg2 to requirements**

```bash
echo "psycopg2-binary==2.9.9" >> requirements-vercel.txt
```

**Step 4: Set environment variables**

```bash
vercel env add POSTGRES_URL
# Paste your connection string

vercel env add SECRET_KEY
# Generate: python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Deployment Commands

### First Deployment

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Update Deployment

```bash
# After making changes
git add .
git commit -m "Update"
vercel --prod
```

---

## 🔐 Environment Variables

Set these in Vercel Dashboard or CLI:

```bash
# Required
vercel env add SECRET_KEY
vercel env add POSTGRES_URL

# Optional
vercel env add JWT_EXPIRATION_HOURS
vercel env add ALLOWED_ORIGINS
```

Or in Vercel Dashboard:
1. Go to Project Settings
2. Environment Variables
3. Add variables

---

## 📝 Update app.py for Vercel

Add at the top of app.py:

```python
import os

# Vercel-specific configuration
if os.environ.get('VERCEL'):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # Disable debug in production
    app.config['DEBUG'] = False
```

---

## 🗄️ Database Migration on Vercel

### Option 1: Run Locally, Connect to Vercel Postgres

```bash
# Set environment variable locally
export POSTGRES_URL="your-vercel-postgres-url"

# Run migration
python migrate_to_multitenancy.py
```

### Option 2: Use Vercel CLI

```bash
# Run command on Vercel
vercel env pull .env.local
python migrate_to_multitenancy.py
```

---

## 📂 Project Structure for Vercel

```
pharmacy-system/
├── api/
│   └── index.py          # Vercel entry point
├── static/
│   ├── css/
│   └── js/
├── templates/            # Create this folder
│   ├── index.html
│   ├── login.html
│   └── register-org.html
├── app.py               # Main Flask app
├── database.py          # Database connection
├── ai_predictor.py      # AI predictions
├── vercel.json          # Vercel config
├── requirements-vercel.txt
└── .vercelignore
```

---

## 🔄 Move HTML Files to Templates

```bash
# Create templates folder
mkdir templates

# Move HTML files
move index.html templates/
move login.html templates/
move register-org.html templates/
```

Update app.py:

```python
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register-org')
def register_org_page():
    return render_template('register-org.html')
```

---

## ✅ Deployment Checklist

### Before Deployment

- [ ] Move HTML files to `templates/` folder
- [ ] Update app.py to use `render_template()`
- [ ] Set up Vercel Postgres (or external database)
- [ ] Update database.py for PostgreSQL
- [ ] Set environment variables in Vercel
- [ ] Test locally with production database

### Deploy

```bash
# 1. Test locally
python app.py

# 2. Deploy to preview
vercel

# 3. Test preview URL
# Visit the URL provided

# 4. Deploy to production
vercel --prod
```

### After Deployment

- [ ] Run database migration
- [ ] Test login functionality
- [ ] Test organization registration
- [ ] Verify multi-tenancy works
- [ ] Test all features

---

## 🌐 Custom Domain

### Add Custom Domain

```bash
vercel domains add yourdomain.com
```

Or in Vercel Dashboard:
1. Go to Project Settings
2. Domains
3. Add Domain
4. Follow DNS instructions

---

## 📊 Monitoring

### View Logs

```bash
vercel logs
```

Or in Vercel Dashboard:
1. Go to Deployments
2. Click on deployment
3. View Function Logs

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Check `requirements-vercel.txt` includes all dependencies

### Issue: "Database connection failed"
**Solution**: 
- Verify POSTGRES_URL is set
- Check database is accessible
- Test connection locally

### Issue: "Function timeout"
**Solution**:
- Optimize slow queries
- Add database indexes
- Reduce data processing

### Issue: "Static files not loading"
**Solution**:
- Check `vercel.json` routes
- Verify static files are in `static/` folder
- Check file paths in HTML

### Issue: "CORS errors"
**Solution**:
```python
# Update CORS in app.py
CORS(app, resources={
    r"/*": {
        "origins": ["https://yourdomain.vercel.app"]
    }
})
```

---

## 💡 Best Practices

### 1. Use Environment Variables
Never hardcode secrets in code

### 2. Use PostgreSQL
SQLite doesn't work on serverless

### 3. Optimize Queries
Keep functions fast (<10 seconds)

### 4. Add Caching
Use Vercel KV for caching

### 5. Monitor Performance
Check function execution times

---

## 🔄 Alternative: Vercel + External Database

### Using Railway PostgreSQL

```bash
# 1. Create database on Railway
# 2. Get connection string
# 3. Add to Vercel env vars
vercel env add DATABASE_URL
```

### Using Supabase

```bash
# 1. Create project on Supabase
# 2. Get connection string
# 3. Add to Vercel
vercel env add POSTGRES_URL
```

---

## 📞 Quick Commands

```bash
# Deploy
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Remove deployment
vercel rm [deployment-url]

# Pull env variables
vercel env pull

# Open in browser
vercel open
```

---

## 🎯 Production Checklist

- [ ] PostgreSQL database set up
- [ ] Environment variables configured
- [ ] Custom domain added (optional)
- [ ] SSL/HTTPS enabled (automatic)
- [ ] Database migrated
- [ ] All features tested
- [ ] Monitoring set up
- [ ] Backups configured

---

## 🆘 Need Help?

1. Check Vercel logs: `vercel logs`
2. Review this guide
3. Check Vercel documentation: https://vercel.com/docs
4. Test locally first

---

**Ready to Deploy!** 🚀

Run: `vercel --prod`

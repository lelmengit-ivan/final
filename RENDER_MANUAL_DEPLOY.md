# Manual Render Deployment (No Blueprint)

## Step-by-Step Manual Deployment

### Step 1: Create PostgreSQL Database

1. Go to https://render.com and login
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in the form:
   - **Name**: `pharmacy-db`
   - **Database**: `pharmacy_db`
   - **User**: `pharmacy_user`
   - **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: **Free**
4. Click **"Create Database"**
5. Wait 2-3 minutes for database to be ready
6. **Copy the Internal Database URL** (you'll need this later)
   - It looks like: `postgresql://pharmacy_user:password@dpg-xxx/pharmacy_db`

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Choose **"Build and deploy from a Git repository"**
3. Click **"Connect account"** (if not connected)
4. Select your GitHub repository
5. Click **"Connect"**

### Step 3: Configure Web Service

Fill in the configuration:

#### Basic Settings
- **Name**: `pharmacy-system`
- **Region**: **Same as your database** (important!)
- **Branch**: `main` (or your default branch)
- **Root Directory**: (leave empty)
- **Runtime**: **Python 3**

#### Build Settings
- **Build Command**: 
  ```bash
  chmod +x build.sh && ./build.sh
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

#### Instance Type
- **Plan**: **Free**

### Step 4: Add Environment Variables

Click **"Advanced"** to expand environment variables section.

Add these variables:

1. **PYTHON_VERSION**
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: Click **"Generate"** button (or use any random string)

3. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL from Step 1
   - Example: `postgresql://pharmacy_user:password@dpg-xxx/pharmacy_db`

### Step 5: Create Web Service

1. Review all settings
2. Click **"Create Web Service"**
3. Deployment will start automatically

### Step 6: Watch Deployment

You'll see logs like:
```
==> Cloning from https://github.com/your-repo...
==> Downloading cache...
==> Running build command: chmod +x build.sh && ./build.sh
==> Installing dependencies from requirements.txt...
==> Initializing database...
    Creating organizations table...
    Creating users table...
    Creating default admin user...
    ✅ Database initialized successfully!
==> Build successful!
==> Starting server with gunicorn...
==> Your service is live at https://pharmacy-system-xyz.onrender.com
```

**This takes 5-10 minutes for first deployment.**

### Step 7: Get Your URL

Once deployed, you'll see:
```
🎉 Your service is live at https://pharmacy-system-abc123.onrender.com
```

**Copy this URL!**

### Step 8: Test Login

1. Go to: `https://your-url.onrender.com/login`
2. Login with:
   - **Email**: `admin@pharmacy.com`
   - **Password**: `admin123`
3. Should redirect to dashboard ✅

## Configuration Summary

### Database Configuration
```
Name: pharmacy-db
Database: pharmacy_db
User: pharmacy_user
Region: [Your chosen region]
Plan: Free
```

### Web Service Configuration
```
Name: pharmacy-system
Region: [Same as database]
Branch: main
Runtime: Python 3

Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn app:app

Environment Variables:
  - PYTHON_VERSION: 3.11.0
  - SECRET_KEY: [auto-generated]
  - DATABASE_URL: [from database]
```

## Troubleshooting

### Build Fails

**Check logs for specific error:**

1. **"requirements.txt not found"**
   - Make sure file is in root directory
   - Check it's committed to Git

2. **"Module not found"**
   - Missing dependency in requirements.txt
   - Add it and push again

3. **"Permission denied: build.sh"**
   - Build command should include: `chmod +x build.sh`

### Database Connection Error

**Check these:**
1. DATABASE_URL is set correctly
2. Database is running (check database dashboard)
3. Database and web service in same region
4. Internal Database URL used (not External)

### Login Shows "Connection Error"

**Database not initialized:**
1. Go to your web service in Render
2. Click **"Shell"** tab (top right)
3. Wait for shell to load
4. Run: `python init_render_db.py`
5. Wait for success message
6. Try login again

### Service Keeps Restarting

**Check logs for Python errors:**
- Syntax error in code
- Missing environment variable
- Database connection issue

## Manual Database Initialization

If automatic initialization fails:

1. Go to Render Dashboard
2. Click your web service
3. Click **"Shell"** tab
4. Wait for shell prompt
5. Run these commands:

```bash
# Check if database is accessible
python -c "import os; print(os.environ.get('DATABASE_URL'))"

# Initialize database
python init_render_db.py

# Check if tables were created
python -c "
import os
import psycopg2
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()
cursor.execute(\"SELECT tablename FROM pg_tables WHERE schemaname='public'\")
print(cursor.fetchall())
"
```

## Verify Deployment

### Check 1: Service Status
- Dashboard should show **"Live"** (green dot)
- Not "Build Failed" or "Deploying"

### Check 2: Database Status
- Database should show **"Available"**
- Not "Creating" or "Unavailable"

### Check 3: Test API
```bash
curl https://your-url.onrender.com/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```

Should return JSON with token.

### Check 4: Browser Test
1. Visit: `https://your-url.onrender.com/login`
2. Should load login page
3. Login should work
4. Should redirect to dashboard

## Update Deployment

When you make changes:

```bash
git add .
git commit -m "Update feature"
git push
```

Render will automatically:
1. Detect the push
2. Start new build
3. Run build.sh
4. Deploy new version
5. Zero-downtime switch

## Environment Variables Reference

### Required Variables

**PYTHON_VERSION**
- Specifies Python version
- Value: `3.11.0`
- Required for compatibility

**SECRET_KEY**
- Used for JWT token signing
- Value: Random string (use Generate button)
- Keep this secret!

**DATABASE_URL**
- PostgreSQL connection string
- Value: From database (Internal URL)
- Format: `postgresql://user:pass@host/db`

### Optional Variables

**DEBUG**
- Enable debug mode
- Value: `False` (recommended for production)
- Default: False

**PORT**
- Server port
- Value: Render sets this automatically
- Don't set manually

## Free Tier Limitations

⚠️ **Important:**
- Web service sleeps after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- 750 hours/month (enough for 1 service)
- Database: 1GB storage, 97 hours/month

💡 **Upgrade to paid tier ($7/month) for:**
- Always-on service
- Better performance
- More resources
- No sleep

## Next Steps After Deployment

1. ✅ Test all features
2. ✅ Change admin password
3. ✅ Create your organization
4. ✅ Add users
5. ✅ Configure custom domain (optional)
6. ✅ Set up monitoring

## Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## Quick Reference

### Your URLs
- **Login**: `https://your-url.onrender.com/login`
- **Dashboard**: `https://your-url.onrender.com/`
- **API**: `https://your-url.onrender.com/api/*`

### Default Credentials
```
Email: admin@pharmacy.com
Password: admin123
```

### Important Commands
```bash
# Test API
curl https://your-url.onrender.com/api/login -X POST -H "Content-Type: application/json" -d '{"email":"admin@pharmacy.com","password":"admin123"}'

# Initialize database (in Render Shell)
python init_render_db.py

# Check logs
# Go to Dashboard → Your Service → Logs
```

---

## Ready to Deploy Manually?

1. ✅ Push code to GitHub
2. ✅ Create PostgreSQL database on Render
3. ✅ Create Web Service on Render
4. ✅ Configure environment variables
5. ✅ Wait for deployment
6. ✅ Test login

Good luck! 🚀

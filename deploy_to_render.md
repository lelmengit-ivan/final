# Quick Deploy to Render

## Prerequisites
- Git repository with your code
- Render account (free tier works)

## Step-by-Step Deployment

### 1. Prepare Your Code
```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for Render deployment"
git push
```

### 2. Create Render Account
1. Go to: https://render.com
2. Sign up (free)
3. Connect your GitHub account

### 3. Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Fill in:
   - **Name**: `pharmacy-db`
   - **Database**: `pharmacy_db`
   - **User**: `pharmacy_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
3. Click "Create Database"
4. Wait for it to be ready (2-3 minutes)

### 4. Create Web Service

1. Click "New +" → "Web Service"
2. Connect your Git repository
3. Fill in:
   - **Name**: `pharmacy-system`
   - **Region**: Same as database
   - **Branch**: `main` (or your branch)
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. Add Environment Variables:
   - Click "Advanced"
   - Add:
     - `PYTHON_VERSION` = `3.11.0`
     - `SECRET_KEY` = (click "Generate" or use any random string)

5. Connect Database:
   - Scroll to "Environment Variables"
   - Click "Add from Database"
   - Select `pharmacy-db`
   - Choose `DATABASE_URL`

6. Click "Create Web Service"

### 5. Wait for Deployment

Watch the logs:
- Building...
- Installing dependencies...
- Running build.sh...
- Initializing database...
- Starting server...
- **Live** ✅

This takes 5-10 minutes for first deployment.

### 6. Get Your URL

Once deployed, you'll see:
```
Your service is live at https://pharmacy-system-abc123.onrender.com
```

Copy this URL!

### 7. Test Login

1. Go to: `https://your-url.onrender.com/login`
2. Login with:
   - Email: `admin@pharmacy.com`
   - Password: `admin123`
3. Should redirect to dashboard

## If Login Fails

### Check 1: Is Service Running?
- Dashboard should show "Live" (green)
- If "Build Failed" (red), check logs

### Check 2: Is Database Initialized?
Look in logs for:
```
Initializing database...
✅ Database initialized successfully!
```

If not found, run manually:
1. Click "Shell" tab
2. Run: `python init_render_db.py`
3. Wait for success message

### Check 3: Test API
```bash
curl https://your-url.onrender.com/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```

Should return JSON with token.

## Files Needed for Render

Make sure you have these files:

✅ `render.yaml` - Render configuration
✅ `build.sh` - Build script
✅ `requirements.txt` - Python dependencies
✅ `init_render_db.py` - Database initialization
✅ `app.py` - Flask application
✅ `database.py` - Database class
✅ All HTML/CSS/JS files

## Render Configuration Files

### render.yaml
```yaml
services:
  - type: web
    name: pharmacy-system
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: pharmacy-db
          property: connectionString

databases:
  - name: pharmacy-db
    databaseName: pharmacy_db
    user: pharmacy_user
```

### build.sh
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python init_render_db.py
```

### requirements.txt
Must include:
```
Flask
flask-cors
gunicorn
psycopg2-binary
PyJWT
```

## After Deployment

### Update Local Config (Optional)
If you want to use Render backend locally:

Edit `config.js`:
```javascript
const CONFIG = {
    API_URL: 'https://your-url.onrender.com/api'
};
```

### Monitor Your Service
- Dashboard → Your Service → Logs
- Watch for errors
- Check resource usage

### Free Tier Limitations
- Service sleeps after 15 minutes of inactivity
- 750 hours/month (enough for one service)
- First request after sleep takes 30-60 seconds
- Database: 1GB storage, 97 hours/month

## Updating Your Deployment

When you make changes:
```bash
git add .
git commit -m "Your changes"
git push
```

Render will automatically:
1. Detect the push
2. Start new build
3. Run build.sh
4. Deploy new version
5. Switch traffic to new version

## Troubleshooting

### Build Fails
- Check logs for error message
- Usually missing dependency in requirements.txt
- Or syntax error in Python code

### Service Crashes
- Check logs for Python errors
- Usually database connection issue
- Or missing environment variable

### Database Connection Error
- Check DATABASE_URL is set
- Check database is running
- Check database and service are in same region

### Slow Response
- Free tier services sleep
- First request wakes it up (30-60s)
- Subsequent requests are fast
- Consider paid tier for always-on

## Success Checklist

✅ Service shows "Live" in dashboard
✅ Can access: https://your-url.onrender.com
✅ Can access: https://your-url.onrender.com/login
✅ Can login with admin@pharmacy.com / admin123
✅ Dashboard loads after login
✅ Can add/view medicines, sales, etc.

## Next Steps

1. Change default admin password
2. Create your organization
3. Add users
4. Start using the system
5. Consider upgrading for better performance

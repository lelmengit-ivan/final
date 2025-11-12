# Fix Render Connection Error

## Problem
Login shows "Connection error. Please try again" on Render deployment.

## Root Causes
1. ❌ Database not initialized on Render
2. ❌ No default admin user created
3. ✅ API URL fixed (was hardcoded to localhost)

## Solution

### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Fix API URLs and add database initialization"
git push
```

### Step 2: Render Will Auto-Deploy
Render will automatically:
1. Run `build.sh` which calls `init_render_db.py`
2. Initialize PostgreSQL database
3. Create default organization
4. Create admin user

### Step 3: Check Deployment Logs
In Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for:
   ```
   Initializing database...
   Creating organizations table...
   Creating users table...
   ✅ Database initialized successfully!
   ```

### Step 4: Test Login
Once deployed, go to:
```
https://your-app.onrender.com/login
```

**Default Credentials:**
- Email: `admin@pharmacy.com`
- Password: `admin123`

## What Was Fixed

### 1. API URLs (static/js/login.js & script.js)
**Before:**
```javascript
const API_URL = 'http://localhost:5000/api';
```

**After:**
```javascript
const API_URL = window.location.origin + '/api';
```

This makes it work on both:
- Local: `http://localhost:5000/api`
- Render: `https://your-app.onrender.com/api`

### 2. Database Initialization (build.sh)
**Before:**
```bash
pip install -r requirements.txt
python migrate_to_multitenancy.py
```

**After:**
```bash
pip install -r requirements.txt
python init_render_db.py
```

The new script:
- Creates all tables
- Creates default organization
- Creates admin user
- Works with PostgreSQL

## Troubleshooting

### If still getting connection error:

1. **Check if service is running:**
   - Go to Render dashboard
   - Service should show "Live" status

2. **Check database connection:**
   - In Render dashboard, go to your database
   - Verify it's connected to your web service

3. **Check logs for errors:**
   ```
   Look for Python errors or database connection issues
   ```

4. **Manually run initialization:**
   In Render Shell (Dashboard → Shell):
   ```bash
   python init_render_db.py
   ```

5. **Check browser console:**
   - Press F12 in browser
   - Go to Console tab
   - Look for actual error messages

### Common Issues:

**"Failed to fetch"**
- Service is not running
- Check Render dashboard status

**"401 Unauthorized"**
- Wrong credentials
- Use: admin@pharmacy.com / admin123

**"403 Forbidden"**
- Organization subscription inactive
- Check database organization status

**"500 Internal Server Error"**
- Database not initialized
- Run init_render_db.py manually

## Verify It's Working

After deployment, you should be able to:
1. ✅ Load login page
2. ✅ Login with admin credentials
3. ✅ See dashboard
4. ✅ Access all features

## Next Steps

After successful login:
1. Change admin password
2. Create your organization
3. Add users
4. Start using the system

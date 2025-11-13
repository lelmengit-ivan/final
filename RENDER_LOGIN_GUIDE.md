# How to Login Successfully on Render

## Step 1: Deploy to Render

### 1.1 Commit and Push Changes
```bash
git add .
git commit -m "Add database initialization and fix API URLs"
git push
```

### 1.2 Wait for Deployment
- Go to Render Dashboard: https://dashboard.render.com
- Watch the deployment logs
- Wait for "Build successful" and "Live" status

## Step 2: Initialize Database

The `build.sh` script should automatically run `init_render_db.py`, but if it doesn't:

### Option A: Check Build Logs
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. Look for:
   ```
   Initializing database...
   Creating organizations table...
   Creating users table...
   ✅ Database initialized successfully!
   ```

### Option B: Manual Initialization (if needed)
1. Go to Render Dashboard
2. Click your service
3. Click "Shell" tab (top right)
4. Run:
   ```bash
   python init_render_db.py
   ```
5. Wait for success message

## Step 3: Test Login

### 3.1 Get Your Render URL
Your URL will be something like:
```
https://pharmacy-system-abc123.onrender.com
```

### 3.2 Go to Login Page
```
https://your-app.onrender.com/login
```

### 3.3 Login with Default Credentials
```
Email: admin@pharmacy.com
Password: admin123
```

## Troubleshooting

### Issue 1: "Connection error. Please try again"

**Cause**: Database not initialized or service not running

**Solution**:
1. Check Render dashboard - service should show "Live"
2. Check logs for errors
3. Run `python init_render_db.py` in Render Shell

### Issue 2: "Invalid credentials"

**Cause**: Database initialized but wrong password

**Solution**:
Try these credentials:
- Email: `admin@pharmacy.com`, Password: `admin123`
- Username: `admin`, Password: `admin123`

### Issue 3: "Failed to fetch" or CORS error

**Cause**: API endpoint not responding

**Solution**:
1. Check if service is running (Render dashboard)
2. Test API directly:
   ```bash
   curl https://your-app.onrender.com/api/login \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@pharmacy.com","password":"admin123"}'
   ```

### Issue 4: Service keeps sleeping

**Cause**: Render free tier sleeps after 15 minutes

**Solution**:
- First request takes 30-60 seconds to wake up
- Be patient and wait
- Consider upgrading to paid tier for always-on service

### Issue 5: 500 Internal Server Error

**Cause**: Database connection issue or missing tables

**Solution**:
1. Check DATABASE_URL is set in Render environment variables
2. Check PostgreSQL database is running
3. Run database initialization:
   ```bash
   python init_render_db.py
   ```

## Verify Everything is Working

### Test 1: Check Service Status
```bash
curl https://your-app.onrender.com
```
Should return HTML (status 200)

### Test 2: Test Login API
```bash
curl -X POST https://your-app.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```
Should return JSON with token

### Test 3: Browser Login
1. Go to: `https://your-app.onrender.com/login`
2. Enter credentials
3. Should redirect to dashboard

## Expected Flow

```
1. User visits: https://your-app.onrender.com/login
   ↓
2. Enters: admin@pharmacy.com / admin123
   ↓
3. JavaScript sends POST to: /api/login
   ↓
4. Flask backend checks PostgreSQL database
   ↓
5. Returns JWT token
   ↓
6. Frontend stores token in localStorage
   ↓
7. Redirects to: /dashboard (index.html)
   ↓
8. Dashboard loads with user data
```

## Common Mistakes

❌ **Forgot to push changes**
- Solution: `git push` to trigger new deployment

❌ **Database not initialized**
- Solution: Run `python init_render_db.py` in Shell

❌ **Wrong URL**
- Solution: Use the URL from Render dashboard

❌ **Service sleeping**
- Solution: Wait 30-60 seconds for first request

❌ **Environment variables not set**
- Solution: Check DATABASE_URL in Render settings

## After Successful Login

Once logged in, you should:

1. ✅ See the dashboard
2. ✅ See your username in header
3. ✅ Be able to navigate tabs
4. ✅ Add medicines, sales, etc.

## Security: Change Default Password

After first login:
1. Go to Settings (if available)
2. Change admin password from `admin123`
3. Or update directly in database

## Need Help?

If still having issues:

1. **Check Render Logs**:
   - Dashboard → Your Service → Logs
   - Look for Python errors

2. **Check Database**:
   - Dashboard → Your Database
   - Verify it's connected to web service

3. **Test API Manually**:
   ```bash
   python test_render_api.py
   ```
   Enter your Render URL when prompted

4. **Check Browser Console**:
   - Press F12
   - Go to Console tab
   - Look for JavaScript errors

# Deploy Backend to Render NOW

## What You Need
- GitHub account
- Render account (free) - https://render.com
- Your code pushed to GitHub

## Step 1: Push Code to GitHub

If not already done:
```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

## Step 2: Create Render Account

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repositories

## Step 3: Deploy Using render.yaml (Easiest Method)

### Option A: Blueprint (Recommended - Deploys Everything)

1. In Render Dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repository
3. Render will detect `render.yaml` automatically
4. Click "Apply"
5. Render will create:
   - PostgreSQL database (`pharmacy-db`)
   - Web service (`pharmacy-system`)
   - Connect them automatically
6. Wait 5-10 minutes for deployment
7. Done! ✅

### Option B: Manual Setup (If Blueprint doesn't work)

#### 3.1 Create Database First
1. Click "New +" → "PostgreSQL"
2. Fill in:
   - Name: `pharmacy-db`
   - Database: `pharmacy_db`
   - User: `pharmacy_user`
   - Region: Choose closest to you
   - Plan: **Free**
3. Click "Create Database"
4. Wait 2-3 minutes

#### 3.2 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository
4. Fill in:
   - **Name**: `pharmacy-system`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free**

5. Click "Advanced" to add environment variables:
   - `PYTHON_VERSION` = `3.11.0`
   - `SECRET_KEY` = Click "Generate" button

6. Add Database Connection:
   - Still in "Advanced" section
   - Click "Add Environment Variable"
   - Click "Add from Database"
   - Select `pharmacy-db`
   - Select `DATABASE_URL`
   - Click "Add"

7. Click "Create Web Service"

## Step 4: Watch Deployment

You'll see logs like:
```
==> Cloning from https://github.com/your-repo...
==> Downloading cache...
==> Running build command: chmod +x build.sh && ./build.sh
==> Installing dependencies...
==> Initializing database...
    Creating organizations table...
    Creating users table...
    ✅ Database initialized successfully!
==> Build successful!
==> Starting server...
==> Your service is live at https://pharmacy-system-xyz.onrender.com
```

This takes **5-10 minutes** for first deployment.

## Step 5: Get Your URL

Once deployed, you'll see:
```
🎉 Your service is live at https://pharmacy-system-abc123.onrender.com
```

**Copy this URL!**

## Step 6: Test Login

1. Go to: `https://your-url.onrender.com/login`
2. Login with:
   - **Email**: `admin@pharmacy.com`
   - **Password**: `admin123`
3. Should redirect to dashboard ✅

## Troubleshooting

### Build Failed

**Check logs for errors:**
- Missing dependency? Add to `requirements.txt`
- Syntax error? Fix in code and push again
- Permission denied on build.sh? Already fixed in render.yaml

### Service Created but Not Starting

**Check logs:**
- Database connection error? Check DATABASE_URL is set
- Port binding error? Render handles this automatically
- Python error? Check app.py for issues

### Login Shows "Connection Error"

**Database not initialized:**
1. Go to your service in Render
2. Click "Shell" tab (top right)
3. Run: `python init_render_db.py`
4. Wait for success message
5. Try login again

### Service Keeps Sleeping

**This is normal for free tier:**
- Service sleeps after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast
- Upgrade to paid tier for always-on

## What Gets Deployed

✅ **Backend**: Flask app with all API endpoints
✅ **Frontend**: HTML/CSS/JS files served by Flask
✅ **Database**: PostgreSQL with all tables
✅ **Default User**: admin@pharmacy.com / admin123

## After Successful Deployment

### Your URLs:
- **Login**: `https://your-url.onrender.com/login`
- **Dashboard**: `https://your-url.onrender.com/`
- **API**: `https://your-url.onrender.com/api/*`

### Test API:
```bash
curl https://your-url.onrender.com/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```

Should return JSON with token.

## Automatic Redeployment

Every time you push to GitHub:
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
5. Zero downtime switch

## Cost

**Free Tier Includes:**
- 750 hours/month web service (enough for 1 service)
- PostgreSQL database (1GB, 97 hours/month)
- Automatic HTTPS
- Custom domain support
- Automatic deploys from Git

**Limitations:**
- Service sleeps after 15 minutes
- Slower performance
- Limited resources

**Paid Tier ($7/month):**
- Always-on service
- Better performance
- More resources
- No sleep

## Need Help?

If deployment fails:
1. Check Render logs for error message
2. Check GitHub repository is accessible
3. Check all files are committed and pushed
4. Try manual setup instead of Blueprint

## Quick Commands

**Check if code is ready:**
```bash
git status
git log -1
```

**Push to GitHub:**
```bash
git add .
git commit -m "Deploy to Render"
git push
```

**Test locally first:**
```bash
python app.py
# Visit http://localhost:5000/login
```

## Success Checklist

Before deploying:
✅ Code pushed to GitHub
✅ `requirements.txt` has all dependencies
✅ `render.yaml` configured
✅ `build.sh` exists
✅ `init_render_db.py` exists
✅ `app.py` works locally

After deploying:
✅ Service shows "Live" (green)
✅ Can access login page
✅ Can login with admin credentials
✅ Dashboard loads
✅ Can add/view data

---

## Ready to Deploy?

1. Make sure code is pushed to GitHub
2. Go to https://render.com
3. Sign up/Login
4. Click "New +" → "Blueprint"
5. Select your repository
6. Click "Apply"
7. Wait 5-10 minutes
8. Test login!

Good luck! 🚀

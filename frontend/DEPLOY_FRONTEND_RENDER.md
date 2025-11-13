# 🎨 Deploy Frontend to Render (Static Site)

Deploy your frontend as a static site on Render.

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Code pushed to GitHub
- ✅ Render account
- ✅ Backend already deployed (to get API URL)

## ⚙️ Step 1: Configure API URL

Before deploying, update the backend API URL.

Edit `frontend/static/config.js`:

```javascript
const CONFIG = {
    // Replace with your Render backend URL
    API_URL: 'https://pharmacy-system-abc123.onrender.com/api'
};

window.CONFIG = CONFIG;
```

**Get your backend URL:**
1. Go to Render Dashboard
2. Click your backend service
3. Copy the URL (e.g., `https://pharmacy-system-xyz.onrender.com`)
4. Add `/api` to the end

## 🚀 Step 2: Push to GitHub

```bash
# Commit the config change
git add frontend/static/config.js
git commit -m "Configure API URL for production"
git push
```

## 📦 Step 3: Create Static Site on Render

### 3.1 Go to Render Dashboard
- Visit: https://dashboard.render.com
- Login with your account

### 3.2 Create New Static Site
1. Click **"New +"**
2. Select **"Static Site"**

### 3.3 Connect Repository
1. Click **"Connect account"** (if not connected)
2. Select your GitHub repository
3. Click **"Connect"**

### 3.4 Configure Static Site

Fill in the configuration:

#### Basic Settings:
```
Name: pharmacy-frontend
Branch: main
```

#### Build Settings:
```
Root Directory: frontend
Build Command: (leave empty)
Publish Directory: .
```

**Important:** Set `Root Directory` to `frontend` so Render uses only the frontend folder.

### 3.5 Advanced Settings (Optional)

Click **"Advanced"** if you need to:
- Add custom headers
- Set up redirects
- Configure custom domain

### 3.6 Create Static Site

1. Review all settings
2. Click **"Create Static Site"**
3. Deployment will start

## ⏱️ Step 4: Wait for Deployment

Deployment takes 1-2 minutes.

You'll see logs:
```
==> Cloning from GitHub...
==> Building static site...
==> Deploying to CDN...
==> Your site is live at https://pharmacy-frontend.onrender.com
```

## 🌐 Step 5: Get Your URL

Once deployed:
```
🎉 https://pharmacy-frontend-abc123.onrender.com
```

## 🧪 Step 6: Test Your Frontend

### Test 1: Open Login Page
```
https://pharmacy-frontend-abc123.onrender.com/login.html
```

Should load the login page.

### Test 2: Login
Use default credentials:
```
Email: admin@pharmacy.com
Password: admin123
```

### Test 3: Dashboard
After login, should redirect to dashboard:
```
https://pharmacy-frontend-abc123.onrender.com/index.html
```

### Test 4: Check API Connection
Open browser console (F12) and check:
- No CORS errors
- API calls successful
- Data loads correctly

## 🔧 Configuration Details

### Directory Structure:
```
Your Repository
└── frontend/              ← Root Directory (set in Render)
    ├── index.html
    ├── login.html
    ├── register-org.html
    └── static/
        ├── config.js      ← API URL configured here
        ├── css/
        └── js/
```

### Render Settings:
```
Type: Static Site
Name: pharmacy-frontend
Root Directory: frontend
Build Command: (empty)
Publish Directory: .
Auto-Deploy: Yes
```

## 🔄 Update Deployment

When you make changes:

```bash
# 1. Make changes to frontend files
# 2. Commit
git add frontend/
git commit -m "Update frontend"

# 3. Push
git push
```

Render will automatically:
1. Detect the push
2. Rebuild the site
3. Deploy new version
4. Update CDN

## 🌍 Enable CORS on Backend

Your backend must allow requests from the frontend domain.

In your backend `app.py`, ensure CORS is configured:

```python
from flask_cors import CORS

# Allow all origins (simple)
CORS(app, resources={r"/*": {"origins": "*"}})

# Or specific origins (recommended)
CORS(app, resources={r"/*": {
    "origins": [
        "https://pharmacy-frontend-abc123.onrender.com",
        "http://localhost:5000"  # for local development
    ]
}})
```

After changing CORS:
```bash
git add app.py
git commit -m "Update CORS for frontend domain"
git push
```

Backend will auto-redeploy.

## 🔗 Custom Domain (Optional)

### Step 1: Add Domain in Render
1. Go to your static site settings
2. Click **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `pharmacy.yourdomain.com`)

### Step 2: Update DNS
Add these records to your DNS provider:

**For subdomain (pharmacy.yourdomain.com):**
```
Type: CNAME
Name: pharmacy
Value: pharmacy-frontend-abc123.onrender.com
```

**For root domain (yourdomain.com):**
```
Type: A
Name: @
Value: [IP provided by Render]
```

### Step 3: Wait for SSL
Render will automatically provision SSL certificate (5-10 minutes).

## 📊 Monitoring

### Check Deployment Status:
1. Go to Render Dashboard
2. Click your static site
3. View deployment history

### Check Logs:
1. Click **"Logs"** tab
2. View deployment logs
3. Check for errors

### Analytics:
Render provides basic analytics:
- Bandwidth usage
- Request count
- Deploy history

## 🚨 Troubleshooting

### Issue 1: Site Not Loading

**Problem:** 404 or blank page

**Solution:**
1. Check Root Directory is set to `frontend`
2. Check Publish Directory is `.`
3. Verify files exist in GitHub
4. Check deployment logs

### Issue 2: CORS Error

**Problem:** "Access-Control-Allow-Origin" error

**Solution:**
1. Update backend CORS configuration
2. Add frontend domain to allowed origins
3. Redeploy backend
4. Clear browser cache

### Issue 3: API Not Working

**Problem:** API calls fail or return 404

**Solution:**
1. Check `static/config.js` has correct API URL
2. Verify backend is running
3. Test API directly:
   ```bash
   curl https://your-backend.onrender.com/api/login \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@pharmacy.com","password":"admin123"}'
   ```

### Issue 4: CSS/JS Not Loading

**Problem:** Styles or scripts not working

**Solution:**
1. Check file paths in HTML
2. Ensure `static/` folder structure is correct
3. Check browser console for 404 errors
4. Verify files are in GitHub

### Issue 5: Login Redirects to Wrong URL

**Problem:** After login, redirects to localhost

**Solution:**
1. Check `static/js/login.js`
2. Ensure redirect uses relative path:
   ```javascript
   window.location.href = '/';  // Good
   // Not: window.location.href = 'http://localhost:5000/';
   ```

## 🎯 Best Practices

### 1. Environment-Specific Config
Use different config for different environments:

**Development (local):**
```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000/api'
};
```

**Production (Render):**
```javascript
const CONFIG = {
    API_URL: 'https://pharmacy-backend.onrender.com/api'
};
```

### 2. Use Relative Paths
In HTML files:
```html
<!-- Good -->
<link rel="stylesheet" href="/static/css/styles.css">
<script src="/static/js/script.js"></script>

<!-- Avoid -->
<link rel="stylesheet" href="http://localhost:5000/static/css/styles.css">
```

### 3. Cache Busting
Add version to static files:
```html
<link rel="stylesheet" href="/static/css/styles.css?v=1.0.0">
<script src="/static/js/script.js?v=1.0.0"></script>
```

### 4. Error Handling
Add error handling in JavaScript:
```javascript
fetch(API_URL + '/login', {...})
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Connection error. Please try again.');
    });
```

## 📈 Performance

### Render Static Site Features:
- ✅ Global CDN
- ✅ Automatic HTTPS
- ✅ Instant cache invalidation
- ✅ Automatic compression
- ✅ HTTP/2 support

### Free Tier:
- 100 GB bandwidth/month
- Unlimited sites
- Custom domains
- Automatic SSL

## 🔐 Security

### HTTPS:
- ✅ Automatic SSL certificate
- ✅ Auto-renewal
- ✅ Force HTTPS redirect

### Headers:
Add security headers (optional):
1. Go to static site settings
2. Add custom headers:
   ```
   X-Frame-Options: DENY
   X-Content-Type-Options: nosniff
   X-XSS-Protection: 1; mode=block
   ```

## 📝 Deployment Checklist

**Before Deployment:**
- [ ] `static/config.js` has correct API URL
- [ ] All files committed to GitHub
- [ ] Backend is deployed and running
- [ ] CORS configured on backend
- [ ] Tested locally

**After Deployment:**
- [ ] Site loads correctly
- [ ] Login works
- [ ] Dashboard loads
- [ ] API calls successful
- [ ] No CORS errors
- [ ] Mobile responsive
- [ ] HTTPS enabled

## 🎨 Architecture

```
User Browser
    ↓
Render Static Site (Frontend)
    ↓ API Calls
Render Web Service (Backend)
    ↓
PostgreSQL Database
```

**URLs:**
```
Frontend: https://pharmacy-frontend.onrender.com
Backend:  https://pharmacy-backend.onrender.com
```

## 📊 Comparison: Static Site vs Web Service

| Feature | Static Site | Web Service |
|---------|-------------|-------------|
| Use Case | Frontend only | Backend + Frontend |
| Build | No build needed | Runs build.sh |
| Server | CDN only | Python/Node server |
| Database | No | Yes |
| Cost | Free | Free (with limits) |
| Sleep | Never | After 15 min |
| Speed | Very fast | Fast |

## ✅ Success Indicators

After deployment:
- ✅ Site shows "Live" status
- ✅ Login page loads
- ✅ Can login successfully
- ✅ Dashboard loads with data
- ✅ All features work
- ✅ No console errors
- ✅ Mobile responsive

## 🆘 Support

**Render Docs:**
- https://render.com/docs/static-sites

**Community:**
- https://community.render.com

**Status:**
- https://status.render.com

---

## 🎉 Quick Deploy Summary

```bash
# 1. Configure API URL
# Edit frontend/static/config.js

# 2. Push to GitHub
git add .
git commit -m "Configure for Render"
git push

# 3. Create Static Site on Render
# - New + → Static Site
# - Root Directory: frontend
# - Publish Directory: .

# 4. Deploy!
# Wait 1-2 minutes

# 5. Test
# Visit: https://your-frontend.onrender.com/login.html
```

Your frontend is now live on Render! 🚀

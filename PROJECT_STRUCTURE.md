# Pharmacy Management System - Clean Project Structure

## 📁 Clean Structure

```
pharmacy-system/
│
├── backend/                    # Backend files (organized copy)
│   ├── app.py
│   ├── database.py
│   ├── ai_predictor.py
│   ├── init_render_db.py
│   ├── requirements.txt
│   ├── render.yaml
│   ├── build.sh
│   ├── .gitignore
│   └── .renderignore
│
├── frontend/                   # Frontend files (organized copy)
│   ├── index.html
│   ├── login.html
│   ├── register-org.html
│   ├── README.md
│   └── static/
│       ├── config.js
│       ├── css/
│       │   ├── styles.css
│       │   └── login.css
│       └── js/
│           ├── script.js
│           └── login.js
│
├── static/                     # Static assets (root)
│   ├── config.js
│   ├── css/
│   │   ├── styles.css
│   │   └── login.css
│   └── js/
│       ├── script.js
│       └── login.js
│
├── app.py                      # Main Flask application
├── database.py                 # Database handler
├── ai_predictor.py             # AI predictions module
├── init_render_db.py           # Database initialization
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── build.sh                    # Build script
├── .gitignore                  # Git ignore rules
├── .renderignore               # Render ignore rules
│
├── index.html                  # Dashboard page
├── login.html                  # Login page
├── register-org.html           # Organization registration
│
├── pharmacy.db                 # SQLite database (local only)
├── README.md                   # Main documentation
└── PROJECT_STRUCTURE.md        # This file
```

## 🎯 Deployment Options

### Option 1: Deploy from Root (Recommended)
Deploy the entire project as-is. Render will use files from root directory.

**Advantages:**
- Simple, no changes needed
- All files in expected locations
- Works immediately

**Deploy:**
```bash
git add .
git commit -m "Deploy to Render"
git push
```

### Option 2: Deploy Backend Folder Only
Deploy only the `backend/` folder to Render.

**Advantages:**
- Clean separation
- Smaller deployment
- Backend-only focus

**Deploy:**
1. Update `render.yaml` to set `rootDirectory: backend`
2. Or create new repo with only backend files

### Option 3: Separate Frontend & Backend
Deploy frontend and backend separately.

**Frontend:** Netlify, Vercel, GitHub Pages  
**Backend:** Render, Heroku, Railway

**Advantages:**
- Independent scaling
- Separate domains
- Better for large teams

## 📦 What to Deploy

### For Render (Backend + Frontend):
```
✅ app.py
✅ database.py
✅ ai_predictor.py
✅ init_render_db.py
✅ requirements.txt
✅ render.yaml
✅ build.sh
✅ index.html
✅ login.html
✅ register-org.html
✅ static/ folder
✅ .gitignore
✅ .renderignore
```

### Not Needed for Deployment:
```
❌ test_*.py files
❌ check_*.py files
❌ fix_*.py files
❌ *_GUIDE.md files
❌ debug files
❌ backup files
❌ __pycache__/
❌ pharmacy.db (local only)
```

## 🚀 Quick Deploy

### From Root Directory:
```bash
# 1. Commit changes
git add .
git commit -m "Ready for deployment"
git push

# 2. Deploy on Render
# - Go to render.com
# - New + → Web Service
# - Connect repository
# - Use root directory
# - Deploy!
```

### From Backend Directory:
```bash
# 1. Update render.yaml
# Add: rootDirectory: backend

# 2. Commit and push
git add .
git commit -m "Deploy backend"
git push

# 3. Deploy on Render
# - Render will use backend/ folder
```

## 📝 Files Explained

### Backend Files:
- **app.py** - Main Flask application, all API routes
- **database.py** - Database connection and operations
- **ai_predictor.py** - Stock prediction AI model
- **init_render_db.py** - Initialize PostgreSQL database
- **requirements.txt** - Python dependencies
- **render.yaml** - Render deployment configuration
- **build.sh** - Build script (installs deps, inits DB)

### Frontend Files:
- **index.html** - Main dashboard page
- **login.html** - Login/registration page
- **register-org.html** - Organization registration
- **static/config.js** - API URL configuration
- **static/css/** - Stylesheets
- **static/js/** - JavaScript logic

### Configuration Files:
- **.gitignore** - Files to ignore in Git
- **.renderignore** - Files to ignore in Render
- **README.md** - Project documentation

## 🔧 Configuration

### For Local Development:
```javascript
// static/config.js
const CONFIG = {
    API_URL: 'http://localhost:5000/api'
};
```

### For Production (Render):
```javascript
// static/config.js
const CONFIG = {
    API_URL: window.location.origin + '/api'
};
```

## 📊 Database

### Local (SQLite):
- File: `pharmacy.db`
- Auto-created on first run
- For development only

### Production (PostgreSQL):
- Hosted on Render
- Configured via DATABASE_URL
- Initialized by `init_render_db.py`

## 🎨 Customization

### Change API URL:
Edit `static/config.js`

### Change Styles:
Edit `static/css/styles.css` or `static/css/login.css`

### Add Features:
1. Update `app.py` for backend
2. Update `static/js/script.js` for frontend
3. Update HTML files for UI

## 📚 Documentation

- **README.md** - Main project documentation
- **frontend/README.md** - Frontend-specific docs
- **PROJECT_STRUCTURE.md** - This file

## ✅ Deployment Checklist

Before deploying:
- [ ] All files committed to Git
- [ ] `requirements.txt` has all dependencies
- [ ] `render.yaml` configured correctly
- [ ] `build.sh` is executable
- [ ] `static/config.js` uses auto-detect
- [ ] No hardcoded localhost URLs
- [ ] Database initialization script ready
- [ ] .gitignore excludes unnecessary files

After deploying:
- [ ] Service shows "Live" status
- [ ] Database initialized successfully
- [ ] Login page loads
- [ ] Can login with admin credentials
- [ ] Dashboard loads correctly
- [ ] All features work

## 🆘 Support

If you need help:
1. Check README.md
2. Check frontend/README.md
3. Check Render logs
4. Test API endpoints manually

---

**Clean Structure Created:** November 2025  
**Ready for Deployment:** ✅

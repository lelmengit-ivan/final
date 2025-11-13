# 📁 Project Files Overview

## Essential Files (Root Directory)

### Application Files:
- `app.py` - Main Flask application
- `database.py` - Database handler
- `ai_predictor.py` - AI predictions module
- `init_render_db.py` - Database initialization

### Frontend Files:
- `index.html` - Dashboard page
- `login.html` - Login page
- `register-org.html` - Organization registration
- `static/` - CSS, JS, images

### Configuration:
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment config
- `build.sh` - Build script
- `.gitignore` - Git ignore rules
- `.renderignore` - Render ignore rules

### Documentation:
- `README.md` - Main project documentation
- `DEPLOYMENT.md` - Deployment quick reference

### Database:
- `pharmacy.db` - SQLite database (local only)

## Organized Folders

### backend/
Complete backend files for separate deployment:
- All backend code
- `DEPLOY_BACKEND.md` - Backend deployment guide

### frontend/
Complete frontend files for separate deployment:
- All HTML, CSS, JS files
- `README.md` - Frontend documentation
- `DEPLOY_FRONTEND_RENDER.md` - Frontend deployment guide

## File Count

**Root:** 14 essential files  
**Backend folder:** 9 files  
**Frontend folder:** 7 files  
**Total:** ~30 files (clean and minimal)

## What Was Removed

- ❌ Test files (test_*.py)
- ❌ Check files (check_*.py)
- ❌ Fix files (fix_*.py)
- ❌ Debug files
- ❌ Excessive documentation (20+ MD files)
- ❌ Platform-specific files (Heroku, Vercel)
- ❌ Utility scripts
- ❌ Backup folders
- ❌ Python cache

## Deployment

**Full Stack:** Use root files  
**Backend Only:** Use `backend/` folder  
**Frontend Only:** Use `frontend/` folder  

See `DEPLOYMENT.md` for quick reference.

---

**Status:** ✅ Clean, minimal, production-ready

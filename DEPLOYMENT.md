# 🚀 Deployment Guide

Quick reference for deploying the Pharmacy Management System.

## 📁 Project Structure

```
pharmacy-system/
├── backend/              # Backend deployment files
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── DEPLOY_BACKEND.md    ← Backend deployment guide
│
├── frontend/             # Frontend deployment files
│   ├── index.html
│   ├── login.html
│   ├── static/
│   └── DEPLOY_FRONTEND_RENDER.md    ← Frontend deployment guide
│
├── app.py               # Main application
├── database.py          # Database handler
├── requirements.txt     # Dependencies
├── render.yaml          # Render config
└── README.md            # Main documentation
```

## 🎯 Deployment Options

### Option 1: Full Stack on Render (Recommended)
Deploy both backend and frontend together.

**Steps:**
1. Push code to GitHub
2. Create PostgreSQL database on Render
3. Create Web Service on Render
4. Configure environment variables
5. Deploy!

**Guide:** See root `README.md`

### Option 2: Backend Only
Deploy just the API backend.

**Steps:**
1. Follow `backend/DEPLOY_BACKEND.md`
2. Get API URL
3. Use with any frontend

**Guide:** `backend/DEPLOY_BACKEND.md`

### Option 3: Frontend as Static Site
Deploy frontend separately from backend.

**Steps:**
1. Deploy backend first
2. Update frontend config with API URL
3. Deploy frontend as static site

**Guide:** `frontend/DEPLOY_FRONTEND_RENDER.md`

## 📚 Documentation

- **Main README**: `README.md` - Project overview
- **Backend Deploy**: `backend/DEPLOY_BACKEND.md` - Backend deployment
- **Frontend Deploy**: `frontend/DEPLOY_FRONTEND_RENDER.md` - Frontend deployment
- **Frontend Docs**: `frontend/README.md` - Frontend documentation

## ⚡ Quick Deploy

### Backend to Render:
```bash
git push
# Then follow backend/DEPLOY_BACKEND.md
```

### Frontend to Render:
```bash
# Update frontend/static/config.js with API URL
git push
# Then follow frontend/DEPLOY_FRONTEND_RENDER.md
```

## 🔗 Links

- **Render**: https://render.com
- **Docs**: Check individual deployment guides
- **Support**: See README.md

---

**For detailed instructions, see the specific deployment guides above.**

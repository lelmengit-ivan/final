# Use Render Backend with Local Frontend

This setup allows you to run the frontend locally while connecting to your Render backend API.

## Setup Steps

### 1. Get Your Render URL

Go to your Render dashboard and copy your service URL:
```
https://pharmacy-system-abc123.onrender.com
```

### 2. Update config.js

Open `config.js` and replace `YOUR_RENDER_URL_HERE` with your actual Render URL:

```javascript
const CONFIG = {
    API_URL: 'https://pharmacy-system-abc123.onrender.com/api'
};
```

**Example:**
```javascript
const CONFIG = {
    API_URL: 'https://pharmacy-mgmt-xyz789.onrender.com/api'
};
```

### 3. Start Local Server

You still need a local server to serve the HTML files:

**Option A: Python (Recommended)**
```bash
python app.py
```

**Option B: Simple HTTP Server**
```bash
python -m http.server 5000
```

### 4. Open in Browser

Go to: `http://localhost:5000/login.html`

Now your frontend will connect to the Render backend!

## How It Works

- **Frontend**: Runs locally (HTML/CSS/JS files)
- **Backend**: Runs on Render (API endpoints)
- **Database**: PostgreSQL on Render

```
Browser (localhost:5000)
    ↓
    → Loads HTML/CSS/JS locally
    ↓
    → Makes API calls to Render
    ↓
Render Backend (your-app.onrender.com/api)
    ↓
PostgreSQL Database (Render)
```

## Switch Between Local and Render Backend

### Use Render Backend:
```javascript
// config.js
const CONFIG = {
    API_URL: 'https://your-app.onrender.com/api'
};
```

### Use Local Backend:
```javascript
// config.js
const CONFIG = {
    API_URL: 'http://localhost:5000/api'
};
```

### Auto-detect (Default):
```javascript
// config.js
const CONFIG = {
    API_URL: window.location.origin + '/api'
};
```

## Troubleshooting

### CORS Errors
If you get CORS errors, the Render backend needs to allow your local origin.

Check `app.py`:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

This should already be set to allow all origins.

### Connection Timeout
- Render free tier services sleep after 15 minutes of inactivity
- First request may take 30-60 seconds to wake up
- Subsequent requests will be fast

### 401 Unauthorized
- Token expired
- Clear localStorage and login again
- Check if you're using correct credentials

### 500 Internal Server Error
- Database not initialized on Render
- Go to Render Shell and run: `python init_render_db.py`

## Benefits of This Setup

✅ **Fast Development**: Edit HTML/CSS/JS locally, see changes instantly
✅ **Real Data**: Use production database from Render
✅ **No Local Database**: Don't need to set up PostgreSQL locally
✅ **Test Production**: Test against real production environment
✅ **No CORS Issues**: Backend already configured for CORS

## When to Use This

- Testing frontend changes against production data
- Developing new features without local database setup
- Debugging production issues locally
- Working on UI without backend changes

## When NOT to Use This

- Making backend changes (use local backend instead)
- Testing database migrations (use local SQLite)
- Offline development (no internet = no backend)
- Heavy testing (avoid hitting Render rate limits)

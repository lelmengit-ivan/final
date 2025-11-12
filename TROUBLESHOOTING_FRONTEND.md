# Troubleshooting Frontend Issues

## Issue: Inventory, Prescriptions, Suppliers Not Loading

### Quick Fixes

#### 1. Clear Browser Cache & Storage
```javascript
// Open browser console (F12) and run:
localStorage.clear();
sessionStorage.clear();
location.reload();
```

#### 2. Check Console for Errors
1. Open browser (F12)
2. Go to Console tab
3. Look for red errors
4. Check Network tab for failed requests

#### 3. Re-login
1. Logout completely
2. Clear browser data
3. Login again with: admin@pharmacy.com / admin123

#### 4. Test API Directly
Open: http://localhost:5000/test_frontend.html
This will test all endpoints

### Common Issues

#### Issue: "401 Unauthorized"
**Cause:** Token expired or missing
**Fix:**
```javascript
// In browser console:
localStorage.removeItem('token');
localStorage.removeItem('user');
window.location.href = '/login';
```

#### Issue: "CORS Error"
**Cause:** Server not allowing requests
**Fix:** Server already has CORS enabled, restart server:
```bash
# Stop server (Ctrl+C)
python app.py
```

#### Issue: "Network Error"
**Cause:** Server not running
**Fix:**
```bash
python app.py
```

#### Issue: Data Not Showing
**Cause:** Empty database or wrong organization
**Fix:**
```bash
# Check database
python -c "import sqlite3; conn = sqlite3.connect('pharmacy.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM medicines WHERE user_id=1'); print('Medicines:', cursor.fetchone()[0]); cursor.execute('SELECT COUNT(*) FROM suppliers WHERE user_id=1'); print('Suppliers:', cursor.fetchone()[0])"
```

### Manual Test Steps

#### Test 1: Login
1. Go to: http://localhost:5000/login
2. Enter: admin@pharmacy.com / admin123
3. Should redirect to dashboard

#### Test 2: Check Token
```javascript
// In browser console:
console.log('Token:', localStorage.getItem('token'));
console.log('User:', localStorage.getItem('user'));
```

#### Test 3: Test API Call
```javascript
// In browser console:
const token = localStorage.getItem('token');
fetch('http://localhost:5000/api/medicines', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
}).then(r => r.json()).then(d => console.log('Medicines:', d));
```

#### Test 4: Test Suppliers
```javascript
// In browser console:
const token = localStorage.getItem('token');
fetch('http://localhost:5000/api/suppliers', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
}).then(r => r.json()).then(d => console.log('Suppliers:', d));
```

#### Test 5: Test Prescriptions
```javascript
// In browser console:
const token = localStorage.getItem('token');
fetch('http://localhost:5000/api/prescriptions', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
}).then(r => r.json()).then(d => console.log('Prescriptions:', d));
```

### Verification Commands

#### Check Server Status
```bash
# Should show "Running on http://127.0.0.1:5000"
# If not, run: python app.py
```

#### Test All Endpoints
```bash
python test_endpoints.py
```

#### Check Database
```bash
python -c "import sqlite3; conn = sqlite3.connect('pharmacy.db'); cursor = conn.cursor(); cursor.execute('SELECT id, name FROM medicines LIMIT 5'); print('Medicines:', cursor.fetchall()); cursor.execute('SELECT id, name FROM suppliers LIMIT 5'); print('Suppliers:', cursor.fetchall())"
```

### If Still Not Working

#### Nuclear Option: Complete Reset
```bash
# 1. Stop server (Ctrl+C)

# 2. Backup database
copy pharmacy.db pharmacy_backup.db

# 3. Reset admin
python fix_admin_login.py

# 4. Start server
python app.py

# 5. In browser:
# - Clear all site data (F12 > Application > Clear storage)
# - Go to http://localhost:5000/login
# - Login with admin@pharmacy.com / admin123
```

### Debug Mode

#### Enable Verbose Logging
Add to browser console:
```javascript
// Override fetch to log all requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('Fetch:', args[0]);
    return originalFetch.apply(this, args)
        .then(response => {
            console.log('Response:', response.status, args[0]);
            return response;
        });
};
```

### Contact Points

If issues persist:
1. Check server terminal for errors
2. Check browser console for errors
3. Run: `python test_endpoints.py`
4. Open: http://localhost:5000/test_frontend.html
5. Check: `SETUP_COMPLETE.md` for full setup

### Expected Behavior

When working correctly:
- ✅ Login redirects to dashboard
- ✅ Inventory tab shows 11 medicines
- ✅ Suppliers tab shows 6 suppliers
- ✅ Prescriptions tab shows 1 prescription
- ✅ All tabs load without errors
- ✅ No 401/403 errors in console

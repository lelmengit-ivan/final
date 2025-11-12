# Login Troubleshooting Guide

## Current Issue: Connection Error

The login is experiencing CORS (Cross-Origin Resource Sharing) issues. Here are solutions:

### Solution 1: Clear Browser Cache and Cookies

1. Open browser Developer Tools (F12)
2. Go to Application tab (Chrome) or Storage tab (Firefox)
3. Clear all cookies for localhost:5000
4. Clear cache
5. Refresh the page (Ctrl+F5)
6. Try logging in again

### Solution 2: Check Browser Console

1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for error messages
4. Common errors:
   - CORS policy error
   - Network error
   - 401 Unauthorized

### Solution 3: Use Incognito/Private Mode

1. Open browser in incognito/private mode
2. Go to http://localhost:5000
3. Try logging in

### Solution 4: Try Different Browser

- Chrome
- Firefox
- Edge

### Solution 5: Check Server is Running

```bash
# Check if server is running
curl http://localhost:5000

# Or in PowerShell
Invoke-WebRequest http://localhost:5000
```

### Solution 6: Manual Test

Open a new terminal and run:

```bash
# Test login endpoint directly
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Solution 7: Restart Everything

```bash
# Stop the server (Ctrl+C)
# Delete the database
del pharmacy.db

# Recreate everything
python seed_data.py
python create_admin.py
python app.py
```

### Solution 8: Check Firewall

- Make sure Windows Firewall isn't blocking port 5000
- Check antivirus software

### Solution 9: Use Different Port

Edit `app.py` last line:
```python
app.run(debug=True, port=8000)  # Change to 8000
```

Then access: http://localhost:8000

### Solution 10: Disable CORS Temporarily

In `app.py`, change CORS line to:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

## Expected Behavior

When login works correctly:
1. Enter username: `admin`
2. Enter password: `admin123`
3. Click Login
4. See "Login successful! Redirecting..."
5. Redirect to main dashboard

## Debug Information

### Check Session Cookie

In browser DevTools:
1. Application tab → Cookies
2. Look for `session` cookie
3. Should be set after successful login

### Check Network Tab

1. Open DevTools → Network tab
2. Try logging in
3. Look for `/api/login` request
4. Check:
   - Status: Should be 200
   - Response: Should have user data
   - Cookies: Should set session cookie

## Common Error Messages

### "Connection error. Please try again"
- Server not running
- CORS blocking request
- Network issue

### "Invalid username or password"
- Wrong credentials
- Database not seeded
- Password hash mismatch

### "Username or email already exists"
- Trying to register with existing username
- Use different username or login instead

## Quick Fix Commands

```bash
# Full reset
del pharmacy.db
python seed_data.py
python create_admin.py

# Restart server
# Press Ctrl+C to stop
python app.py
```

## Still Not Working?

Try the simple HTML form version (no AJAX):

Create `simple_login.html`:
```html
<!DOCTYPE html>
<html>
<body>
<h1>Simple Login</h1>
<form action="/api/login" method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>
</body>
</html>
```

Access: http://localhost:5000/simple_login.html

## Contact Information

If none of these work, the issue might be:
- Python version incompatibility
- Flask version issue
- System-specific problem

Check:
- Python version: `python --version` (should be 3.7+)
- Flask version: `pip show Flask`
- Operating System: Windows/Mac/Linux

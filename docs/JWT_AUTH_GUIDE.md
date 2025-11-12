# JWT Authentication Guide

## ✅ JWT Authentication is Now Implemented!

The pharmacy system now uses **JWT (JSON Web Tokens)** for authentication instead of sessions. This is more reliable, scalable, and works better with CORS.

---

## 🔐 How JWT Works

### 1. **Login Process**
- User enters username and password
- Server verifies credentials
- Server creates a JWT token containing user info
- Token is sent to client
- Client stores token in `localStorage`

### 2. **Authenticated Requests**
- Client sends token in `Authorization` header
- Server verifies token signature
- Server extracts user info from token
- Request is processed

### 3. **Logout Process**
- Client removes token from `localStorage`
- User is redirected to login page

---

## 🚀 Quick Start

### Start the Server
```bash
python app.py
```

### Login
1. Go to http://localhost:5000
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click Login
4. Token is automatically stored
5. Redirected to dashboard

---

## 🔧 Technical Details

### JWT Token Structure

```json
{
  "user_id": 1,
  "username": "admin",
  "email": "admin@pharmacy.com",
  "role": "admin",
  "exp": 1699876543,  // Expiration timestamp
  "iat": 1699790143   // Issued at timestamp
}
```

### Token Expiration
- Default: **24 hours**
- Configurable in `app.py`: `JWT_EXPIRATION_HOURS`

### Token Storage
- Stored in browser's `localStorage`
- Key: `token`
- Automatically included in API requests

### Authorization Header Format
```
Authorization: Bearer <your-jwt-token-here>
```

---

## 📝 API Changes

### Login Endpoint
**POST** `/api/login`

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "System Administrator",
    "email": "admin@pharmacy.com",
    "role": "admin"
  }
}
```

### Check Auth Endpoint
**GET** `/api/check-auth`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "authenticated": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@pharmacy.com",
    "role": "admin"
  }
}
```

### Logout Endpoint
**POST** `/api/logout`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

---

## 💻 Frontend Implementation

### Storing Token (login.js)
```javascript
// After successful login
localStorage.setItem('token', data.token);
localStorage.setItem('user', JSON.stringify(data.user));
```

### Sending Token (script.js)
```javascript
// Helper function
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Usage in API calls
fetch(`${API_URL}/medicines`, {
    headers: getAuthHeaders()
})
```

### Checking Authentication
```javascript
async function checkAuth() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        window.location.href = '/';
        return false;
    }
    
    const response = await fetch(`${API_URL}/check-auth`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (!response.ok) {
        localStorage.removeItem('token');
        window.location.href = '/';
        return false;
    }
    
    return true;
}
```

### Logout
```javascript
async function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}
```

---

## 🔒 Security Features

### ✅ Implemented
- Password hashing (SHA-256)
- Token expiration (24 hours)
- Token signature verification
- Secure token generation
- CORS configuration
- Authorization header validation

### 🔐 Production Recommendations
- Use HTTPS (required for production)
- Change SECRET_KEY to a strong random value
- Use bcrypt instead of SHA-256 for passwords
- Implement token refresh mechanism
- Add rate limiting
- Implement token blacklist for logout
- Use environment variables for secrets
- Add CSRF protection
- Implement 2FA

---

## 🎯 Advantages of JWT

### vs Sessions
✅ **No server-side storage** - Stateless
✅ **Works with CORS** - No cookie issues
✅ **Scalable** - Works across multiple servers
✅ **Mobile-friendly** - Easy to use in apps
✅ **Flexible** - Can include custom claims

### vs Cookies
✅ **No CORS issues** - Sent in headers
✅ **More control** - Client manages storage
✅ **Cross-domain** - Works across domains
✅ **API-friendly** - Standard for REST APIs

---

## 🐛 Troubleshooting

### Token Not Working
1. Check if token exists:
   ```javascript
   console.log(localStorage.getItem('token'));
   ```

2. Check token expiration:
   - Tokens expire after 24 hours
   - Login again to get new token

3. Check Authorization header:
   - Must be: `Bearer <token>`
   - Check for typos

### Login Not Storing Token
1. Check browser console for errors
2. Verify localStorage is enabled
3. Check if response contains token
4. Clear browser cache

### 401 Unauthorized Errors
- Token expired - login again
- Token invalid - clear localStorage and login
- Token missing - check Authorization header
- Wrong format - must be `Bearer <token>`

---

## 📊 Token Debugging

### View Token in Browser
1. Open DevTools (F12)
2. Go to Application tab
3. Click Local Storage
4. Look for `token` key

### Decode Token
Visit: https://jwt.io
Paste your token to see contents

### Test Token
```bash
# Get token from login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use token
curl http://localhost:5000/api/check-auth \
  -H "Authorization: Bearer <your-token>"
```

---

## 🔄 Migration from Sessions

### What Changed
- ❌ Removed Flask-Login
- ❌ Removed session management
- ❌ Removed cookies
- ✅ Added JWT tokens
- ✅ Added localStorage
- ✅ Added Authorization headers

### Files Modified
- `app.py` - Complete rewrite with JWT
- `script.js` - Added token handling
- `login.js` - Store token on login
- `requirements.txt` - Added PyJWT

### Backup
- Old session-based app: `app_old_session.py`

---

## 📚 Additional Resources

### JWT Libraries
- Python: PyJWT
- JavaScript: jsonwebtoken (Node.js)

### Learn More
- JWT.io - https://jwt.io
- RFC 7519 - JWT Specification
- OWASP JWT Cheat Sheet

---

## ✅ Testing Checklist

- [ ] Login with admin/admin123
- [ ] Token stored in localStorage
- [ ] Redirected to dashboard
- [ ] User info displayed in header
- [ ] Can access all tabs
- [ ] Can add medicine
- [ ] Can record sale
- [ ] Can add supplier
- [ ] Logout clears token
- [ ] Redirected to login after logout
- [ ] Cannot access dashboard without token
- [ ] Token expires after 24 hours

---

**JWT authentication is now fully functional! 🎉**

**Server running at: http://localhost:5000**

**Login with: admin / admin123**

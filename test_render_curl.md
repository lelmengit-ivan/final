# Test Render API with cURL

Replace `YOUR_RENDER_URL` with your actual Render URL (e.g., `https://pharmacy-system-abc123.onrender.com`)

## 1. Test Server Health
```bash
curl https://YOUR_RENDER_URL
```

## 2. Test Login Endpoint
```bash
curl -X POST https://YOUR_RENDER_URL/api/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@pharmacy.com\",\"password\":\"admin123\"}"
```

**Expected Success Response:**
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@pharmacy.com",
    "role": "admin",
    "organization_id": 1,
    "organization_name": "Default Pharmacy"
  }
}
```

**Expected Error Responses:**

**Database not initialized (500):**
```json
{
  "error": "Internal server error"
}
```
→ Solution: Run `python init_render_db.py` on Render

**Wrong credentials (401):**
```json
{
  "error": "Invalid credentials"
}
```
→ Solution: Check username/password

**Organization inactive (403):**
```json
{
  "error": "Organization subscription is not active"
}
```
→ Solution: Check organization status in database

## 3. Test Authenticated Endpoint
First, get the token from login response, then:

```bash
curl https://YOUR_RENDER_URL/api/medicines \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 4. Test Organization Registration
```bash
curl -X POST https://YOUR_RENDER_URL/api/organizations/register \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Test Pharmacy\",
    \"contact_email\": \"test@pharmacy.com\",
    \"contact_phone\": \"1234567890\",
    \"subscription_plan\": \"basic\"
  }"
```

## PowerShell Version (Windows)

### Test Login:
```powershell
$body = @{
    email = "admin@pharmacy.com"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/api/login" -Method Post -Body $body -ContentType "application/json"
```

### Test with Token:
```powershell
$token = "YOUR_TOKEN_HERE"
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/api/medicines" -Headers $headers
```

## Python Test Script

Run the interactive test:
```bash
python test_render_api.py
```

This will:
1. Test server health
2. Test login
3. Test authenticated endpoints
4. Show detailed error messages

## Common Issues

### Connection Refused
- Service is not running
- Check Render dashboard → Service status

### 404 Not Found
- Wrong URL
- API endpoint doesn't exist
- Check app.py routes

### 500 Internal Server Error
- Database not initialized
- Check Render logs
- Run init_render_db.py

### CORS Error (in browser)
- CORS is configured in app.py
- Should allow all origins
- Check browser console for details

## Check Render Logs

In Render Dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for errors when making requests
4. Check for database connection errors

## Manual Database Initialization

If database is not initialized:

1. Go to Render Dashboard
2. Click your service
3. Click "Shell" tab
4. Run:
```bash
python init_render_db.py
```

5. Check output for success message
6. Try login again

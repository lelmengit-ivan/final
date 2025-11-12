# Quick Start: Multi-Tenancy

## ✅ Migration Complete!

Your system now supports multiple organizations. All existing data has been preserved under "Default Pharmacy" (Organization ID: 1).

## 🚀 Quick Actions

### 1. Start the Server
```bash
python app.py
```

### 2. Register a New Pharmacy
- Visit: http://localhost:5000/register-org
- Fill in pharmacy details
- Create admin account
- Select subscription plan
- Click "Register Organization"

### 3. Login Options

**Option A: Email Login (Recommended)**
- Visit: http://localhost:5000/login
- Enter: email + password
- System automatically finds your organization

**Option B: Username Login**
- Enter: username + password
- Works if username is unique across organizations

### 4. Add Team Members

**As Admin:**
1. Share your Organization ID (shown in dashboard header)
2. Team member visits: http://localhost:5000/login
3. Click "Register here"
4. Enter Organization ID
5. Complete registration

## 📊 Test Multi-Tenancy

### Create Test Organizations
```bash
# Organization A
curl -X POST http://localhost:5000/api/organizations/register \
  -H "Content-Type: application/json" \
  -d '{"organization_name":"Pharmacy A","contact_email":"a@test.com","username":"adminA","email":"a@test.com","password":"test123","full_name":"Admin A"}'

# Organization B  
curl -X POST http://localhost:5000/api/organizations/register \
  -H "Content-Type: application/json" \
  -d '{"organization_name":"Pharmacy B","contact_email":"b@test.com","username":"adminB","email":"b@test.com","password":"test123","full_name":"Admin B"}'
```

### Verify Isolation
1. Login as Admin A → Add medicines
2. Login as Admin B → Add different medicines
3. Confirm each admin only sees their own data ✓

## 🔑 Key Features

- ✅ Complete data isolation per organization
- ✅ Separate user management per pharmacy
- ✅ Subscription plans (Free, Basic, Pro, Enterprise)
- ✅ Organization ID shown in dashboard
- ✅ Admin badge for administrators
- ✅ Existing data preserved in Organization ID: 1

## 📝 Subscription Plans

| Plan | Users | Price/Month |
|------|-------|-------------|
| Free Trial | 5 | Free (30 days) |
| Basic | 10 | KSH 2,000 |
| Professional | 25 | KSH 5,000 |
| Enterprise | Unlimited | KSH 10,000 |

## 🔧 API Changes

All endpoints now require JWT token with organization info:
```javascript
fetch('/api/medicines', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
```

JWT token includes:
- user_id
- username
- email
- role
- **organization_id** ← NEW
- **organization_name** ← NEW

## 📖 Full Documentation

See `MULTI_TENANCY_GUIDE.md` for complete details.

# 🔐 Login Credentials

## Server Running
✅ Server: http://localhost:5000

## Default Admin Account

### Login Options (Both Work!)

**Option 1: Email Login**
- Email: `admin@pharmacy.com`
- Password: `admin123`

**Option 2: Username Login**
- Username: `admin`
- Password: `admin123`

## Organization Details
- Organization: Default Pharmacy
- Organization ID: 1
- Subscription: Enterprise (Unlimited users)
- Status: Active

## Quick Links
- 🏠 Dashboard: http://localhost:5000
- 🔑 Login: http://localhost:5000/login
- 🏢 Register Organization: http://localhost:5000/register-org

## Testing Multi-Tenancy

### Create a Test Organization
1. Visit: http://localhost:5000/register-org
2. Fill in details:
   - Organization Name: Test Pharmacy
   - Email: test@pharmacy.com
   - Username: testadmin
   - Password: test123
3. Login with new credentials
4. Verify data isolation (can't see Default Pharmacy's data)

## Troubleshooting

### Can't Login?
Run this command to reset admin password:
```bash
python fix_admin_login.py
```

### Dashboard Not Loading?
All API calls now include authentication headers. If you see issues:
1. Clear browser cache and localStorage
2. Logout and login again
3. Check browser console for errors

### Need to Check Users?
```bash
python -c "import sqlite3; conn = sqlite3.connect('pharmacy.db'); cursor = conn.cursor(); cursor.execute('SELECT id, organization_id, username, email, role FROM users'); [print(row) for row in cursor.fetchall()]"
```

### Server Not Running?
```bash
python app.py
```

## Features Available
- ✅ Multi-tenancy with data isolation
- ✅ JWT authentication
- ✅ Organization management
- ✅ User management
- ✅ Inventory tracking
- ✅ Sales recording
- ✅ AI predictions
- ✅ Analytics dashboard
- ✅ Reports with export

## Next Steps
1. Login with admin credentials
2. Explore the dashboard
3. Add medicines, record sales
4. Create new organizations
5. Add team members

---
**Last Updated:** After multi-tenancy implementation
**Status:** ✅ All systems operational

# Login System Guide

## ✅ Login System is Now Fully Functional!

The pharmacy management system now includes a complete authentication system with user registration, login, and session management.

---

## 🚀 Quick Start

### Step 1: Setup Database
```bash
pip install -r requirements.txt
python seed_data.py
```

### Step 2: Create Admin User
```bash
python create_admin.py
```

This creates a default admin account:
- **Username**: `admin`
- **Password**: `admin123`

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the System
Open your browser to: **http://localhost:5000**

You'll be automatically redirected to the login page.

---

## 👤 User Management

### Default Admin Account
After running `create_admin.py`:
- Username: **admin**
- Password: **admin123**
- Role: **admin**

⚠️ **IMPORTANT**: Change the admin password after first login!

### Creating New Users
1. Click "Register here" on the login page
2. Fill in the registration form:
   - Full Name
   - Username (unique)
   - Email (unique)
   - Password (min 6 characters)
   - Confirm Password
3. Click "Register"
4. Login with your new credentials

---

## 🔐 Authentication Features

### Login Page
- Clean, modern design
- Username/password authentication
- Session-based security
- Password hashing (SHA-256)
- Error handling with user-friendly messages

### Registration Page
- Full name, username, email fields
- Password strength validation (min 6 chars)
- Password confirmation
- Duplicate username/email detection
- Automatic redirect to login after success

### Session Management
- Secure session cookies
- Auto-redirect to login if not authenticated
- User info displayed in header
- Logout functionality
- Session persistence across page refreshes

### Protected Routes
All API endpoints are accessible after login:
- Medicines CRUD
- Sales recording
- Supplier management
- AI predictions
- Analytics

---

## 🎨 Login Page Features

### Visual Design
- Gradient purple background
- Animated slide-in effect
- Responsive layout (mobile-friendly)
- Clean white card design
- Smooth transitions

### User Experience
- Toggle between login/register forms
- Real-time validation
- Success/error messages
- Auto-hide messages after 5 seconds
- Remember session

---

## 🔧 Technical Details

### Password Security
- SHA-256 hashing
- No plain text storage
- Secure session cookies
- HTTPS recommended for production

### Database Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user',
    created_date TEXT,
    last_login TEXT
)
```

### Session Data Stored
- user_id
- username
- full_name
- role

### API Endpoints

**Authentication:**
- `POST /api/register` - Create new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/check-auth` - Check if authenticated

**Response Examples:**

Login Success:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "System Administrator",
    "email": "admin@pharmacy.com",
    "role": "admin"
  }
}
```

Login Error:
```json
{
  "error": "Invalid username or password"
}
```

---

## 🎯 User Workflow

### First Time Setup
1. Run `python create_admin.py`
2. Start server: `python app.py`
3. Open http://localhost:5000
4. Login with admin/admin123
5. Start using the system!

### Regular User Flow
1. Open http://localhost:5000
2. Click "Register here"
3. Fill registration form
4. Login with new credentials
5. Access all features

### Logout Flow
1. Click "Logout" button in header
2. Redirected to login page
3. Session cleared
4. Must login again to access

---

## 🛡️ Security Features

### Implemented
✅ Password hashing (SHA-256)
✅ Session management
✅ Duplicate prevention
✅ Input validation
✅ CORS configuration
✅ Secure cookies

### Recommended for Production
⚠️ Use HTTPS
⚠️ Implement rate limiting
⚠️ Add CSRF protection
⚠️ Use stronger hashing (bcrypt)
⚠️ Add password reset
⚠️ Implement 2FA
⚠️ Add account lockout
⚠️ Log authentication attempts

---

## 📱 Responsive Design

The login page works perfectly on:
- Desktop computers (1920x1080+)
- Laptops (1366x768+)
- Tablets (768x1024)
- Mobile phones (375x667+)

---

## 🐛 Troubleshooting

### "Username or email already exists"
- Choose a different username
- Use a different email address
- Check if you already registered

### "Invalid username or password"
- Check your username spelling
- Verify password is correct
- Ensure caps lock is off

### "Connection error"
- Make sure server is running
- Check if port 5000 is available
- Verify Flask is installed

### Session Not Persisting
- Clear browser cookies
- Check browser privacy settings
- Restart the Flask server

### Can't Access Dashboard
- Make sure you're logged in
- Check session hasn't expired
- Try logging out and back in

---

## 🔄 Password Reset (Manual)

If you forget the admin password:

1. Stop the server
2. Delete `pharmacy.db`
3. Run `python seed_data.py`
4. Run `python create_admin.py`
5. Start server again

---

## 📊 User Roles

### Current Roles
- **admin**: Full system access
- **user**: Standard access

### Future Role Features
- Pharmacist: Manage prescriptions
- Manager: View reports only
- Cashier: Sales only
- Inventory Manager: Stock management only

---

## 🎉 What's Working

✅ User registration
✅ User login
✅ Session management
✅ Password hashing
✅ Auto-redirect to login
✅ Logout functionality
✅ User info in header
✅ Protected routes
✅ Error handling
✅ Success messages
✅ Responsive design
✅ Form validation

---

## 📝 Test Accounts

After running `create_admin.py`:

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | admin | admin@pharmacy.com |

Create your own test users through the registration page!

---

## 🚀 Next Steps

1. Login with admin account
2. Add some medicines
3. Record sales
4. Add suppliers
5. Check AI predictions
6. View analytics
7. Create additional user accounts

---

**Your pharmacy system is now secure and ready to use! 🎉**

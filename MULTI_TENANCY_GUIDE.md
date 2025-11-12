# Multi-Tenancy Implementation Guide

## Overview
Your Pharmacy Management System now supports **multi-tenancy**, allowing multiple independent pharmacies/organizations to use the same system while keeping their data completely isolated.

## Key Features

### 1. **Organization Management**
- Each pharmacy is a separate organization with its own data
- Organizations have their own subscription plans and user limits
- Complete data isolation between organizations

### 2. **User Management**
- Users belong to a specific organization
- Username and email are unique within an organization (not globally)
- Each organization has admin users who can manage their team

### 3. **Data Isolation**
- All data (medicines, sales, suppliers, prescriptions) is scoped to the organization
- Users can only see and manage data from their own organization
- No cross-organization data access

## How It Works

### For New Organizations (Pharmacies)

#### Step 1: Register Organization
1. Visit `/register-org` page
2. Fill in organization details:
   - Pharmacy/Organization Name
   - Subdomain (optional, for custom URLs)
   - Contact Email & Phone
   - Address
3. Create admin account:
   - Full Name
   - Username
   - Email
   - Password
4. Select subscription plan:
   - **Free Trial**: 5 users, 30 days
   - **Basic**: 10 users, KSH 2,000/month
   - **Professional**: 25 users, KSH 5,000/month
   - **Enterprise**: Unlimited users, KSH 10,000/month

#### Step 2: Access Your Dashboard
- After registration, login with your credentials
- You'll be automatically assigned as the admin
- Start adding medicines, recording sales, etc.

### For Existing Organizations

#### Adding New Users
1. Admin shares the **Organization ID** with new team members
2. New users visit `/login` and click "Register here"
3. Enter the Organization ID provided by admin
4. Complete registration form
5. Login and access the organization's data

#### Finding Your Organization ID
- Admins can find it in the dashboard (will be displayed)
- Or check the database: `SELECT id, name FROM organizations`

## Database Schema

### Organizations Table
```sql
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    subdomain TEXT UNIQUE,
    contact_email TEXT NOT NULL,
    contact_phone TEXT,
    address TEXT,
    subscription_plan TEXT DEFAULT 'free',
    subscription_status TEXT DEFAULT 'active',
    created_date TEXT,
    expiry_date TEXT,
    max_users INTEGER DEFAULT 5,
    settings TEXT
)
```

### Users Table (Updated)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    organization_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    email TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_date TEXT,
    last_login TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations (id),
    UNIQUE(organization_id, username),
    UNIQUE(organization_id, email)
)
```

## API Endpoints

### Organization Endpoints

#### Register New Organization
```http
POST /api/organizations/register
Content-Type: application/json

{
  "organization_name": "ABC Pharmacy",
  "subdomain": "abc",
  "contact_email": "admin@abc.com",
  "contact_phone": "0712345678",
  "address": "123 Main St",
  "full_name": "John Doe",
  "username": "admin",
  "email": "john@abc.com",
  "password": "secure123",
  "subscription_plan": "professional",
  "max_users": 25
}
```

#### Get Organization Details
```http
GET /api/organizations/{org_id}
Authorization: Bearer {token}
```

#### Update Organization
```http
PUT /api/organizations/{org_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "ABC Pharmacy Ltd",
  "contact_email": "info@abc.com",
  "contact_phone": "0712345678",
  "address": "456 New St"
}
```

#### Update Subscription
```http
PUT /api/organizations/{org_id}/subscription
Authorization: Bearer {token}
Content-Type: application/json

{
  "subscription_plan": "enterprise",
  "subscription_status": "active",
  "expiry_date": "2026-12-31",
  "max_users": 999
}
```

### Authentication Endpoints

#### Login (Email-based)
```http
POST /api/login
Content-Type: application/json

{
  "email": "user@pharmacy.com",
  "password": "password123"
}
```

#### Register User (Join Organization)
```http
POST /api/register
Content-Type: application/json

{
  "organization_id": 1,
  "full_name": "Jane Smith",
  "username": "jsmith",
  "email": "jane@pharmacy.com",
  "password": "secure123"
}
```

## Migration from Single-Tenant

If you have an existing database, run the migration script:

```bash
python migrate_to_multitenancy.py
```

This will:
1. Create the organizations table
2. Create a default organization (ID: 1)
3. Assign all existing users to the default organization
4. Update all tables to support multi-tenancy
5. Preserve all existing data

## Security Features

### Data Isolation
- All API endpoints check `organization_id` from JWT token
- Database queries filter by `organization_id`
- Users cannot access other organizations' data

### Authentication
- JWT tokens include organization information
- Tokens expire after 24 hours (configurable)
- Password hashing using SHA-256

### Authorization
- Role-based access control (admin, user)
- Admins can manage users within their organization
- Subscription status checked on login

## Subscription Plans

| Plan | Users | Price | Features |
|------|-------|-------|----------|
| Free Trial | 5 | Free (30 days) | Basic features |
| Basic | 10 | KSH 2,000/month | Full inventory, reports |
| Professional | 25 | KSH 5,000/month | AI predictions, analytics |
| Enterprise | Unlimited | KSH 10,000/month | All features, priority support |

## Testing Multi-Tenancy

### Test Scenario 1: Create Two Organizations
```bash
# Register Organization A
curl -X POST http://localhost:5000/api/organizations/register \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Pharmacy A",
    "contact_email": "admin@pharmacya.com",
    "username": "adminA",
    "email": "admin@pharmacya.com",
    "password": "test123",
    "full_name": "Admin A"
  }'

# Register Organization B
curl -X POST http://localhost:5000/api/organizations/register \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Pharmacy B",
    "contact_email": "admin@pharmacyb.com",
    "username": "adminB",
    "email": "admin@pharmacyb.com",
    "password": "test123",
    "full_name": "Admin B"
  }'
```

### Test Scenario 2: Verify Data Isolation
1. Login as Admin A, add medicines
2. Login as Admin B, add different medicines
3. Verify Admin A cannot see Admin B's medicines
4. Verify Admin B cannot see Admin A's medicines

## Troubleshooting

### Issue: "Organization ID is required"
- Make sure you're providing `organization_id` when registering users
- For new organizations, use `/register-org` instead

### Issue: "Maximum user limit reached"
- Check your subscription plan's user limit
- Upgrade to a higher plan or remove inactive users

### Issue: "Organization subscription is not active"
- Check the `subscription_status` in organizations table
- Update expiry_date if subscription expired

### Issue: Existing users can't login
- Run the migration script: `python migrate_to_multitenancy.py`
- All existing users will be assigned to Organization ID: 1

## Future Enhancements

Potential features to add:
1. **Subdomain routing**: Access via `pharmacy-name.yourdomain.com`
2. **Billing integration**: M-Pesa, Stripe for automatic payments
3. **Organization settings**: Custom branding, currency, timezone
4. **Data export**: Allow organizations to export their data
5. **Usage analytics**: Track API usage per organization
6. **White-label**: Custom domains for enterprise clients

## Support

For questions or issues:
- Check the documentation
- Review API responses for error messages
- Ensure JWT tokens are valid and not expired
- Verify organization subscription status

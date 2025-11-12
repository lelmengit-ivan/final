"""
Quick fix to test admin login
"""
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Check current admin
cursor.execute('SELECT id, username, email, organization_id FROM users WHERE username = ?', ('admin',))
admin = cursor.fetchone()

if admin:
    print(f"Admin user found:")
    print(f"  ID: {admin[0]}")
    print(f"  Username: {admin[1]}")
    print(f"  Email: {admin[2]}")
    print(f"  Organization ID: {admin[3]}")
    print()
    
    # Update password to ensure it's correct
    new_password = hash_password('admin123')
    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, admin[0]))
    conn.commit()
    print("✅ Password reset to 'admin123'")
    print()
    print("Login options:")
    print(f"  1. Email: {admin[2]} / Password: admin123")
    print(f"  2. Username: {admin[1]} / Password: admin123")
else:
    print("❌ Admin user not found!")
    print("Creating admin user...")
    
    cursor.execute('SELECT id FROM organizations WHERE id = 1')
    if not cursor.fetchone():
        print("Creating default organization...")
        cursor.execute('''
            INSERT INTO organizations (id, name, subdomain, contact_email, subscription_plan, 
                                      subscription_status, created_date, expiry_date, max_users, settings)
            VALUES (1, 'Default Pharmacy', 'default', 'admin@pharmacy.com', 'enterprise', 'active',
                    date('now'), date('now', '+365 days'), 999, '{}')
        ''')
    
    hashed_password = hash_password('admin123')
    cursor.execute('''
        INSERT INTO users (organization_id, username, password, full_name, email, role, created_date)
        VALUES (1, 'admin', ?, 'Administrator', 'admin@pharmacy.com', 'admin', date('now'))
    ''', (hashed_password,))
    conn.commit()
    print("✅ Admin user created!")
    print()
    print("Login with:")
    print("  Email: admin@pharmacy.com")
    print("  Password: admin123")

conn.close()

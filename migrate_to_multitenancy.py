"""
Migration script to add multi-tenancy support to existing pharmacy database
This script will:
1. Create organizations table
2. Add organization_id to users table
3. Create a default organization for existing data
4. Update all existing records
"""

import sqlite3
from datetime import datetime, timedelta

def migrate_database():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    print("Starting multi-tenancy migration...")
    
    # Step 1: Create organizations table
    print("Creating organizations table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    ''')
    
    # Step 2: Check if default organization exists
    cursor.execute('SELECT id FROM organizations WHERE id = 1')
    if not cursor.fetchone():
        print("Creating default organization...")
        cursor.execute('''
            INSERT INTO organizations (name, subdomain, contact_email, subscription_plan, 
                                      subscription_status, created_date, expiry_date, max_users, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('Default Pharmacy', 'default', 'admin@pharmacy.com', 'enterprise', 'active',
              datetime.now().strftime('%Y-%m-%d'),
              (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
              999, '{}'))
        print("Default organization created with ID: 1")
    
    # Step 3: Check if users table needs migration
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'organization_id' not in columns:
        print("Migrating users table...")
        
        # Create new users table with organization_id
        cursor.execute('''
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL DEFAULT 1,
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
        ''')
        
        # Copy data from old table
        cursor.execute('''
            INSERT INTO users_new (id, organization_id, username, password, full_name, email, role, created_date, last_login)
            SELECT id, 1, username, password, full_name, email, role, created_date, last_login
            FROM users
        ''')
        
        # Drop old table and rename new one
        cursor.execute('DROP TABLE users')
        cursor.execute('ALTER TABLE users_new RENAME TO users')
        print("Users table migrated successfully")
    else:
        print("Users table already has organization_id column")
    
    # Step 4: Update medicines table to ensure user_id exists
    cursor.execute("PRAGMA table_info(medicines)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id to medicines table...")
        cursor.execute('ALTER TABLE medicines ADD COLUMN user_id INTEGER DEFAULT 1')
        cursor.execute('UPDATE medicines SET user_id = 1 WHERE user_id IS NULL')
    
    # Step 5: Update sales table
    cursor.execute("PRAGMA table_info(sales)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id to sales table...")
        cursor.execute('ALTER TABLE sales ADD COLUMN user_id INTEGER DEFAULT 1')
        cursor.execute('UPDATE sales SET user_id = 1 WHERE user_id IS NULL')
    
    # Step 6: Update suppliers table
    cursor.execute("PRAGMA table_info(suppliers)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id to suppliers table...")
        cursor.execute('ALTER TABLE suppliers ADD COLUMN user_id INTEGER DEFAULT 1')
        cursor.execute('UPDATE suppliers SET user_id = 1 WHERE user_id IS NULL')
    
    # Step 7: Update prescriptions table
    cursor.execute("PRAGMA table_info(prescriptions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id to prescriptions table...")
        cursor.execute('ALTER TABLE prescriptions ADD COLUMN user_id INTEGER DEFAULT 1')
        cursor.execute('UPDATE prescriptions SET user_id = 1 WHERE user_id IS NULL')
    
    conn.commit()
    conn.close()
    
    print("\n✅ Migration completed successfully!")
    print("=" * 60)
    print("Default Organization Details:")
    print("  - Organization ID: 1")
    print("  - Name: Default Pharmacy")
    print("  - Subdomain: default")
    print("  - All existing users have been assigned to this organization")
    print("  - All existing data is now associated with Organization ID: 1")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Register new organizations at: /register-org")
    print("2. Users can join existing organizations with Organization ID")
    print("3. Each organization's data is completely isolated")

if __name__ == '__main__':
    try:
        migrate_database()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

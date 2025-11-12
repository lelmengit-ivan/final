"""
Universal migration script for both SQLite and PostgreSQL
Migrates users to multi-tenancy structure
"""

import os
import sys
from datetime import datetime, timedelta

def migrate_sqlite():
    """Migrate SQLite database (local)"""
    import sqlite3
    
    print("\n" + "=" * 60)
    print("MIGRATING SQLite DATABASE (Local)")
    print("=" * 60)
    
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    try:
        # Create organizations table
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
        
        # Check if default organization exists
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
        
        # Check if users table needs migration
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'organization_id' not in columns:
            print("Adding organization_id to users table...")
            
            # Create new users table
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
            
            # Copy existing users
            cursor.execute('''
                INSERT INTO users_new (id, organization_id, username, password, full_name, email, role, created_date, last_login)
                SELECT id, 1, username, password, full_name, email, role, created_date, last_login
                FROM users
            ''')
            
            # Replace old table
            cursor.execute('DROP TABLE users')
            cursor.execute('ALTER TABLE users_new RENAME TO users')
            print("✓ Users migrated to organization ID: 1")
        else:
            print("✓ Users table already has organization_id")
        
        # Ensure all tables have user_id for multi-tenancy
        for table in ['medicines', 'sales', 'suppliers', 'prescriptions']:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'user_id' not in columns:
                print(f"Adding user_id to {table} table...")
                cursor.execute(f'ALTER TABLE {table} ADD COLUMN user_id INTEGER DEFAULT 1')
                cursor.execute(f'UPDATE {table} SET user_id = 1 WHERE user_id IS NULL')
        
        conn.commit()
        print("\n✅ SQLite migration completed successfully!")
        
        # Show summary
        cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = 1')
        user_count = cursor.fetchone()[0]
        print(f"   - {user_count} users assigned to Default Pharmacy (Org ID: 1)")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ SQLite migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def migrate_postgresql():
    """Migrate PostgreSQL database (production)"""
    try:
        import psycopg2
    except ImportError:
        print("\n⚠️  psycopg2 not installed. Skipping PostgreSQL migration.")
        print("   Install with: pip install psycopg2-binary")
        return
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("\n⚠️  DATABASE_URL not set. Skipping PostgreSQL migration.")
        return
    
    # Fix Heroku postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("\n" + "=" * 60)
    print("MIGRATING PostgreSQL DATABASE (Production)")
    print("=" * 60)
    
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    try:
        # Create organizations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizations (
                id SERIAL PRIMARY KEY,
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
        
        # Check if default organization exists
        cursor.execute('SELECT id FROM organizations WHERE id = 1')
        if not cursor.fetchone():
            print("Creating default organization...")
            cursor.execute('''
                INSERT INTO organizations (id, name, subdomain, contact_email, subscription_plan, 
                                          subscription_status, created_date, expiry_date, max_users, settings)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (1, 'Default Pharmacy', 'default', 'admin@pharmacy.com', 'enterprise', 'active',
                  datetime.now().strftime('%Y-%m-%d'),
                  (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                  999, '{}'))
            
            # Reset sequence
            cursor.execute("SELECT setval('organizations_id_seq', (SELECT MAX(id) FROM organizations))")
        
        # Check if users table needs migration
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'organization_id'
        """)
        
        if not cursor.fetchone():
            print("Adding organization_id to users table...")
            
            # Add column
            cursor.execute('ALTER TABLE users ADD COLUMN organization_id INTEGER DEFAULT 1')
            cursor.execute('ALTER TABLE users ADD FOREIGN KEY (organization_id) REFERENCES organizations (id)')
            
            # Update constraints
            cursor.execute('ALTER TABLE users DROP CONSTRAINT IF EXISTS users_username_key')
            cursor.execute('ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_key')
            cursor.execute('ALTER TABLE users ADD UNIQUE (organization_id, username)')
            cursor.execute('ALTER TABLE users ADD UNIQUE (organization_id, email)')
            
            print("✓ Users migrated to organization ID: 1")
        else:
            print("✓ Users table already has organization_id")
        
        # Ensure all tables have user_id
        for table in ['medicines', 'sales', 'suppliers', 'prescriptions']:
            cursor.execute(f"""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = '{table}' AND column_name = 'user_id'
            """)
            
            if not cursor.fetchone():
                print(f"Adding user_id to {table} table...")
                cursor.execute(f'ALTER TABLE {table} ADD COLUMN user_id INTEGER DEFAULT 1')
                cursor.execute(f'UPDATE {table} SET user_id = 1 WHERE user_id IS NULL')
        
        conn.commit()
        print("\n✅ PostgreSQL migration completed successfully!")
        
        # Show summary
        cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = 1')
        user_count = cursor.fetchone()[0]
        print(f"   - {user_count} users assigned to Default Pharmacy (Org ID: 1)")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ PostgreSQL migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def main():
    print("\n" + "=" * 60)
    print("MULTI-TENANCY MIGRATION TOOL")
    print("=" * 60)
    print("This will migrate users to the multi-tenancy structure")
    print("for both SQLite (local) and PostgreSQL (production)")
    print("=" * 60)
    
    # Migrate SQLite
    migrate_sqlite()
    
    # Migrate PostgreSQL
    migrate_postgresql()
    
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    print("✓ All users assigned to 'Default Pharmacy' (Org ID: 1)")
    print("✓ All data isolated by organization")
    print("\nNext steps:")
    print("1. Register new organizations at: /register-org")
    print("2. Users can join organizations with Organization ID")
    print("3. Test login with existing credentials")
    print("=" * 60)

if __name__ == '__main__':
    main()
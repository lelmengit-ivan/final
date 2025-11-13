"""
Initialize and migrate Render PostgreSQL database
Run this after deploying to Render
"""

import os
import sys
from datetime import datetime, timedelta
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_render_database():
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not set. This script is for Render deployment.")
        print("   Set DATABASE_URL environment variable or run on Render.")
        return False
    
    try:
        import psycopg2
    except ImportError:
        print("❌ psycopg2 not installed")
        print("   Install with: pip install psycopg2-binary")
        return False
    
    # Fix Heroku-style URL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("\n" + "=" * 60)
    print("INITIALIZING RENDER POSTGRESQL DATABASE")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Create organizations table
        print("Creating organizations table...")
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
        
        # Create default organization
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
            cursor.execute("SELECT setval('organizations_id_seq', (SELECT MAX(id) FROM organizations))")
        
        # Create users table
        print("Creating users table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
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
        ''')
        
        # Create default admin user
        cursor.execute('SELECT id FROM users WHERE email = %s', ('admin@pharmacy.com',))
        if not cursor.fetchone():
            print("Creating default admin user...")
            cursor.execute('''
                INSERT INTO users (organization_id, username, password, full_name, email, role, created_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (1, 'admin', hash_password('admin123'), 'System Administrator', 
                  'admin@pharmacy.com', 'admin', datetime.now().strftime('%Y-%m-%d')))
        
        # Create medicines table
        print("Creating medicines table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL,
                expiry_date TEXT,
                reorder_level INTEGER DEFAULT 10,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create sales table
        print("Creating sales table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                medicine_id INTEGER,
                quantity INTEGER,
                total_price REAL,
                sale_date TEXT,
                payment_method TEXT DEFAULT 'cash',
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Create suppliers table
        print("Creating suppliers table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                rating REAL DEFAULT 0,
                created_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create medicine_suppliers table
        print("Creating medicine_suppliers table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_suppliers (
                id SERIAL PRIMARY KEY,
                medicine_id INTEGER,
                supplier_id INTEGER,
                supply_price REAL,
                last_supply_date TEXT,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
            )
        ''')
        
        # Create prescriptions table
        print("Creating prescriptions table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                patient_name TEXT NOT NULL,
                patient_phone TEXT,
                doctor_name TEXT NOT NULL,
                prescription_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create prescription_items table
        print("Creating prescription_items table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescription_items (
                id SERIAL PRIMARY KEY,
                prescription_id INTEGER,
                medicine_id INTEGER,
                quantity INTEGER,
                dosage TEXT,
                duration TEXT,
                FOREIGN KEY (prescription_id) REFERENCES prescriptions (id),
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        conn.commit()
        
        # Show summary
        cursor.execute('SELECT COUNT(*) FROM organizations')
        org_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        print("\n✅ Database initialized successfully!")
        print("=" * 60)
        print(f"Organizations: {org_count}")
        print(f"Users: {user_count}")
        print("\nDefault Login Credentials:")
        print("  Email: admin@pharmacy.com")
        print("  Password: admin123")
        print("=" * 60)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_render_database()
    sys.exit(0 if success else 1)

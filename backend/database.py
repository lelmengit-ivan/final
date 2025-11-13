import sqlite3
import json
from datetime import datetime
import os

class PharmacyDB:
    def __init__(self, db_name='pharmacy.db'):
        self.db_name = db_name
        
        # Check if we're on Heroku (DATABASE_URL will be set)
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # We're on Heroku - use PostgreSQL
            try:
                import psycopg2
                # Heroku uses postgres:// but psycopg2 needs postgresql://
                if database_url.startswith('postgres://'):
                    database_url = database_url.replace('postgres://', 'postgresql://', 1)
                self.db_url = database_url
                self.use_postgres = True
                print("Using PostgreSQL database")
            except ImportError:
                print("Warning: psycopg2 not installed, falling back to SQLite")
                self.use_postgres = False
        else:
            # Local development - use SQLite
            self.use_postgres = False
            print("Using SQLite database")
        
        self.init_db()
    
    def get_connection(self):
        if self.use_postgres:
            import psycopg2
            return psycopg2.connect(self.db_url)
        else:
            return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Use SERIAL for PostgreSQL, INTEGER for SQLite
        id_type = "SERIAL PRIMARY KEY" if self.use_postgres else "INTEGER PRIMARY KEY AUTOINCREMENT"
        
        # Organizations table (multi-tenancy)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS organizations (
                id {id_type},
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
        
        # Medicines table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS medicines (
                id {id_type},
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
        
        # Sales table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS sales (
                id {id_type},
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
        
        # Suppliers table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS suppliers (
                id {id_type},
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
        
        # Medicine-Supplier relationship table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS medicine_suppliers (
                id {id_type},
                medicine_id INTEGER,
                supplier_id INTEGER,
                supply_price REAL,
                last_supply_date TEXT,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
            )
        ''')
        
        # Prescriptions table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id {id_type},
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
        
        # Prescription items table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS prescription_items (
                id {id_type},
                prescription_id INTEGER,
                medicine_id INTEGER,
                quantity INTEGER,
                dosage TEXT,
                duration TEXT,
                FOREIGN KEY (prescription_id) REFERENCES prescriptions (id),
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Users table for authentication (with organization)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS users (
                id {id_type},
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
        
        conn.commit()
        conn.close()

import sqlite3
import json
from datetime import datetime

class PharmacyDB:
    def __init__(self, db_name='pharmacy.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Organizations table (multi-tenancy)
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
        
        # Medicines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id INTEGER,
                supplier_id INTEGER,
                supply_price REAL,
                last_supply_date TEXT,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
            )
        ''')
        
        # Prescriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescription_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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

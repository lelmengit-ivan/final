import sqlite3
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin_user():
    """Create a default admin user"""
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone():
        print("Admin user already exists!")
        conn.close()
        return
    
    # Create admin user
    admin_data = {
        'username': 'admin',
        'password': hash_password('admin123'),  # Change this password!
        'full_name': 'System Administrator',
        'email': 'admin@pharmacy.com',
        'role': 'admin',
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    cursor.execute('''
        INSERT INTO users (username, password, full_name, email, role, created_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (admin_data['username'], admin_data['password'], admin_data['full_name'],
          admin_data['email'], admin_data['role'], admin_data['created_date']))
    
    conn.commit()
    conn.close()
    
    print("✅ Admin user created successfully!")
    print("\nLogin credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\n⚠️  IMPORTANT: Change the admin password after first login!")

if __name__ == '__main__':
    create_admin_user()

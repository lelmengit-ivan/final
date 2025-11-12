import sqlite3
from datetime import datetime

def seed_suppliers():
    """Add sample supplier data to the database"""
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    # Sample suppliers data
    suppliers = [
        {
            'name': 'MediSupply Corp',
            'contact_person': 'John Anderson',
            'phone': '+1-555-0101',
            'email': 'john.anderson@medisupply.com',
            'address': '123 Medical Plaza, New York, NY 10001',
            'rating': 4.8
        },
        {
            'name': 'PharmaDirect Ltd',
            'contact_person': 'Sarah Johnson',
            'phone': '+1-555-0202',
            'email': 'sarah.j@pharmadirect.com',
            'address': '456 Healthcare Ave, Boston, MA 02101',
            'rating': 4.5
        },
        {
            'name': 'Global Pharma Solutions',
            'contact_person': 'Michael Chen',
            'phone': '+1-555-0303',
            'email': 'mchen@globalpharma.com',
            'address': '789 Wellness Blvd, Chicago, IL 60601',
            'rating': 4.9
        },
        {
            'name': 'HealthFirst Distributors',
            'contact_person': 'Emily Rodriguez',
            'phone': '+1-555-0404',
            'email': 'emily.r@healthfirst.com',
            'address': '321 Care Street, Los Angeles, CA 90001',
            'rating': 4.6
        },
        {
            'name': 'MedExpress Supply Chain',
            'contact_person': 'David Kim',
            'phone': '+1-555-0505',
            'email': 'dkim@medexpress.com',
            'address': '654 Pharmacy Lane, Houston, TX 77001',
            'rating': 4.7
        },
        {
            'name': 'Apex Medical Supplies',
            'contact_person': 'Lisa Thompson',
            'phone': '+1-555-0606',
            'email': 'lisa.t@apexmedical.com',
            'address': '987 Health Park, Miami, FL 33101',
            'rating': 4.4
        }
    ]
    
    created_date = datetime.now().strftime('%Y-%m-%d')
    
    for supplier in suppliers:
        # Check if supplier already exists
        cursor.execute('SELECT id FROM suppliers WHERE email = ?', (supplier['email'],))
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO suppliers (name, contact_person, phone, email, address, rating, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (supplier['name'], supplier['contact_person'], supplier['phone'],
                  supplier['email'], supplier['address'], supplier['rating'], created_date))
            print(f"Added supplier: {supplier['name']}")
        else:
            print(f"Supplier already exists: {supplier['name']}")
    
    conn.commit()
    conn.close()
    print("\nSupplier seeding completed!")

if __name__ == '__main__':
    seed_suppliers()

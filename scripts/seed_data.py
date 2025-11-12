import sqlite3
from datetime import datetime, timedelta
import random
from database import PharmacyDB

def seed_all_data():
    """Add comprehensive sample data to the database"""
    # Initialize database first
    print("Initializing database...")
    db = PharmacyDB()
    
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    # Sample medicines
    medicines = [
        {'name': 'Paracetamol 500mg', 'category': 'Pain Relief', 'quantity': 150, 'price': 5.99, 'reorder_level': 50},
        {'name': 'Ibuprofen 400mg', 'category': 'Pain Relief', 'quantity': 120, 'price': 7.49, 'reorder_level': 40},
        {'name': 'Amoxicillin 250mg', 'category': 'Antibiotic', 'quantity': 80, 'price': 12.99, 'reorder_level': 30},
        {'name': 'Cetirizine 10mg', 'category': 'Antihistamine', 'quantity': 200, 'price': 8.99, 'reorder_level': 60},
        {'name': 'Omeprazole 20mg', 'category': 'Antacid', 'quantity': 90, 'price': 15.49, 'reorder_level': 35},
        {'name': 'Metformin 500mg', 'category': 'Diabetes', 'quantity': 110, 'price': 18.99, 'reorder_level': 45},
        {'name': 'Aspirin 75mg', 'category': 'Cardiovascular', 'quantity': 180, 'price': 6.49, 'reorder_level': 55},
        {'name': 'Vitamin D3 1000IU', 'category': 'Supplement', 'quantity': 250, 'price': 9.99, 'reorder_level': 70},
        {'name': 'Cough Syrup', 'category': 'Cold & Flu', 'quantity': 45, 'price': 11.99, 'reorder_level': 25},
        {'name': 'Loratadine 10mg', 'category': 'Antihistamine', 'quantity': 160, 'price': 7.99, 'reorder_level': 50},
    ]
    
    # Add medicines
    medicine_ids = []
    for med in medicines:
        expiry_date = (datetime.now() + timedelta(days=random.randint(180, 730))).strftime('%Y-%m-%d')
        cursor.execute('SELECT id FROM medicines WHERE name = ?', (med['name'],))
        existing = cursor.fetchone()
        
        if existing is None:
            cursor.execute('''
                INSERT INTO medicines (name, category, quantity, price, expiry_date, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (med['name'], med['category'], med['quantity'], med['price'], expiry_date, med['reorder_level']))
            medicine_ids.append(cursor.lastrowid)
            print(f"Added medicine: {med['name']}")
        else:
            medicine_ids.append(existing[0])
            print(f"Medicine already exists: {med['name']}")
    
    # Add sample sales (last 30 days)
    print("\nAdding sample sales...")
    for i in range(100):
        med_id = random.choice(medicine_ids)
        quantity = random.randint(1, 10)
        days_ago = random.randint(0, 30)
        sale_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Get medicine price
        cursor.execute('SELECT price FROM medicines WHERE id = ?', (med_id,))
        price = cursor.fetchone()[0]
        total_price = price * quantity
        
        cursor.execute('''
            INSERT INTO sales (medicine_id, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?)
        ''', (med_id, quantity, total_price, sale_date))
    
    print(f"Added 100 sample sales")
    
    # Add suppliers
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
        }
    ]
    
    print("\nAdding suppliers...")
    created_date = datetime.now().strftime('%Y-%m-%d')
    
    for supplier in suppliers:
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
    print("\n✅ Database seeding completed successfully!")
    print("\nYou can now:")
    print("1. Run 'python app.py' to start the server")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Explore the Inventory, Sales, Suppliers, Predictions, and Analytics tabs")

if __name__ == '__main__':
    seed_all_data()

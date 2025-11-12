"""
Add indexes to database for faster queries
"""
import sqlite3

def optimize_database():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    print("Adding database indexes for performance...")
    
    try:
        # Index on medicines.user_id for faster filtering
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_medicines_user_id ON medicines(user_id)')
        print("✅ Index on medicines.user_id")
        
        # Index on sales.user_id for faster revenue calculations
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_user_id ON sales(user_id)')
        print("✅ Index on sales.user_id")
        
        # Index on sales.sale_date for date filtering
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date)')
        print("✅ Index on sales.sale_date")
        
        # Composite index on sales for today's sales query
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_user_date ON sales(user_id, sale_date)')
        print("✅ Composite index on sales(user_id, sale_date)")
        
        # Index on suppliers.user_id
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_suppliers_user_id ON suppliers(user_id)')
        print("✅ Index on suppliers.user_id")
        
        # Index on prescriptions.user_id
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_prescriptions_user_id ON prescriptions(user_id)')
        print("✅ Index on prescriptions.user_id")
        
        # Index on medicines for low stock queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_medicines_stock ON medicines(user_id, quantity, reorder_level)')
        print("✅ Composite index on medicines(user_id, quantity, reorder_level)")
        
        conn.commit()
        print("\n✅ Database optimization complete!")
        print("\nPerformance improvements:")
        print("  - Faster revenue calculations")
        print("  - Faster medicine filtering")
        print("  - Faster sales queries")
        print("  - Faster low stock checks")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    optimize_database()

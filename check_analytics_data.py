"""
Check analytics and reports data
"""
import requests
import sqlite3

API_URL = 'http://localhost:5000/api'

# Login
print("Logging in...")
login_response = requests.post(f'{API_URL}/login', json={
    'email': 'admin@pharmacy.com',
    'password': 'admin123'
})

token = login_response.json()['token']
headers = {'Authorization': f'Bearer {token}'}

print("✅ Login successful\n")
print("=" * 60)

# Check database directly
print("\n📊 DATABASE CHECK:")
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM medicines WHERE user_id = 1')
med_count = cursor.fetchone()[0]
print(f"  Medicines: {med_count}")

cursor.execute('SELECT COUNT(*) FROM sales WHERE user_id = 1')
sales_count = cursor.fetchone()[0]
print(f"  Sales: {sales_count}")

cursor.execute('SELECT SUM(total_price) FROM sales WHERE user_id = 1')
total_revenue = cursor.fetchone()[0] or 0
print(f"  Total Revenue: KSH {total_revenue:.2f}")

cursor.execute('SELECT COUNT(*) FROM medicines WHERE user_id = 1 AND quantity <= reorder_level')
low_stock = cursor.fetchone()[0]
print(f"  Low Stock Items: {low_stock}")

conn.close()

# Test Analytics API
print("\n📈 ANALYTICS API:")
try:
    response = requests.get(f'{API_URL}/analytics/summary', headers=headers)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ Total Medicines: {data.get('total_medicines', 0)}")
        print(f"  ✅ Low Stock: {data.get('low_stock_count', 0)}")
        print(f"  ✅ Today Sales: {data.get('today_sales_count', 0)}")
        print(f"  ✅ Today Revenue: KSH {data.get('today_revenue', 0):.2f}")
        print(f"  ✅ Total Revenue: KSH {data.get('total_revenue', 0):.2f}")
    else:
        print(f"  ❌ Error: {response.text}")
except Exception as e:
    print(f"  ❌ Exception: {e}")

# Test Sales API
print("\n💰 SALES API:")
try:
    response = requests.get(f'{API_URL}/sales', headers=headers)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        sales = response.json()
        print(f"  ✅ Sales Records: {len(sales)}")
        if len(sales) > 0:
            print(f"  Latest Sale: {sales[0]['medicine_name']} - KSH {sales[0]['total_price']}")
    else:
        print(f"  ❌ Error: {response.text}")
except Exception as e:
    print(f"  ❌ Exception: {e}")

print("\n" + "=" * 60)
print("\n📋 SUMMARY:")
print(f"  Database has {med_count} medicines and {sales_count} sales")
print(f"  Analytics should show immediately when you click the tab")
print(f"  Reports should show all {sales_count} sales records")
print("\n💡 If not showing:")
print("  1. Hard refresh browser: Ctrl+Shift+R")
print("  2. Check browser console (F12) for errors")
print("  3. Make sure you're on Analytics or Reports tab")

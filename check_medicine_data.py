"""
Check what data is actually being returned from medicines API
"""
import requests

API_URL = 'http://localhost:5000/api'

# Login
login_response = requests.post(f'{API_URL}/login', json={
    'email': 'admin@pharmacy.com',
    'password': 'admin123'
})

token = login_response.json()['token']

# Get medicines
medicines_response = requests.get(f'{API_URL}/medicines', headers={
    'Authorization': f'Bearer {token}'
})

medicines = medicines_response.json()

print("Medicines API Response:")
print("=" * 60)
print(f"Total medicines: {len(medicines)}")
print()

if len(medicines) > 0:
    print("First medicine data:")
    print(medicines[0])
    print()
    print("Fields available:")
    for key in medicines[0].keys():
        print(f"  - {key}: {medicines[0][key]}")
else:
    print("No medicines found!")

import sqlite3

conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Check organizations
print("=" * 60)
print("ORGANIZATIONS:")
print("=" * 60)
cursor.execute('SELECT * FROM organizations')
orgs = cursor.fetchall()
for org in orgs:
    print(f"ID: {org[0]}, Name: {org[1]}, Subdomain: {org[2]}, Email: {org[3]}")
    print(f"  Plan: {org[6]}, Status: {org[7]}, Max Users: {org[10]}")
    print()

# Check users
print("=" * 60)
print("USERS:")
print("=" * 60)
cursor.execute('SELECT id, organization_id, username, full_name, email, role FROM users')
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]}, Org ID: {user[1]}, Username: {user[2]}")
    print(f"  Name: {user[3]}, Email: {user[4]}, Role: {user[5]}")
    print()

print("=" * 60)
print(f"Total Organizations: {len(orgs)}")
print(f"Total Users: {len(users)}")
print("=" * 60)

conn.close()

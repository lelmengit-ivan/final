"""
Automatically fix all SQL queries in backend/app.py
"""
import re

# Read the file
with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match cursor.execute with ? placeholders
# Matches both single and triple quoted strings
patterns = [
    (r"cursor\.execute\('([^']*\?[^']*)'", r"cursor.execute(db.convert_query('\1')"),
    (r'cursor\.execute\("([^"]*\?[^"]*)"', r'cursor.execute(db.convert_query("\1")'),
    (r"cursor\.execute\('''([^']*\?[^']*)'''", r"cursor.execute(db.convert_query('''\1''')"),
]

# Apply all patterns
for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content)

# Write back
with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all SQL queries in backend/app.py")
print("\nNow run:")
print("  git add backend/app.py")
print("  git commit -m 'Fix all PostgreSQL queries'")
print("  git push")

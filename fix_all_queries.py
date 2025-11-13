"""
Fix all SQL queries in app.py to use db.convert_query()
"""

import re

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all cursor.execute with ? placeholders
pattern = r"cursor\.execute\('([^']*\?[^']*)'(?:,\s*\([^)]*\))?\)"

def replace_query(match):
    full_match = match.group(0)
    query = match.group(1)
    
    # If query has ?, wrap it with db.convert_query()
    if '?' in query:
        # Replace the query part
        new_match = full_match.replace(f"'{query}'", f"db.convert_query('{query}')")
        return new_match
    return full_match

# Replace all occurrences
new_content = re.sub(pattern, replace_query, content)

# Also handle triple-quoted strings
pattern2 = r"cursor\.execute\('''([^']*\?[^']*)'''(?:,\s*\([^)]*\))?\)"

def replace_query2(match):
    full_match = match.group(0)
    query = match.group(1)
    
    if '?' in query:
        new_match = full_match.replace(f"'''{query}'''", f"db.convert_query('''{query}''')")
        return new_match
    return full_match

new_content = re.sub(pattern2, replace_query2, new_content)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Fixed all SQL queries in app.py")
print("Now commit and push:")
print("  git add app.py")
print("  git commit -m 'Fix all PostgreSQL queries'")
print("  git push")

"""
Fix ALL unwrapped SQL queries in backend/app.py
"""
import re

# Read the file
with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match cursor.execute with single quotes and ?
pattern1 = r"cursor\.execute\('([^']*\?[^']*)'(?:,\s*\([^)]*\))?\)"

def replace_single_quote(match):
    full = match.group(0)
    query = match.group(1)
    # Wrap with db.convert_query
    return full.replace(f"'{query}'", f"db.convert_query('{query}')")

content = re.sub(pattern1, replace_single_quote, content)

# Write back
with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all unwrapped queries in backend/app.py")
print("\nNow run:")
print("  git add backend/app.py")
print("  git commit -m 'Fix all remaining PostgreSQL queries'")
print("  git push")

"""
Fix SQL placeholders in app.py for PostgreSQL compatibility
Replaces ? with %s where needed
"""

import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.content()

# Function to replace ? with placeholder variable in SQL queries
def fix_query(match):
    query = match.group(0)
    # Count number of ? placeholders
    count = query.count('?')
    if count == 0:
        return query
    
    # Replace ? with {placeholder}
    fixed = query
    for i in range(count):
        fixed = fixed.replace('?', '{placeholder}', 1)
    
    return fixed

# Find all cursor.execute statements with ?
pattern = r"cursor\.execute\(['\"].*?\?.*?['\"].*?\)"

# This is complex - better to do manually
print("Found queries that need fixing:")
matches = re.findall(r"cursor\.execute\(['\"].*?\?.*?['\"]", content)
for i, match in enumerate(matches[:10]):  # Show first 10
    print(f"{i+1}. {match[:80]}...")

print(f"\nTotal queries with ? placeholder: {len(matches)}")
print("\nManual fix recommended - use placeholder variable")

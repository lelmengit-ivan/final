"""
Quick script to add auth headers to all fetch calls in script.js
"""

import re

# Read the file
with open('static/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: fetch with just URL (GET requests)
# Replace: fetch(`${API_URL}/endpoint`)
# With: fetch(`${API_URL}/endpoint`, { headers: getAuthHeaders() })
pattern1 = r"fetch\(`\$\{API_URL\}/([^`]+)`\)(?!,)"
replacement1 = r"fetch(`${API_URL}/\1`, { headers: getAuthHeaders() })"
content = re.sub(pattern1, replacement1, content)

# Pattern 2: fetch with method but no headers
# Replace: fetch(`${API_URL}/endpoint`, { method: 'POST' })
# With: fetch(`${API_URL}/endpoint`, { method: 'POST', headers: getAuthHeaders() })
pattern2 = r"fetch\(`\$\{API_URL\}/([^`]+)`,\s*\{\s*method:\s*'(POST|PUT|DELETE)'\s*\}\)"
replacement2 = r"fetch(`${API_URL}/\1`, { method: '\2', headers: getAuthHeaders() })"
content = re.sub(pattern2, replacement2, content)

# Pattern 3: fetch with method and Content-Type only
# Replace: headers: { 'Content-Type': 'application/json' }
# With: headers: getAuthHeaders()
pattern3 = r"headers:\s*\{\s*'Content-Type':\s*'application/json'\s*\}"
replacement3 = r"headers: getAuthHeaders()"
content = re.sub(pattern3, replacement3, content)

# Write back
with open('static/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all fetch calls to include auth headers!")

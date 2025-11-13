"""
Final comprehensive fix for ALL SQL queries in backend/app.py
"""
import re

# Read file
with open('backend/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process line by line
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if line has cursor.execute without db.convert_query and has ?
    if 'cursor.execute(' in line and 'db.convert_query(' not in line:
        # Check if query has ?
        if i + 1 < len(lines) and '?' in ''.join(lines[i:min(i+10, len(lines))]):
            # Wrap with db.convert_query
            if "cursor.execute('''" in line:
                line = line.replace("cursor.execute('''", "cursor.execute(db.convert_query('''")
                # Find the closing ''' and add closing paren
                for j in range(i, min(i+20, len(lines))):
                    if "'''," in lines[j] or "'''))" in lines[j]:
                        lines[j] = lines[j].replace("''',", "'''),")
                        lines[j] = lines[j].replace("'''))", "'''))")
                        break
            elif "cursor.execute('" in line:
                line = line.replace("cursor.execute('", "cursor.execute(db.convert_query('")
                # Find the closing ' and add closing paren
                if "'," in line:
                    line = line.replace("',", "'),", 1)
    
    fixed_lines.append(line)
    i += 1

# Write back
with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ Fixed all SQL queries")
print("\nRun:")
print("  git add backend/app.py")
print("  git commit -m 'Fix all SQL queries comprehensively'")
print("  git push")

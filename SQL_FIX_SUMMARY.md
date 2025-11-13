# SQL Query Fix Summary

## Problem:
Many `cursor.execute()` statements in `backend/app.py` still have `?` placeholders that are NOT wrapped with `db.convert_query()`.

## Solution:
Every `cursor.execute()` with `?` must be wrapped like this:

### Before:
```python
cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
```

### After:
```python
cursor.execute(db.convert_query('SELECT * FROM users WHERE id = ?'), (user_id,))
```

## Lines That Need Fixing in backend/app.py:

- Line 117: INSERT INTO organizations
- Line 133: INSERT INTO users  
- Line 189: INSERT INTO users
- Line 321: INSERT INTO medicines
- Line 341: UPDATE medicines
- Line 391: INSERT INTO sales
- Line 397: UPDATE medicines
- Line 508: INSERT INTO suppliers
- Line 529: UPDATE suppliers
- Line 606: SELECT prescription_items
- Line 644: INSERT INTO prescriptions
- Line 655: INSERT INTO prescription_items
- Line 706: SELECT organizations (no ?)
- Line 741: SELECT organizations (no ?)

## Quick Fix Command:

Since there are many, the easiest way is to:

1. Go to GitHub.com
2. Edit backend/app.py directly
3. Search for `cursor.execute('''` 
4. Replace with `cursor.execute(db.convert_query('''`
5. Add closing `)` before the `,` in the parameters

OR

Run this PowerShell command:
```powershell
(Get-Content backend\app.py) -replace "cursor\.execute\('''", "cursor.execute(db.convert_query('''" | Set-Content backend\app.py
(Get-Content backend\app.py) -replace "''', \(", "''')), (" | Set-Content backend\app.py
```

Then:
```bash
git add backend/app.py
git commit -m "Fix all SQL queries"
git push
```

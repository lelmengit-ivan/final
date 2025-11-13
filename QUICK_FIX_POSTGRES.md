# 🔧 PostgreSQL Placeholder Fix

## Problem
PostgreSQL uses `%s` for placeholders, but the code was using `?` (SQLite syntax).

## Solution
Added `convert_query()` method to `database.py` that automatically converts `?` to `%s` when using PostgreSQL.

## What Was Fixed
1. Added `convert_query()` method in `database.py`
2. Updated login endpoint in `app.py` to use `db.convert_query()`

## Deploy Fix

```bash
# 1. Commit changes
git add database.py app.py
git commit -m "Fix PostgreSQL placeholder syntax"

# 2. Push to GitHub
git push

# 3. Render will auto-deploy
# Wait 2-3 minutes

# 4. Test login
# Should work now!
```

## Test
```bash
curl https://pharmacy-backened.onrender.com/api/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pharmacy.com","password":"admin123"}'
```

Should return JSON with token (not HTML error).

## Note
Other endpoints may still have the same issue. They need to be updated to use `db.convert_query()` as well.

For now, login should work!

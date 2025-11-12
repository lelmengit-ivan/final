# 🔍 Debug Instructions for Analytics & Reports

## The data IS in the database (207 sales, 11 medicines)
## The API IS working (tested successfully)
## Issue: Frontend not displaying

---

## Step 1: Open Browser Console

1. Open http://localhost:5000
2. Login with: admin@pharmacy.com / admin123
3. Press **F12** to open Developer Tools
4. Go to **Console** tab

---

## Step 2: Check for Errors

Look for RED error messages in console. Common issues:

### Error: "Chart is not defined"
**Fix:** Chart.js not loaded
- Check if `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>` is in index.html
- Check Network tab to see if it loaded

### Error: "Cannot read property 'getContext' of null"
**Fix:** Canvas element not found
- The chart canvas doesn't exist in HTML
- Check if you're on the right tab

### Error: "401 Unauthorized"
**Fix:** Token expired or missing
```javascript
// Run in console:
localStorage.clear();
location.reload();
// Then login again
```

---

## Step 3: Manual Test in Console

### Test Analytics Data Loading
```javascript
// Paste this in browser console (F12):
const token = localStorage.getItem('token');

// Test medicines
fetch('http://localhost:5000/api/medicines', {
    headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json()).then(d => console.log('Medicines:', d));

// Test sales
fetch('http://localhost:5000/api/sales', {
    headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json()).then(d => console.log('Sales:', d));

// Test predictions
fetch('http://localhost:5000/api/predictions', {
    headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json()).then(d => console.log('Predictions:', d));
```

### Manually Load Analytics
```javascript
// Paste this in console:
loadAnalytics();
// Watch console for "Loading analytics..." and any errors
```

### Manually Load Reports
```javascript
// Paste this in console:
loadReports();
// Watch console for "Loading reports..." and any errors
```

---

## Step 4: Check Elements Exist

```javascript
// Paste in console to check if elements exist:
console.log('Sales Trend Chart:', document.getElementById('salesTrendChart'));
console.log('Reports Table:', document.getElementById('reportsTableBody'));
console.log('Analytics Tab:', document.getElementById('analytics'));
console.log('Reports Tab:', document.getElementById('reports'));
```

If any return `null`, the HTML element is missing.

---

## Step 5: Force Reload Everything

```javascript
// Nuclear option - paste in console:
localStorage.clear();
sessionStorage.clear();
location.reload(true);
```

Then:
1. Login again
2. Click Analytics tab
3. Click Reports tab
4. Check console for messages

---

## Step 6: Check Tab Switching

```javascript
// Test if tab switching works:
showTab('analytics');  // Should load analytics
showTab('reports');    // Should load reports
```

---

## Expected Console Output

When working correctly, you should see:

```
Loading analytics...
Fetching data...
Loaded: 11 medicines, 50 sales, 11 predictions
Analytics loaded successfully!
```

```
Loading reports...
Loaded 50 sales records
Displayed 50 sales in reports table
Reports loaded successfully!
```

---

## Common Solutions

### Solution 1: Hard Refresh
- Press `Ctrl + Shift + R` (Windows)
- Or `Cmd + Shift + R` (Mac)

### Solution 2: Clear Everything
1. F12 → Application tab
2. Clear storage → Clear site data
3. Refresh page
4. Login again

### Solution 3: Incognito Window
- Open new incognito/private window
- Go to http://localhost:5000/login
- Login and test

### Solution 4: Check Chart.js
```javascript
// In console:
console.log('Chart.js loaded:', typeof Chart !== 'undefined');
```

If false, Chart.js didn't load. Check internet connection or use local copy.

---

## Report Back

After trying these steps, report:

1. **What errors appear in console?**
2. **What happens when you run `loadAnalytics()` in console?**
3. **Do the API test calls return data?**
4. **Does `typeof Chart` return 'function' or 'undefined'?**

This will help identify the exact issue!

# Download Fix - "Failed to Load" Error

## Issue
Downloaded PDF/Excel files show "Failed to load" error when opening.

## Common Causes

### 1. No Sales Data
**Symptom:** Files download but are empty/corrupted
**Fix:** 
- Make sure you have sales data
- Go to Sales tab and record at least one sale
- Then try downloading again

### 2. Browser Console Errors
**Check:**
1. Open browser console (F12)
2. Go to Reports tab
3. Click download button
4. Look for error messages

### 3. Libraries Not Loaded
**Check console for:**
- "jsPDF library not loaded"
- "XLSX library not loaded"
**Fix:** Refresh page (Ctrl+F5)

## Quick Test

### Step 1: Check if you have sales data
1. Go to Sales tab
2. Record a test sale:
   - Select any medicine
   - Enter quantity: 5
   - Select payment: Cash
   - Click "Record Sale"

### Step 2: Go to Reports tab
1. Click on "Reports" tab
2. Wait for table to load
3. Verify you see sales in the table

### Step 3: Try download
1. Click "📄 Download PDF" or "📊 Download Excel"
2. Check browser console for messages
3. Check Downloads folder

## Expected Console Output

**When clicking download:**
```
downloadPDF called
allSalesData: [{...}, {...}]
PDF saved successfully
```

**Or for Excel:**
```
downloadExcel called
allSalesData: [{...}, {...}]
Excel saved successfully
```

## If Still Failing

### Check 1: Verify data is loaded
Open console and type:
```javascript
console.log(allSalesData);
```
Should show array of sales, not empty []

### Check 2: Test libraries manually
```javascript
// Test jsPDF
const { jsPDF } = window.jspdf;
const doc = new jsPDF();
doc.text('Test', 10, 10);
doc.save('test.pdf');

// Test XLSX
const wb = XLSX.utils.book_new();
const ws = XLSX.utils.aoa_to_sheet([['Test']]);
XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
XLSX.writeFile(wb, 'test.xlsx');
```

### Check 3: Browser compatibility
- Try different browser (Chrome, Firefox, Edge)
- Disable browser extensions
- Check popup blocker settings

## Most Common Solution

**The issue is usually NO SALES DATA!**

1. Record at least one sale
2. Go to Reports tab
3. Wait for data to load (table shows sales)
4. Then download

## Verification Steps

✅ Server is running
✅ Logged in successfully
✅ Can see Sales tab
✅ Can record a sale
✅ Reports tab loads
✅ Table shows sales data
✅ Console shows no errors
✅ Download button works
✅ File downloads
✅ File opens successfully

---

**If you see "No sales data available" alert, you need to record some sales first!**

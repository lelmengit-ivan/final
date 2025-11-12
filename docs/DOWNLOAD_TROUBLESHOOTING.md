# Download Troubleshooting Guide

## Issue: PDF/Excel Not Downloading

### Quick Fixes:

1. **Refresh the Browser**
   - Press Ctrl+F5 (hard refresh)
   - This clears cache and reloads all scripts

2. **Check Browser Console**
   - Press F12
   - Go to Console tab
   - Look for error messages
   - Check if libraries loaded

3. **Test Libraries**
   - Open: http://localhost:5000/test_download.html
   - Click "Test PDF" and "Test Excel" buttons
   - If these work, the libraries are fine

4. **Check Reports Tab**
   - Go to Reports tab
   - Wait for data to load (table should show sales)
   - Then try download buttons

### Common Issues:

#### 1. Libraries Not Loading
**Symptoms:** Alert says "library not loaded"
**Fix:** 
- Check internet connection (libraries load from CDN)
- Refresh page (Ctrl+F5)
- Check browser console for 404 errors

#### 2. No Data Available
**Symptoms:** Alert says "No sales data available"
**Fix:**
- Make sure you're on the Reports tab
- Wait a few seconds for data to load
- Check if sales table shows data
- If table is empty, record some sales first

#### 3. Browser Blocking Downloads
**Symptoms:** Nothing happens when clicking button
**Fix:**
- Check browser popup blocker
- Allow downloads from localhost
- Check Downloads folder

#### 4. Console Errors
**Symptoms:** Errors in browser console
**Fix:**
- Read the error message
- Common errors:
  - "XLSX is not defined" → Library not loaded
  - "allSalesData is not defined" → Data not loaded
  - "Cannot read property" → Wait for data

### Debug Steps:

1. **Open Browser Console (F12)**
2. **Go to Reports Tab**
3. **Check Console Output:**
   - Should see: "downloadPDF called" or "downloadExcel called"
   - Should see: "allSalesData: [...]" with data
4. **If No Output:**
   - Button onclick not working
   - Check if buttons exist in HTML
5. **If Error Messages:**
   - Read the error
   - Follow fix suggestions

### Manual Test:

Open browser console and run:
```javascript
// Test if libraries loaded
console.log('jsPDF:', typeof window.jspdf);
console.log('XLSX:', typeof XLSX);

// Test if data loaded
console.log('allSalesData:', allSalesData);

// Test download functions
downloadPDF();
downloadExcel();
```

### Expected Behavior:

**When clicking Download PDF:**
1. Console shows: "downloadPDF called"
2. Console shows: "allSalesData: [array of sales]"
3. PDF file downloads
4. Filename: `sales_report_YYYY-MM-DD.pdf`

**When clicking Download Excel:**
1. Console shows: "downloadExcel called"
2. Console shows: "allSalesData: [array of sales]"
3. Excel file downloads
4. Filename: `sales_report_YYYY-MM-DD.xlsx`

### Still Not Working?

1. **Clear Browser Cache:**
   - Settings → Privacy → Clear browsing data
   - Select "Cached images and files"
   - Clear data

2. **Try Different Browser:**
   - Chrome
   - Firefox
   - Edge

3. **Check Server:**
   - Make sure Flask server is running
   - Check: http://localhost:5000/api/sales
   - Should return JSON data

4. **Restart Everything:**
   ```bash
   # Stop server (Ctrl+C)
   # Restart
   python app.py
   ```
   - Refresh browser
   - Login again
   - Go to Reports tab
   - Try downloads

### Success Indicators:

✅ Reports tab loads
✅ Sales table shows data
✅ Statistics cards show numbers
✅ Console shows no errors
✅ Clicking button shows console logs
✅ File downloads to Downloads folder

### Files to Check:

- `index.html` - Has script tags for jsPDF and XLSX
- `static/js/script.js` - Has downloadPDF() and downloadExcel() functions
- Browser Downloads folder - Check if files are there

---

**If still not working, check browser console (F12) and share the error messages!**

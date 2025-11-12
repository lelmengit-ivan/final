# 📥 Custom Report Download Guide

## ✅ Download Features Available

Your pharmacy system supports **custom filtered report downloads** in both PDF and Excel formats!

---

## 🎯 How to Download Reports

### Step 1: Go to Reports Tab
Click on the **Reports** tab in the navigation menu.

### Step 2: Filter Your Data (Optional)
Use the filter options to customize your report:

- **Search Medicine**: Type medicine name to filter
- **Start Date**: Select start date for date range
- **End Date**: Select end date for date range
- **Payment Method**: Filter by Cash, Bank, or M-Pesa

### Step 3: Download
Click either button:
- **📄 Download PDF** - Professional PDF report
- **📊 Download Excel** - Spreadsheet with multiple sheets

---

## 📄 PDF Report Includes

- **Header**: Sales Report title
- **Period**: Date range or "All Time"
- **Statistics**:
  - Total Sales count
  - Total Revenue in KSH
- **Sales Table**:
  - Medicine name
  - Quantity sold
  - Price
  - Payment method
  - Date & time

**Filename**: `sales_report_YYYY-MM-DD.pdf`

---

## 📊 Excel Report Includes

### Sheet 1: Summary
- Report period
- Generation date & time
- **Statistics**:
  - Total Sales
  - Total Revenue
  - Cash Sales breakdown
  - Bank Sales breakdown
  - M-Pesa Sales breakdown

### Sheet 2: Sales Data
- Complete sales records with:
  - Medicine name
  - Quantity
  - Price (KSH)
  - Payment method
  - Date & time
- **Formatted columns** with proper widths

**Filename**: `sales_report_YYYY-MM-DD.xlsx`

---

## 🎨 Custom Report Examples

### Example 1: Monthly Cash Sales
1. Set Start Date: `2024-11-01`
2. Set End Date: `2024-11-30`
3. Payment Method: `Cash`
4. Click Download PDF or Excel

### Example 2: Specific Medicine Sales
1. Search Medicine: `Paracetamol`
2. Leave dates empty (all time)
3. Click Download

### Example 3: M-Pesa Transactions
1. Payment Method: `M-Pesa`
2. Click Download Excel
3. Get detailed breakdown in spreadsheet

### Example 4: Last Week's Sales
1. Set Start Date: 7 days ago
2. Set End Date: Today
3. Click Download PDF

---

## 🔧 Technical Details

### Libraries Used
- **jsPDF 2.5.1** - PDF generation
- **jsPDF-AutoTable 3.5.31** - PDF tables
- **SheetJS (XLSX) 0.18.5** - Excel generation

### Browser Compatibility
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### File Size
- PDF: ~50-200 KB (depends on records)
- Excel: ~20-100 KB (depends on records)

---

## 💡 Tips

### Best Practices
1. **Filter before downloading** - Smaller files are faster
2. **Use date ranges** - Get specific period reports
3. **Excel for analysis** - Better for calculations
4. **PDF for sharing** - Professional presentation

### Performance
- Downloads are instant for up to 1000 records
- Large datasets (>5000 records) may take a few seconds
- All processing happens in browser (no server load)

### Troubleshooting

#### "Library not loaded" error
**Solution**: Refresh the page (Ctrl+F5)

#### "No sales data available" error
**Solution**: 
1. Wait for data to load
2. Make sure you have sales records
3. Check if filters are too restrictive

#### Download doesn't start
**Solution**:
1. Check browser pop-up blocker
2. Allow downloads from localhost
3. Try different browser

---

## 📊 Data Included in Downloads

### Always Included
- Medicine name
- Quantity sold
- Total price
- Payment method
- Sale date & time

### Summary Statistics
- Total number of sales
- Total revenue
- Payment method breakdown (Excel only)

### Filtered Data
- Only shows records matching your filters
- Statistics calculated from filtered data
- Date range shown in report header

---

## 🎯 Use Cases

### For Management
- Monthly revenue reports
- Payment method analysis
- Sales trends by period

### For Accounting
- Cash vs digital payments
- Daily/weekly/monthly summaries
- Tax reporting data

### For Inventory
- Medicine sales frequency
- Stock movement analysis
- Reorder planning

### For Auditing
- Complete transaction history
- Date-specific records
- Payment verification

---

## ✅ Current Status

**Status**: ✅ Fully Functional

- PDF Download: Working
- Excel Download: Working
- Filtering: Working
- Custom date ranges: Working
- Payment method filter: Working
- Search by medicine: Working

---

## 🚀 Quick Start

1. Click **Reports** tab
2. (Optional) Set filters
3. Click **Download PDF** or **Download Excel**
4. File downloads automatically!

**That's it!** Your custom report is ready to use.

---

**Note**: All downloads happen in your browser - no data is sent to external servers. Your data stays private and secure.

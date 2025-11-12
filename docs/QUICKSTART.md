# Quick Start Guide - Pharmacy Management System

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Seed Sample Data (Optional but Recommended)
```bash
python seed_data.py
```

This will add:
- 10 sample medicines across different categories
- 100 sample sales transactions (last 30 days)
- 5 supplier companies with contact details

### Step 3: Run the Application
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📋 Features Overview

### 1. Inventory Tab
- Add new medicines with details (name, category, quantity, price, expiry date)
- View all medicines in a table
- Color-coded stock levels (red = low stock, green = adequate)
- Delete medicines
- Track reorder levels

### 2. Sales Tab
- Record sales transactions
- Select medicine from dropdown
- Automatic stock deduction
- View recent sales history
- Real-time price calculation

### 3. Suppliers Tab
- Add supplier information
- Track contact details (person, phone, email, address)
- Rate suppliers (0-5 stars)
- View suppliers in card layout
- Delete suppliers

### 4. AI Predictions Tab
- 7-day demand forecasting
- Confidence levels (high/medium/low)
- Reorder recommendations
- Stock alerts (urgent/warning/ok)
- Based on 30-day sales history

### 5. Analytics Tab
- **Sales Trend**: Line chart of daily sales (30 days)
- **Top Medicines**: Bar chart of best sellers
- **Inventory Status**: Doughnut chart (adequate vs low stock)
- **Category Distribution**: Pie chart of medicine categories
- **Revenue Trend**: Bar chart of daily revenue
- **Prediction vs Current**: Comparison of stock levels

---

## 💡 Usage Tips

### Adding Your First Medicine
1. Go to **Inventory** tab
2. Click **+ Add Medicine**
3. Fill in all fields:
   - Name: e.g., "Aspirin 100mg"
   - Category: e.g., "Pain Relief"
   - Quantity: e.g., 100
   - Price: e.g., 5.99
   - Expiry Date: Select future date
   - Reorder Level: e.g., 20 (alert when stock falls below this)
4. Click **Add Medicine**

### Recording a Sale
1. Go to **Sales** tab
2. Select medicine from dropdown
3. Enter quantity sold
4. Click **Record Sale**
5. Stock automatically updates!

### Adding a Supplier
1. Go to **Suppliers** tab
2. Click **+ Add Supplier**
3. Fill in company details
4. Set rating (0-5)
5. Click **Add Supplier**

### Viewing AI Predictions
1. Go to **AI Predictions** tab
2. Click **🔄 Refresh** to update
3. View predictions for each medicine:
   - Current stock
   - Average daily sales
   - 7-day predicted demand
   - Confidence level
   - Reorder recommendation

### Analyzing Data
1. Go to **Analytics** tab
2. Click **🔄 Refresh** to load charts
3. Hover over charts for detailed values
4. All charts are interactive and responsive

---

## 🎯 Sample Workflow

1. **Start with sample data**: Run `python seed_data.py`
2. **Explore inventory**: Check the 10 pre-loaded medicines
3. **Record a sale**: Sell some Paracetamol or Ibuprofen
4. **Check predictions**: See AI recommendations for restocking
5. **View analytics**: Explore the 6 interactive charts
6. **Add a supplier**: Create your own supplier entry
7. **Monitor stock**: Watch for low stock alerts (red text)

---

## 🔧 Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Database Issues
Delete `pharmacy.db` and run `python seed_data.py` again to reset.

### Charts Not Loading
Make sure you have internet connection (Chart.js loads from CDN).

### No Predictions Showing
You need sales history first. Record some sales, then check predictions.

---

## 📊 Understanding AI Predictions

The system uses a **Moving Average Algorithm**:
- Analyzes last 30 days of sales
- Calculates average daily sales
- Projects demand for next 7 days
- Compares with current stock
- Generates recommendations

**Confidence Levels:**
- **High**: 10+ sales records, reliable prediction
- **Medium**: 5-10 sales records, moderate reliability
- **Low**: <5 sales records, limited data

**Recommendations:**
- **URGENT**: Stock will run out before 7 days
- **REORDER NEEDED**: Stock will fall below reorder level
- **Stock levels adequate**: No action needed

---

## 🎨 Color Coding

- 🟢 **Green**: Adequate stock, good status
- 🔴 **Red**: Low stock, urgent attention needed
- 🟡 **Yellow**: Warning, monitor closely
- 🔵 **Blue**: Information, normal status

---

## 📱 Mobile Friendly

The system is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

All tables and charts adapt to screen size automatically.

---

## 🔐 Security Note

This is a demo system. For production use, add:
- User authentication
- Password protection
- HTTPS encryption
- Input validation
- SQL injection prevention
- Access control

---

## 🆘 Need Help?

Check the main README.md for:
- Full feature list
- Database schema
- API endpoints
- Future enhancements

---

**Enjoy managing your pharmacy! 💊🏥**

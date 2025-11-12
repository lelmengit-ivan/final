# Pharmacy Management System with AI Prediction

A complete pharmacy management system with AI-powered stock prediction capabilities.

## Features

- **Inventory Management**: Add, view, and delete medicines with expiry tracking
- **Sales Recording**: Record sales transactions and automatically update stock
- **Prescription Tracking**: Complete prescription management system
  - Create prescriptions with patient and doctor details
  - Add multiple medicines per prescription
  - Track dosage and duration
  - Manage prescription status (pending/completed/cancelled)
  - Automatic inventory updates on completion
- **Supplier Management**: Manage supplier information with contact details and ratings
  - Add/delete suppliers
  - Track contact information
  - Rate suppliers (0-5 stars)
  - View supplier history
- **AI Predictions**: Machine learning-based stock demand forecasting
- **Analytics Dashboard**: Interactive charts and graphs for data visualization
  - Sales trend analysis
  - Top selling medicines
  - Inventory status distribution
  - Category breakdown
  - Revenue tracking
  - Prediction vs current stock comparison
- **Reports & Analytics**: Comprehensive reporting system
  - Summary dashboard with key metrics
  - Top selling medicines report
  - Low stock alerts
  - Expiry predictions
  - Customizable date ranges
  - Export to PDF (ready for implementation)
- **Low Stock Alerts**: Automatic warnings for medicines below reorder level
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js for interactive data visualization
- **Backend**: Python (Flask)
- **Database**: SQLite
- **AI**: Custom prediction algorithm using sales history analysis

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Seed the database with sample data:
```bash
python seed_data.py
```

3. Create admin user:
```bash
python create_admin.py
```
Default credentials: `admin` / `admin123`

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

6. Login with admin credentials or register a new account

## Usage

### Adding Medicines
1. Go to the Inventory tab
2. Click "Add Medicine"
3. Fill in the medicine details
4. Click "Add Medicine" to save

### Recording Sales
1. Go to the Sales tab
2. Select a medicine from the dropdown
3. Enter the quantity sold
4. Click "Record Sale"

### Viewing AI Predictions
1. Go to the AI Predictions tab
2. View predicted demand for the next 7 days
3. Check recommendations for reordering

## AI Prediction Algorithm

The system uses a simple moving average algorithm that:
- Analyzes sales history from the past 30 days
- Calculates average daily sales
- Predicts demand for the next 7 days
- Provides confidence levels based on data availability
- Generates reorder recommendations

## Database Schema

### Medicines Table
- id (PRIMARY KEY)
- name
- category
- quantity
- price
- expiry_date
- reorder_level

### Sales Table
- id (PRIMARY KEY)
- medicine_id (FOREIGN KEY)
- quantity
- total_price
- sale_date

### Prescriptions Table
- id (PRIMARY KEY)
- patient_name
- patient_phone
- doctor_name
- prescription_date
- status
- notes
- created_date

### Prescription Items Table
- id (PRIMARY KEY)
- prescription_id (FOREIGN KEY)
- medicine_id (FOREIGN KEY)
- quantity
- dosage
- duration

### Suppliers Table
- id (PRIMARY KEY)
- name
- contact_person
- phone
- email
- address
- rating
- created_date

## Future Enhancements

- Advanced ML models (LSTM, ARIMA)
- User authentication
- Supplier management
- Prescription tracking
- Reports and analytics
- Email notifications for low stock

# Pharmacy Management System - Project Structure

```
pharmacy-system/
│
├── 📄 index.html              # Main HTML file with all tabs
├── 🎨 styles.css              # Complete styling for all components
├── ⚡ script.js               # Frontend JavaScript logic
│
├── 🐍 app.py                  # Flask backend API server
├── 💾 database.py             # Database initialization & schema
├── 🤖 ai_predictor.py         # AI prediction algorithms
│
├── 🌱 seed_data.py            # Complete database seeding script
├── 🌱 seed_suppliers.py       # Supplier-only seeding script
│
├── 🚀 run.bat                 # Windows quick start script
├── 🚀 run.sh                  # Linux/Mac quick start script
│
├── 📋 requirements.txt        # Python dependencies
├── 📖 README.md               # Main documentation
├── 📖 QUICKSTART.md           # Quick start guide
├── 📖 PROJECT_STRUCTURE.md    # This file
├── 🚫 .gitignore              # Git ignore rules
│
└── 💾 pharmacy.db             # SQLite database (created on first run)
```

## File Descriptions

### Frontend Files

**index.html** (Main Interface)
- 5 tabs: Inventory, Sales, Suppliers, Predictions, Analytics
- Forms for adding medicines and suppliers
- Tables for displaying data
- Canvas elements for charts
- Responsive layout

**styles.css** (Styling)
- Modern gradient design
- Card layouts for predictions and suppliers
- Responsive grid systems
- Color-coded status indicators
- Hover effects and animations
- Mobile-friendly media queries

**script.js** (Client Logic)
- Tab switching functionality
- CRUD operations for medicines
- Sales recording
- Supplier management
- Chart.js integration (6 charts)
- API communication
- Form handling

### Backend Files

**app.py** (Flask Server)
- RESTful API endpoints
- Medicine CRUD operations
- Sales recording with stock updates
- Supplier management
- AI prediction endpoints
- Analytics summary
- CORS enabled
- Runs on port 5000

**database.py** (Database Layer)
- SQLite connection management
- Table creation (4 tables)
- Schema definitions:
  - medicines
  - sales
  - suppliers
  - medicine_suppliers

**ai_predictor.py** (AI Engine)
- Moving average algorithm
- 7-day demand forecasting
- Confidence scoring
- Reorder recommendations
- Sales history analysis
- Stock prediction logic

### Data Seeding Files

**seed_data.py** (Complete Seeding)
- 10 sample medicines
- 100 sales transactions (30 days)
- 5 supplier companies
- Random but realistic data
- Prevents duplicates

**seed_suppliers.py** (Suppliers Only)
- 6 supplier companies
- Contact information
- Ratings
- Addresses

### Utility Files

**run.bat** (Windows Launcher)
- Checks Python installation
- Installs dependencies
- Seeds database if needed
- Starts Flask server
- User-friendly output

**run.sh** (Unix Launcher)
- Same as run.bat for Linux/Mac
- Bash script
- Executable permissions needed

**requirements.txt** (Dependencies)
- Flask==3.0.0
- Flask-CORS==4.0.0

**.gitignore** (Git Rules)
- Python cache files
- Database files
- IDE settings
- OS files
- Environment variables

## Database Schema

### medicines
```sql
id              INTEGER PRIMARY KEY
name            TEXT NOT NULL
category        TEXT
quantity        INTEGER DEFAULT 0
price           REAL
expiry_date     TEXT
reorder_level   INTEGER DEFAULT 10
```

### sales
```sql
id              INTEGER PRIMARY KEY
medicine_id     INTEGER (FK)
quantity        INTEGER
total_price     REAL
sale_date       TEXT
```

### suppliers
```sql
id              INTEGER PRIMARY KEY
name            TEXT NOT NULL
contact_person  TEXT
phone           TEXT
email           TEXT
address         TEXT
rating          REAL DEFAULT 0
created_date    TEXT
```

### medicine_suppliers
```sql
id                  INTEGER PRIMARY KEY
medicine_id         INTEGER (FK)
supplier_id         INTEGER (FK)
supply_price        REAL
last_supply_date    TEXT
```

## API Endpoints

### Medicines
- `GET    /api/medicines`           - Get all medicines
- `POST   /api/medicines`           - Add new medicine
- `PUT    /api/medicines/<id>`      - Update medicine
- `DELETE /api/medicines/<id>`      - Delete medicine

### Sales
- `GET    /api/sales`               - Get recent sales
- `POST   /api/sales`               - Record new sale

### Suppliers
- `GET    /api/suppliers`           - Get all suppliers
- `POST   /api/suppliers`           - Add new supplier
- `PUT    /api/suppliers/<id>`      - Update supplier
- `DELETE /api/suppliers/<id>`      - Delete supplier

### Predictions
- `GET    /api/predictions`         - Get all predictions
- `GET    /api/predictions/<id>`    - Get medicine prediction

### Analytics
- `GET    /api/analytics/summary`   - Get summary stats

## Technology Stack

### Frontend
- HTML5
- CSS3 (Grid, Flexbox, Animations)
- JavaScript (ES6+)
- Chart.js 4.4.0 (CDN)

### Backend
- Python 3.x
- Flask 3.0.0
- SQLite3
- Flask-CORS 4.0.0

### AI/ML
- Custom Moving Average Algorithm
- Statistical Analysis
- Time Series Prediction

## Features by Tab

### 1. Inventory Tab
- Add medicine form (7 fields)
- Medicine table (sortable)
- Low stock indicators
- Delete functionality
- Expiry date tracking

### 2. Sales Tab
- Sale recording form
- Medicine dropdown (with stock)
- Recent sales table
- Automatic stock updates
- Price calculation

### 3. Suppliers Tab
- Add supplier form (6 fields)
- Supplier cards (grid layout)
- Star ratings
- Contact information
- Delete functionality

### 4. AI Predictions Tab
- Prediction cards (grid)
- 7-day forecasts
- Confidence badges
- Recommendations
- Color-coded alerts

### 5. Analytics Tab
- Sales Trend (line chart)
- Top Medicines (bar chart)
- Inventory Status (doughnut)
- Category Distribution (pie)
- Revenue Trend (bar chart)
- Prediction Comparison (bar chart)

## Color Scheme

- Primary: #667eea (Purple-Blue)
- Secondary: #764ba2 (Purple)
- Success: #28a745 (Green)
- Danger: #dc3545 (Red)
- Warning: #ffc107 (Yellow)
- Info: #17a2b8 (Cyan)

## Responsive Breakpoints

- Desktop: > 768px (multi-column grids)
- Tablet: 768px (2-column grids)
- Mobile: < 768px (single column)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Lightweight (< 1MB total)
- Fast loading (< 2s)
- Smooth animations (60fps)
- Efficient database queries
- Minimal dependencies

## Security Considerations

⚠️ **This is a demo system. For production:**
- Add user authentication
- Implement HTTPS
- Validate all inputs
- Sanitize SQL queries
- Add rate limiting
- Implement CSRF protection
- Add session management
- Encrypt sensitive data

## Future Enhancements

- User authentication & roles
- Barcode scanning
- Prescription management
- Email notifications
- PDF reports
- Advanced ML models (LSTM, ARIMA)
- Multi-pharmacy support
- Mobile app
- Real-time updates (WebSocket)
- Backup & restore
- Audit logs
- Advanced analytics

---

**Built with ❤️ for efficient pharmacy management**

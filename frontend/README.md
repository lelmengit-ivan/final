# Pharmacy Management System - Frontend

This folder contains all frontend files for the Pharmacy Management System.

## 📁 Structure

```
frontend/
├── index.html              # Main dashboard
├── login.html              # Login page
├── register-org.html       # Organization registration
├── README.md               # This file
└── static/
    ├── config.js           # API configuration
    ├── css/
    │   ├── styles.css      # Dashboard styles
    │   └── login.css       # Login page styles
    └── js/
        ├── script.js       # Dashboard functionality
        └── login.js        # Login functionality
```

## 🚀 Usage

### Option 1: With Backend (Full Stack)
Run the Flask backend which serves the frontend:
```bash
cd ..
python app.py
```
Then visit: `http://localhost:5000`

### Option 2: Standalone (Static Server)
Serve frontend files with any static server:

**Python:**
```bash
python -m http.server 8000
```

**Node.js (http-server):**
```bash
npx http-server -p 8000
```

**Live Server (VS Code):**
Right-click `index.html` → "Open with Live Server"

Then configure `static/config.js` to point to your backend API.

## ⚙️ Configuration

Edit `static/config.js` to set your backend API URL:

### Local Backend:
```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000/api'
};
```

### Render Backend:
```javascript
const CONFIG = {
    API_URL: 'https://your-app.onrender.com/api'
};
```

### Auto-detect:
```javascript
const CONFIG = {
    API_URL: window.location.origin + '/api'
};
```

## 📄 Pages

### 1. Login Page (`login.html`)
- User authentication
- Organization-based login
- Registration form
- JWT token management

**Features:**
- Email or username login
- Password validation
- Remember me (localStorage)
- Error handling

### 2. Dashboard (`index.html`)
- Inventory management
- Sales tracking
- Analytics & reports
- AI predictions
- Multi-tenancy support

**Tabs:**
- Dashboard - Overview & analytics
- Inventory - Medicine management
- Sales - Sales transactions
- Suppliers - Supplier management
- Prescriptions - Prescription tracking
- Reports - Download reports

### 3. Organization Registration (`register-org.html`)
- Create new organization
- Subscription plans
- Admin user setup

## 🎨 Styling

### CSS Files:
- `static/css/styles.css` - Main dashboard styles
- `static/css/login.css` - Login page styles

### Design:
- Modern, clean interface
- Responsive design
- Color scheme: Blue/white theme
- Icons: Emoji-based

## 🔧 JavaScript

### `static/js/login.js`
- Login/registration logic
- JWT token handling
- Form validation
- API communication

### `static/js/script.js`
- Dashboard functionality
- CRUD operations
- Chart rendering (Chart.js)
- Report generation (jsPDF, xlsx)
- Real-time updates

## 📊 Dependencies

### External Libraries (CDN):
- **Chart.js** - Data visualization
- **jsPDF** - PDF generation
- **jsPDF-AutoTable** - PDF tables
- **xlsx** - Excel export

All loaded from CDN, no npm install needed.

## 🔐 Authentication

### JWT Token Flow:
1. User logs in via `login.html`
2. Backend returns JWT token
3. Token stored in `localStorage`
4. Token sent with every API request
5. Auto-redirect if token invalid

### Token Storage:
```javascript
localStorage.setItem('token', token);
localStorage.setItem('user', JSON.stringify(user));
```

## 🌐 API Integration

All API calls use the configured `API_URL` from `config.js`:

```javascript
// Example API call
fetch(`${API_URL}/medicines`, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
```

### API Endpoints:
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `GET /api/medicines` - Get medicines
- `POST /api/medicines` - Add medicine
- `GET /api/sales` - Get sales
- `POST /api/sales` - Record sale
- `GET /api/analytics/summary` - Get analytics
- And more...

## 🚢 Deployment

### Deploy with Backend:
The frontend is automatically served by Flask when you deploy the backend to Render.

### Deploy Separately (Static Hosting):
1. Upload `frontend/` folder to:
   - Netlify
   - Vercel
   - GitHub Pages
   - Any static host

2. Update `static/config.js` with your backend URL

3. Enable CORS on backend for your frontend domain

## 🔍 Troubleshooting

### Login Not Working:
1. Check `static/config.js` has correct API URL
2. Check backend is running
3. Check browser console for errors
4. Disable ad blockers
5. Clear browser cache

### API Errors:
1. Verify backend URL is accessible
2. Check CORS is enabled on backend
3. Verify JWT token is valid
4. Check network tab in DevTools

### Styling Issues:
1. Clear browser cache
2. Check CSS files are loading
3. Check browser console for 404s

## 📱 Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern browsers with ES6+ support

## 🎯 Features

### Dashboard:
- Real-time analytics
- Interactive charts
- Quick stats
- Recent activities

### Inventory:
- Add/edit/delete medicines
- Stock tracking
- Expiry alerts
- Low stock warnings

### Sales:
- Record sales
- Payment methods
- Sales history
- Revenue tracking

### Reports:
- PDF export
- Excel export
- Custom date ranges
- Detailed analytics

### Multi-tenancy:
- Organization isolation
- User management
- Role-based access
- Subscription plans

## 🔄 Updates

To update frontend:
1. Edit HTML/CSS/JS files
2. Test locally
3. Commit changes
4. Push to Git
5. Backend auto-serves updated files

## 📝 Notes

- All frontend files are static (HTML/CSS/JS)
- No build process required
- No npm dependencies
- Works with any backend
- Mobile-responsive
- PWA-ready (can be enhanced)

## 🤝 Contributing

When modifying frontend:
1. Test all features
2. Check responsive design
3. Verify API integration
4. Update this README if needed

## 📞 Support

For issues:
1. Check browser console
2. Check network tab
3. Verify backend is running
4. Check API configuration

---

**Version:** 1.0.0  
**Last Updated:** November 2025

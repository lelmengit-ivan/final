from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import PharmacyDB
from ai_predictor import StockPredictor
from datetime import datetime, timedelta
from functools import wraps
import sqlite3
import hashlib
import jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-jwt-secret-key-change-in-production-12345678')
app.config['JWT_EXPIRATION_HOURS'] = 24

CORS(app, resources={r"/*": {"origins": "*"}})

db = PharmacyDB()
predictor = StockPredictor()

# Helper function to get correct SQL placeholder
def get_placeholder():
    """Return correct SQL placeholder based on database type"""
    return '%s' if db.use_postgres else '?'

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to create JWT token
def create_token(user_id, username, email, role, organization_id, organization_name):
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'role': role,
        'organization_id': organization_id,
        'organization_name': organization_name,
        'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS']),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Helper function to verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to require authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Add user info to request
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/register-org')
def register_org_page():
    return send_from_directory('.', 'register-org.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Organization registration endpoint
@app.route('/api/organizations/register', methods=['POST'])
def register_organization():
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check if subdomain already exists
    if data.get('subdomain'):
        cursor.execute('SELECT id FROM organizations WHERE subdomain = ?', (data['subdomain'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Subdomain already taken'}), 400
    
    # Create organization
    cursor.execute('''
        INSERT INTO organizations (name, subdomain, contact_email, contact_phone, address, 
                                   subscription_plan, subscription_status, created_date, 
                                   expiry_date, max_users, settings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['organization_name'], data.get('subdomain'), data['contact_email'], 
          data.get('contact_phone', ''), data.get('address', ''), 
          data.get('subscription_plan', 'free'), 'active', 
          datetime.now().strftime('%Y-%m-%d'),
          (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
          data.get('max_users', 5), '{}'))
    
    organization_id = cursor.lastrowid
    
    # Create admin user for the organization
    hashed_password = hash_password(data['password'])
    cursor.execute('''
        INSERT INTO users (organization_id, username, password, full_name, email, role, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (organization_id, data['username'], hashed_password, data['full_name'], 
          data['email'], 'admin', datetime.now().strftime('%Y-%m-%d')))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': 'Organization registered successfully',
        'organization_id': organization_id,
        'user_id': user_id
    })

# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get organization_id (required)
    organization_id = data.get('organization_id')
    if not organization_id:
        conn.close()
        return jsonify({'error': 'Organization ID is required'}), 400
    
    # Check if organization exists and is active
    cursor.execute('SELECT subscription_status, max_users FROM organizations WHERE id = ?', (organization_id,))
    org = cursor.fetchone()
    if not org:
        conn.close()
        return jsonify({'error': 'Organization not found'}), 404
    
    if org[0] != 'active':
        conn.close()
        return jsonify({'error': 'Organization subscription is not active'}), 403
    
    # Check user limit
    cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = ?', (organization_id,))
    user_count = cursor.fetchone()[0]
    if user_count >= org[1]:
        conn.close()
        return jsonify({'error': 'Maximum user limit reached for this organization'}), 403
    
    # Check if username or email already exists in this organization
    cursor.execute('SELECT id FROM users WHERE organization_id = ? AND (username = ? OR email = ?)', 
                   (organization_id, data['username'], data['email']))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Username or email already exists in this organization'}), 400
    
    # Create new user
    hashed_password = hash_password(data['password'])
    cursor.execute('''
        INSERT INTO users (organization_id, username, password, full_name, email, role, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (organization_id, data['username'], hashed_password, data['full_name'], 
          data['email'], 'user', datetime.now().strftime('%Y-%m-%d')))
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'message': 'Registration successful', 'user_id': user_id})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor()
    
    hashed_password = hash_password(data['password'])
    
    # Determine login method
    email_or_username = data.get('email') or data.get('username')
    
    # Login with organization_id (if provided) or email/username
    if data.get('organization_id'):
        query = db.convert_query('''
            SELECT u.id, u.username, u.full_name, u.email, u.role, u.organization_id, o.name
            FROM users u
            JOIN organizations o ON u.organization_id = o.id
            WHERE u.organization_id = ? AND u.username = ? AND u.password = ?
        ''')
        cursor.execute(query, (data['organization_id'], email_or_username, hashed_password))
    else:
        # Try email first, then username
        query = db.convert_query('''
            SELECT u.id, u.username, u.full_name, u.email, u.role, u.organization_id, o.name
            FROM users u
            JOIN organizations o ON u.organization_id = o.id
            WHERE (u.email = ? OR u.username = ?) AND u.password = ?
        ''')
        cursor.execute(query, (email_or_username, email_or_username, hashed_password))
    
    user = cursor.fetchone()
    
    if user:
        # Check organization subscription status
        cursor.execute('SELECT subscription_status FROM organizations WHERE id = ?', (user[5],))
        org_status = cursor.fetchone()
        
        if org_status and org_status[0] != 'active':
            conn.close()
            return jsonify({'error': 'Organization subscription is not active'}), 403
        
        # Update last login
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user[0]))
        conn.commit()
        conn.close()
        
        # Create JWT token with organization info
        token = create_token(user[0], user[1], user[3], user[4], user[5], user[6])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'email': user[3],
                'role': user[4],
                'organization_id': user[5],
                'organization_name': user[6]
            }
        })
    
    conn.close()
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    # With JWT, logout is handled client-side by removing the token
    return jsonify({'message': 'Logout successful'})

@app.route('/api/check-auth', methods=['GET'])
@token_required
def check_auth():
    return jsonify({
        'authenticated': True,
        'user': {
            'id': request.current_user['user_id'],
            'username': request.current_user['username'],
            'email': request.current_user['email'],
            'role': request.current_user['role'],
            'organization_id': request.current_user['organization_id'],
            'organization_name': request.current_user['organization_name']
        }
    })

# Medicine endpoints
@app.route('/api/medicines', methods=['GET'])
@token_required
def get_medicines():
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, quantity, price, expiry_date, reorder_level FROM medicines WHERE user_id = ?', (user_id,))
    medicines = cursor.fetchall()
    conn.close()
    
    result = []
    for med in medicines:
        result.append({
            'id': med[0],
            'name': med[1],
            'category': med[2],
            'quantity': med[3],
            'price': med[4],
            'expiry_date': med[5],
            'reorder_level': med[6]
        })
    return jsonify(result)

@app.route('/api/medicines', methods=['POST'])
@token_required
def add_medicine():
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO medicines (user_id, name, category, quantity, price, expiry_date, reorder_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, data['name'], data['category'], data['quantity'], 
          data['price'], data['expiry_date'], data.get('reorder_level', 10)))
    
    conn.commit()
    med_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': med_id, 'message': 'Medicine added successfully'})

@app.route('/api/medicines/<int:med_id>', methods=['PUT'])
@token_required
def update_medicine(med_id):
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE medicines 
        SET name=?, category=?, quantity=?, price=?, expiry_date=?, reorder_level=?
        WHERE id=? AND user_id=?
    ''', (data['name'], data['category'], data['quantity'], 
          data['price'], data['expiry_date'], data.get('reorder_level', 10), med_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Medicine updated successfully'})

@app.route('/api/medicines/<int:med_id>', methods=['DELETE'])
@token_required
def delete_medicine(med_id):
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM medicines WHERE id=? AND user_id=?', (med_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Medicine deleted successfully'})

# Sales endpoints
@app.route('/api/sales', methods=['POST'])
@token_required
def add_sale():
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check stock (only user's own medicines)
    cursor.execute('SELECT quantity, price FROM medicines WHERE id=? AND user_id=?', (data['medicine_id'], user_id))
    result = cursor.fetchone()
    
    if not result:
        return jsonify({'error': 'Medicine not found'}), 404
    
    current_qty, price = result
    if current_qty < data['quantity']:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Get payment method (default to 'cash' if not provided)
    payment_method = data.get('payment_method', 'cash')
    
    # Record sale with current date and time
    total_price = price * data['quantity']
    sale_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO sales (user_id, medicine_id, quantity, total_price, sale_date, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, data['medicine_id'], data['quantity'], total_price, sale_datetime, payment_method))
    
    # Update stock
    cursor.execute('''
        UPDATE medicines SET quantity = quantity - ? WHERE id = ? AND user_id = ?
    ''', (data['quantity'], data['medicine_id'], user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Sale recorded successfully', 'total_price': total_price})

@app.route('/api/sales', methods=['GET'])
@token_required
def get_sales():
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, m.name, s.quantity, s.total_price, s.sale_date, 
               COALESCE(s.payment_method, 'cash') as payment_method
        FROM sales s
        JOIN medicines m ON s.medicine_id = m.id
        WHERE s.user_id = ?
        ORDER BY s.id DESC
        LIMIT 50
    ''', (user_id,))
    sales = cursor.fetchall()
    conn.close()
    
    result = []
    for sale in sales:
        result.append({
            'id': sale[0],
            'medicine_name': sale[1],
            'quantity': sale[2],
            'total_price': sale[3],
            'sale_date': sale[4],
            'payment_method': sale[5]
        })
    return jsonify(result)

# AI Prediction endpoints
@app.route('/api/predictions', methods=['GET'])
@token_required
def get_predictions():
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get only user's medicines
    cursor.execute('SELECT id, name FROM medicines WHERE user_id = ?', (user_id,))
    medicines = cursor.fetchall()
    conn.close()
    
    predictions = []
    for med_id, med_name in medicines:
        pred = predictor.predict_stock_needs(med_id)
        pred['medicine_id'] = med_id
        pred['medicine_name'] = med_name
        predictions.append(pred)
    
    return jsonify(predictions)

@app.route('/api/predictions/<int:med_id>', methods=['GET'])
@token_required
def get_medicine_prediction(med_id):
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Verify medicine belongs to user
    cursor.execute('SELECT id FROM medicines WHERE id = ? AND user_id = ?', (med_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Medicine not found'}), 404
    
    conn.close()
    prediction = predictor.predict_stock_needs(med_id)
    return jsonify(prediction)

# Supplier endpoints
@app.route('/api/suppliers', methods=['GET'])
@token_required
def get_suppliers():
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, contact_person, phone, email, address, rating, created_date FROM suppliers WHERE user_id = ?', (user_id,))
    suppliers = cursor.fetchall()
    conn.close()
    
    result = []
    for sup in suppliers:
        result.append({
            'id': sup[0],
            'name': sup[1],
            'contact_person': sup[2],
            'phone': sup[3],
            'email': sup[4],
            'address': sup[5],
            'rating': sup[6],
            'created_date': sup[7]
        })
    return jsonify(result)

@app.route('/api/suppliers', methods=['POST'])
@token_required
def add_supplier():
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO suppliers (user_id, name, contact_person, phone, email, address, rating, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, data['name'], data['contact_person'], data['phone'], 
          data['email'], data['address'], data.get('rating', 0), 
          datetime.now().strftime('%Y-%m-%d')))
    
    conn.commit()
    supplier_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': supplier_id, 'message': 'Supplier added successfully'})

@app.route('/api/suppliers/<int:supplier_id>', methods=['PUT'])
@token_required
def update_supplier(supplier_id):
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE suppliers 
        SET name=?, contact_person=?, phone=?, email=?, address=?, rating=?
        WHERE id=? AND user_id=?
    ''', (data['name'], data['contact_person'], data['phone'], 
          data['email'], data['address'], data.get('rating', 0), supplier_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Supplier updated successfully'})

@app.route('/api/suppliers/<int:supplier_id>', methods=['DELETE'])
@token_required
def delete_supplier(supplier_id):
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM suppliers WHERE id=? AND user_id=?', (supplier_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Supplier deleted successfully'})

@app.route('/api/analytics/summary', methods=['GET'])
@token_required
def get_analytics_summary():
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Total medicines
    cursor.execute('SELECT COUNT(*) FROM medicines WHERE user_id = ?', (user_id,))
    total_medicines = cursor.fetchone()[0]
    
    # Low stock count
    cursor.execute('SELECT COUNT(*) FROM medicines WHERE user_id = ? AND quantity <= reorder_level', (user_id,))
    low_stock = cursor.fetchone()[0]
    
    # Total sales today
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*), SUM(total_price) FROM sales WHERE user_id = ? AND sale_date LIKE ?', (user_id, today + '%'))
    today_sales = cursor.fetchone()
    
    # Total revenue
    cursor.execute('SELECT SUM(total_price) FROM sales WHERE user_id = ?', (user_id,))
    total_revenue = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'total_medicines': total_medicines,
        'low_stock_count': low_stock,
        'today_sales_count': today_sales[0] or 0,
        'today_revenue': today_sales[1] or 0,
        'total_revenue': total_revenue
    })

# Prescription endpoints
@app.route('/api/prescriptions', methods=['GET'])
@token_required
def get_prescriptions():
    user_id = request.current_user['user_id']
    status = request.args.get('status', None)
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if status and status != 'all':
        cursor.execute('SELECT id, patient_name, patient_phone, doctor_name, prescription_date, status, notes, created_date FROM prescriptions WHERE user_id = ? AND status = ? ORDER BY created_date DESC', (user_id, status))
    else:
        cursor.execute('SELECT id, patient_name, patient_phone, doctor_name, prescription_date, status, notes, created_date FROM prescriptions WHERE user_id = ? ORDER BY created_date DESC', (user_id,))
    
    prescriptions = cursor.fetchall()
    
    result = []
    for presc in prescriptions:
        # Get prescription items
        cursor.execute('''
            SELECT pi.id, pi.prescription_id, pi.medicine_id, pi.quantity, pi.dosage, pi.duration, m.name as medicine_name
            FROM prescription_items pi
            JOIN medicines m ON pi.medicine_id = m.id
            WHERE pi.prescription_id = ?
        ''', (presc[0],))
        items = cursor.fetchall()
        
        result.append({
            'id': presc[0],
            'patient_name': presc[1],
            'patient_phone': presc[2],
            'doctor_name': presc[3],
            'prescription_date': presc[4],
            'status': presc[5],
            'notes': presc[6],
            'created_date': presc[7],
            'items': [{
                'medicine_id': item[2],
                'medicine_name': item[6],
                'quantity': item[3],
                'dosage': item[4],
                'duration': item[5]
            } for item in items]
        })
    
    conn.close()
    return jsonify(result)

@app.route('/api/prescriptions', methods=['POST'])
@token_required
def add_prescription():
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Insert prescription
    cursor.execute('''
        INSERT INTO prescriptions (user_id, patient_name, patient_phone, doctor_name, prescription_date, status, notes, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, data['patient_name'], data['patient_phone'], data['doctor_name'],
          data['prescription_date'], 'pending', data.get('notes', ''),
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    prescription_id = cursor.lastrowid
    
    # Insert prescription items
    for item in data['items']:
        cursor.execute('''
            INSERT INTO prescription_items (prescription_id, medicine_id, quantity, dosage, duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (prescription_id, item['medicine_id'], item['quantity'], item['dosage'], item['duration']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': prescription_id, 'message': 'Prescription created successfully'})

@app.route('/api/prescriptions/<int:prescription_id>/status', methods=['PUT'])
@token_required
def update_prescription_status(prescription_id):
    data = request.json
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE prescriptions SET status = ? WHERE id = ? AND user_id = ?', (data['status'], prescription_id, user_id))
    
    # If completing prescription, update inventory
    if data['status'] == 'completed':
        cursor.execute('SELECT medicine_id, quantity FROM prescription_items WHERE prescription_id = ?', (prescription_id,))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute('UPDATE medicines SET quantity = quantity - ? WHERE id = ? AND user_id = ?', (item[1], item[0], user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Prescription status updated'})

@app.route('/api/prescriptions/<int:prescription_id>', methods=['DELETE'])
@token_required
def delete_prescription(prescription_id):
    user_id = request.current_user['user_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM prescription_items WHERE prescription_id = ?', (prescription_id,))
    cursor.execute('DELETE FROM prescriptions WHERE id = ? AND user_id = ?', (prescription_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Prescription deleted successfully'})

# Organization Management endpoints
@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, subdomain, contact_email, contact_phone, address, 
               subscription_plan, subscription_status, created_date, expiry_date, max_users
        FROM organizations
        ORDER BY created_date DESC
    ''')
    organizations = cursor.fetchall()
    conn.close()
    
    result = []
    for org in organizations:
        result.append({
            'id': org[0],
            'name': org[1],
            'subdomain': org[2],
            'contact_email': org[3],
            'contact_phone': org[4],
            'address': org[5],
            'subscription_plan': org[6],
            'subscription_status': org[7],
            'created_date': org[8],
            'expiry_date': org[9],
            'max_users': org[10]
        })
    return jsonify(result)

@app.route('/api/organizations/<int:org_id>', methods=['GET'])
@token_required
def get_organization(org_id):
    # Users can only view their own organization
    if request.current_user['organization_id'] != org_id and request.current_user['role'] != 'superadmin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, subdomain, contact_email, contact_phone, address, 
               subscription_plan, subscription_status, created_date, expiry_date, max_users, settings
        FROM organizations WHERE id = ?
    ''', (org_id,))
    org = cursor.fetchone()
    
    if not org:
        conn.close()
        return jsonify({'error': 'Organization not found'}), 404
    
    # Get user count
    cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = ?', (org_id,))
    user_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'id': org[0],
        'name': org[1],
        'subdomain': org[2],
        'contact_email': org[3],
        'contact_phone': org[4],
        'address': org[5],
        'subscription_plan': org[6],
        'subscription_status': org[7],
        'created_date': org[8],
        'expiry_date': org[9],
        'max_users': org[10],
        'settings': org[11],
        'current_users': user_count
    })

@app.route('/api/organizations/<int:org_id>', methods=['PUT'])
@token_required
def update_organization(org_id):
    # Only admins can update their organization
    if request.current_user['organization_id'] != org_id or request.current_user['role'] not in ['admin', 'superadmin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE organizations 
        SET name=?, contact_email=?, contact_phone=?, address=?, settings=?
        WHERE id=?
    ''', (data['name'], data['contact_email'], data.get('contact_phone', ''), 
          data.get('address', ''), data.get('settings', '{}'), org_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Organization updated successfully'})

@app.route('/api/organizations/<int:org_id>/subscription', methods=['PUT'])
@token_required
def update_subscription(org_id):
    # Only admins can update subscription
    if request.current_user['organization_id'] != org_id or request.current_user['role'] not in ['admin', 'superadmin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Update subscription plan
    cursor.execute('''
        UPDATE organizations 
        SET subscription_plan=?, subscription_status=?, expiry_date=?, max_users=?
        WHERE id=?
    ''', (data['subscription_plan'], data.get('subscription_status', 'active'),
          data.get('expiry_date'), data.get('max_users', 5), org_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Subscription updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# User Management endpoints
@app.route('/api/users', methods=['GET'])
@token_required
def get_users():
    organization_id = request.current_user['organization_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, full_name, email, role, created_date, last_login 
        FROM users WHERE organization_id = ?
    ''', (organization_id,))
    users = cursor.fetchall()
    conn.close()
    
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'username': user[1],
            'full_name': user[2],
            'email': user[3],
            'role': user[4],
            'created_date': user[5],
            'last_login': user[6]
        })
    return jsonify(result)

@app.route('/api/users', methods=['POST'])
@token_required
def add_user():
    # Only admins can add users
    if request.current_user['role'] not in ['admin', 'superadmin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    organization_id = request.current_user['organization_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check user limit
    cursor.execute('SELECT max_users FROM organizations WHERE id = ?', (organization_id,))
    max_users = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = ?', (organization_id,))
    user_count = cursor.fetchone()[0]
    
    if user_count >= max_users:
        conn.close()
        return jsonify({'error': 'Maximum user limit reached'}), 403
    
    # Check if username or email already exists in organization
    cursor.execute('SELECT id FROM users WHERE organization_id = ? AND (username = ? OR email = ?)', 
                   (organization_id, data['username'], data['email']))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Create new user
    hashed_password = hash_password(data['password'])
    cursor.execute('''
        INSERT INTO users (organization_id, username, password, full_name, email, role, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (organization_id, data['username'], hashed_password, data['full_name'], 
          data['email'], data.get('role', 'user'), datetime.now().strftime('%Y-%m-%d')))
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': user_id, 'message': 'User added successfully'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    # Only admins can delete users
    if request.current_user['role'] not in ['admin', 'superadmin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    organization_id = request.current_user['organization_id']
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check if user belongs to same organization
    cursor.execute('SELECT role FROM users WHERE id = ? AND organization_id = ?', (user_id, organization_id))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent deleting the last admin
    if user[0] == 'admin':
        cursor.execute('SELECT COUNT(*) FROM users WHERE organization_id = ? AND role = ?', (organization_id, 'admin'))
        admin_count = cursor.fetchone()[0]
        if admin_count <= 1:
            conn.close()
            return jsonify({'error': 'Cannot delete the last admin user'}), 400
    
    cursor.execute('DELETE FROM users WHERE id = ? AND organization_id = ?', (user_id, organization_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User deleted successfully'})

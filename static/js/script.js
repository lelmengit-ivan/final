const API_URL = 'http://localhost:5000/api';

// Store chart instances
let charts = {};

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'inventory') loadMedicines();
    if (tabName === 'sales') {
        loadSales();
        loadMedicineOptions();
    }
    if (tabName === 'prescriptions') loadPrescriptions();
    if (tabName === 'suppliers') loadSuppliers();
    if (tabName === 'predictions') loadPredictions();
    if (tabName === 'analytics') loadAnalytics();
    if (tabName === 'reports') loadReports();
    if (tabName === 'users') loadUsers();
}

// Medicine functions
function showAddMedicineForm() {
    document.getElementById('addMedicineForm').style.display = 'block';
}

function hideAddMedicineForm() {
    document.getElementById('addMedicineForm').style.display = 'none';
    document.querySelector('#addMedicineForm form').reset();
}

async function addMedicine(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('medName').value,
        category: document.getElementById('medCategory').value,
        quantity: parseInt(document.getElementById('medQuantity').value),
        price: parseFloat(document.getElementById('medPrice').value),
        expiry_date: document.getElementById('medExpiry').value,
        reorder_level: parseInt(document.getElementById('medReorder').value)
    };
    
    try {
        const response = await fetch(`${API_URL}/medicines`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Medicine added successfully!');
            hideAddMedicineForm();
            loadMedicines();
        }
    } catch (error) {
        alert('Error adding medicine: ' + error.message);
    }
}

async function loadMedicines() {
    const tbody = document.getElementById('medicineTableBody');
    try {
        const response = await fetch(`${API_URL}/medicines`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            tbody.innerHTML = `<tr><td colspan="7">Error: ${response.status} - ${response.statusText}</td></tr>`;
            return;
        }
        
        const medicines = await response.json();
        
        if (medicines.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No medicines found</td></tr>';
            return;
        }
        
        tbody.innerHTML = medicines.map(med => {
            const isLowStock = med.quantity <= med.reorder_level;
            const stockClass = isLowStock ? 'status-low' : 'status-ok';
            const price = parseFloat(med.price) || 0;
            
            return `
                <tr>
                    <td>${med.name}</td>
                    <td>${med.category}</td>
                    <td class="${stockClass}">${med.quantity}</td>
                    <td>KSH ${price.toFixed(2)}</td>
                    <td>${med.expiry_date}</td>
                    <td>${med.reorder_level}</td>
                    <td>
                        <button class="btn btn-danger" onclick="deleteMedicine(${med.id})">Delete</button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading medicines:', error);
        tbody.innerHTML = `<tr><td colspan="7">Error loading medicines: ${error.message}</td></tr>`;
    }
}

async function deleteMedicine(id) {
    if (!confirm('Are you sure you want to delete this medicine?')) return;
    
    try {
        const response = await fetch(`${API_URL}/medicines/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (response.ok) {
            alert('Medicine deleted successfully!');
            loadMedicines();
        }
    } catch (error) {
        alert('Error deleting medicine: ' + error.message);
    }
}

// Sales functions
async function loadMedicineOptions() {
    try {
        const response = await fetch(`${API_URL}/medicines`, { headers: getAuthHeaders() });
        const medicines = await response.json();
        
        const select = document.getElementById('saleMedicine');
        select.innerHTML = '<option value="">Select Medicine</option>' +
            medicines.map(med => `<option value="${med.id}">${med.name} (Stock: ${med.quantity})</option>`).join('');
    } catch (error) {
        console.error('Error loading medicine options:', error);
    }
}

async function recordSale(event) {
    event.preventDefault();
    
    const data = {
        medicine_id: parseInt(document.getElementById('saleMedicine').value),
        quantity: parseInt(document.getElementById('saleQuantity').value),
        payment_method: document.getElementById('paymentMethod').value
    };
    
    try {
        const response = await fetch(`${API_URL}/sales`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const totalPrice = parseFloat(result.total_price) || 0;
            alert(`Sale recorded! Total: KSH ${totalPrice.toFixed(2)}`);
            document.querySelector('#sales form').reset();
            loadSales();
            loadMedicineOptions();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error recording sale: ' + error.message);
    }
}

let allSales = [];

async function loadSales() {
    try {
        const response = await fetch(`${API_URL}/sales`, { headers: getAuthHeaders() });
        const sales = await response.json();
        allSales = sales;
        
        displaySales(sales);
    } catch (error) {
        console.error('Error loading sales:', error);
    }
}

function displaySales(sales) {
    const tbody = document.getElementById('salesTableBody');
    if (sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No sales recorded</td></tr>';
        return;
    }
    
    tbody.innerHTML = sales.map(sale => `
            <tr>
                <td>${sale.medicine_name}</td>
                <td style="text-align: center;">${sale.quantity}</td>
                <td style="text-align: right;">KSH ${(parseFloat(sale.total_price) || 0).toFixed(2)}</td>
                <td style="text-align: center;">${
                    sale.payment_method === 'cash' ? '<span class="payment-badge payment-cash">💵 Cash</span>' :
                    sale.payment_method === 'bank' ? '<span class="payment-badge payment-bank">🏦 Bank</span>' :
                    sale.payment_method === 'mpesa' ? '<span class="payment-badge payment-mpesa">📱 M-Pesa</span>' :
                    '<span class="payment-badge payment-cash">💵 Cash</span>'
                }</td>
                <td style="text-align: center;">${sale.sale_date}</td>
            </tr>
        `).join('');
}

// Search sales
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchSales');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const filtered = allSales.filter(sale => 
                sale.medicine_name.toLowerCase().includes(searchTerm) ||
                sale.payment_method.toLowerCase().includes(searchTerm) ||
                sale.sale_date.includes(searchTerm)
            );
            displaySales(filtered);
        });
    }
});

// Predictions functions
async function loadPredictions() {
    const grid = document.getElementById('predictionsGrid');
    grid.innerHTML = '<div class="loading">Loading predictions...</div>';
    
    try {
        const response = await fetch(`${API_URL}/predictions`, { headers: getAuthHeaders() });
        const predictions = await response.json();
        
        if (predictions.length === 0) {
            grid.innerHTML = '<div class="loading">No predictions available</div>';
            return;
        }
        
        grid.innerHTML = predictions.map(pred => {
            let cardClass = 'prediction-card';
            let recClass = 'recommendation ok';
            
            if (pred.recommendation.includes('URGENT')) {
                cardClass += ' urgent';
                recClass = 'recommendation urgent';
            } else if (pred.recommendation.includes('REORDER')) {
                cardClass += ' warning';
                recClass = 'recommendation warning';
            }
            
            const confidenceClass = `confidence-${pred.confidence}`;
            
            return `
                <div class="${cardClass}">
                    <h3>${pred.medicine_name}</h3>
                    <div class="prediction-info">
                        <div class="prediction-row">
                            <span class="prediction-label">Current Stock:</span>
                            <span class="prediction-value">${pred.current_stock}</span>
                        </div>
                        <div class="prediction-row">
                            <span class="prediction-label">Avg Daily Sales:</span>
                            <span class="prediction-value">${pred.avg_daily_sales}</span>
                        </div>
                        <div class="prediction-row">
                            <span class="prediction-label">7-Day Demand:</span>
                            <span class="prediction-value">${pred.predicted_demand}</span>
                        </div>
                        <div class="prediction-row">
                            <span class="prediction-label">Confidence:</span>
                            <span class="confidence-badge ${confidenceClass}">${pred.confidence.toUpperCase()}</span>
                        </div>
                    </div>
                    <div class="${recClass}">
                        ${pred.recommendation}
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        grid.innerHTML = '<div class="loading">Error loading predictions</div>';
        console.error('Error loading predictions:', error);
    }
}

// Analytics functions
async function loadAnalytics() {
    console.log('Loading analytics...');
    try {
        // Destroy existing charts
        Object.values(charts).forEach(chart => chart.destroy());
        charts = {};
        
        // Load all data
        console.log('Fetching data...');
        const [medicines, sales, predictions] = await Promise.all([
            fetch(`${API_URL}/medicines`, { headers: getAuthHeaders() }).then(r => {
                if (!r.ok) throw new Error(`Medicines API failed: ${r.status}`);
                return r.json();
            }),
            fetch(`${API_URL}/sales`, { headers: getAuthHeaders() }).then(r => {
                if (!r.ok) throw new Error(`Sales API failed: ${r.status}`);
                return r.json();
            }),
            fetch(`${API_URL}/predictions`, { headers: getAuthHeaders() }).then(r => {
                if (!r.ok) throw new Error(`Predictions API failed: ${r.status}`);
                return r.json();
            })
        ]);
        
        console.log(`Loaded: ${medicines.length} medicines, ${sales.length} sales, ${predictions.length} predictions`);
        
        createSalesTrendChart(sales);
        createTopMedicinesChart(sales);
        createInventoryChart(medicines);
        createCategoryChart(medicines);
        createRevenueChart(sales);
        createPredictionChart(predictions);
        
        console.log('Analytics loaded successfully!');
    } catch (error) {
        console.error('Error loading analytics:', error);
        alert('Error loading analytics: ' + error.message);
    }
}

function createSalesTrendChart(sales) {
    try {
        const salesByDate = {};
        sales.forEach(sale => {
            // Extract just the date part (YYYY-MM-DD) from datetime
            const dateOnly = sale.sale_date ? sale.sale_date.split(' ')[0] : 'Unknown';
            salesByDate[dateOnly] = (salesByDate[dateOnly] || 0) + (sale.quantity || 0);
        });
        
        const dates = Object.keys(salesByDate).sort().slice(-30);
        const quantities = dates.map(date => salesByDate[date]);
        
        const ctx = document.getElementById('salesTrendChart');
        if (!ctx) {
            console.error('salesTrendChart canvas not found');
            return;
        }
        
        charts.salesTrend = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Units Sold',
                    data: quantities,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        console.log('Sales trend chart created');
    } catch (error) {
        console.error('Error creating sales trend chart:', error);
    }
}

function createTopMedicinesChart(sales) {
    const salesByMedicine = {};
    sales.forEach(sale => {
        salesByMedicine[sale.medicine_name] = (salesByMedicine[sale.medicine_name] || 0) + sale.quantity;
    });
    
    const sorted = Object.entries(salesByMedicine)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const ctx = document.getElementById('topMedicinesChart').getContext('2d');
    charts.topMedicines = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(s => s[0]),
            datasets: [{
                label: 'Units Sold',
                data: sorted.map(s => s[1]),
                backgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { beginAtZero: true }
            }
        }
    });
}

function createInventoryChart(medicines) {
    const lowStock = medicines.filter(m => m.quantity <= m.reorder_level).length;
    const adequateStock = medicines.length - lowStock;
    
    const ctx = document.getElementById('inventoryChart').getContext('2d');
    charts.inventory = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Adequate Stock', 'Low Stock'],
            datasets: [{
                data: [adequateStock, lowStock],
                backgroundColor: ['#28a745', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function createCategoryChart(medicines) {
    const categories = {};
    medicines.forEach(med => {
        categories[med.category] = (categories[med.category] || 0) + 1;
    });
    
    const ctx = document.getElementById('categoryChart').getContext('2d');
    charts.category = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe',
                    '#43e97b', '#fa709a', '#fee140', '#30cfd0'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function createRevenueChart(sales) {
    const revenueByDate = {};
    sales.forEach(sale => {
        revenueByDate[sale.sale_date] = (revenueByDate[sale.sale_date] || 0) + sale.total_price;
    });
    
    const dates = Object.keys(revenueByDate).sort().slice(-30);
    const revenues = dates.map(date => revenueByDate[date]);
    
    const ctx = document.getElementById('revenueChart').getContext('2d');
    charts.revenue = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: 'Revenue ($)',
                data: revenues,
                backgroundColor: '#28a745'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createPredictionChart(predictions) {
    const top10 = predictions
        .sort((a, b) => b.predicted_demand - a.predicted_demand)
        .slice(0, 10);
    
    const ctx = document.getElementById('predictionChart').getContext('2d');
    charts.prediction = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top10.map(p => p.medicine_name),
            datasets: [
                {
                    label: 'Current Stock',
                    data: top10.map(p => p.current_stock),
                    backgroundColor: '#667eea'
                },
                {
                    label: '7-Day Predicted Demand',
                    data: top10.map(p => p.predicted_demand),
                    backgroundColor: '#dc3545'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Supplier functions
function showAddSupplierForm() {
    document.getElementById('addSupplierForm').style.display = 'block';
}

function hideAddSupplierForm() {
    document.getElementById('addSupplierForm').style.display = 'none';
    document.querySelector('#addSupplierForm form').reset();
}

async function addSupplier(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('supplierName').value,
        contact_person: document.getElementById('supplierContact').value,
        phone: document.getElementById('supplierPhone').value,
        email: document.getElementById('supplierEmail').value,
        address: document.getElementById('supplierAddress').value,
        rating: parseFloat(document.getElementById('supplierRating').value)
    };
    
    try {
        const response = await fetch(`${API_URL}/suppliers`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Supplier added successfully!');
            hideAddSupplierForm();
            loadSuppliers();
        }
    } catch (error) {
        alert('Error adding supplier: ' + error.message);
    }
}

async function loadSuppliers() {
    const grid = document.getElementById('suppliersGrid');
    try {
        const response = await fetch(`${API_URL}/suppliers`, { headers: getAuthHeaders() });
        
        if (!response.ok) {
            grid.innerHTML = `<div class="loading">Error: ${response.status} - ${response.statusText}</div>`;
            return;
        }
        
        const suppliers = await response.json();
        
        if (suppliers.length === 0) {
            grid.innerHTML = '<div class="loading">No suppliers found</div>';
            return;
        }
        
        grid.innerHTML = suppliers.map(supplier => {
            const rating = parseFloat(supplier.rating) || 0;
            const stars = '⭐'.repeat(Math.round(rating));
            
            return `
                <div class="supplier-card">
                    <div class="supplier-header">
                        <h3>${supplier.name}</h3>
                        <div class="supplier-rating">${stars} ${rating.toFixed(1)}</div>
                    </div>
                    <div class="supplier-info">
                        <div class="info-row">
                            <span class="info-label">👤 Contact:</span>
                            <span class="info-value">${supplier.contact_person}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">📞 Phone:</span>
                            <span class="info-value">${supplier.phone}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">📧 Email:</span>
                            <span class="info-value">${supplier.email}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">📍 Address:</span>
                            <span class="info-value">${supplier.address}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">📅 Added:</span>
                            <span class="info-value">${supplier.created_date}</span>
                        </div>
                    </div>
                    <div class="supplier-actions">
                        <button class="btn btn-danger" onclick="deleteSupplier(${supplier.id})">Delete</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading suppliers:', error);
        grid.innerHTML = `<div class="loading">Error loading suppliers: ${error.message}</div>`;
    }
}

async function deleteSupplier(id) {
    if (!confirm('Are you sure you want to delete this supplier?')) return;
    
    try {
        const response = await fetch(`${API_URL}/suppliers/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
        
        if (response.ok) {
            alert('Supplier deleted successfully!');
            loadSuppliers();
        }
    } catch (error) {
        alert('Error deleting supplier: ' + error.message);
    }
}

// Check authentication on load
async function checkAuth() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    
    try {
        const response = await fetch(`${API_URL}/check-auth`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return false;
        }
        
        const data = await response.json();
        if (data.authenticated) {
            // Display user info
            displayUserInfo(data.user);
            return true;
        } else {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return false;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return false;
    }
}

// Helper function to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

function displayUserInfo(user) {
    const userInfoDiv = document.getElementById('userInfo');
    if (userInfoDiv) {
        userInfoDiv.innerHTML = `
            <div style="text-align: right;">
                <div style="font-size: 12px; color: #7f8c8d; margin-bottom: 3px;">
                    🏢 ${user.organization_name || 'Organization'} ${user.organization_id ? `(ID: ${user.organization_id})` : ''}
                </div>
                <div>
                    <span class="user-name">👤 ${user.full_name || user.username}</span>
                    ${user.role === 'admin' ? '<span style="background: #e74c3c; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-left: 5px;">ADMIN</span>' : ''}
                    <button class="btn btn-secondary btn-sm" onclick="handleLogout()">Logout</button>
                </div>
            </div>
        `;
    }
}

async function handleLogout() {
    if (!confirm('Are you sure you want to logout?')) return;
    
    try {
        await fetch(`${API_URL}/logout`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    // Clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', async () => {
    const isAuthenticated = await checkAuth();
    if (isAuthenticated) {
        loadMedicines();
    }
});

// Prescription functions
let prescriptionMedicinesList = [];

function showAddPrescriptionForm() {
    document.getElementById('addPrescriptionForm').style.display = 'block';
    loadPrescriptionMedicineOptions();
}

function hideAddPrescriptionForm() {
    document.getElementById('addPrescriptionForm').style.display = 'none';
    document.querySelector('#addPrescriptionForm form').reset();
    document.getElementById('prescriptionMedicines').innerHTML = `
        <div class="prescription-medicine-row">
            <select class="prescription-medicine" required>
                <option value="">Select Medicine</option>
            </select>
            <input type="number" class="prescription-quantity" placeholder="Qty" min="1" required>
            <input type="text" class="prescription-dosage" placeholder="Dosage (e.g., 2x daily)" required>
            <input type="text" class="prescription-duration" placeholder="Duration (e.g., 7 days)" required>
        </div>
    `;
}

async function loadPrescriptionMedicineOptions() {
    try {
        const response = await fetch(`${API_URL}/medicines`, { headers: getAuthHeaders() });
        prescriptionMedicinesList = await response.json();
        
        const selects = document.querySelectorAll('.prescription-medicine');
        selects.forEach(select => {
            select.innerHTML = '<option value="">Select Medicine</option>' +
                prescriptionMedicinesList.map(med => `<option value="${med.id}">${med.name}</option>`).join('');
        });
    } catch (error) {
        console.error('Error loading medicines:', error);
    }
}

function addPrescriptionMedicineRow() {
    const container = document.getElementById('prescriptionMedicines');
    const newRow = document.createElement('div');
    newRow.className = 'prescription-medicine-row';
    newRow.innerHTML = `
        <select class="prescription-medicine" required>
            <option value="">Select Medicine</option>
            ${prescriptionMedicinesList.map(med => `<option value="${med.id}">${med.name}</option>`).join('')}
        </select>
        <input type="number" class="prescription-quantity" placeholder="Qty" min="1" required>
        <input type="text" class="prescription-dosage" placeholder="Dosage (e.g., 2x daily)" required>
        <input type="text" class="prescription-duration" placeholder="Duration (e.g., 7 days)" required>
        <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()">Remove</button>
    `;
    container.appendChild(newRow);
}

async function addPrescription(event) {
    event.preventDefault();
    
    const rows = document.querySelectorAll('.prescription-medicine-row');
    const items = [];
    
    rows.forEach(row => {
        const medicineId = row.querySelector('.prescription-medicine').value;
        const quantity = row.querySelector('.prescription-quantity').value;
        const dosage = row.querySelector('.prescription-dosage').value;
        const duration = row.querySelector('.prescription-duration').value;
        
        if (medicineId) {
            items.push({
                medicine_id: parseInt(medicineId),
                quantity: parseInt(quantity),
                dosage: dosage,
                duration: duration
            });
        }
    });
    
    const data = {
        patient_name: document.getElementById('patientName').value,
        patient_phone: document.getElementById('patientPhone').value,
        doctor_name: document.getElementById('doctorName').value,
        prescription_date: document.getElementById('prescriptionDate').value,
        notes: document.getElementById('prescriptionNotes').value,
        items: items
    };
    
    try {
        const response = await fetch(`${API_URL}/prescriptions`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Prescription created successfully!');
            hideAddPrescriptionForm();
            loadPrescriptions();
        }
    } catch (error) {
        alert('Error creating prescription: ' + error.message);
    }
}

async function loadPrescriptions(status = 'all') {
    try {
        const url = status === 'all' ? `${API_URL}/prescriptions` : `${API_URL}/prescriptions?status=${status}`;
        const response = await fetch(url, { headers: getAuthHeaders() });
        const prescriptions = await response.json();
        
        const grid = document.getElementById('prescriptionsGrid');
        if (prescriptions.length === 0) {
            grid.innerHTML = '<div class="loading">No prescriptions found</div>';
            return;
        }
        
        grid.innerHTML = prescriptions.map(presc => {
            const statusClass = presc.status === 'completed' ? 'status-completed' : 
                               presc.status === 'cancelled' ? 'status-cancelled' : 'status-pending';
            
            return `
                <div class="prescription-card">
                    <div class="prescription-header">
                        <div>
                            <h3>${presc.patient_name}</h3>
                            <p>📞 ${presc.patient_phone}</p>
                        </div>
                        <span class="prescription-status ${statusClass}">${presc.status.toUpperCase()}</span>
                    </div>
                    <div class="prescription-info">
                        <div class="info-row">
                            <span class="info-label">👨‍⚕️ Doctor:</span>
                            <span class="info-value">${presc.doctor_name}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">📅 Date:</span>
                            <span class="info-value">${presc.prescription_date}</span>
                        </div>
                        ${presc.notes ? `
                        <div class="info-row">
                            <span class="info-label">📝 Notes:</span>
                            <span class="info-value">${presc.notes}</span>
                        </div>
                        ` : ''}
                    </div>
                    <div class="prescription-medicines">
                        <h4>Medicines:</h4>
                        ${presc.items.map(item => `
                            <div class="medicine-item">
                                <strong>${item.medicine_name}</strong> - 
                                Qty: ${item.quantity}, 
                                ${item.dosage}, 
                                ${item.duration}
                            </div>
                        `).join('')}
                    </div>
                    <div class="prescription-actions">
                        ${presc.status === 'pending' ? `
                            <button class="btn btn-primary" onclick="updatePrescriptionStatus(${presc.id}, 'completed')">Complete</button>
                            <button class="btn btn-secondary" onclick="updatePrescriptionStatus(${presc.id}, 'cancelled')">Cancel</button>
                        ` : ''}
                        <button class="btn btn-danger" onclick="deletePrescription(${presc.id})">Delete</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading prescriptions:', error);
    }
}

async function updatePrescriptionStatus(id, status) {
    try {
        const response = await fetch(`${API_URL}/prescriptions/${id}/status`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ status })
        });
        
        if (response.ok) {
            alert(`Prescription ${status}!`);
            loadPrescriptions();
        }
    } catch (error) {
        alert('Error updating prescription: ' + error.message);
    }
}

async function deletePrescription(id) {
    if (!confirm('Are you sure you want to delete this prescription?')) return;
    
    try {
        const response = await fetch(`${API_URL}/prescriptions/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
        
        if (response.ok) {
            alert('Prescription deleted successfully!');
            loadPrescriptions();
        }
    } catch (error) {
        alert('Error deleting prescription: ' + error.message);
    }
}

function filterPrescriptions(status) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    loadPrescriptions(status);
}

// Reports functions
async function generateReport() {
    await loadReportSummary();
    await loadTopSellingReport();
    await loadLowStockReport();
    await loadExpiryReport();
}

async function loadReportSummary() {
    try {
        const response = await fetch(`${API_URL}/analytics/summary`, { headers: getAuthHeaders() });
        if (!response.ok) {
            throw new Error(`Analytics summary failed: ${response.status}`);
        }
        const data = await response.json();
        
        console.log('Summary data:', data);
        
        document.getElementById('totalMedicines').textContent = data.total_medicines || 0;
        document.getElementById('lowStockCount').textContent = data.low_stock_count || 0;
        document.getElementById('totalRevenue').textContent = `KSH ${(parseFloat(data.total_revenue) || 0).toFixed(2)}`;
        document.getElementById('todaySales').textContent = data.today_sales_count || 0;
    } catch (error) {
        console.error('Error loading report summary:', error);
    }
}

async function loadTopSellingReport() {
    try {
        // Use sales data instead of non-existent endpoint
        if (!allSalesData || allSalesData.length === 0) return;
        
        const salesByMedicine = {};
        allSalesData.forEach(sale => {
            const name = sale.medicine_name;
            if (!salesByMedicine[name]) {
                salesByMedicine[name] = { units_sold: 0, revenue: 0 };
            }
            salesByMedicine[name].units_sold += sale.quantity;
            salesByMedicine[name].revenue += parseFloat(sale.total_price) || 0;
        });
        
        const data = Object.entries(salesByMedicine)
            .map(([name, stats]) => ({
                medicine_name: name,
                category: 'N/A',
                units_sold: stats.units_sold,
                revenue: stats.revenue
            }))
            .sort((a, b) => b.units_sold - a.units_sold)
            .slice(0, 10);
        
        const tbody = document.getElementById('topSellingBody');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No data available</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.map((item, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${item.medicine_name}</td>
                <td>${item.category}</td>
                <td>${item.units_sold}</td>
                <td>KSH ${(parseFloat(item.revenue) || 0).toFixed(2)}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading top selling report:', error);
    }
}

async function loadLowStockReport() {
    try {
        // Use medicines data instead
        const response = await fetch(`${API_URL}/medicines`, { headers: getAuthHeaders() });
        if (!response.ok) return;
        const medicines = await response.json();
        const data = medicines.filter(m => m.quantity <= m.reorder_level);
        
        const tbody = document.getElementById('lowStockBody');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">No low stock items</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.map(item => {
            const status = item.quantity === 0 ? 'Out of Stock' : item.quantity < item.reorder_level / 2 ? 'Critical' : 'Low';
            const statusClass = status === 'Critical' || status === 'Out of Stock' ? 'status-critical' : 'status-low';
            return `
                <tr>
                    <td>${item.name}</td>
                    <td class="status-low">${item.quantity}</td>
                    <td>${item.reorder_level}</td>
                    <td><span class="status-badge ${statusClass}">${status}</span></td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading low stock report:', error);
    }
}

async function loadExpiryReport() {
    try {
        // Use medicines data instead
        const response = await fetch(`${API_URL}/medicines`, { headers: getAuthHeaders() });
        if (!response.ok) return;
        const medicines = await response.json();
        
        const today = new Date();
        const ninetyDaysFromNow = new Date(today.getTime() + 90 * 24 * 60 * 60 * 1000);
        
        const data = medicines
            .filter(m => {
                const expiryDate = new Date(m.expiry_date);
                return expiryDate <= ninetyDaysFromNow;
            })
            .map(m => ({
                medicine_name: m.name,
                quantity: m.quantity,
                expiry_date: m.expiry_date,
                days_until_expiry: Math.floor((new Date(m.expiry_date) - today) / (1000 * 60 * 60 * 24))
            }))
            .sort((a, b) => a.days_until_expiry - b.days_until_expiry);
        
        const tbody = document.getElementById('expiryBody');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">No medicines expiring soon</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.map(item => {
            const daysClass = item.days_until_expiry < 30 ? 'status-critical' : item.days_until_expiry < 60 ? 'status-low' : '';
            return `
                <tr>
                    <td>${item.medicine_name}</td>
                    <td>${item.quantity}</td>
                    <td>${item.expiry_date}</td>
                    <td class="${daysClass}">${item.days_until_expiry} days</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading expiry report:', error);
    }
}

function downloadReport() {
    alert('PDF download feature would be implemented here using a library like jsPDF or server-side PDF generation.');
}


// Reports functions
let allSalesData = [];

async function loadReports() {
    console.log('Loading reports...');
    try {
        const response = await fetch(`${API_URL}/sales`, { headers: getAuthHeaders() });
        if (!response.ok) {
            throw new Error(`Sales API failed: ${response.status}`);
        }
        allSalesData = await response.json();
        console.log(`Loaded ${allSalesData.length} sales records`);
        
        // Load all report sections
        await loadReportSummary();
        await loadTopSellingReport();
        await loadLowStockReport();
        await loadExpiryReport();
        
        // Display reports and stats
        displayReports(allSalesData);
        updateStats(allSalesData);
        
        console.log('Reports loaded successfully!');
    } catch (error) {
        console.error('Error loading reports:', error);
        alert('Error loading reports: ' + error.message);
    }
}

function displayReports(sales) {
    const tbody = document.getElementById('reportsTableBody');
    
    if (!tbody) {
        console.error('reportsTableBody element not found!');
        return;
    }
    
    if (!sales || sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No sales found</td></tr>';
        return;
    }
    
    try {
        tbody.innerHTML = sales.map(sale => {
            const method = sale.payment_method || 'cash';
            let paymentBadge = '';
            
            if (method === 'cash') {
                paymentBadge = '<span class="payment-badge payment-cash">💵 Cash</span>';
            } else if (method === 'bank') {
                paymentBadge = '<span class="payment-badge payment-bank">🏦 Bank</span>';
            } else if (method === 'mpesa') {
                paymentBadge = '<span class="payment-badge payment-mpesa">📱 M-Pesa</span>';
            }
            
            return `
                <tr>
                    <td>${sale.medicine_name || 'Unknown'}</td>
                    <td style="text-align: center;">${sale.quantity || 0}</td>
                    <td style="text-align: right;">KSH ${(parseFloat(sale.total_price) || 0).toFixed(2)}</td>
                    <td style="text-align: center;">${paymentBadge}</td>
                    <td style="text-align: center;">${sale.sale_date || 'N/A'}</td>
                </tr>
            `;
        }).join('');
        console.log(`Displayed ${sales.length} sales in reports table`);
    } catch (error) {
        console.error('Error displaying reports:', error);
        tbody.innerHTML = `<tr><td colspan="5">Error displaying reports: ${error.message}</td></tr>`;
    }
}

function updateStats(sales) {
    const totalSales = sales.length;
    const totalRevenue = sales.reduce((sum, sale) => sum + sale.total_price, 0);
    const cashSales = sales.filter(s => (s.payment_method || 'cash') === 'cash').reduce((sum, s) => sum + s.total_price, 0);
    const bankSales = sales.filter(s => s.payment_method === 'bank').reduce((sum, s) => sum + s.total_price, 0);
    const mpesaSales = sales.filter(s => s.payment_method === 'mpesa').reduce((sum, s) => sum + s.total_price, 0);
    
    document.getElementById('totalSalesCount').textContent = totalSales;
    document.getElementById('totalRevenue').textContent = `KSH ${totalRevenue.toFixed(2)}`;
    document.getElementById('cashSales').textContent = `KSH ${cashSales.toFixed(2)}`;
    document.getElementById('bankSales').textContent = `KSH ${bankSales.toFixed(2)}`;
    document.getElementById('mpesaSales').textContent = `KSH ${mpesaSales.toFixed(2)}`;
}

function filterReports() {
    const searchText = document.getElementById('searchMedicine').value.toLowerCase();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const paymentFilter = document.getElementById('filterPayment').value;
    
    let filtered = allSalesData.filter(sale => {
        const matchesSearch = !searchText || sale.medicine_name.toLowerCase().includes(searchText);
        const matchesStartDate = !startDate || sale.sale_date >= startDate;
        const matchesEndDate = !endDate || sale.sale_date <= endDate;
        const matchesPayment = !paymentFilter || (sale.payment_method || 'cash') === paymentFilter;
        
        return matchesSearch && matchesStartDate && matchesEndDate && matchesPayment;
    });
    
    displayReports(filtered);
    updateStats(filtered);
}

function clearFilters() {
    document.getElementById('searchMedicine').value = '';
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('filterPayment').value = '';
    displayReports(allSalesData);
    updateStats(allSalesData);
}

function downloadPDF() {
    try {
        console.log('downloadPDF called');
        console.log('allSalesData:', allSalesData);
        
        if (!window.jspdf) {
            alert('jsPDF library not loaded. Please refresh the page.');
            return;
        }
        
        if (!allSalesData || allSalesData.length === 0) {
            alert('No sales data available. Please wait for data to load or record some sales first.');
            return;
        }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
    
    // Get filtered data
    const searchText = document.getElementById('searchMedicine').value.toLowerCase();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const paymentFilter = document.getElementById('filterPayment').value;
    
    let filtered = allSalesData.filter(sale => {
        const matchesSearch = !searchText || sale.medicine_name.toLowerCase().includes(searchText);
        const matchesStartDate = !startDate || sale.sale_date >= startDate;
        const matchesEndDate = !endDate || sale.sale_date <= endDate;
        const matchesPayment = !paymentFilter || (sale.payment_method || 'cash') === paymentFilter;
        return matchesSearch && matchesStartDate && matchesEndDate && matchesPayment;
    });
    
    // Title
    doc.setFontSize(18);
    doc.text('Sales Report', 14, 20);
    
    // Date range
    doc.setFontSize(10);
    const dateRange = startDate && endDate ? `${startDate} to ${endDate}` : 'All Time';
    doc.text(`Period: ${dateRange}`, 14, 28);
    
    // Stats
    const totalRevenue = filtered.reduce((sum, sale) => sum + sale.total_price, 0);
    doc.text(`Total Sales: ${filtered.length}`, 14, 35);
    doc.text(`Total Revenue: KSH ${totalRevenue.toFixed(2)}`, 14, 42);
    
    // Table
    const tableData = filtered.map(sale => [
        String(sale.medicine_name || ''),
        String(sale.quantity || 0),
        `KSH ${(sale.total_price || 0).toFixed(2)}`,
        String((sale.payment_method || 'cash')).toUpperCase(),
        String(sale.sale_date || '')
    ]);
    
    doc.autoTable({
        startY: 50,
        head: [['Medicine', 'Qty', 'Price', 'Payment', 'Date']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [102, 126, 234] }
    });
    
    // Save
    const filename = `sales_report_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
    console.log('PDF saved successfully');
    } catch (error) {
        console.error('PDF generation error:', error);
        alert('Error generating PDF: ' + error.message);
    }
}



function downloadExcel() {
    try {
        console.log('downloadExcel called');
        console.log('allSalesData:', allSalesData);
        
        if (typeof XLSX === 'undefined') {
            alert('XLSX library not loaded. Please refresh the page.');
            return;
        }
        
        if (!allSalesData || allSalesData.length === 0) {
            alert('No sales data available. Please wait for data to load or record some sales first.');
            return;
        }
    
    // Get filtered data
    const searchText = document.getElementById('searchMedicine').value.toLowerCase();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const paymentFilter = document.getElementById('filterPayment').value;
    
    let filtered = allSalesData.filter(sale => {
        const matchesSearch = !searchText || sale.medicine_name.toLowerCase().includes(searchText);
        const matchesStartDate = !startDate || sale.sale_date >= startDate;
        const matchesEndDate = !endDate || sale.sale_date <= endDate;
        const matchesPayment = !paymentFilter || (sale.payment_method || 'cash') === paymentFilter;
        return matchesSearch && matchesStartDate && matchesEndDate && matchesPayment;
    });
    
    // Calculate statistics
    const totalRevenue = filtered.reduce((sum, sale) => sum + sale.total_price, 0);
    const cashSales = filtered.filter(s => (s.payment_method || 'cash') === 'cash').reduce((sum, s) => sum + s.total_price, 0);
    const bankSales = filtered.filter(s => s.payment_method === 'bank').reduce((sum, s) => sum + s.total_price, 0);
    const mpesaSales = filtered.filter(s => s.payment_method === 'mpesa').reduce((sum, s) => sum + s.total_price, 0);
    
    // Create workbook
    const wb = XLSX.utils.book_new();
    
    // Summary sheet
    const summaryData = [
        ['Sales Report Summary'],
        [''],
        ['Period:', startDate && endDate ? `${startDate} to ${endDate}` : 'All Time'],
        ['Generated:', new Date().toLocaleString()],
        [''],
        ['Statistics'],
        ['Total Sales:', filtered.length],
        ['Total Revenue:', `KSH ${totalRevenue.toFixed(2)}`],
        ['Cash Sales:', `KSH ${cashSales.toFixed(2)}`],
        ['Bank Sales:', `KSH ${bankSales.toFixed(2)}`],
        ['M-Pesa Sales:', `KSH ${mpesaSales.toFixed(2)}`]
    ];
    
    const wsSummary = XLSX.utils.aoa_to_sheet(summaryData);
    XLSX.utils.book_append_sheet(wb, wsSummary, 'Summary');
    
    // Sales data sheet
    const salesData = [
        ['Medicine', 'Quantity', 'Price (KSH)', 'Payment Method', 'Date & Time']
    ];
    
    filtered.forEach(sale => {
        salesData.push([
            sale.medicine_name,
            sale.quantity,
            (parseFloat(sale.total_price) || 0).toFixed(2),
            (sale.payment_method || 'cash').toUpperCase(),
            sale.sale_date
        ]);
    });
    
    const wsSales = XLSX.utils.aoa_to_sheet(salesData);
    
    // Set column widths
    wsSales['!cols'] = [
        { wch: 30 }, // Medicine
        { wch: 10 }, // Quantity
        { wch: 15 }, // Price
        { wch: 15 }, // Payment
        { wch: 20 }  // Date
    ];
    
    XLSX.utils.book_append_sheet(wb, wsSales, 'Sales Data');
    
    // Download
    const filename = `sales_report_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, filename);
    console.log('Excel saved successfully');
    } catch (error) {
        console.error('Excel generation error:', error);
        alert('Error generating Excel: ' + error.message);
    }
}


// User Management functions
function showAddUserForm() {
    document.getElementById('addUserForm').style.display = 'block';
}

function hideAddUserForm() {
    document.getElementById('addUserForm').style.display = 'none';
    document.querySelector('#addUserForm form').reset();
}

async function addUser(event) {
    event.preventDefault();
    
    const data = {
        username: document.getElementById('newUsername').value,
        full_name: document.getElementById('newFullName').value,
        email: document.getElementById('newEmail').value,
        password: document.getElementById('newPassword').value,
        role: document.getElementById('newRole').value
    };
    
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('User added successfully!');
            hideAddUserForm();
            loadUsers();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error adding user: ' + error.message);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_URL}/users`, { headers: getAuthHeaders() });
        const users = await response.json();
        
        const tbody = document.getElementById('usersTableBody');
        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No users found</td></tr>';
            return;
        }
        
        tbody.innerHTML = users.map(user => {
            const roleClass = user.role === 'admin' ? 'status-ok' : '';
            
            return `
                <tr>
                    <td>${user.username}</td>
                    <td>${user.full_name || '-'}</td>
                    <td>${user.email}</td>
                    <td class="${roleClass}">${user.role.toUpperCase()}</td>
                    <td>${user.created_date || '-'}</td>
                    <td>${user.last_login || 'Never'}</td>
                    <td>
                        <button class="btn btn-danger" onclick="deleteUser(${user.id}, '${user.username}')">Delete</button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

async function deleteUser(id, username) {
    if (username === 'admin') {
        alert('Cannot delete admin user!');
        return;
    }
    
    if (!confirm(`Are you sure you want to delete user: ${username}?`)) return;
    
    try {
        const response = await fetch(`${API_URL}/users/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
        
        if (response.ok) {
            alert('User deleted successfully!');
            loadUsers();
        }
    } catch (error) {
        alert('Error deleting user: ' + error.message);
    }
}

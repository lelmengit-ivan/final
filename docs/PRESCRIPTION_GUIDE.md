# Prescription Management Guide

## ✅ Prescription Endpoints Now Available!

The prescription management system is now fully functional with all CRUD operations.

---

## 📋 API Endpoints

### 1. Get All Prescriptions
**GET** `/api/prescriptions`

**Optional Query Parameters:**
- `status` - Filter by status (pending, completed, cancelled, all)

**Example:**
```bash
GET /api/prescriptions?status=pending
```

**Response:**
```json
[
  {
    "id": 1,
    "patient_name": "John Doe",
    "patient_phone": "+1-555-0123",
    "doctor_name": "Dr. Smith",
    "prescription_date": "2025-11-12",
    "status": "pending",
    "notes": "Take after meals",
    "created_date": "2025-11-12 10:30:00",
    "items": [
      {
        "medicine_id": 1,
        "medicine_name": "Paracetamol 500mg",
        "quantity": 20,
        "dosage": "1 tablet",
        "duration": "5 days"
      }
    ]
  }
]
```

### 2. Create Prescription
**POST** `/api/prescriptions`

**Request Body:**
```json
{
  "patient_name": "John Doe",
  "patient_phone": "+1-555-0123",
  "doctor_name": "Dr. Smith",
  "prescription_date": "2025-11-12",
  "notes": "Take after meals",
  "items": [
    {
      "medicine_id": 1,
      "quantity": 20,
      "dosage": "1 tablet twice daily",
      "duration": "10 days"
    },
    {
      "medicine_id": 3,
      "quantity": 15,
      "dosage": "1 capsule",
      "duration": "7 days"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "message": "Prescription created successfully"
}
```

### 3. Update Prescription Status
**PUT** `/api/prescriptions/{id}/status`

**Request Body:**
```json
{
  "status": "completed"
}
```

**Status Options:**
- `pending` - Prescription created, not yet dispensed
- `completed` - Medicines dispensed, inventory updated
- `cancelled` - Prescription cancelled

**Response:**
```json
{
  "message": "Prescription status updated"
}
```

**Note:** When status is changed to `completed`, the system automatically:
- Deducts medicine quantities from inventory
- Updates stock levels

### 4. Delete Prescription
**DELETE** `/api/prescriptions/{id}`

**Response:**
```json
{
  "message": "Prescription deleted successfully"
}
```

---

## 🔧 Testing with cURL

### Get All Prescriptions
```bash
curl http://localhost:5000/api/prescriptions
```

### Get Pending Prescriptions
```bash
curl http://localhost:5000/api/prescriptions?status=pending
```

### Create Prescription
```bash
curl -X POST http://localhost:5000/api/prescriptions \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "patient_phone": "+1-555-0123",
    "doctor_name": "Dr. Smith",
    "prescription_date": "2025-11-12",
    "notes": "Take after meals",
    "items": [
      {
        "medicine_id": 1,
        "quantity": 20,
        "dosage": "1 tablet twice daily",
        "duration": "10 days"
      }
    ]
  }'
```

### Update Status to Completed
```bash
curl -X PUT http://localhost:5000/api/prescriptions/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete Prescription
```bash
curl -X DELETE http://localhost:5000/api/prescriptions/1
```

---

## 💻 JavaScript Example

### Fetch All Prescriptions
```javascript
async function getPrescriptions() {
    const response = await fetch('http://localhost:5000/api/prescriptions');
    const prescriptions = await response.json();
    console.log(prescriptions);
}
```

### Create Prescription
```javascript
async function createPrescription() {
    const data = {
        patient_name: "John Doe",
        patient_phone: "+1-555-0123",
        doctor_name: "Dr. Smith",
        prescription_date: "2025-11-12",
        notes: "Take after meals",
        items: [
            {
                medicine_id: 1,
                quantity: 20,
                dosage: "1 tablet twice daily",
                duration: "10 days"
            }
        ]
    };
    
    const response = await fetch('http://localhost:5000/api/prescriptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    console.log(result);
}
```

### Update Status
```javascript
async function completePrescription(id) {
    const response = await fetch(`http://localhost:5000/api/prescriptions/${id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'completed' })
    });
    
    const result = await response.json();
    console.log(result);
}
```

---

## 📊 Database Schema

### Prescriptions Table
```sql
CREATE TABLE prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    patient_phone TEXT,
    doctor_name TEXT NOT NULL,
    prescription_date TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    notes TEXT,
    created_date TEXT
);
```

### Prescription Items Table
```sql
CREATE TABLE prescription_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER,
    medicine_id INTEGER,
    quantity INTEGER,
    dosage TEXT,
    duration TEXT,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions (id),
    FOREIGN KEY (medicine_id) REFERENCES medicines (id)
);
```

---

## 🎯 Use Cases

### 1. Doctor Creates Prescription
1. Doctor examines patient
2. Creates prescription with multiple medicines
3. System stores prescription as "pending"
4. Patient takes prescription to pharmacy

### 2. Pharmacist Dispenses Medicine
1. Pharmacist receives prescription
2. Checks medicine availability
3. Prepares medicines
4. Updates prescription status to "completed"
5. System automatically deducts from inventory

### 3. Prescription Tracking
1. View all pending prescriptions
2. Filter by status
3. Track which prescriptions are completed
4. Monitor medicine usage

---

## ⚠️ Important Notes

### Inventory Management
- When prescription status changes to `completed`:
  - Medicine quantities are automatically deducted
  - Stock levels are updated
  - Low stock alerts may trigger

### Validation
- Patient name is required
- Doctor name is required
- Prescription date is required
- At least one medicine item is required
- Medicine must exist in inventory

### Status Workflow
```
pending → completed (inventory updated)
pending → cancelled (no inventory change)
```

---

## 🔍 Example Workflow

### Step 1: Create Prescription
```json
POST /api/prescriptions
{
  "patient_name": "Jane Smith",
  "patient_phone": "+1-555-9876",
  "doctor_name": "Dr. Johnson",
  "prescription_date": "2025-11-12",
  "notes": "Take with food",
  "items": [
    {
      "medicine_id": 1,
      "quantity": 30,
      "dosage": "1 tablet twice daily",
      "duration": "15 days"
    },
    {
      "medicine_id": 4,
      "quantity": 10,
      "dosage": "1 tablet once daily",
      "duration": "10 days"
    }
  ]
}
```

### Step 2: View Prescription
```bash
GET /api/prescriptions/1
```

### Step 3: Complete Prescription
```json
PUT /api/prescriptions/1/status
{
  "status": "completed"
}
```

Result:
- Paracetamol stock: 150 → 120 (30 deducted)
- Cetirizine stock: 200 → 190 (10 deducted)

---

## 🐛 Troubleshooting

### "Medicine not found"
- Check if medicine_id exists in medicines table
- Verify medicine hasn't been deleted

### "Insufficient stock"
- Check current medicine quantity
- Reduce prescription quantity
- Reorder medicine first

### Prescription not updating
- Check prescription ID is correct
- Verify status value is valid
- Check server logs for errors

---

## 📈 Future Enhancements

- [ ] Prescription history per patient
- [ ] Doctor authentication
- [ ] E-prescription support
- [ ] Prescription refills
- [ ] Insurance integration
- [ ] Barcode scanning
- [ ] PDF generation
- [ ] Email notifications
- [ ] Prescription analytics

---

## ✅ Testing Checklist

- [ ] Create prescription with single medicine
- [ ] Create prescription with multiple medicines
- [ ] View all prescriptions
- [ ] Filter by status (pending)
- [ ] Filter by status (completed)
- [ ] Update status to completed
- [ ] Verify inventory updated
- [ ] Update status to cancelled
- [ ] Delete prescription
- [ ] Check error handling

---

**Prescription management is now fully functional! 🎉**

**Test it at: http://localhost:5000/api/prescriptions**

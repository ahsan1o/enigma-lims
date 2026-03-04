# Kotli LIMS - Architecture & Design Document

## 🏥 System Overview

**Kotli Clinical Laboratory LIMS** - A modern, offline-capable Laboratory Information Management System designed specifically for Kotli's clinical labs.

```
┌─────────────────────────────────────────────────────┐
│    PyQt6 Desktop Application (Modern UI/UX)         │
│  ┌──────────────────────────────────────────────┐   │
│  │ • Sample Registration & Tracking             │   │
│  │ • Test Order Management                      │   │
│  │ • Machine Data Integration                   │   │
│  │ • Results Entry & Validation                 │   │
│  │ • Supervisor Approval Workflow               │   │
│  │ • Report Generation (PDF)                    │   │
│  │ • Dashboard & Analytics                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────┬──────────────────────────────────┘
                  │ Local HTTP
                  ↓
┌─────────────────────────────────────────────────────┐
│   FastAPI Backend (Local Server)                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ • REST API endpoints (JSON)                  │   │
│  │ • Business logic & validation                │   │
│  │ • Barcode generation                         │   │
│  │ • Machine data receiver                      │   │
│  │ • Report engine                              │   │
│  │ • Offline sync engine                        │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────┬──────────────────────────────────┘
                  │ Local I/O
                  ↓
┌─────────────────────────────────────────────────────┐
│    SQLite Database (Local File)                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ • Samples, Tests, Results                    │   │
│  │ • Patients, Doctors, Users                   │   │
│  │ • Audit Logs, Timestamps                     │   │
│  │ • Instruments, Calibration                   │   │
│  │ • Sync queue (for cloud backup)              │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features (MVP)

### **MUST HAVE (Tier 1)**
- ✅ Sample Registration with barcode generation
- ✅ Patient & Doctor management
- ✅ Test order workflow
- ✅ Machine data import (JSON/CSV)
- ✅ Results entry with validation
- ✅ Reference ranges (age/gender-specific)
- ✅ Supervisor approval workflow
- ✅ PDF report generation
- ✅ Audit trail (who, what, when)
- ✅ User authentication & roles (Admin, Tech, Supervisor, Doctor view)
- ✅ **OFFLINE MODE** (works without internet)
- ✅ QC validation before approval

### **NICE TO HAVE (Tier 2)**
- 📊 Dashboard with metrics
- 🔔 Notifications (results ready, delays)
- 📱 Sample batch management
- 🔗 Critical value alerts
- ☁️ Cloud sync when internet available
- 💾 Automatic backup to USB
- 📄 Customizable reports

---

## 🗄️ Database Schema

### **Core Tables**

```sql
-- PATIENTS
patients:
  id (PK)
  name
  age
  gender
  phone
  doctor_id (FK)
  created_at
  
-- DOCTORS
doctors:
  id (PK)
  name
  registration_number
  phone
  clinic_name
  
-- SAMPLES
samples:
  id (PK)
  sample_id (BARCODE - unique)
  patient_id (FK)
  sample_type (blood, urine, etc)
  collection_date
  collection_time
  received_date
  status (pending, testing, completed, approved)
  
-- TESTS
tests:
  id (PK)
  test_id
  test_name
  unit
  reference_min
  reference_max
  method
  machine_id
  
-- ORDERS
orders:
  id (PK)
  sample_id (FK)
  test_id (FK)
  doctor_id (FK)
  status (pending, in_progress, completed)
  
-- RESULTS
results:
  id (PK)
  order_id (FK)
  test_id (FK)
  result_value
  unit
  status (normal, abnormal, critical)
  qc_passed (boolean)
  entered_by (tech_id)
  entered_date
  approved_by (supervisor_id)
  approved_date
  
-- USERS
users:
  id (PK)
  username (unique)
  password (hashed)
  full_name
  role (admin, technician, supervisor, doctor)
  email
  phone
  
-- AUDIT_LOG
audit_log:
  id (PK)
  user_id (FK)
  action (registered_sample, entered_result, approved_result)
  table_name
  record_id
  old_value
  new_value
  timestamp
  
-- INSTRUMENTS
instruments:
  id (PK)
  instrument_id
  instrument_name (machine make/model)
  location
  last_calibration
  next_calibration
  status (active, inactive, maintenance)
  
-- SYNC_QUEUE (for cloud backup)
sync_queue:
  id (PK)
  entity_type (sample, result, etc)
  entity_id
  action (create, update, delete)
  data (JSON)
  synced (boolean)
  synced_at
```

---

## 🔌 Machine Integration Points

### **Receiving Machine Data**

**Endpoint:** `POST /api/machine/results`

**Machine sends:**
```json
{
  "machine_id": "HAM-001",
  "timestamp": "2026-03-04T10:35:00",
  "sample_id": "LAB-2026-00145",
  "results": [
    {
      "test_id": "WBC",
      "test_name": "White Blood Cells",
      "value": 7.2,
      "unit": "10^9/L",
      "reference_min": 4.5,
      "reference_max": 11.0
    }
  ],
  "qc_status": "PASSED"
}
```

**LIMS processes:**
1. Validates format
2. Matches to sample_id
3. Gets reference ranges
4. Checks QC
5. Stores in database
6. Notifies supervisor

---

## 🎨 UI/UX Design Principles

### **Clean, Modern Design**
- Dark theme (easy on eyes for lab technicians)
- Large, readable fonts
- High contrast buttons
- Minimal clicks to complete tasks
- Keyboard shortcuts for speed

### **Key UI Modules**

1. **Dashboard Home**
   - Quick stats (pending samples, approved today)
   - Recent activity
   - Alerts (critical values)

2. **Sample Registration**
   - Patient info form
   - Barcode auto-generation
   - Print label immediately
   - Quick lookup if returning patient

3. **Test Orders**
   - Select tests to ordere
   - Doctor assignment
   - Priority flags
   - Batch operations

4. **Machine Integration**
   - Waiting for data...
   - Receive results automatically
   - Show import progress
   - Error handling

5. **Results Entry**
   - Machine auto-filled (when from machine)
   - Manual entry form (if needed)
   - Real-time validation
   - Reference range highlighting

6. **Approval Workflow**
   - Supervisor review panel
   - Flag abnormal results
   - Approve/Reject with comments
   - Bulk operations

7. **Reports**
   - PDF generation
   - Email to doctor
   - Patient summary report
   - Doctor summary (all patients)

8. **Settings**
   - User management
   - Lab configuration
   - Instrument setup
   - Reference ranges
   - Backup/Sync settings

---

## 🔐 Security & Data Integrity

### **Authentication**
- Username & password (hashed with bcrypt)
- Session tokens
- Auto-logout after 30 minutes inactivity

### **Authorization**
- Role-based access control (Admin, Tech, Supervisor, Doctor)
- Admin: Full access
- Technician: Sample + results entry
- Supervisor: Reviews & approvals
- Doctor: View-only (their patients)

### **Data Integrity**
- All changes logged in audit_log
- Timestamps on all records
- Supervisor approval required for final results
- No deletion (soft delete with reason)
- Encryption of sensitive data (patient info, results)

### **Offline Security**
- Database encrypted (SQLCipher)
- Local authentication
- Sync only over HTTPS (when connected)

---

## 💾 Offline Sync Strategy

### **When Internet Down**
- ✅ App works normally (all local)
- ✅ All data in SQLite
- ✅ No internet required

### **When Internet Returns**
1. Detect connection
2. Queue pending syncs
3. Upload samples & results to central server
4. Sync back any reference range updates
5. Resolve conflicts (last-write-wins)
6. Archive local backup
7. Continue working

### **Sync Queue Tracking**
```
sync_queue table:
├─ entity_type: "sample" | "result" | "user"
├─ action: "create" | "update" | "delete"
├─ data: {full JSON}
├─ synced: false → true
└─ synced_at: timestamp
```

---

## 📦 Project Structure

```
kotli-lims/
├── backend/                      # FastAPI backend
│   ├── app.py                    # Main app
│   ├── config.py                 # Settings
│   ├── database.py               # SQLite setup
│   ├── models.py                 # SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas
│   ├── api/
│   │   ├── samples.py           # Sample endpoints
│   │   ├── tests.py             # Test endpoints
│   │   ├── results.py           # Results endpoints
│   │   ├── users.py             # User management
│   │   ├── machines.py          # Machine integration
│   │   ├── reports.py           # Reporting
│   │   └── sync.py              # Offline sync
│   ├── services/
│   │   ├── barcode_service.py   # Barcode generation
│   │   ├── report_service.py    # PDF generation
│   │   ├── sync_service.py      # Sync logic
│   │   └── validation_service.py # Data validation
│   ├── utils/
│   │   ├── auth.py              # Authentication
│   │   ├── logger.py            # Logging
│   │   └── helpers.py           # Utilities
│   ├── migrations/              # Database migrations
│   ├── tests/                   # Unit tests
│   └── requirements.txt
│
├── frontend/                     # PyQt6 desktop app
│   ├── main.py                  # Entry point
│   ├── config.py                # UI settings
│   ├── styles.css               # Qt stylesheet
│   ├── ui/
│   │   ├── main_window.py       # Main window
│   │   ├── dashboard.py         # Dashboard screen
│   │   ├── sample_registration.py
│   │   ├── test_orders.py
│   │   ├── results_entry.py
│   │   ├── approval_panel.py
│   │   ├── reports.py
│   │   ├── settings.py
│   │   └── dialogs.py           # Dialogs/modals
│   ├── widgets/
│   │   ├── tables.py            # Custom table widget
│   │   ├── forms.py             # Reusable forms
│   │   ├── buttons.py           # Custom buttons
│   │   └── indicators.py        # Status indicators
│   ├── api_client.py            # HTTP calls to backend
│   ├── utils/
│   │   ├── validators.py        # Input validation
│   │   ├── formatters.py        # Data formatting
│   │   └── printers.py          # Barcode printer
│   └── resources/
│       ├── icons/               # Icons
│       ├── fonts/               # Custom fonts
│       └── images/              # Images
│
├── docs/
│   ├── ARCHITECTURE.md          # This file
│   ├── API_DOCS.md              # API endpoints
│   ├── USER_GUIDE.md            # User manual
│   ├── DEPLOYMENT.md            # Setup instructions
│   └── DATABASE_SCHEMA.md       # Full DB design
│
├── README.md
├── docker-compose.yml           # Optional Docker setup
├── requirements.txt             # All dependencies
└── .env.example                 # Environment template
```

---

## 🚀 Deployment Strategy

### **Single Lab (Kotli)**
```
1. Install Python 3.11+
2. Install dependencies
3. Run backend: python backend/app.py
4. Run frontend: python frontend/main.py
5. Create SQLite database (auto-created)
6. Login (default: admin/admin)
7. Configure machines
```

### **Multiple Labs (Future)**
```
1. Central PostgreSQL server (for backups)
2. Each lab has local SQLite + FastAPI
3. Sync via HTTPS when internet available
4. Central dashboard monitors all labs
5. Data never lost (redundant backup)
```

---

## 📊 Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Desktop UI | PyQt6 | Modern, native, fast |
| Backend API | FastAPI | Python, async, auto-docs |
| Database | SQLite (local) | No server needed, offline |
| Encryption | SQLCipher | Encrypted local DB |
| Reports | ReportLab/FPDF | PDF generation |
| Barcodes | python-barcode | Code128, QR support |
| Auth | JWT/bcrypt | Secure |
| Logger | Python logging | Built-in |
| UI Theme | Modern dark theme | Easy on eyes |

---

## 🔄 User Workflows

### **Sample Registration Workflow**
```
1. Receptionist enters patient info
2. Select doctor
3. Select tests
4. System generates barcode: LAB-2026-00145
5. Print label
6. Stick on sample tube
7. Sample sent to lab
8. Done!
```

### **Results Workflow**
```
1. Machine receives sample (scans barcode)
2. Analyzes automatically
3. Sends results to LIMS
4. LIMS validates QC
5. Technician verifies (if manual entry needed)
6. Supervisor reviews
7. Supervisor approves
8. Doctor notified
9. Patient notified
10. Report archived
```

### **Offline Scenario**
```
1. Internet down
2. Lab continues normally (all local)
3. Samples registered locally
4. Machine results stored locally
5. Results approved locally
6. Reports generated locally
7. Internet back
8. Auto-sync to cloud backup
9. Continue
```

---

## ✅ Success Metrics

- ✅ Sample registration: < 2 minutes
- ✅ Results approval: < 5 minutes
- ✅ Report generation: < 1 minute
- ✅ 99.9% uptime (offline capable)
- ✅ Zero data loss
- ✅ Full audit trail
- ✅ User training < 1 hour

---

## 📝 Implementation Phases

**Phase 1 (Week 1-2):** Backend + Database
- FastAPI setup
- SQLite schema
- Core API endpoints
- Authentication

**Phase 2 (Week 3-4):** Frontend UI
- PyQt6 dashboard
- Sample registration
- Test orders
- Results entry

**Phase 3 (Week 5-6):** Integration
- Machine data receiver
- Approval workflow
- Report generation

**Phase 4 (Week 7-8):** Polish & Deploy
- Testing
- UI/UX refinement
- Documentation
- Deployment to lab

---

**This is our roadmap. Let's build it! 🚀**

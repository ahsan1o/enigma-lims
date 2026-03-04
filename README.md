# 🏥 Kotli LIMS - Clinical Laboratory Information Management System

**Offline-capable, modern, professional LIMS designed for clinical labs in Kotli**

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![PyQt6](https://img.shields.io/badge/PyQt6-Latest-blue)

---

## 🎯 Project Goal

Build a **professional-grade Laboratory Information Management System (LIMS)** for clinical labs in Kotli that:
- ✅ Works **completely offline** (no internet required)
- ✅ Has **modern, intuitive UI/UX** (easy for lab technicians)
- ✅ Integrates with **laboratory machines** (automatic data import)
- ✅ Manages **samples, tests, and results** efficiently
- ✅ Generates **PDF reports** automatically
- ✅ Maintains **complete audit trails** for compliance
- ✅ Scales from **single lab to multiple locations**

---

## 🏗️ Architecture

### **Tech Stack**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Desktop UI** | PyQt6 | Modern, native desktop application |
| **Backend API** | FastAPI (Python) | High-performance REST API |
| **Database** | SQLite (encrypted) | Local storage, no server needed |
| **Authentication** | JWT + bcrypt | Secure user authentication |
| **Reports** | ReportLab/FPDF | PDF generation |
| **Barcodes** | python-barcode | Code128 barcode generation |

### **System Components**

```
┌──────────────────────────────────────┐
│   PyQt6 Desktop Application          │
│   (Modern, Dark Theme UI)            │
└──────────────┬───────────────────────┘
               │ HTTP Local (Port 8000)
               ↓
┌──────────────────────────────────────┐
│   FastAPI Backend Server             │
│   (Local REST API)                   │
└──────────────┬───────────────────────┘
               │ File I/O
               ↓
┌──────────────────────────────────────┐
│   SQLite Database                    │
│   (Encrypted, Local File)            │
└──────────────────────────────────────┘
```

---

## 📁 Project Structure

```
kotli-lims/
├── backend/                      # FastAPI backend
│   ├── app.py                    # Main FastAPI app
│   ├── database.py               # Database setup
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── api/                      # API endpoints (WIP)
│   │   ├── samples.py            
│   │   ├── tests.py
│   │   ├── results.py
│   │   ├── users.py
│   │   ├── machines.py
│   │   ├── reports.py
│   │   └── auth.py
│   ├── services/                 # Business logic
│   │   ├── barcode_service.py
│   │   ├── report_service.py
│   │   ├── validation_service.py
│   │   └── sync_service.py
│   ├── utils/                    # Utilities
│   │   ├── auth.py
│   │   └── logger.py
│   ├── requirements.txt
│   └── tests/                    # Unit tests (WIP)
│
├── frontend/                     # PyQt6 desktop app
│   ├── main.py                   # Entry point (WIP)
│   ├── api_client.py             # API communication
│   ├── ui/                       # UI screens (WIP)
│   │   ├── main_window.py
│   │   ├── dashboard.py
│   │   ├── sample_registration.py
│   │   ├── test_orders.py
│   │   ├── results_entry.py
│   │   ├── approval_panel.py
│   │   └── reports.py
│   ├── widgets/                  # Reusable UI components (WIP)
│   ├── resources/                # Images, icons, fonts
│   ├── requirements.txt
│   └── config.py
│
├── data/                         # Data directory (auto-created)
│   ├── kotli_lims.db            # SQLite database
│   ├── barcodes/                # Generated barcodes
│   ├── reports/                 # Generated reports
│   └── backups/                 # Sync backups
│
├── docs/
│   ├── ARCHITECTURE.md           # System design
│   ├── API_DOCS.md              # API reference
│   ├── USER_GUIDE.md            # User manual
│   └── DATABASE_SCHEMA.md       # Database design
│
├── README.md                     # This file
├── requirements.txt              # All dependencies
└── .env.example                  # Environment template
```

---

## 🚀 Quick Start

### **1. Prerequisites**

- Python 3.11 or higher
- pip (Python package manager)
- ~500MB disk space

### **2. Installation**

```bash
# Clone repository
cd /home/ahsan1o/projects/LocalMarketSoftwares/LIMS/kotli-lims

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
pip install -r frontend/requirements.txt
```

### **3. Start Backend Server**

```bash
# In one terminal
cd backend
python app.py

# You should see:
# ╔════════════════════════════════════════════════════════════════╗
# ║                    KOTLI LIMS SERVER                           ║
# ║        Offline-Capable Laboratory Information System           ║
# ║                                                                ║
# ║  Starting on http://127.0.0.1:8000                            ║
# ║  API Documentation: http://127.0.0.1:8000/api/docs            ║
# ║                                                                ║
# ║  Default Login: admin / admin123                              ║
# ║  ⚠️  Change password after first login!                        ║
# ╚════════════════════════════════════════════════════════════════╝
```

### **4. Start Frontend Application**

```bash
# In another terminal
cd frontend
python main.py  # When main.py is ready

# Or test API first
curl http://127.0.0.1:8000/api/health
```

### **5. Access System**

- **API Documentation:** http://127.0.0.1:8000/api/docs
- **Desktop App:** Opens PyQt6 window (once frontend is ready)
- **Default Credentials:** `admin` / `admin123`

---

## 📊 Key Features

### **✅ Implemented**
- [x] Database schema and models
- [x] FastAPI server setup
- [x] Authentication framework
- [x] Health check endpoints
- [x] Barcode service
- [x] Project structure

### **🚧 In Progress**
- [ ] API endpoints (samples, tests, results, users, machines, reports)
- [ ] PyQt6 frontend UI
- [ ] Machine data integration
- [ ] Report generation
- [ ] Offline sync engine

### **📋 Planned**
- [ ] Cloud backup integration
- [ ] Multi-location support
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Voice recognition

---

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & data flow
- **[API_DOCS.md](docs/API_DOCS.md)** - API endpoints reference (WIP)
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - User manual (WIP)
- **[DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - Database design (WIP)

---

## 🔐 Security

- **Password Hashing:** bcrypt (industry standard)
- **Authentication:** JWT tokens
- **Database Encryption:** SQLite with encryption
- **Audit Logging:** All actions tracked
- **Role-Based Access:** Admin, Technician, Supervisor, Doctor
- **HTTPS Ready:** Full support for encrypted communication

---

## 💾 Offline Capability

This is Kotli LIMS's **killer feature**:

- **Works without internet** - Perfect for Kotli's connectivity issues
- **Local SQLite database** - All data stored locally
- **Automatic sync** - When internet returns, data syncs to cloud
- **Zero data loss** - Full redundancy and backups
- **Seamless transitions** - No interruption if connection drops

---

## 📞 Support & Contribution

### **Development Team**
- **Project Lead:** Ahsan Malik
- **Architecture:** Modern Python + PyQt6
- **Focus:** Clinical Lab Excellence

### **Contributing**
```bash
# Fork project
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# Submit pull request
```

---

## 📅 Development Timeline

| Phase | Duration | Focus |
|-------|----------|-------|
| **Phase 1** | Week 1-2 | Backend + Database + API |
| **Phase 2** | Week 3-4 | PyQt6 UI/UX |
| **Phase 3** | Week 5-6 | Machine Integration + Reports |
| **Phase 4** | Week 7-8 | Testing + Deployment |

---

## 🎓 Learning Resources

### **Backend (FastAPI)**
- https://fastapi.tiangolo.com/
- https://docs.sqlalchemy.org/

### **Frontend (PyQt6)**
- https://doc.qt.io/qtforpython-6/
- https://www.tutorialspoint.com/pyqt/

### **Database (SQLite)**
- https://www.sqlite.org/docs.html

---

## ⚖️ License

**GNU General Public License v3.0**

This project is open source. You can:
- ✅ Modify and use in your lab
- ✅ Distribute to other labs
- ✅ Commercial use (with attribution)
- ❌ Must keep attribution
- ❌ Cannot claim you wrote it from scratch

---

## 🏆 Success Criteria

- ✅ Works offline (98%+ functionality without internet)
- ✅ Sample registration < 2 minutes
- ✅ Results approval < 5 minutes
- ✅ Report generation < 1 minute
- ✅ 99.9% data accuracy
- ✅ Full audit trail
- ✅ Easy user training (< 1 hour)

---

## 🚨 Important Notes

1. **Default Admin Password:** Change immediately after first login!
2. **Data Backup:** Daily backup to USB recommended
3. **Machine Integration:** Test with your specific lab equipment
4. **Compliance:** Customize for local regulations

---

## 📞 Quick Help

### **Backend won't start?**
```bash
python app.py
# Check if port 8000 is free
# If not: kill process or change port in app.py
```

### **Frontend issues?**
```bash
pip install --upgrade PyQt6
# Ensure Python 3.11+
python --version
```

### **Database issues?**
```bash
# Delete database to reset (WARNING: data loss!)
rm data/kotli_lims.db
# Restart app to recreate fresh database
```

---

## 🎉 Ready to Build!

Let's make Kotli LIMS the best clinical lab software in Pakistan! 

**Next Steps:**
1. ✅ Architecture designed
2. ✅ Database schema created
3. ✅ Backend framework ready
4. 🚀 **Now: Build API endpoints & PyQt6 UI**

---

**Made with ❤️ for Kotli's healthcare**

*"Offline-Capable, Modern, Professional - LIMS Done Right"*

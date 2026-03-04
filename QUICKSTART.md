# Kotli LIMS - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### **Step 1: Setup Python Environment**

```bash
# Go to project directory
cd /home/ahsan1o/projects/LocalMarketSoftwares/LIMS/kotli-lims

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### **Step 2: Install Dependencies**

```bash
# Install both backend and frontend dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### **Step 3: Start Backend Server** (Terminal 1)

```bash
# Activate venv first
source venv/bin/activate

# Start backend
cd backend
python app.py
```

You should see:
```
╔════════════════════════════════════════════════════════════════╗
║                    KOTLI LIMS SERVER                           ║
║        Offline-Capable Laboratory Information System           ║
║                                                                ║
║  Starting on http://127.0.0.1:8000                            ║
║  API Documentation: http://127.0.0.1:8000/api/docs            ║
║                                                                ║
║  Default Login: admin / admin123                              ║
║  ⚠️  Change password after first login!                        ║
╚════════════════════════════════════════════════════════════════╝
```

### **Step 4: Start Frontend Application** (Terminal 2)

```bash
# In new terminal, activate venv
source venv/bin/activate

# Start frontend
cd frontend
python main.py
```

## 🎯 What You Can Do Right Now

### **Test Backend API**

Visit in your browser:
- **Health Check:** http://127.0.0.1:8000/api/health
- **API Docs:** http://127.0.0.1:8000/api/docs (click to test)
- **Server Info:** http://127.0.0.1:8000/api/info

### **Test Backend with Curl**

```bash
# Health check
curl http://127.0.0.1:8000/api/health

# Get server info
curl http://127.0.0.1:8000/api/info

# Try login (test authentication)
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### **Frontend Dashboard**

- See modern dark theme
- Sidebar navigation
- Demo dashboard with stats
- Switch between screens
- Server status indicator

---

## 📱 What's Already Working

### **Backend**
- ✅ FastAPI server foundation
- ✅ SQLite database with all tables
- ✅ User authentication framework
- ✅ Health check endpoints
- ✅ CORS enabled for frontend
- ✅ Error handling
- ✅ Logging system

### **Frontend**
- ✅ PyQt6 main window
- ✅ Modern dark theme
- ✅ Sidebar navigation
- ✅ Dashboard screen with stats
- ✅ Placeholder screens for other modules
- ✅ Server connection checking
- ✅ Professional color scheme

### **Database**
- ✅ 11 tables (Patients, Doctors, Samples, Tests, Results, etc)
- ✅ Auto-created on first run
- ✅ Default admin user (admin/admin123)
- ✅ Indexes for performance
- ✅ Relationships defined

---

## 🔄 Typical Development Workflow

```
1. Start Backend Server
   └─ Terminal 1: cd backend && python app.py

2. Start Frontend App
   └─ Terminal 2: cd frontend && python main.py

3. Test in API Docs
   └─ Browser: http://127.0.0.1:8000/api/docs

4. Make changes to code

5. Server auto-reloads (if using reload=True)

6. Frontend auto-detects changes (PyQt6 restart needed)

7. Check database
   └─ Can use SQLite Browser: data/kotli_lims.db
```

---

## 🛠️ Useful Commands

### **Database Inspection**

```bash
# View database (requires SQLite Browser)
sqlite3 data/kotli_lims.db

# List all tables
.tables

# View table structure
.schema samples

# Export data
.output backup.sql
.dump
.output stdout
```

### **Backend Testing**

```bash
# Run unit tests (when added)
cd backend
pytest

# Run with verbose output
pytest -v

# Test specific file
pytest tests/test_samples.py
```

### **Frontend Testing**

```bash
# Check PyQt6 import
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# Run app with verbose output
python main.py --verbose
```

---

## 📊 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **Architecture** | ✅ Complete | Full system design documented |
| **Database** | ✅ Ready | All tables, relationships defined |
| **Backend Foundation** | ✅ Ready | FastAPI, models, auth layer |
| **Frontend Foundation** | ✅ Ready | PyQt6 window, theme, navigation |
| **API Endpoints** | 🚧 Partial | Login endpoint ready, others needed |
| **Backend Services** | 🚧 Needed | Barcode, Report, Sync services |
| **UI Screens** | 🚧 Partial | Dashboard done, others templates |
| **Machine Integration** | 📋 Planned | Receiver endpoint designed |
| **Offline Sync** | 📋 Planned | Architecture defined |
| **Testing** | 📋 Planned | Unit tests to be added |

---

## ⚠️ Important Notes

1. **Change Default Password Immediately!**
   - After first login, change admin password
   - Go to Settings in frontend (when implemented)

2. **Database Location**
   - Stored at: `data/kotli_lims.db`
   - Backup this file regularly!

3. **Offline Mode**
   - App works completely offline (when implemented)
   - All data stored locally in SQLite
   - Syncs to cloud when internet available

4. **For Lab Use**
   - Test with real lab equipment first
   - Configure machine IP/port
   - Train staff before deployment
   - Keep daily backups

---

## 🎓 Learning Resources

### **Backend Development**
- FastAPI: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy: https://docs.sqlalchemy.org/tutorial/
- Python: https://docs.python.org/3/

### **Frontend Development**
- PyQt6: https://www.learnpyqt.com/
- Signals/Slots: https://www.riverbankcomputing.com/static/Docs/PyQt6/

### **Database**
- SQLite: https://www.sqlite.org/quickstart.html
- Query builder: https://sqlalchemy-utils.readthedocs.io/

---

## 🐛 Troubleshooting

### **Q: Backend won't start**
```bash
# Check Python version
python --version  # Should be 3.11+

# Check all dependencies installed
pip list | grep -i fastapi

# Reset dependencies
pip install --upgrade -r backend/requirements.txt
```

### **Q: Frontend crashes**
```bash
# Check PyQt6
python -c "from PyQt6 import QtCore; print('OK')"

# Reinstall PyQt6
pip install --force-reinstall PyQt6
```

### **Q: Database error**
```bash
# Delete and recreate
rm data/kotli_lims.db
python backend/app.py  # Recreates on startup
```

### **Q: Port 8000 already in use**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port (edit app.py)
```

---

## 📚 Next Steps

1. ✅ Start backend and frontend
2. ✅ Play with the dashboard
3. 🔄 Read IMPLEMENTATION_GUIDE.md
4. 📖 Review ARCHITECTURE.md for design
5. 🛠️ Start implementing API endpoints
6. 🎨 Customize UI screens

---

## 🎉 You're All Set!

Your Kotli LIMS project is ready to develop. 

**Current Status:**
- Foundation complete ✅
- Backend running ✅
- Frontend showing ✅  
- Database ready ✅

**Next:** Implement API endpoints and UI screens based on IMPLEMENTATION_GUIDE.md

**Questions?** Check the documentation files:
- `ARCHITECTURE.md` - System design
- `IMPLEMENTATION_GUIDE.md` - Feature roadmap
- `README.md` - Project overview

Good luck! 🚀

---

**Made with ❤️ for Kotli's healthcare**

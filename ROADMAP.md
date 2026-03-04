# Enigma LIMS — Product Roadmap

**Current version:** v1.0 — Offline desktop app (Windows EXE + local server)
**Owner:** Ahsan (LocalMarketSoftwares)

---

## v1.0 — Offline EXE (Current — Shippable Now)

Single-lab, offline-first desktop application. Each lab gets their own EXE installer. All data lives on the lab's own machine.

**What's done:**
- Full lab workflow: Patients → Samples → Orders → Results → Reports
- Two roles: Super Admin (full access) + Lab Technician (core workflow only)
- Test catalog with prices; bill summary on patient reports
- Role-based nav: Admin section hidden from technicians
- Per-page help system + first-visit onboarding tour
- Default accounts: `admin / admin123` and `tech / tech123`
- Admin can create/manage additional users via Users page
- Audit log, billing, instruments, reagents, test panels
- Windows EXE built with PyInstaller (bundles Python + FastAPI + SQLite)

**How to sell this:**
- Each lab buys a license, gets the EXE
- Lab admin logs in day 1, changes passwords, creates real staff accounts
- All data stays on-premises — clinics prefer this
- No internet dependency — works in areas with unreliable connectivity
- No ongoing server costs for you

---

## v2.0 — SaaS Platform (Future — Major Rewrite)

**Goal:** One hosted platform serving multiple labs. Patients and doctors can access results online.

### Architecture

```
enigma-lims.com (your hosted server)
├── /developer  → Your personal dashboard (God view)
├── /           → Lab staff interface (current UI, scoped per lab)
├── /patient    → Patient portal (view own results by phone/DOB)
└── /doctor     → Doctor portal (view referred patients' reports)
```

### User Tiers

| Role | Access | Created by |
|---|---|---|
| **Developer** (you) | All labs, software management, no patient data | Hardcoded / seeded |
| **Lab Admin** | Their lab only: full LIMS + user management | Developer dashboard |
| **Technician** | Their lab only: core workflow tabs | Lab Admin |
| **Patient** (future) | Their own results only | Auto on report approval |
| **Doctor** (future) | Their referred patients | Lab Admin |

### What Needs to Be Built

#### 1. Database — Multi-tenancy

Add `labs` table and `lab_id` FK on every data table:

```sql
CREATE TABLE labs (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,   -- e.g. "kotli-path-lab"
    city        TEXT,
    phone       TEXT,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    subscription_expiry  DATE
);

-- Add to ALL data tables:
ALTER TABLE patients    ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE samples     ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE tests       ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE orders      ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE results     ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE reports     ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE instruments ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE reagents    ADD COLUMN lab_id INTEGER REFERENCES labs(id);
ALTER TABLE users       ADD COLUMN lab_id INTEGER REFERENCES labs(id);
```

Switch from SQLite to **PostgreSQL** for the hosted version (SQLite doesn't scale multi-user cloud).

#### 2. Backend — Lab Context Middleware

Every API request must know which lab it belongs to. Extract from JWT:

```python
# JWT payload:
{ "sub": "admin", "role": "lab_admin", "lab_id": 3, "exp": ... }

# Middleware injects current_lab_id into every endpoint
# All queries add: .filter(Model.lab_id == current_lab_id)
```

Developer-tier endpoints (`/api/developer/...`) skip lab filtering and require `role == "developer"`.

#### 3. Developer Dashboard (new frontend pages)

Pages needed:
- `developer/dashboard.html` — system stats: total labs, active today, new signups
- `developer/labs.html` — create/suspend labs, set subscription expiry
- `developer/lab-detail.html` — view a specific lab's usage (counts only, not patient data)
- `developer/software.html` — app version management, changelog

#### 4. Lab Onboarding Flow

When developer creates a new lab:
1. System generates Lab Slug + initial Admin credentials
2. Developer hands credentials to lab owner
3. Lab admin logs in → forced password change → lab is live

#### 5. Patient Portal (future)

- Patients receive an SMS with a link + OTP when results are approved
- `patient/results.html` — enter phone + OTP → see results PDF
- Or: static shareable link per report (no account needed)
- No patient username/password to manage — reduces support burden

#### 6. Doctor Portal (future)

- Doctors registered in the system by Lab Admin
- Doctor logs in → sees all patients from that lab referred by them
- Read-only: can view/download reports, cannot modify anything

### Infrastructure (SaaS)

| Component | Tool | Notes |
|---|---|---|
| Backend hosting | Railway / Render / DigitalOcean | ~$5-20/month to start |
| Database | PostgreSQL (Supabase free tier to start) | Replace SQLite |
| Frontend | Same GitHub Pages OR serve from backend | No change needed |
| Auth | JWT (current, keep it) | Add lab_id claim |
| File storage | Local disk or Cloudflare R2 | For report PDFs |
| Domain | enigma-lims.com | ~$10/year |

### Migration Path (v1 → v2)

- v1 labs can optionally migrate: export their SQLite DB, import into cloud with lab_id stamped
- Or: v1 labs stay offline forever, v2 is a new product tier at higher price
- Recommended: **two tiers** — "Offline" (EXE, one-time license) and "Cloud" (monthly subscription with patient portal)

---

## Pricing Model Ideas

| Tier | What they get | Price |
|---|---|---|
| **Starter (Offline)** | EXE, 1 lab, unlimited users, no patient portal | PKR 15,000 one-time |
| **Pro (Cloud)** | Hosted, patient portal, doctor access, updates | PKR 3,000/month |
| **Enterprise** | Multi-branch, custom branding, priority support | Custom |

---

## Near-Term Priorities (Before SaaS)

These can be added to v1 without architecture changes:

1. **First-run password change wizard** — force admin to set new password on first login
2. **Lab branding** — lab name + logo on printed reports (Settings page)
3. **Backup/restore** — one-click SQLite backup download from admin panel
4. **Print report improvements** — letterhead, doctor name, digital signature line
5. **WhatsApp result sharing** — generate a share link for a report (wa.me deep link with text)

---

## Notes for Developer

- Current repo: `github.com/ahsan1o/kotli-lims`
- Backend: FastAPI + SQLAlchemy + SQLite (Python 3.12)
- Frontend: Vanilla JS + Tailwind CSS (no framework)
- Auth: JWT (HS256) via `python-jose`
- EXE build: PyInstaller via `enigma_lims.spec`
- GitHub Pages serves `docs/` folder as static demo

When starting v2, create a new branch `saas-v2` and do not merge into `main` until fully tested. The offline v1 on `main` should remain stable and shippable at all times.

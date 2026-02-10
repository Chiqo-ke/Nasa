# NASA - Quick Reference Guide

## 🎯 What Is This?

**NASA** = **N**ational **A**dministration **S**ystem for **A**ccountability

A blockchain-powered government financial management platform that ensures transparent, accountable, and secure handling of public funds.

---

## ⚡ Quick Start

### Start Everything (Easiest Way)
```bash
# Windows: Double-click this file
START_PROJECT.bat
```

### Manual Start
```bash
# Terminal 1 - Backend
cd gok_backend
..\.venv\Scripts\activate
python main.py

# Terminal 2 - Frontend  
cd NASA
python -m http.server 5500
```

### Access Points
- **Login**: http://localhost:5500/login.html
- **API Docs**: http://localhost:8000/docs
- **React Dashboard**: http://localhost:5173 (if running federal-ledger)

---

## 👤 Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Super Admin | FinanceOffice | finance2025 |
| Ministry Admin | EducationOffice | education2025 |
| Ministry Admin | HealthcareOffice | healthcare2025 |

---

## 🔑 Key Features

### For Government (Admin/Ministry)
✅ Create and manage ministries  
✅ Allocate budgets transparently  
✅ Create projects and track spending
✅ Submit and approve expense requests  
✅ View all transactions on blockchain  
✅ Review citizen reports

### For Citizens
✅ Pay taxes online  
✅ Get instant payment receipts  
✅ Report suspicious activities  
✅ View public spending (transparency)  
✅ Verify transactions on blockchain

---

## 📊 System Components

```
┌─────────────────────────────────────────┐
│        Frontend (Browser)               │
│  HTML/CSS/JS  |  React TypeScript       │
└──────────────────┬──────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼──────────────────────┐
│        Backend (FastAPI)                 │
│  • Authentication (JWT)                  │
│  • Ministry Management                   │
│  • Project Tracking                      │
│  • Expense Workflow                      │
│  • Tax Payments                          │
│  • Report System                         │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐  ┌────────▼─────────┐
│   Database     │  │   Blockchain     │
│  (SQLite/PG)   │  │  (JSON file)     │
│  • Users       │  │  • Transactions  │
│  • Ministries  │  │  • Blocks        │
│  • Projects    │  │  • Validators    │
│  • Expenses    │  │                  │
│  • Tax Payments│  │                  │
│  • Reports     │  │                  │
└────────────────┘  └──────────────────┘
```

---

## 🔄 Common Workflows

### 1. Allocate Budget to Ministry
```
Super Admin → Select Ministry → Allocate Budget 
→ Enter Amount & Purpose → Approve 
→ Blockchain Transaction Created 
→ Ministry Balance Updated ✓
```

### 2. Submit & Approve Expense
```
Ministry Officer → Create Expense Request 
→ Enter Details (Amount, Purpose, Project)
→ Submit → Status: Pending

Super Admin → Review Request → Approve 
→ Funds Transferred → Blockchain Record 
→ Project Spending Updated ✓
```

### 3. Citizen Pays Tax
```
Citizen → Tax Payment Portal 
→ Fill Details (Name, ID, Tax Type, Amount)
→ Submit Payment → Receipt Generated 
→ Blockchain Transaction → Payment Complete ✓
```

### 4. Report Suspicious Activity
```
Citizen → Report Portal → Submit Report 
→ Admin Reviews → Investigate 
→ Update Status (Pending → Reviewed → Resolved)
→ Add Notes → Close Report ✓
```

---

## 📁 Project Structure

```
NASA/
├── gok_backend/              # FastAPI Backend
│   ├── main.py              # Entry point
│   ├── models.py            # Database models
│   ├── schemas.py           # API schemas
│   ├── endpoints.py         # Core API routes
│   ├── ministry_endpoints.py
│   ├── tax_endpoints.py
│   ├── auth.py              # JWT authentication
│   ├── blockchain.py        # Blockchain logic
│   ├── database.py          # DB connection
│   └── requirements.txt     # Python dependencies
│
├── NASA/                    # Traditional Frontend
│   ├── login.html
│   ├── index.html           # Dashboard
│   ├── tax-payment.html
│   ├── citizen-portal.html
│   └── reports.html
│
├── federal-ledger/          # Modern React Frontend
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── components/      # UI components
│   │   ├── services/api.ts  # API client
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── blockchain.json          # Blockchain storage
├── validators.json          # Approved validators
├── wallets.json            # Wallet balances
└── START_PROJECT.bat       # Quick start script
```

---

## 🛠️ Tech Stack

**Backend**: FastAPI + Python + SQLAlchemy + JWT  
**Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui  
**Blockchain**: Custom Python implementation (SHA-256)  
**Database**: SQLite (dev) / PostgreSQL (prod)  
**WebSocket**: Real-time updates

---

## 📡 API Cheat Sheet

### Authentication
```http
POST /token                  # Login
POST /refresh               # Refresh token
POST /logout                # Logout
```

### Ministries
```http
GET    /ministries          # List all
POST   /ministries          # Create new
POST   /ministries/{id}/allocate  # Allocate budget
```

### Projects
```http
GET    /projects            # List all
POST   /projects            # Create
GET    /ministries/{id}/projects  # Get ministry projects
```

### Expenses
```http
GET    /expense-requests    # List all
POST   /expense-requests    # Submit new
PUT    /expense-requests/{id}  # Approve/Reject
```

### Tax Payments
```http
POST   /tax-payments        # Submit payment
GET    /tax-payments        # View history
```

### Reports
```http
POST   /reports             # Submit report (public)
GET    /reports             # View all (admin)
PUT    /reports/{id}        # Update status
```

### Blockchain
```http
GET    /blockchain          # View full chain
GET    /transactions        # View transactions
GET    /balance/{wallet}    # Check balance
```

---

## 🔐 Security Notes

✅ **Passwords**: Bcrypt hashed + salted  
✅ **Tokens**: JWT with 30-min expiry  
✅ **CORS**: Configured allowed origins  
✅ **SQL Injection**: ORM prevents it  
✅ **Blockchain**: Immutable transaction records  
✅ **Audit Trail**: All actions logged

---

## 🐛 Common Issues

### Port Already In Use
```bash
netstat -ano | findstr :8000
taskkill /F /PID <number>
```

### Database Not Found
```bash
cd gok_backend
python database_init.py
```

### CORS Error
Check `main.py` → CORS allowed origins match your frontend URL

### Module Not Found
```bash
pip install -r gok_backend/requirements.txt
```

---

## 📈 System Stats

- **User Roles**: 4 (Super Admin, Ministry Admin, Officer, Citizen)
- **Ministry Types**: 11 (Education, Health, Finance, etc.)
- **Database Tables**: 6 (Users, Ministries, Projects, Expenses, Tax Payments, Reports)
- **API Endpoints**: 40+
- **Transaction Types**: Budget allocation, Expense payment, Tax payment, Transfers

---

## 🎓 Learn More

For detailed documentation, see: **PROJECT_DOCUMENTATION.md**

---

**Quick Tips**:
- Always start backend before frontend
- Use `/docs` endpoint for interactive API testing
- Check blockchain.json to see actual transaction records
- WebSocket connects automatically for real-time updates
- All financial data is transparent and verifiable

---

**Version**: 2.0  
**Last Updated**: February 10, 2026

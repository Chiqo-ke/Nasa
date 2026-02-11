# 🏛️ NASA - National Financial Blockchain Administration System

> A comprehensive government financial management platform leveraging blockchain technology for transparency, accountability, and security in public fund management.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.140.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)

---

## 📚 Documentation

This project has extensive documentation to help you understand and work with the system:

### Quick Links

| Document | Description | Best For |
|----------|-------------|----------|
| **[Quick Reference](QUICK_REFERENCE.md)** | Fast overview and common tasks | Users & Operators |
| **[Project Documentation](PROJECT_DOCUMENTATION.md)** | Complete feature documentation | All Users |
| **[Technical Architecture](TECHNICAL_ARCHITECTURE.md)** | Deep technical details | Developers |
| **[Startup Guide](README_STARTUP.txt)** | How to start the system | Getting Started |
| **[Report System Guide](REPORT_SYSTEM_GUIDE.txt)** | Citizen reporting features | Citizens & Admins |

---

## 🎯 What Is NASA?

NASA (National Financial Blockchain Administration System) is a full-stack blockchain-powered platform that enables:

- ✅ **Transparent Government Spending** - All transactions recorded on immutable blockchain
- ✅ **Ministry Budget Management** - Create, allocate, and track ministry budgets
- ✅ **Project Tracking** - Monitor government projects from planning to completion
- ✅ **Expense Workflow** - Submit, approve, and execute expense requests
- ✅ **Citizen Tax Payments** - Online tax payment with instant receipts
- ✅ **Public Reporting** - Citizens can report suspicious financial activities
- ✅ **Real-time Updates** - WebSocket-powered live data synchronization

---

## 🚀 Quick Start

### Automatic Start (Easiest)

**Windows:**
```bash
# Double-click this file
START_PROJECT.bat
```

Your browser will automatically open to the login page. Use these credentials:

| Username | Password | Role |
|----------|----------|------|
| FinanceOffice | finance2025 | Super Admin |
| EducationOffice | education2025 | Ministry Admin |
| HealthcareOffice | healthcare2025 | Ministry Admin |

### Manual Start

**Backend Server:**
```bash
cd gok_backend
..\.venv\Scripts\activate  # Windows
# source ../.venv/bin/activate  # Linux/Mac
python main.py
```

**Frontend Server (Traditional):**
```bash
cd NASA
python -m http.server 5500
```

**Frontend Server (Modern React):**
```bash
cd federal-ledger
npm install
npm run dev
```

**Access Points:**
- Traditional Portal: http://localhost:5500/login.html
- React Dashboard: http://localhost:5173
- API Documentation: http://localhost:8001/docs
- Backend API: http://localhost:8001

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│  HTML/CSS/JS Portal  |  React TypeScript Dashboard      │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS + WebSocket
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend                         │
│  • JWT Authentication  • Ministry Management             │
│  • Blockchain Engine   • Expense Workflow                │
│  • Tax System         • Reporting System                 │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼─────────┐          ┌────────▼──────────┐
│   PostgreSQL    │          │   Blockchain      │
│   Database      │          │   (JSON Files)    │
│                 │          │                   │
│ • Users         │          │ • Transactions    │
│ • Ministries    │          │ • Blocks          │
│ • Projects      │          │ • Validators      │
│ • Expenses      │          │ • Immutable       │
│ • Tax Payments  │          │   Ledger          │
│ • Reports       │          │                   │
└─────────────────┘          └───────────────────┘
```

---

## 💼 Key Features

### For Government Officials

**Ministry Management**
- Create and manage government ministries
- Automatic wallet address generation
- Budget allocation and tracking
- Real-time balance updates

**Project Management**
- Create projects under ministries
- Allocate budgets to projects
- Track project spending and status
- Timeline management

**Expense Request Workflow**
- Submit expense requests
- Multi-level approval system
- Automatic blockchain recording
- Real-time status updates

### For Citizens

**Tax Payment System**
- Pay taxes online (Income, VAT, Corporate, Property, Excise)
- Instant receipt generation
- Blockchain verification
- Payment history tracking

**Citizen Reporting**
- Report suspicious financial activities
- Track report status
- Admin investigation workflow
- Public transparency access

---

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI 0.140.0 (Python 3.11+)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **ORM:** SQLAlchemy 2.x with Alembic migrations
- **Authentication:** JWT (python-jose) + Bcrypt password hashing
- **Server:** Uvicorn (ASGI)
- **WebSocket:** FastAPI native support

### Frontend
- **Modern Dashboard:** React 18 + TypeScript + Vite
- **UI Components:** shadcn/ui + Tailwind CSS
- **State Management:** React Query (TanStack)
- **HTTP Client:** Axios with interceptors
- **Traditional Portal:** HTML5 + CSS3 + JavaScript ES6+

### Blockchain
- **Custom Implementation:** Python-based blockchain
- **Hashing:** SHA-256
- **Storage:** JSON file persistence
- **Validation:** Chain integrity verification

---

## 📁 Project Structure

```
NASA/
├── gok_backend/              # FastAPI Backend
│   ├── main.py              # Application entry point
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── endpoints.py         # Core API routes
│   ├── ministry_endpoints.py
│   ├── tax_endpoints.py
│   ├── auth.py              # JWT authentication
│   ├── blockchain.py        # Blockchain engine
│   ├── database.py          # DB configuration
│   └── requirements.txt
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
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── blockchain.json          # Blockchain storage
├── validators.json
├── wallets.json
├── START_PROJECT.bat        # Quick start script
│
├── README.md               # This file
├── QUICK_REFERENCE.md      # Quick reference guide
├── PROJECT_DOCUMENTATION.md # Complete documentation
└── TECHNICAL_ARCHITECTURE.md # Technical deep dive
```

---

## 🔐 Security Features

- ✅ **Password Security:** Bcrypt hashing with automatic salting
- ✅ **JWT Tokens:** Access (30min) + Refresh (7 days) tokens
- ✅ **Token Revocation:** Blacklist support for logged-out tokens
- ✅ **Role-Based Access:** 4 roles (Super Admin, Ministry Admin, Officer, Citizen)
- ✅ **CORS Protection:** Configured allowed origins
- ✅ **SQL Injection Prevention:** ORM parameterized queries
- ✅ **Blockchain Integrity:** Immutable transaction records with hash verification
- ✅ **Audit Trail:** Complete logging of all financial activities

---

## 👥 User Roles & Permissions

| Role | Ministry Mgmt | Budget Allocation | Expense Approval | Tax Payment | Reports |
|------|---------------|-------------------|------------------|-------------|---------|
| **Super Admin** | ✅ Create/Manage | ✅ Allocate | ✅ Approve/Reject | ✅ View All | ✅ Review |
| **Ministry Admin** | ❌ | ❌ | ❌ | ✅ Pay | ❌ |
| **Ministry Officer** | ❌ | ❌ | ❌ | ✅ Pay | ❌ |
| **Citizen** | ❌ | ❌ | ❌ | ✅ Pay | ✅ Submit |

---

## 📊 System Statistics

- **User Roles:** 4 (Super Admin, Ministry Admin, Officer, Citizen)
- **Ministry Types:** 11+ (Education, Health, Finance, Technology, etc.)
- **Database Tables:** 6 (Users, Ministries, Projects, Expenses, Tax Payments, Reports)
- **API Endpoints:** 40+
- **Transaction Types:** Budget allocation, Expense payment, Tax payment, Transfers
- **Supported Tax Types:** 5 (Income, VAT, Corporate, Property, Excise)

---

## 🚀 Installation

### Prerequisites

```bash
# Required
- Python 3.11 or higher
- Node.js 18+ and npm (for React frontends)
- Git

# Recommended
- PostgreSQL (for production)
- Redis (for caching - future enhancement)
```

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NASA
   ```

2. **Backend Setup**
   ```bash
   cd gok_backend
   python -m venv ../.venv
   ..\.venv\Scripts\activate
   pip install -r requirements.txt
   python database_init.py
   python create_test_user.py
   ```

3. **Frontend Setup (React)**
   ```bash
   cd ../federal-ledger
   npm install
   ```

4. **Start Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd gok_backend
   python main.py

   # Terminal 2 - Frontend
   cd federal-ledger
   npm run dev
   ```

5. **Access Application**
   - Modern UI: http://localhost:5173
   - API Docs: http://localhost:8001/docs

---

## 📖 Usage Examples

### Allocate Budget to Ministry (API)

```bash
curl -X POST "http://localhost:8001/ministries/1/allocate" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "purpose": "Q1 2025 Budget Allocation",
    "approved_by": "FinanceOffice"
  }'
```

### Submit Tax Payment

```bash
curl -X POST "http://localhost:8001/tax-payments" \
  -H "Content-Type: application/json" \
  -d '{
    "taxpayer_name": "John Doe",
    "id_number": "12345678",
    "tax_type": "income",
    "amount": 15000,
    "payment_method": "M-Pesa"
  }'
```

### View Blockchain

```bash
curl -X GET "http://localhost:8001/blockchain" \
  -H "Authorization: Bearer <token>"
```

---

## 🧪 Testing

### Run Backend Tests (When implemented)
```bash
cd gok_backend
pytest tests/ -v
```

### API Testing
Use the interactive API documentation:
```
http://localhost:8001/docs
```

### Manual Testing Checklist
- [ ] User login/logout
- [ ] Ministry creation
- [ ] Budget allocation
- [ ] Project creation
- [ ] Expense request workflow
- [ ] Tax payment processing
- [ ] Report submission
- [ ] Blockchain verification
- [ ] WebSocket real-time updates

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8001
taskkill /F /PID <process_id>

# Linux/Mac
lsof -ti:8001 | xargs kill -9
```

### Database Not Found
```bash
cd gok_backend
python database_init.py
```

### Module Not Found
```bash
pip install -r gok_backend/requirements.txt
```

### CORS Errors
Check `gok_backend/main.py` and ensure frontend URL is in `allow_origins` list.

---

## 🔮 Future Enhancements

### Phase 1: Enhanced Security
- [ ] Two-factor authentication (2FA)
- [ ] Biometric authentication
- [ ] IP whitelist/blacklist
- [ ] Rate limiting

### Phase 2: Advanced Features
- [ ] Email/SMS notifications
- [ ] PDF receipt generation
- [ ] Advanced analytics with AI
- [ ] Multi-language support

### Phase 3: Scalability
- [ ] Redis caching
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] Microservices architecture

### Phase 4: Integration
- [ ] Mobile apps (iOS/Android)
- [ ] M-Pesa payment gateway
- [ ] Bank API integrations
- [ ] Government ID verification

### Phase 5: Blockchain Enhancement
- [ ] Consensus mechanism
- [ ] Multi-node network
- [ ] Smart contracts
- [ ] Blockchain explorer UI

---

## 📞 Support

### Documentation
- **Quick Start:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Complete Guide:** [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **For Developers:** [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)
- **Startup Help:** [README_STARTUP.txt](README_STARTUP.txt)

### Common Issues
See the [Troubleshooting](#-troubleshooting) section above.

### API Reference
Interactive API documentation available at: http://localhost:8001/docs

---

## 🤝 Contributing

This is an educational/demonstration project. Contributions are welcome for:

- Bug fixes
- Feature enhancements
- Documentation improvements
- Test coverage
- Performance optimizations

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 👨‍💻 Development Team

Built as a comprehensive demonstration of a government financial management system with blockchain technology.

---

## 🌟 Highlights

- **🔒 Secure:** JWT authentication, bcrypt password hashing, token revocation
- **🔗 Transparent:** All transactions on immutable blockchain
- **⚡ Real-time:** WebSocket for live updates
- **🎨 Modern UI:** React + TypeScript + Tailwind CSS
- **📊 Comprehensive:** Covers entire government financial workflow
- **🧪 Well-Documented:** Extensive documentation for users and developers
- **🚀 Production-Ready Architecture:** Scalable and maintainable codebase

---

## 📈 Project Status

**Version:** 2.0  
**Status:** ✅ Active Development  
**Last Updated:** February 10, 2026

---

<div align="center">

**[⬆ Back to Top](#-nasa---national-financial-blockchain-administration-system)**

---

Made with ❤️ for transparent government financial management

</div>

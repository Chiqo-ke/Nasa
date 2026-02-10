# NASA System Overview - Visual Guide

## 🎯 System at a Glance

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              NASA - National Financial Blockchain                ║
║              Administration System                               ║
║                                                                  ║
║  Purpose: Transparent Government Financial Management            ║
║  Technology: FastAPI + React + Blockchain                        ║
║  Users: Government Officials + Citizens                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🏛️ The Problem NASA Solves

### Before NASA ❌
```
Government Finance
    ↓
  [Black Box]
    ↓
 No Transparency
 No Accountability
 Manual Processes
 Slow Approvals
 Citizen Distrust
```

### After NASA ✅
```
Government Finance
    ↓
[Blockchain Ledger]
    ↓
 ✓ Complete Transparency
 ✓ Full Accountability
 ✓ Automated Workflow
 ✓ Instant Approvals
 ✓ Citizen Trust
```

---

## 🔄 Main Workflows

### 1. Budget Allocation Workflow

```
┌──────────────┐
│ Super Admin  │
│ (Finance)    │
└──────┬───────┘
       │
       │ 1. Allocate Budget
       │    $100,000 → Ministry of Education
       ▼
┌──────────────────────────┐
│ System creates           │
│ blockchain transaction   │
└──────┬───────────────────┘
       │
       │ 2. Record on Blockchain
       ▼
┌──────────────────────────┐
│ • Sender: SYSTEM         │
│ • Recipient: EDU Wallet  │
│ • Amount: $100,000       │
│ • Hash: 0xabc123...      │
│ • IMMUTABLE ✓            │
└──────┬───────────────────┘
       │
       │ 3. Update Database
       ▼
┌──────────────────────────┐
│ Ministry of Education    │
│ Balance: $100,000        │
│ Status: Ready to spend   │
└──────┬───────────────────┘
       │
       │ 4. Real-time Notification
       ▼
┌──────────────────────────┐
│ Ministry Dashboard       │
│ ⚡ New budget allocated  │
│ 💰 Balance updated       │
└──────────────────────────┘
```

### 2. Expense Request & Approval

```
┌──────────────────┐
│ Ministry Officer │
│ (Education)      │
└────────┬─────────┘
         │
         │ 1. Request: $25,000 for school materials
         ▼
┌──────────────────────┐
│ Expense Request DB   │
│ Status: PENDING      │
└────────┬─────────────┘
         │
         │ 2. Notification
         ▼
┌──────────────────────┐
│ Super Admin          │
│ Reviews request      │
└────────┬─────────────┘
         │
         │ Decision?
         │
    ┌────┴────┐
    │         │
[APPROVE]  [REJECT]
    │         │
    │         └─────────────────┐
    │                           │
    │ 3. Create Transaction     │ 3. Update Status
    ▼                           │    Status: REJECTED
┌──────────────────────┐        │    No funds transfer
│ Blockchain Record    │        ▼
│ • From: EDU Wallet   │   ┌───────────────┐
│ • To: Vendor         │   │ Notify Officer│
│ • Amount: $25,000    │   │ With reason   │
│ • Hash: 0xdef456...  │   └───────────────┘
└────────┬─────────────┘
         │
         │ 4. Transfer Funds
         ▼
┌──────────────────────┐
│ Update Balances      │
│ EDU: -$25,000        │
│ Vendor: +$25,000     │
│ Project Spent: +$25k │
└────────┬─────────────┘
         │
         │ 5. Notify
         ▼
┌──────────────────────┐
│ Officer Dashboard    │
│ ✓ Request Approved   │
│ 💰 Funds Transferred │
└──────────────────────┘
```

### 3. Citizen Tax Payment

```
┌──────────────┐
│   Citizen    │
│  John Doe    │
└──────┬───────┘
       │
       │ 1. Access Tax Portal
       ▼
┌──────────────────────────┐
│ Tax Payment Form         │
│ • Name: John Doe         │
│ • ID: 12345678          │
│ • Type: Income Tax      │
│ • Amount: $15,000       │
│ • Method: M-Pesa        │
└──────┬───────────────────┘
       │
       │ 2. Submit Payment
       ▼
┌──────────────────────────┐
│ Backend Processing       │
│ • Validate data          │
│ • Generate receipt #     │
│ • Create transaction     │
└──────┬───────────────────┘
       │
       │ 3. Record on Blockchain
       ▼
┌──────────────────────────┐
│ Blockchain Transaction   │
│ • From: John's wallet    │
│ • To: TREASURY          │
│ • Amount: $15,000       │
│ • Hash: 0x789abc...     │
│ • IMMUTABLE ✓           │
└──────┬───────────────────┘
       │
       │ 4. Save to Database
       ▼
┌──────────────────────────┐
│ Tax Payment Record       │
│ Receipt: TAX-20250210-01│
│ Status: COMPLETED        │
└──────┬───────────────────┘
       │
       │ 5. Return Receipt
       ▼
┌──────────────────────────┐
│ Citizen Confirmation     │
│ ✓ Payment Successful     │
│ 📄 Receipt: TAX-...-01  │
│ 🔗 Hash: 0x789abc...    │
│ 💰 Amount: $15,000      │
└──────────────────────────┘
```

### 4. Citizen Report Submission

```
┌──────────────┐
│   Citizen    │
│  Jane Smith  │
└──────┬───────┘
       │
       │ 1. Notice suspicious activity
       ▼
┌──────────────────────────┐
│ Report Portal            │
│ • Type: Tax irregularity │
│ • Subject: Suspicious TX │
│ • Description: Details   │
│ • TX Hash: Reference     │
└──────┬───────────────────┘
       │
       │ 2. Submit Report
       ▼
┌──────────────────────────┐
│ Report Database          │
│ Status: PENDING          │
│ Created: 2025-02-10     │
└──────┬───────────────────┘
       │
       │ 3. Notification
       ▼
┌──────────────────────────┐
│ Finance Office Dashboard │
│ 🔔 New Report (#7)      │
└──────┬───────────────────┘
       │
       │ 4. Admin Reviews
       ▼
┌──────────────────────────┐
│ Investigation Process    │
│ • Review details         │
│ • Check blockchain       │
│ • Verify transaction     │
│ • Investigate claim      │
└──────┬───────────────────┘
       │
       │ 5. Update Status
       ▼
┌──────────────────────────┐
│ Report Updated           │
│ Status: REVIEWED         │
│ Admin Notes: Findings    │
└──────┬───────────────────┘
       │
       │ 6. Resolution
       ▼
┌──────────────────────────┐
│ Status: RESOLVED         │
│ Action: Corrective steps │
│ Transparency: Public log │
└──────────────────────────┘
```

---

## 🔐 Security Layers

```
┌─────────────────────────────────────────────────────┐
│                Application Layer                     │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 1: Authentication (JWT Tokens)          │ │
│  │ • Access Token (30 min expiry)                │ │
│  │ • Refresh Token (7 days)                      │ │
│  │ • Token revocation on logout                  │ │
│  └───────────────────────────────────────────────┘ │
│                                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 2: Authorization (Role-Based)           │ │
│  │ • Super Admin → Full access                   │ │
│  │ • Ministry Admin → Ministry scope             │ │
│  │ • Ministry Officer → Limited operations       │ │
│  │ • Citizen → Public services only              │ │
│  └───────────────────────────────────────────────┘ │
│                                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 3: Password Security                    │ │
│  │ • Bcrypt hashing (12 rounds)                  │ │
│  │ • Automatic salt generation                   │ │
│  │ • Constant-time comparison                    │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                Data Layer                            │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 4: SQL Injection Prevention             │ │
│  │ • ORM parameterized queries                   │ │
│  │ • No raw SQL strings                          │ │
│  │ • Input validation via Pydantic               │ │
│  └───────────────────────────────────────────────┘ │
│                                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 5: Blockchain Integrity                 │ │
│  │ • Immutable transaction records               │ │
│  │ • Hash chain verification                     │ │
│  │ • Tamper detection                            │ │
│  │ • Cryptographic signatures                    │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              Network Layer                           │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 6: CORS Protection                      │ │
│  │ • Configured allowed origins                  │ │
│  │ • Credential validation                       │ │
│  │ • Pre-flight request handling                 │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│            Audit Layer                               │
│  ┌───────────────────────────────────────────────┐ │
│  │ Level 7: Activity Logging                     │ │
│  │ • All actions timestamped                     │ │
│  │ • User attribution                            │ │
│  │ • Complete audit trail                        │ │
│  │ • Blockchain-verified transparency            │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                         │
└────────────┬───────────────────────────────────────────────────┘
             │
        [HTTP Request]
             │
             ▼
┌────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                          │
├────────────────────────────────────────────────────────────────┤
│  1. Middleware Processing                                      │
│     • CORS validation                                          │
│     • Request logging                                          │
│     • Error handling                                           │
│                                                                 │
│  2. Authentication                                             │
│     • JWT token extraction                                     │
│     • Signature verification                                   │
│     • Expiry check                                             │
│     • User identification                                      │
│                                                                 │
│  3. Authorization                                              │
│     • Role extraction                                          │
│     • Permission check                                         │
│     • Endpoint access validation                               │
│                                                                 │
│  4. Request Validation                                         │
│     • Pydantic schema validation                               │
│     • Type checking                                            │
│     • Business rule validation                                 │
│                                                                 │
│  5. Business Logic                                             │
│     • Process request                                          │
│     • Database operations                                      │
│     • Blockchain operations                                    │
│                                                                 │
│  6. Response Formation                                         │
│     • Serialize data                                           │
│     • Format response                                          │
│     • Set status code                                          │
└────────────┬───────────────────────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌─────────────┐ ┌──────────────┐
│  Database   │ │  Blockchain  │
│  Operation  │ │  Operation   │
└─────┬───────┘ └──────┬───────┘
      │                │
      │ CRUD           │ Add Transaction
      │                │ Mine Block
      │                │ Verify Chain
      ▼                ▼
┌─────────────┐ ┌──────────────┐
│ PostgreSQL  │ │ blockchain   │
│  Database   │ │  .json       │
└─────┬───────┘ └──────┬───────┘
      │                │
      └────────┬───────┘
               │
               ▼
      [Response Data]
               │
               ▼
┌────────────────────────────────────────────────────────────────┐
│                    WEBSOCKET NOTIFICATION                       │
│  If applicable, notify connected clients in real-time          │
└────────────┬───────────────────────────────────────────────────┘
             │
             ▼
    [HTTP Response to Client]
             │
             ▼
┌────────────────────────────────────────────────────────────────┐
│                        FRONTEND UPDATE                          │
│  • Update UI with new data                                     │
│  • Show toast notification                                     │
│  • Refresh affected components                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema Visual

```
┌──────────────────┐       ┌──────────────────┐
│     users        │       │   ministries     │
├──────────────────┤       ├──────────────────┤
│ • id (PK)        │       │ • id (PK)        │
│ • office_name    │◄──────┤ • name           │
│ • wallet_address │  N:1  │ • code           │
│ • hashed_password│       │ • wallet_address │
│ • role           │       │ • allocated_amt  │
│ • ministry_id(FK)│       │ • used_funds     │
└──────────────────┘       └────────┬─────────┘
                                    │
                                    │ 1:N
                      ┌─────────────┼─────────────┐
                      │                           │
                      ▼                           ▼
            ┌──────────────────┐       ┌──────────────────┐
            │    projects      │       │ expense_requests │
            ├──────────────────┤       ├──────────────────┤
            │ • id (PK)        │       │ • id (PK)        │
            │ • ministry_id(FK)│       │ • ministry_id(FK)│
            │ • name           │◄──┐   │ • project_id (FK)│
            │ • budget         │   │   │ • amount         │
            │ • spent          │   │   │ • purpose        │
            │ • status         │   │   │ • status         │
            └────────┬─────────┘   │   │ • requested_by   │
                     │             │   │ • approved_by    │
                     │ 1:N         └───┤ • transaction_   │
                     └─────────────────│   hash           │
                                       └──────────────────┘

┌──────────────────┐       
│  tax_payments    │       
├──────────────────┤       
│ • id (PK)        │       
│ • receipt_number │       
│ • taxpayer_name  │       
│ • id_number      │       
│ • tax_type       │       
│ • amount         │       
│ • payment_method │       
│ • transaction_   │       
│   hash           │       
└──────────────────┘       

┌──────────────────┐
│     reports      │
├──────────────────┤
│ • id (PK)        │
│ • report_type    │
│ • reported_by    │
│ • subject        │
│ • description    │
│ • status         │
│ • reviewed_by    │
│ • admin_notes    │
└──────────────────┘
```

---

## ⛓️ Blockchain Structure Visual

```
┌──────────────────────────────────────────────────────────────┐
│                     BLOCKCHAIN CHAIN                          │
└──────────────────────────────────────────────────────────────┘

Block 0 (Genesis)
┌────────────────────────────────────────┐
│ ID: 0                                  │
│ Timestamp: 2025-01-01T00:00:00Z       │
│ Previous Hash: 0                       │
│ Transactions: []                       │
│ Validator: SYSTEM                      │
│ Current Hash: 0xabc123...             │
└───────────┬────────────────────────────┘
            │ Links via hash
            ▼
Block 1
┌────────────────────────────────────────┐
│ ID: 1                                  │
│ Timestamp: 2025-02-01T12:00:00Z       │
│ Previous Hash: 0xabc123... ◄──────────┼─ Must match Block 0's hash
│ Transactions: [                        │
│   {                                    │
│     sender: "SYSTEM",                  │
│     recipient: "0xEDU123...",         │
│     amount: 100000,                    │
│     purpose: "Budget Allocation",      │
│     transaction_id: "tx001"            │
│   }                                    │
│ ]                                      │
│ Validator: FinanceOffice               │
│ Current Hash: 0xdef456...             │
└───────────┬────────────────────────────┘
            │ Links via hash
            ▼
Block 2
┌────────────────────────────────────────┐
│ ID: 2                                  │
│ Timestamp: 2025-02-05T14:30:00Z       │
│ Previous Hash: 0xdef456... ◄──────────┼─ Must match Block 1's hash
│ Transactions: [                        │
│   {                                    │
│     sender: "0xEDU123...",            │
│     recipient: "0xVENDOR...",         │
│     amount: 25000,                     │
│     purpose: "School materials",       │
│     ministry_id: 1,                    │
│     project_id: 5,                     │
│     transaction_id: "tx002"            │
│   },                                   │
│   {                                    │
│     sender: "0xCITIZEN...",           │
│     recipient: "TREASURY",             │
│     amount: 15000,                     │
│     purpose: "Income Tax",             │
│     transaction_id: "tx003"            │
│   }                                    │
│ ]                                      │
│ Validator: FinanceOffice               │
│ Current Hash: 0xghi789...             │
└───────────┬────────────────────────────┘
            │
            ▼
         [More blocks...]
            │
            ▼
Block N (Latest)
┌────────────────────────────────────────┐
│ ID: N                                  │
│ Timestamp: 2025-02-10T16:00:00Z       │
│ Previous Hash: 0x...                   │
│ Transactions: [...]                    │
│ Validator: FinanceOffice               │
│ Current Hash: 0x...                   │
│                                        │
│ ⚠️ IMMUTABLE - Cannot be altered      │
│ ✓ VERIFIED - Hash chain intact        │
│ ✓ TRANSPARENT - Publicly viewable     │
└────────────────────────────────────────┘
```

---

## 🎨 User Interface Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         LOGIN PAGE                           │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  [NASA Logo]                                          │ │
│  │                                                        │ │
│  │  Username: [________________]                         │ │
│  │  Password: [________________]                         │ │
│  │                                                        │ │
│  │           [Login Button]                              │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ Login successful
                       ▼
           ┌───────────────────────┐
           │   Which role?         │
           └───────────┬───────────┘
                       │
        ┌──────────────┼──────────────┬─────────────┐
        │              │              │             │
        ▼              ▼              ▼             ▼
┌──────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐
│ Super Admin  │ │  Ministry  │ │ Ministry │ │ Citizen  │
│  Dashboard   │ │   Admin    │ │ Officer  │ │Dashboard │
└──────┬───────┘ └─────┬──────┘ └────┬─────┘ └────┬─────┘
       │               │              │            │
       ▼               ▼              ▼            ▼
┌──────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐
│ • Ministries │ │ • My       │ │ • Submit │ │ • Pay Tax│
│ • Budget     │ │   Ministry │ │   Expense│ │ • View   │
│   Allocation │ │ • Projects │ │   Request│ │   Receipt│
│ • Approve    │ │ • Budget   │ │ • Track  │ │ • Submit │
│   Expenses   │ │   Overview │ │   Status │ │   Report │
│ • Review     │ │ • Trans.   │ │ • View   │ │ • Public │
│   Reports    │ │   History  │ │   Projects│ │   Transparency │
│ • View       │ │            │ │          │ │         │
│   Blockchain │ │            │ │          │ │         │
│ • Analytics  │ │            │ │          │ │         │
└──────────────┘ └────────────┘ └──────────┘ └─────────┘
```

---

## 📦 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                │
└─────────────────────────────────────────────────────────┘

                    [Internet]
                         │
                         ▼
            ┌────────────────────────┐
            │    Load Balancer       │
            │     (Nginx)            │
            └───────┬────────────────┘
                    │
        ┌───────────┼───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Frontend   │        │   Frontend   │
│   Server 1   │        │   Server 2   │
│   (React)    │        │   (React)    │
└──────┬───────┘        └──────┬───────┘
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
          ┌────────────────┐
          │  API Gateway   │
          │   (FastAPI)    │
          └────────┬───────┘
                   │
       ┌───────────┼───────────┐
       │                       │
       ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  Backend 1   │        │  Backend 2   │
│  (Uvicorn)   │        │  (Uvicorn)   │
└──────┬───────┘        └──────┬───────┘
       │                       │
       └───────────┬───────────┘
                   │
       ┌───────────┼───────────┐
       │                       │
       ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  PostgreSQL  │        │  Blockchain  │
│  (Primary)   │        │  Storage     │
│              │        │  (Distributed│
│  ┌────────┐  │        │   JSON)      │
│  │Replica │  │        │              │
│  └────────┘  │        └──────────────┘
└──────────────┘

       ┌───────────┐
       │   Redis   │
       │  (Cache)  │
       └───────────┘

       ┌───────────┐
       │ Monitoring│
       │ (Grafana) │
       └───────────┘
```

---

## 🚀 Getting Started - Visual Checklist

```
□ Step 1: Prerequisites
  □ Python 3.11+ installed
  □ Node.js 18+ installed
  □ Git installed

□ Step 2: Clone Repository
  □ git clone <repo-url>
  □ cd NASA

□ Step 3: Backend Setup
  □ cd gok_backend
  □ python -m venv ../.venv
  □ Activate virtual environment
  □ pip install -r requirements.txt
  □ python database_init.py
  □ python create_test_user.py

□ Step 4: Frontend Setup
  □ cd ../federal-ledger
  □ npm install

□ Step 5: Start Servers
  □ Terminal 1: python gok_backend/main.py
  □ Terminal 2: npm run dev (in federal-ledger/)

□ Step 6: Access Application
  □ Open http://localhost:5173
  □ Login with test credentials
  □ Explore the system!

✓ You're ready to use NASA!
```

---

## 📚 Documentation Navigator

```
┌────────────────────────────────────────────────┐
│         DOCUMENTATION STRUCTURE                 │
└────────────────────────────────────────────────┘

README.md (Start here!)
  │
  ├─→ QUICK_REFERENCE.md
  │   └─ For: Quick tasks and common operations
  │   └─ Time: 5-10 minutes
  │
  ├─→ PROJECT_DOCUMENTATION.md
  │   └─ For: Complete system understanding
  │   └─ Time: 30-45 minutes
  │
  ├─→ TECHNICAL_ARCHITECTURE.md
  │   └─ For: Developers and technical staff
  │   └─ Time: 45-60 minutes
  │
  ├─→ README_STARTUP.txt
  │   └─ For: First-time setup
  │   └─ Time: 5 minutes
  │
  └─→ REPORT_SYSTEM_GUIDE.txt
      └─ For: Using the reporting system
      └─ Time: 10 minutes
```

---

**Last Updated:** February 10, 2026  
**Version:** 2.0  
**Status:** Active Development

---


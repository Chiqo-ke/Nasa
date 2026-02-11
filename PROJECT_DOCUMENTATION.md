# NASA - National Financial Blockchain Administration System

## 📋 Table of Contents
- [Overview](#overview)
- [What It Is](#what-it-is)
- [What It Does](#what-it-does)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

**NASA** (National Financial Blockchain Administration System) is a comprehensive government financial management platform that leverages blockchain technology to ensure transparency, accountability, and security in public fund management. The system provides a complete solution for managing government ministries, budgets, projects, tax payments, and citizen engagement.

### Project Goals
- **Transparency**: All financial transactions are recorded on an immutable blockchain
- **Accountability**: Complete audit trail of fund allocation and spending
- **Efficiency**: Streamlined expense request and approval workflows
- **Citizen Engagement**: Public reporting system for suspicious activities
- **Real-time Monitoring**: Live updates on financial activities across ministries

---

## 🔍 What It Is

NASA is a **full-stack web application** consisting of:

1. **Backend API Server** - Built with FastAPI (Python)
2. **Multiple Frontend Interfaces**:
   - Traditional HTML/CSS/JavaScript portal
   - Modern React TypeScript dashboard (Federal Ledger)
   - React finance portal
3. **Custom Blockchain Engine** - For transparent transaction recording
4. **Database System** - PostgreSQL/SQLite with SQLAlchemy ORM
5. **Real-time Communication** - WebSocket support for live updates

The system simulates a national government financial administration system where:
- Government offices/ministries can register and receive wallet addresses
- Funds are allocated from a central treasury to various ministries
- Ministries create projects and submit expense requests
- Citizens can pay taxes and report suspicious activities
- All transactions are recorded on an immutable blockchain

---

## 💼 What It Does

### Core Functionalities

### 1. **Ministry Management**
- Dynamic registration of government ministries (Education, Health, Finance, etc.)
- Automatic wallet address generation for each ministry
- Budget allocation and tracking
- Ministry-specific dashboards showing:
  - Allocated budget
  - Used funds
  - Remaining balance
  - Active projects
  - Recent transactions

### 2. **Project Management**
- Create and track government projects under each ministry
- Project budget allocation and spending monitoring
- Project status tracking (Planning, In Progress, Completed, On Hold, Cancelled)
- Timeline management with start/end dates
- Per-project expense categorization

### 3. **Expense Request Workflow**
- Ministry officers submit expense requests
- Multi-level approval system
- Expense categories (Infrastructure, Salaries, Equipment, etc.)
- Automatic blockchain recording upon approval
- Rejection handling with reason tracking
- Real-time status updates via WebSocket

### 4. **Tax Payment System**
- Citizens can pay various types of taxes:
  - Income Tax
  - VAT (Value Added Tax)
  - Corporate Tax
  - Property Tax
  - Excise Tax
- Receipt generation with unique receipt numbers
- Payment method tracking (M-Pesa, Card, Bank Transfer)
- Transaction hash recording for blockchain verification
- Payment history and reporting

### 5. **Citizen Reporting System**
- Public portal for reporting suspicious financial activities
- Two types of reports:
  - Tax payment irregularities
  - General citizen concerns
- Admin review and resolution workflow
- Status tracking (Pending → Reviewed → Resolved)
- Admin notes and investigation tracking

### 6. **Blockchain Transaction Recording**
- Every financial transaction is recorded on the blockchain
- Immutable transaction history
- Transaction details include:
  - Sender and recipient wallet addresses
  - Amount transferred
  - Purpose/description
  - Ministry and project linkage
  - Approval authority
  - Timestamp
  - Unique transaction hash
- Block mining with validator assignment
- Genesis block initialization

### 7. **Authentication & Authorization**
- JWT-based authentication system
- Access and refresh token management
- Role-based access control (RBAC):
  - Super Admin - Full system access
  - Ministry Admin - Ministry-level management
  - Ministry Officer - Project and expense management
  - Citizen - Tax payments and reporting
- Secure password hashing (bcrypt)
- Token revocation support
- Session management

### 8. **Real-time Updates**
- WebSocket connections for live data
- Automatic balance updates when transactions occur
- Real-time notification system
- Active connection management per wallet address

### 9. **Audit & Transparency**
- Complete transaction history
- User activity logging
- Report management system
- Blockchain verification
- Financial dashboards with KPIs:
  - Total transaction volume
  - Number of transactions
  - Pending transactions
  - Active wallets
  - Blockchain height

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   HTML/CSS   │  │    React     │  │   Federal    │      │
│  │  JavaScript  │  │   Finance    │  │   Ledger     │      │
│  │   Portal     │  │   Portal     │  │  (React TS)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/HTTPS + WebSocket
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   API GATEWAY LAYER                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│                     FastAPI Server                           │
│                  (Python 3.x + Uvicorn)                      │
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │           CORS Middleware                         │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│   ENDPOINT   │ │  ENDPOINT   │ │  ENDPOINT    │
│   ROUTERS    │ │  ROUTERS    │ │  ROUTERS     │
├──────────────┤ ├─────────────┤ ├──────────────┤
│              │ │             │ │              │
│ Core API     │ │ Ministry    │ │ Tax          │
│ (Auth,       │ │ Management  │ │ Payments     │
│ Users,       │ │ (Ministries,│ │ (Tax Pay,    │
│ Blockchain,  │ │ Projects,   │ │ Reports)     │
│ Reports)     │ │ Expenses)   │ │              │
└──────┬───────┘ └──────┬──────┘ └──────┬───────┘
       │                │               │
       └────────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│   BUSINESS   │ │   BUSINESS  │ │   BUSINESS   │
│    LOGIC     │ │    LOGIC    │ │    LOGIC     │
├──────────────┤ ├─────────────┤ ├──────────────┤
│              │ │             │ │              │
│ auth.py      │ │blockchain.py│ │ utils.py     │
│ (JWT,        │ │ (Block,     │ │ (Helpers,    │
│ Password,    │ │ Chain,      │ │ Notifs)      │
│ Tokens)      │ │ Mining)     │ │              │
└──────┬───────┘ └──────┬──────┘ └──────┬───────┘
       │                │               │
       └────────────────┼───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│                   SQLAlchemy ORM                             │
│                   (models.py)                                 │
│                                                               │
│  ┌───────┐ ┌─────────┐ ┌────────┐ ┌──────────┐ ┌────────┐ │
│  │ User  │ │Ministry │ │Project │ │ Expense  │ │  Tax   │ │
│  │ Model │ │ Model   │ │ Model  │ │ Request  │ │Payment │ │
│  └───────┘ └─────────┘ └────────┘ └──────────┘ └────────┘ │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   PERSISTENCE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│              SQLite / PostgreSQL Database                    │
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Tables: users, ministries, projects,             │       │
│  │          expense_requests, tax_payments, reports  │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   BLOCKCHAIN STORAGE                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│                   blockchain.json                            │
│             (Immutable Transaction Ledger)                   │
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Blocks: [Genesis Block, Block 1, Block 2, ...]  │       │
│  │  Each Block Contains:                             │       │
│  │    - Block ID, Timestamp, Previous Hash          │       │
│  │    - Transactions Array                          │       │
│  │    - Validator Address                           │       │
│  │    - Nonce, Current Hash                         │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

1. **User Authentication**:
   ```
   Client → POST /token → Auth Module → Database → JWT Token → Client
   ```

2. **Transaction Processing**:
   ```
   Client → POST /transaction → Validate → Add to Blockchain 
   → Save to Database → Notify via WebSocket → Update Balances
   ```

3. **Ministry Budget Allocation**:
   ```
   Admin → POST /ministries/{id}/allocate → Validate Budget 
   → Create Blockchain Transaction → Update Ministry Balance 
   → Save to Database → Real-time Update via WebSocket
   ```

4. **Expense Request Workflow**:
   ```
   Ministry Officer → POST /expense-requests → Pending Status
   → Super Admin → PUT /expense-requests/{id} → Approve
   → Create Blockchain Transaction → Update Project Spent
   → Transfer Funds → Notify Ministry → Complete
   ```

---

## ⚙️ How It Works

### 1. System Initialization

**Database Setup**:
```bash
python gok_backend/database_init.py
```
- Creates all necessary database tables
- Sets up relationships and constraints
- Initializes the blockchain with a genesis block

**Creating Initial Users**:
```bash
python gok_backend/create_test_user.py
```
- Creates test users with different roles
- Generates wallet addresses
- Hashes passwords securely

### 2. Authentication Flow

```python
# User Login Process
1. User submits credentials (office_name + password)
2. System verifies credentials against hashed password in database
3. If valid:
   - Generate access token (expires in 30 minutes)
   - Generate refresh token (expires in 7 days)
   - Return tokens + user info (wallet_address, role, ministry_id)
4. Client stores tokens in localStorage
5. All subsequent requests include: Authorization: Bearer <access_token>
6. When access token expires, use refresh token to get new access token
```

### 3. Ministry Registration & Budget Allocation

```python
# Ministry Creation Process
1. Super Admin creates ministry with:
   - Name (e.g., "Ministry of Education")
   - Type (Education, Health, Finance, etc.)
   - Description
   - Icon and color for UI
   
2. System automatically:
   - Generates unique ministry code (e.g., "EDU-001")
   - Creates unique wallet address
   - Sets initial budget to 0
   
3. Budget Allocation:
   - Super Admin allocates budget to ministry
   - Creates blockchain transaction: SYSTEM → Ministry Wallet
   - Updates ministry.allocated_budget
   - Records transaction with purpose and approver
   
4. Ministry can now:
   - Create projects
   - Submit expense requests
   - Track spending
```

### 4. Project Management & Expense Workflow

```python
# Project Creation
1. Ministry Admin creates project:
   - Project name and description
   - Allocated budget from ministry funds
   - Timeline (start/end dates)
   
2. Project Status Lifecycle:
   Planning → In Progress → Completed
   (Can also be On Hold or Cancelled)

# Expense Request Process
1. Ministry Officer submits expense request:
   - Amount needed
   - Purpose/description
   - Category (Infrastructure, Salaries, Equipment, etc.)
   - Optional: Link to specific project
   
2. Status: "Pending"
   - Appears in Super Admin dashboard
   
3. Super Admin reviews:
   Option A - Approve:
     - Status changes to "Approved"
     - Blockchain transaction created
     - Funds transferred from ministry to recipient
     - Project.spent updated
     - Ministry.used_funds updated
     - Transaction hash recorded
     
   Option B - Reject:
     - Status changes to "Rejected"
     - Rejection reason recorded
     - No funds transferred
     
4. Real-time notification sent to ministry via WebSocket
```

### 5. Blockchain Transaction Recording

```python
# Transaction Creation
1. Transaction data collected:
   {
     "sender": "ministry_wallet_address",
     "recipient": "vendor_wallet_address",
     "amount": 50000.00,
     "purpose": "School construction materials",
     "approved_by": "FinanceOffice",
     "ministry_id": 1,
     "ministry_name": "Ministry of Education",
     "project_id": 5,
     "category": "Infrastructure",
     "expense_request_id": 12
   }

2. Validation:
   - Check required fields
   - Verify sender wallet has sufficient balance
   - Validate amount is positive (or negative for refunds)
   
3. Add to pending_transactions pool

4. Mine Block:
   - Collect all pending transactions
   - Create new block with:
     * Unique block_id (sequential)
     * Current timestamp
     * Previous block's hash (chain linkage)
     * All transactions
     * Validator (miner address)
     * Nonce for proof of work
   - Calculate block hash (SHA-256)
   
5. Add block to chain:
   - Append to blockchain.chain list
   - Clear pending_transactions
   - Save to blockchain.json file
   - Notify all connected clients via WebSocket

6. Update balances:
   - Deduct from sender wallet
   - Add to recipient wallet
```

### 6. Tax Payment System

```python
# Citizen Tax Payment
1. Citizen accesses tax payment portal
2. Fills in details:
   - Personal info (name, ID, phone, email)
   - Tax type (Income, VAT, Corporate, Property, Excise)
   - Amount to pay
   - Payment method (M-Pesa, Card, Bank)
   
3. System processes:
   - Generate unique receipt number
   - Create tax payment record in database
   - Create blockchain transaction (Citizen → Government Treasury)
   - Record transaction hash
   - Status set to "Completed"
   
4. Citizen receives:
   - Receipt number
   - Payment confirmation
   - Transaction hash for verification
   
5. Payment appears in:
   - Government dashboard (total tax revenue)
   - Blockchain (transparent public record)
   - Tax payment history
```

### 7. Citizen Reporting System

```python
# Report Submission
1. Citizen identifies suspicious activity
2. Navigates to report portal
3. Submits report with:
   - Report type (Tax Payment irregularity or General concern)
   - Reporter name/email
   - Subject line
   - Detailed description
   - Optional: Transaction hash reference
   
4. System creates report:
   - Status: "Pending"
   - Timestamp recorded
   - Stored in database
   
5. Admin Review Process:
   - Finance Office logs in
   - Accesses Reports dashboard
   - Views all reports (filtered by status)
   - Clicks "View Details" on specific report
   - Updates status: Pending → Reviewed → Resolved
   - Adds admin notes (investigation findings)
   
6. Report tracking:
   - Statistics: Total, Pending, Reviewed, Resolved counts
   - Auto-refresh every 30 seconds
   - Full audit trail maintained
```

### 8. Real-time WebSocket Communication

```python
# WebSocket Connection
1. Client connects:
   ws://localhost:8001/ws/{wallet_address}
   
2. Server accepts connection:
   - Stores in active_connections dict
   - Adds to connection manager
   
3. Events that trigger WebSocket messages:
   - New transaction created
   - Block mined
   - Budget allocated
   - Expense approved/rejected
   - Balance updated
   
4. Message format:
   {
     "type": "transaction",
     "data": {
       "action": "balance_update",
       "wallet_address": "0xABC123...",
       "new_balance": 150000.00,
       "transaction_id": "abc123def456"
     }
   }
   
5. Client receives and processes:
   - Updates UI in real-time
   - Shows notifications
   - Refreshes balance displays
   
6. Connection cleanup:
   - On disconnect, remove from active_connections
   - Graceful error handling
```

### 9. Data Persistence

**Database Tables**:

1. **users** - Authentication and user management
2. **ministries** - Government ministry records
3. **projects** - Ministry projects
4. **expense_requests** - Expense approval workflow
5. **tax_payments** - Citizen tax payment history
6. **reports** - Suspicious activity reports

**Blockchain Storage**:
- `blockchain.json` - Immutable transaction ledger
- `validators.json` - Approved validators
- `wallets.json` - Wallet balances (cache)

**Migrations**:
- Alembic for database schema versioning
- Migration scripts in `alembic/versions/`

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.140.0
- **Language**: Python 3.11+
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.x
- **Authentication**: JWT (python-jose)
- **Hashing**: Passlib with bcrypt
- **ASGI Server**: Uvicorn 0.34.0
- **WebSocket**: FastAPI native WebSocket support
- **CORS**: FastAPI CORS middleware
- **Migrations**: Alembic

### Frontend (Multiple Implementations)

**Traditional Portal** (NASA folder):
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- Simple HTTP Server (Python)

**Federal Ledger** (Modern dashboard):
- React 18
- TypeScript
- Vite (build tool)
- Tailwind CSS
- shadcn/ui components
- React Query (TanStack Query)
- Axios for API calls
- React Router for navigation

**NASA Finance React**:
- React
- TypeScript
- Vite
- Tailwind CSS

### Blockchain
- Custom implementation in Python
- SHA-256 hashing
- Proof-of-work concept
- JSON persistence

### Development Tools
- **Package Management**: pip, npm, bun
- **Version Control**: Git
- **Code Quality**: Flake8, ESLint
- **API Testing**: Postman, curl
- **Database Tools**: SQLAlchemy, Alembic

### Deployment
- **Process Manager**: PM2 (for Node.js frontends)
- **Server**: Uvicorn (ASGI)
- **Environment**: Python virtual environment (.venv)

---

## ✨ Key Features

### 🔐 Security Features
1. **JWT Authentication** - Secure token-based auth
2. **Password Hashing** - Bcrypt with salt
3. **Token Revocation** - Blacklist for logged-out tokens
4. **Role-Based Access** - Granular permissions
5. **CORS Protection** - Configured allowed origins
6. **SQL Injection Prevention** - ORM parameterized queries
7. **Activity Logging** - User action audit trail

### 🌐 Multi-Role Support
- **Super Admin**: Full system control, budget allocation, ministry management
- **Ministry Admin**: Ministry-level management, project creation
- **Ministry Officer**: Expense requests, project updates
- **Citizen**: Tax payments, report submission, public transparency view

### 📊 Dashboard & Analytics
- Real-time KPI cards (Total Volume, Transactions, Pending)
- Transaction activity feed
- System status monitoring (Wallets, Blocks, Network)
- Ministry-specific dashboards
- Financial overview charts

### 🔄 Real-time Updates
- WebSocket connections for live data
- Instant balance updates
- Transaction notifications
- Status change alerts

### 📝 Comprehensive Reporting
- Transaction history with filters
- Expense request tracking
- Tax payment receipts
- Suspicious activity reports
- Ministry financial reports

### 🎨 Modern UI/UX
- Responsive design (mobile, tablet, desktop)
- Dark mode support (Federal Ledger)
- Accessible components (ARIA labels)
- Loading states and error handling
- Toast notifications
- Modal dialogs for forms

---

## 👥 User Roles

### 1. Super Admin
**Access**: Full system access

**Capabilities**:
- Create and manage ministries
- Allocate budgets to ministries
- Approve/reject expense requests
- View all transactions across system
- Manage users and roles
- Review citizen reports
- Access complete blockchain history
- System configuration

**Login**: FinanceOffice / finance2025

---

### 2. Ministry Admin
**Access**: Ministry-level management

**Capabilities**:
- View ministry dashboard
- Create and manage projects
- Submit expense requests
- View ministry transactions
- Monitor budget usage
- Manage ministry officers
- View project status

**Login**: EducationOffice / education2025, HealthcareOffice / healthcare2025

---

### 3. Ministry Officer
**Access**: Project and expense management

**Capabilities**:
- Submit expense requests
- Update project information
- View project budgets
- Track expense status
- View ministry transactions

---

### 4. Citizen
**Access**: Public services

**Capabilities**:
- Pay taxes online
- View tax payment history
- Submit suspicious activity reports
- View public transparency dashboard
- Access blockchain verification

---

## 🚀 Installation & Setup

### Prerequisites
```bash
# Required Software
- Python 3.11 or higher
- Node.js 18+ and npm (for React frontends)
- Git
- Virtual environment tool (venv)
```

### Backend Setup

```bash
# 1. Navigate to backend directory
cd c:\Users\nyaga\Documents\NASA\Nasa\gok_backend

# 2. Create virtual environment
python -m venv ../.venv

# 3. Activate virtual environment
# Windows:
..\.venv\Scripts\activate
# Linux/Mac:
source ../.venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize database
python database_init.py

# 6. Create test users
python create_test_user.py

# 7. Run backend server
python main.py

# Server starts on: http://0.0.0.0:8001
# API docs available at: http://localhost:8001/docs
```

### Frontend Setup (Traditional HTML Portal)

```bash
# 1. Navigate to frontend directory
cd c:\Users\nyaga\Documents\NASA\Nasa\NASA

# 2. Start simple HTTP server
python -m http.server 5500

# Frontend available at: http://localhost:5500
# Login page: http://localhost:5500/login.html
```

### Frontend Setup (Federal Ledger - React)

```bash
# 1. Navigate to federal-ledger directory
cd c:\Users\nyaga\Documents\NASA\federal-ledger

# 2. Install dependencies
npm install
# or with bun:
bun install

# 3. Run development server
npm run dev
# or:
bun run dev

# Frontend available at: http://localhost:5173
```

### Automated Start (Windows)

```bash
# Use the batch file for automatic startup
cd c:\Users\nyaga\Documents\NASA\Nasa
START_PROJECT.bat

# This automatically:
# 1. Starts backend server
# 2. Starts frontend server
# 3. Opens browser to login page
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8001
```

### Authentication Endpoints

#### Register User
```http
POST http://localhost:8001/register
Content-Type: application/json

{
  "office_name": "string",
  "password": "string",
  "role": "citizen" | "ministry_officer" | "ministry_admin" | "super_admin",
  "ministry_id": number | null
}

Response:
{
  "message": "User registered successfully",
  "wallet_address": "0xABC123...",
  "role": "citizen",
  "ministry_id": null
}
```

#### Login
```http
POST /token
Content-Type: application/json

{
  "office_name": "FinanceOffice",
  "password": "finance2025"
}

Response:
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "wallet_address": "0xDEF456...",
  "office_name": "FinanceOffice",
  "role": "super_admin",
  "ministry_id": null
}
```

#### Refresh Token
```http
POST /refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Logout
```http
POST /logout
Authorization: Bearer <access_token>

Response:
{
  "message": "Successfully logged out"
}
```

### Ministry Endpoints

#### Get All Ministries
```http
GET /ministries
Authorization: Bearer <access_token>

Response:
[
  {
    "id": 1,
    "name": "Ministry of Education",
    "code": "EDU-001",
    "ministry_type": "education",
    "description": "Manages education sector",
    "wallet_address": "0xEDU123...",
    "allocated_budget": 1000000.00,
    "used_funds": 250000.00,
    "remaining_balance": 750000.00,
    "icon": "GraduationCap",
    "color": "#3b82f6",
    "is_active": true,
    "created_at": "2025-01-15T10:30:00Z",
    "active_projects": 5,
    "total_projects": 8
  }
]
```

#### Create Ministry
```http
POST /ministries
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Ministry of Technology",
  "ministry_type": "technology",
  "description": "Manages technology initiatives",
  "icon": "Cpu",
  "color": "#8b5cf6",
  "allocated_budget": 500000.00
}

Response:
{
  "id": 10,
  "name": "Ministry of Technology",
  "code": "TECH-010",
  "wallet_address": "0xTECH789...",
  ...
}
```

#### Allocate Budget to Ministry
```http
POST /ministries/{ministry_id}/allocate
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "amount": 100000.00,
  "purpose": "Q1 2025 Budget Allocation",
  "approved_by": "FinanceOffice"
}

Response:
{
  "message": "Budget allocated successfully",
  "transaction_id": "abc123def456",
  "new_balance": 850000.00
}
```

### Project Endpoints

#### Create Project
```http
POST /projects
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "ministry_id": 1,
  "name": "School Infrastructure Development",
  "description": "Build 10 new classrooms",
  "budget": 150000.00,
  "start_date": "2025-02-01T00:00:00Z",
  "end_date": "2025-12-31T00:00:00Z"
}

Response:
{
  "id": 5,
  "ministry_id": 1,
  "name": "School Infrastructure Development",
  "budget": 150000.00,
  "spent": 0.00,
  "status": "planning",
  ...
}
```

#### Get Ministry Projects
```http
GET /ministries/{ministry_id}/projects
Authorization: Bearer <access_token>

Response:
[
  {
    "id": 5,
    "name": "School Infrastructure Development",
    "status": "in_progress",
    "budget": 150000.00,
    "spent": 45000.00,
    ...
  }
]
```

### Expense Request Endpoints

#### Submit Expense Request
```http
POST /expense-requests
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "ministry_id": 1,
  "project_id": 5,
  "amount": 25000.00,
  "purpose": "Purchase construction materials",
  "category": "Infrastructure"
}

Response:
{
  "id": 12,
  "status": "pending",
  "requested_by": "EducationOffice",
  ...
}
```

#### Approve Expense Request
```http
PUT /expense-requests/{request_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "approved"
}

Response:
{
  "id": 12,
  "status": "approved",
  "approved_by": "FinanceOffice",
  "approved_at": "2025-02-10T14:30:00Z",
  "transaction_hash": "0x789abc...",
  ...
}
```

### Tax Payment Endpoints

#### Submit Tax Payment
```http
POST /tax-payments
Content-Type: application/json

{
  "taxpayer_name": "John Doe",
  "id_number": "12345678",
  "phone_number": "+254712345678",
  "email": "john@example.com",
  "tax_type": "income",
  "amount": 15000.00,
  "payment_method": "M-Pesa"
}

Response:
{
  "id": 45,
  "receipt_number": "TAX-20250210-000045",
  "status": "completed",
  "transaction_hash": "0xabc123...",
  ...
}
```

#### Get Tax Payment History
```http
GET /tax-payments
Authorization: Bearer <access_token>

Query Parameters:
- id_number: Filter by taxpayer ID
- tax_type: Filter by tax type
- start_date: Filter from date
- end_date: Filter to date

Response:
[
  {
    "receipt_number": "TAX-20250210-000045",
    "taxpayer_name": "John Doe",
    "tax_type": "income",
    "amount": 15000.00,
    "created_at": "2025-02-10T10:00:00Z",
    ...
  }
]
```

### Report Endpoints

#### Submit Report (Public Access)
```http
POST /reports
Content-Type: application/json

{
  "report_type": "citizen_portal",
  "reported_by": "jane@example.com",
  "subject": "Suspicious Transaction",
  "description": "I noticed an unusual payment pattern...",
  "transaction_hash": "0xdef456..."
}

Response:
{
  "id": 7,
  "status": "pending",
  "created_at": "2025-02-10T11:00:00Z",
  ...
}
```

#### Get All Reports (Admin Only)
```http
GET /reports
Authorization: Bearer <access_token>

Query Parameters:
- status: Filter by status (pending, reviewed, resolved)

Response:
[
  {
    "id": 7,
    "report_type": "citizen_portal",
    "subject": "Suspicious Transaction",
    "status": "pending",
    ...
  }
]
```

#### Update Report Status (Admin Only)
```http
PUT /reports/{report_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "reviewed",
  "admin_notes": "Investigated - no irregularities found"
}

Response:
{
  "id": 7,
  "status": "reviewed",
  "reviewed_by": "FinanceOffice",
  "admin_notes": "Investigated - no irregularities found",
  ...
}
```

### Blockchain Endpoints

#### Get Blockchain
```http
GET /blockchain
Authorization: Bearer <access_token>

Response:
{
  "chain": [
    {
      "block_id": "0",
      "timestamp": "2025-01-01T00:00:00Z",
      "previous_hash": "0",
      "transactions": [],
      "validator": "SYSTEM",
      "current_hash": "0abc..."
    },
    ...
  ],
  "length": 45
}
```

#### Get Transactions
```http
GET /transactions
Authorization: Bearer <access_token>

Query Parameters:
- wallet_address: Filter by wallet
- ministry_id: Filter by ministry
- project_id: Filter by project

Response:
[
  {
    "transaction_id": "abc123",
    "sender": "0xDEF456...",
    "recipient": "0xEDU123...",
    "amount": 100000.00,
    "timestamp": "2025-02-01T12:00:00Z",
    "purpose": "Q1 Budget Allocation",
    "ministry_name": "Ministry of Education",
    ...
  }
]
```

#### Get Wallet Balance
```http
GET /balance/{wallet_address}
Authorization: Bearer <access_token>

Response:
{
  "wallet_address": "0xEDU123...",
  "balance": 750000.00,
  "total_received": 1000000.00,
  "total_sent": 250000.00
}
```

### Dashboard Endpoints

#### Get KPIs
```http
GET /kpis
Authorization: Bearer <access_token>

Response:
{
  "total_transactions": 1250,
  "total_volume": 45000000.00,
  "pending_transactions": 12
}
```

#### Get Wallet Count
```http
GET /wallets/count
Authorization: Bearer <access_token>

Response:
{
  "count": 25
}
```

#### Get Block Count
```http
GET /blockchain/blocks/count
Authorization: Bearer <access_token>

Response:
{
  "count": 45
}
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    office_name VARCHAR(255) UNIQUE NOT NULL,
    wallet_address VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'citizen' NOT NULL,
    ministry_id INTEGER REFERENCES ministries(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

### Ministries Table
```sql
CREATE TABLE ministries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    ministry_type VARCHAR(100) NOT NULL,
    description TEXT,
    wallet_address VARCHAR(255) UNIQUE NOT NULL,
    allocated_budget FLOAT DEFAULT 0.0,
    used_funds FLOAT DEFAULT 0.0,
    icon VARCHAR(100),
    color VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ministry_id INTEGER NOT NULL REFERENCES ministries(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    budget FLOAT DEFAULT 0.0,
    spent FLOAT DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'planning',
    start_date DATETIME,
    end_date DATETIME,
    created_by VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Expense Requests Table
```sql
CREATE TABLE expense_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ministry_id INTEGER NOT NULL REFERENCES ministries(id),
    project_id INTEGER REFERENCES projects(id),
    amount FLOAT NOT NULL,
    purpose TEXT NOT NULL,
    category VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    requested_by VARCHAR(255) NOT NULL,
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_by VARCHAR(255),
    approved_at DATETIME,
    rejected_by VARCHAR(255),
    rejected_at DATETIME,
    rejection_reason TEXT,
    transaction_hash VARCHAR(255)
);
```

### Tax Payments Table
```sql
CREATE TABLE tax_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number VARCHAR(100) UNIQUE NOT NULL,
    taxpayer_name VARCHAR(255) NOT NULL,
    id_number VARCHAR(100) NOT NULL,
    phone_number VARCHAR(50),
    email VARCHAR(255),
    tax_type VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(50) DEFAULT 'completed',
    transaction_hash VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Reports Table
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type VARCHAR(100) NOT NULL,
    reported_by VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    transaction_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_by VARCHAR(255),
    admin_notes TEXT
);
```

### Entity Relationships
```
users ──┬──< ministries (one-to-many)
        │
ministries ──┬──< projects (one-to-many)
             ├──< expense_requests (one-to-many)
             └──< users (one-to-many)

projects ──< expense_requests (one-to-many)
```

---

## 🔒 Security Features

### 1. Password Security
- **Hashing Algorithm**: Bcrypt with automatic salting
- **Rounds**: 12 rounds (configurable)
- **Plain text passwords never stored**

### 2. JWT Token Security
- **Access Token**: Short-lived (30 minutes)
- **Refresh Token**: Long-lived (7 days)
- **Signed with**: HS256 algorithm
- **Secret Key**: Stored in environment variables (production)
- **Token Revocation**: Blacklist implemented

### 3. API Security
- **CORS**: Configured allowed origins
- **Authentication Required**: Most endpoints protected
- **Role-Based Access Control**: Enforced at endpoint level
- **SQL Injection**: Prevented by ORM parameterization
- **XSS Protection**: Input sanitization

### 4. Blockchain Integrity
- **Immutable**: Once recorded, cannot be altered
- **Hash Chain**: Each block references previous block's hash
- **Validator**: Each block signed by miner/validator
- **Tamper Detection**: Hash verification

### 5. Audit Trail
- **User Activity Logging**: All actions logged with timestamp
- **Transaction History**: Complete record maintained
- **Report Tracking**: Full investigation trail
- **Approval Chain**: Who approved what and when

---

## 🚀 Future Enhancements

### Phase 1: Enhanced Security
- [ ] Two-factor authentication (2FA)
- [ ] Biometric authentication
- [ ] IP whitelist/blacklist
- [ ] Rate limiting on API endpoints
- [ ] Advanced encryption for sensitive data

### Phase 2: Advanced Features
- [ ] Email notifications for expense approvals
- [ ] SMS alerts for tax payment confirmations
- [ ] PDF receipt generation
- [ ] Excel export for financial reports
- [ ] Advanced analytics dashboard
- [ ] Predictive budget analysis using AI

### Phase 3: Scalability
- [ ] Redis caching for improved performance
- [ ] PostgreSQL migration for production
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] Load balancing
- [ ] Auto-scaling infrastructure

### Phase 4: Integration
- [ ] Mobile apps (iOS/Android)
- [ ] M-Pesa payment gateway integration
- [ ] Bank API integrations
- [ ] Government ID verification services
- [ ] External audit system integration
- [ ] Public API for third-party developers

### Phase 5: Blockchain Enhancement
- [ ] Consensus mechanism implementation
- [ ] Multi-node blockchain network
- [ ] Smart contracts for automated approvals
- [ ] Inter-blockchain communication
- [ ] Blockchain explorer UI

### Phase 6: User Experience
- [ ] Progressive Web App (PWA)
- [ ] Offline capability
- [ ] Multi-language support
- [ ] Accessibility improvements (WCAG 2.1 AA)
- [ ] Voice commands
- [ ] Chatbot assistant

---

## 📞 Support & Documentation

### Quick Start Guides
- **Backend Setup**: See [Installation & Setup](#installation--setup)
- **API Reference**: Full documentation at `/docs` endpoint
- **User Manual**: `README_STARTUP.txt`
- **Report System**: `REPORT_SYSTEM_GUIDE.txt`

### Troubleshooting

**Port already in use**:
```bash
# Find process using port 8001
netstat -ano | findstr :8001
# Kill the process
taskkill /F /PID <process_id>
```

**Database not initialized**:
```bash
python gok_backend/database_init.py
```

**Module not found**:
```bash
pip install -r gok_backend/requirements.txt
```

**CORS errors**:
- Check allowed origins in `main.py`
- Ensure frontend URL matches allowed origins

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 👨‍💻 Development Team

Developed as a comprehensive government financial management system demonstration.

---

**Last Updated**: February 10, 2026
**Version**: 2.0
**Status**: Active Development

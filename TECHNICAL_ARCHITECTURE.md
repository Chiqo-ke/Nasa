# NASA - Technical Architecture Document

## 📋 Document Purpose

This document provides in-depth technical details about the NASA (National Financial Blockchain Administration System) architecture, design patterns, data flows, and implementation details for developers and technical stakeholders.

---

## 🏛️ System Architecture Overview

### High-Level Architecture

The NASA system follows a **3-tier architecture** pattern:

1. **Presentation Layer** - Multiple frontend implementations
2. **Application Layer** - FastAPI backend with business logic
3. **Data Layer** - Relational database + Blockchain storage

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  Traditional UI  │  │  Federal Ledger  │  │  NASA Finance │ │
│  │  (HTML/CSS/JS)   │  │  (React + TS)    │  │  (React + TS) │ │
│  │                  │  │                  │  │               │ │
│  │  • Login         │  │  • Dashboard     │  │  • Dashboard  │ │
│  │  • Dashboard     │  │  • Ministries    │  │  • Analytics  │ │
│  │  • Tax Payment   │  │  • Projects      │  │  • Reports    │ │
│  │  • Citizen Portal│  │  • Transparency  │  │               │ │
│  │  • Reports       │  │  • Audit Logs    │  │               │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬───────┘ │
│           │                     │                     │         │
└───────────┼─────────────────────┼─────────────────────┼─────────┘
            │                     │                     │
            └──────────┬──────────┴──────────┬──────────┘
                       │                     │
                    HTTP/S                WebSocket
                       │                     │
┌──────────────────────▼─────────────────────▼───────────────────┐
│                   APPLICATION LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                      FastAPI Application                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Middleware Stack                          │  │
│  │  1. CORS Middleware (Origin validation)                  │  │
│  │  2. Request Logging Middleware (Activity tracking)       │  │
│  │  3. Error Handler Middleware (Exception handling)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routers                            │  │
│  │                                                            │  │
│  │  ┌────────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │  Core Router   │  │   Ministry   │  │  Tax Router  │ │  │
│  │  │  (endpoints.py)│  │   Router     │  │              │ │  │
│  │  │                │  │              │  │              │ │  │
│  │  │ • /register    │  │ • /ministries│  │• /tax-payments││  │
│  │  │ • /token       │  │ • /projects  │  │• /reports    │ │  │
│  │  │ • /refresh     │  │ • /expense-  │  │              │ │  │
│  │  │ • /logout      │  │   requests   │  │              │ │  │
│  │  │ • /blockchain  │  │              │  │              │ │  │
│  │  │ • /transactions│  │              │  │              │ │  │
│  │  └────────────────┘  └──────────────┘  └──────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Business Logic Layer                     │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌────────┐ │  │
│  │  │  Auth    │  │Blockchain │  │  Utils   │  │ Conn.  │ │  │
│  │  │  Module  │  │  Module   │  │  Module  │  │Manager │ │  │
│  │  │          │  │           │  │          │  │        │ │  │
│  │  │• JWT     │  │• Block    │  │• Notify  │  │• WS    │ │  │
│  │  │• Hashing │  │• Chain    │  │• Helpers │  │• Active│ │  │
│  │  │• Tokens  │  │• Mining   │  │• Valid.  │  │  Conn. │ │  │
│  │  │• Validate│  │• Verify   │  │          │  │        │ │  │
│  │  └──────────┘  └───────────┘  └──────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
┌─────────────────────────┐  ┌──────────────────────┐
│     DATA LAYER          │  │   BLOCKCHAIN LAYER   │
├─────────────────────────┤  ├──────────────────────┤
│                         │  │                      │
│  SQLAlchemy ORM         │  │  Custom Engine       │
│                         │  │                      │
│  ┌───────────────────┐ │  │  ┌────────────────┐ │
│  │   Models          │ │  │  │ blockchain.json│ │
│  │                   │ │  │  │                │ │
│  │ • UserDB          │ │  │  │ • Blocks       │ │
│  │ • MinistryDB      │ │  │  │ • Transactions │ │
│  │ • ProjectDB       │ │  │  │ • Hashes       │ │
│  │ • ExpenseRequestDB│ │  │  │ • Validators   │ │
│  │ • TaxPaymentDB    │ │  │  └────────────────┘ │
│  │ • ReportDB        │ │  │                      │
│  └─────────┬─────────┘ │  │  ┌────────────────┐ │
│            │           │  │  │ validators.json│ │
│            ▼           │  │  └────────────────┘ │
│  ┌───────────────────┐ │  │                      │
│  │  SQLite/PostgreSQL│ │  │  ┌────────────────┐ │
│  │                   │ │  │  │  wallets.json  │ │
│  │  Database Tables: │ │  │  └────────────────┘ │
│  │  • users          │ │  │                      │
│  │  • ministries     │ │  └──────────────────────┘
│  │  • projects       │ │
│  │  • expense_requests│ │
│  │  • tax_payments   │ │
│  │  • reports        │ │
│  └───────────────────┘ │
│                         │
└─────────────────────────┘
```

---

## 🔧 Technology Stack Details

### Backend Technologies

#### Core Framework
- **FastAPI 0.140.0**
  - Async/await support for high performance
  - Automatic API documentation (OpenAPI/Swagger)
  - Pydantic for data validation
  - Built-in dependency injection

#### Database & ORM
- **SQLAlchemy 2.x**
  - ORM for database abstraction
  - Support for multiple database backends
  - Migration support via Alembic
  - Relationship management
  
- **SQLite** (Development)
  - Zero configuration
  - File-based storage
  - Good for prototyping
  
- **PostgreSQL** (Production ready)
  - ACID compliance
  - Advanced features
  - Scalable

#### Authentication & Security
- **python-jose[cryptography]**
  - JWT token creation/validation
  - HS256 signing algorithm
  
- **passlib[bcrypt]**
  - Password hashing
  - Bcrypt algorithm (12 rounds)
  - Automatic salt generation

#### Server
- **Uvicorn 0.34.0**
  - ASGI server
  - WebSocket support
  - High performance
  - Production ready

### Frontend Technologies

#### Traditional Portal (NASA/)
- **HTML5**: Semantic markup
- **CSS3**: Modern styling, Grid, Flexbox
- **JavaScript ES6+**: Async/await, Fetch API, WebSocket API

#### Modern Dashboard (federal-ledger/)
- **React 18**: Component-based UI
- **TypeScript**: Type safety
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: High-quality components
- **React Query (TanStack)**: Data fetching and caching
- **Axios**: HTTP client with interceptors
- **React Router**: Client-side routing

### Development Tools
- **Alembic**: Database migrations
- **Flake8**: Python linting
- **ESLint**: JavaScript/TypeScript linting
- **Postman**: API testing

---

## 📊 Data Models & Relationships

### Entity Relationship Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         User System                               │
└────────────┬─────────────────────────────────────────────────────┘
             │
             │ 1:N (one user can belong to one ministry)
             │
             ▼
┌────────────────────────────────────────────────────────────────────┐
│  UserDB                                                             │
├────────────────────────────────────────────────────────────────────┤
│  PK: id                                                             │
│  UK: office_name, wallet_address                                   │
│  FK: ministry_id → ministries.id                                   │
│                                                                     │
│  • office_name (login username)                                    │
│  • wallet_address (blockchain identity)                            │
│  • hashed_password (bcrypt)                                        │
│  • role (super_admin, ministry_admin, ministry_officer, citizen)   │
│  • ministry_id (nullable, links to ministry)                       │
│  • is_active, created_at, last_login                               │
└──────────────┬─────────────────────────────────────────────────────┘
               │
               │ N:1 (many users in one ministry)
               │
               ▼
┌────────────────────────────────────────────────────────────────────┐
│  MinistryDB                                                         │
├────────────────────────────────────────────────────────────────────┤
│  PK: id                                                             │
│  UK: name, code, wallet_address                                    │
│                                                                     │
│  • name (e.g., "Ministry of Education")                            │
│  • code (auto-generated, e.g., "EDU-001")                          │
│  • ministry_type (education, health, finance, etc.)                │
│  • description                                                      │
│  • wallet_address (blockchain identity)                            │
│  • allocated_budget (total allocated)                              │
│  • used_funds (total spent)                                        │
│  • remaining_balance (computed: allocated - used)                  │
│  • icon, color (UI customization)                                  │
│  • is_active, created_at, updated_at                               │
└──────────────┬─────────────────────────────────────────────────────┘
               │
               │ 1:N (one ministry has many projects)
               │
               ▼
┌────────────────────────────────────────────────────────────────────┐
│  ProjectDB                                                          │
├────────────────────────────────────────────────────────────────────┤
│  PK: id                                                             │
│  FK: ministry_id → ministries.id                                   │
│                                                                     │
│  • ministry_id (parent ministry)                                   │
│  • name (project title)                                            │
│  • description                                                      │
│  • budget (allocated to project)                                   │
│  • spent (total expenses)                                          │
│  • status (planning, in_progress, completed, on_hold, cancelled)   │
│  • start_date, end_date                                            │
│  • created_by, created_at, updated_at                              │
└──────────────┬───────┬─────────────────────────────────────────────┘
               │       │
               │       │ 1:N (one project has many expenses)
               │       │
               │       ▼
               │  ┌────────────────────────────────────────────────┐
               │  │  ExpenseRequestDB                              │
               │  ├────────────────────────────────────────────────┤
               │  │  PK: id                                        │
               │  │  FK: ministry_id → ministries.id               │
               │  │  FK: project_id → projects.id (nullable)       │
               │  │                                                 │
               │  │  • ministry_id (requesting ministry)           │
               │  │  • project_id (optional project link)          │
               │  │  • amount (requested funds)                    │
               │  │  • purpose (description)                       │
               │  │  • category (infrastructure, salaries, etc.)   │
               │  │  • status (pending, approved, rejected, paid)  │
               │  │  • requested_by, requested_at                  │
               │  │  • approved_by, approved_at                    │
               │  │  • rejected_by, rejected_at, rejection_reason  │
               │  │  • transaction_hash (blockchain reference)     │
               │  └────────────────────────────────────────────────┘
               │
               │ 1:N (one ministry has many expense requests)
               │
               └────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  TaxPaymentDB (Independent - Citizen payments)                     │
├────────────────────────────────────────────────────────────────────┤
│  PK: id                                                             │
│  UK: receipt_number                                                 │
│                                                                     │
│  • receipt_number (unique, format: TAX-YYYYMMDD-NNNNNN)            │
│  • taxpayer_name, id_number, phone_number, email                   │
│  • tax_type (income, vat, corporate, property, excise)             │
│  • amount                                                           │
│  • payment_method (M-Pesa, Card, Bank)                             │
│  • status (pending, completed, failed)                             │
│  • transaction_hash (blockchain reference)                         │
│  • created_at, updated_at                                          │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  ReportDB (Independent - Citizen reports)                          │
├────────────────────────────────────────────────────────────────────┤
│  PK: id                                                             │
│                                                                     │
│  • report_type (tax_payment, citizen_portal)                       │
│  • reported_by (email/name)                                        │
│  • subject                                                          │
│  • description                                                      │
│  • transaction_hash (optional reference)                           │
│  • status (pending, reviewed, resolved)                            │
│  • created_at                                                      │
│  • reviewed_by, admin_notes                                        │
└────────────────────────────────────────────────────────────────────┘
```

### Relationship Summary

| Parent | Child | Type | Cascade |
|--------|-------|------|---------|
| Ministry | User | 1:N | None |
| Ministry | Project | 1:N | Delete |
| Ministry | ExpenseRequest | 1:N | Delete |
| Project | ExpenseRequest | 1:N | None |

---

## 🔐 Security Architecture

### Authentication Flow

```
┌──────────┐                                        ┌──────────┐
│  Client  │                                        │  Server  │
└────┬─────┘                                        └────┬─────┘
     │                                                    │
     │  1. POST /token                                   │
     │  { office_name, password }                        │
     ├──────────────────────────────────────────────────>│
     │                                                    │
     │                              2. Verify credentials│
     │                                 (check DB + hash) │
     │                                                    ├──┐
     │                                                    │  │
     │                                                    │<─┘
     │                                                    │
     │                            3. Generate JWT tokens │
     │                               • Access (30 min)   │
     │                               • Refresh (7 days)  │
     │                                                    ├──┐
     │                                                    │  │
     │                                                    │<─┘
     │                                                    │
     │  4. Return tokens + user info                     │
     │<──────────────────────────────────────────────────┤
     │  { access_token, refresh_token,                   │
     │    wallet_address, role, ... }                    │
     │                                                    │
     │  5. Store tokens (localStorage)                   │
     ├──┐                                                 │
     │<─┘                                                 │
     │                                                    │
     │  6. Authenticated Request                         │
     │  GET /ministries                                  │
     │  Authorization: Bearer <access_token>             │
     ├──────────────────────────────────────────────────>│
     │                                                    │
     │                              7. Validate JWT token│
     │                                 • Verify signature│
     │                                 • Check expiry    │
     │                                 • Extract user    │
     │                                                    ├──┐
     │                                                    │  │
     │                                                    │<─┘
     │                                                    │
     │                            8. Check authorization │
     │                                (role permissions) │
     │                                                    ├──┐
     │                                                    │  │
     │                                                    │<─┘
     │                                                    │
     │  9. Return protected resource                     │
     │<──────────────────────────────────────────────────┤
     │  [ministries data]                                │
     │                                                    │
     │                                                    │
     │  [30 minutes later - token expired]               │
     │                                                    │
     │  10. POST /refresh                                │
     │  { refresh_token }                                │
     ├──────────────────────────────────────────────────>│
     │                                                    │
     │                       11. Validate refresh token  │
     │                           Issue new access token  │
     │                                                    ├──┐
     │                                                    │  │
     │                                                    │<─┘
     │                                                    │
     │  12. New access token                             │
     │<──────────────────────────────────────────────────┤
     │  { access_token, token_type }                     │
     │                                                    │
```

### Password Hashing

```python
# Registration Flow
plaintext_password = "finance2025"
                ↓
pwd_context.hash(plaintext_password)
                ↓
   Bcrypt algorithm (12 rounds)
                ↓
$2b$12$rAnDomSaLt...hashedPasswordOutput
                ↓
        Store in database

# Login Verification
user_input = "finance2025"
db_hash = "$2b$12$rAnDomSaLt...hashedPasswordOutput"
                ↓
pwd_context.verify(user_input, db_hash)
                ↓
      Compare securely (constant-time)
                ↓
         True or False
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "FinanceOffice",
    "exp": 1675876543,
    "iat": 1675874743
  },
  "signature": "base64UrlEncode(HMACSHA256(
    base64UrlEncode(header) + '.' + base64UrlEncode(payload),
    SECRET_KEY
  ))"
}
```

### Role-Based Access Control (RBAC)

```python
# Endpoint Protection Example

@router.post("/ministries", dependencies=[Depends(require_super_admin)])
async def create_ministry(...):
    # Only super_admin role can access this endpoint
    ...

@router.get("/ministries/{id}", dependencies=[Depends(require_authenticated)])
async def get_ministry(...):
    # Any authenticated user can access
    ...

@router.post("/expense-requests", dependencies=[Depends(require_ministry_role)])
async def create_expense_request(...):
    # Ministry admin or officer can access
    ...
```

**Permission Matrix**:

| Endpoint | Super Admin | Ministry Admin | Ministry Officer | Citizen |
|----------|-------------|----------------|------------------|---------|
| POST /ministries | ✅ | ❌ | ❌ | ❌ |
| POST /ministries/{id}/allocate | ✅ | ❌ | ❌ | ❌ |
| POST /expense-requests | ✅ | ✅ | ✅ | ❌ |
| PUT /expense-requests/{id} | ✅ | ❌ | ❌ | ❌ |
| POST /tax-payments | ✅ | ✅ | ✅ | ✅ |
| GET /reports | ✅ | ❌ | ❌ | ❌ |
| POST /reports | ✅ | ✅ | ✅ | ✅ |

---

## ⛓️ Blockchain Architecture

### Block Structure

```python
class Block:
    def __init__(self, block_id, timestamp, previous_hash, 
                 transactions, validator):
        self.block_id = block_id              # Sequential number
        self.timestamp = timestamp            # ISO 8601 format
        self.previous_hash = previous_hash    # Links to previous block
        self.transactions = transactions      # List of transactions
        self.validator = validator            # Miner/validator address
        self.nonce = 0                       # Proof of work
        self.current_hash = self.calculate_hash()
```

### Transaction Structure

```json
{
  "sender": "0xDEF456...",
  "recipient": "0xEDU123...",
  "amount": 100000.00,
  "timestamp": "2025-02-10T12:00:00Z",
  "date": "2025-02-10",
  "purpose": "Q1 Budget Allocation",
  "approved_by": "FinanceOffice",
  "extra_info": "",
  "transaction_id": "abc123def456",
  "ministry_id": 1,
  "ministry_name": "Ministry of Education",
  "project_id": 5,
  "category": "budget_allocation",
  "expense_request_id": null
}
```

### Blockchain Operations

#### 1. Add Transaction
```python
def add_transaction(transaction: Dict) -> bool:
    # Validate required fields
    if not all(field in transaction for field in required_fields):
        return False
    
    # Check sender balance (except SYSTEM)
    if transaction["sender"] != "SYSTEM":
        balance = calculate_wallet_balance(sender)
        if balance + amount < 0:
            return False
    
    # Generate transaction ID
    tx_id = sha256(timestamp + sender + recipient).hexdigest()[:16]
    
    # Add to pending pool
    pending_transactions.append(transaction)
    return True
```

#### 2. Mine Block
```python
async def mine_block(miner_address: str):
    # Create new block
    block = Block(
        block_id=str(len(chain)),
        timestamp=current_time(),
        previous_hash=chain[-1].current_hash,
        transactions=pending_transactions,
        validator=miner_address
    )
    
    # Add to chain
    chain.append(block)
    
    # Clear pending transactions
    pending_transactions = []
    
    # Persist to file
    save_blockchain_to_file()
    
    # Notify connected clients
    await notify_all_clients(block)
```

#### 3. Calculate Balance
```python
def calculate_wallet_balance(wallet_address: str) -> float:
    balance = 0.0
    
    # Traverse all blocks
    for block in chain:
        for tx in block.transactions:
            if tx["sender"] == wallet_address:
                balance -= tx["amount"]
            if tx["recipient"] == wallet_address:
                balance += tx["amount"]
    
    return balance
```

### Blockchain Integrity

```python
def verify_chain() -> bool:
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i-1]
        
        # Verify current block hash
        if current.current_hash != current.calculate_hash():
            return False
        
        # Verify link to previous block
        if current.previous_hash != previous.current_hash:
            return False
    
    return True
```

---

## 🔄 Business Logic Flows

### 1. Budget Allocation Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Super Admin initiates budget allocation                  │
│    Input: ministry_id, amount, purpose, approved_by         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Validate inputs                                          │
│    • Ministry exists?                                        │
│    • Amount > 0?                                            │
│    • User is super_admin?                                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Create blockchain transaction                            │
│    sender: "SYSTEM"                                         │
│    recipient: ministry.wallet_address                       │
│    amount: input_amount                                     │
│    purpose: input_purpose                                   │
│    approved_by: input_approved_by                           │
│    ministry_id: input_ministry_id                           │
│    category: "budget_allocation"                            │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Mine block                                               │
│    • Add transaction to pending pool                        │
│    • Create new block with all pending transactions         │
│    • Calculate block hash                                   │
│    • Append to blockchain                                   │
│    • Save to blockchain.json                                │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Update ministry database record                          │
│    ministry.allocated_budget += amount                      │
│    ministry.updated_at = now()                              │
│    db.commit()                                              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Notify via WebSocket                                     │
│    Send to ministry's active WebSocket connection:          │
│    {                                                         │
│      type: "budget_allocated",                              │
│      amount: amount,                                        │
│      new_balance: ministry.allocated_budget,                │
│      transaction_id: tx_id                                  │
│    }                                                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Return success response                                  │
│    {                                                         │
│      message: "Budget allocated successfully",              │
│      transaction_id: tx_id,                                 │
│      new_balance: ministry.allocated_budget                 │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
```

### 2. Expense Request Approval Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Ministry officer submits expense request                 │
│    POST /expense-requests                                   │
│    {                                                         │
│      ministry_id: 1,                                        │
│      project_id: 5,                                         │
│      amount: 25000,                                         │
│      purpose: "Purchase materials",                         │
│      category: "Infrastructure"                             │
│    }                                                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Create expense request in database                       │
│    status: "pending"                                        │
│    requested_by: current_user.office_name                   │
│    requested_at: now()                                      │
│    db.commit()                                              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Appear in Super Admin dashboard                          │
│    Status: Pending approval                                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Super Admin reviews request                              │
│    PUT /expense-requests/{id}                               │
│    Decision: Approve or Reject                              │
└────────────┬────────────────────────────────────────────────┘
             │
             ├───────────────┬───────────────┐
             │               │               │
        [Approve]        [Reject]      [Pending]
             │               │               │
             ▼               ▼               ▼
┌──────────────────┐  ┌──────────────┐  ┌────────────┐
│ 5a. Approve Path │  │ 5b. Reject   │  │ No action  │
│                  │  │     Path     │  └────────────┘
│ • Update status  │  │              │
│   to "approved"  │  │ • Update     │
│                  │  │   status to  │
│ • Record         │  │   "rejected" │
│   approved_by    │  │              │
│   and            │  │ • Record     │
│   approved_at    │  │   rejected_by│
│                  │  │   rejected_at│
│ • Create         │  │   and reason │
│   blockchain     │  │              │
│   transaction    │  │ • No         │
│                  │  │   blockchain │
│ • Transfer funds │  │   transaction│
│   from ministry  │  │              │
│   wallet to      │  │ • Save to DB │
│   recipient      │  │              │
│                  │  │ • Notify user│
│ • Update         │  │              │
│   project.spent  │  └──────────────┘
│   += amount      │
│                  │
│ • Update         │
│   ministry.      │
│   used_funds     │
│   += amount      │
│                  │
│ • Record         │
│   transaction_   │
│   hash           │
│                  │
│ • Save to DB     │
│                  │
│ • Notify via     │
│   WebSocket      │
└──────────────────┘
```

### 3. Tax Payment Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Citizen accesses tax payment portal                      │
│    http://localhost:5500/tax-payment.html                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Fill in payment form                                     │
│    • Taxpayer name                                          │
│    • ID number                                              │
│    • Phone & email                                          │
│    • Tax type selection                                     │
│    • Amount                                                  │
│    • Payment method                                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Submit payment                                           │
│    POST /tax-payments                                       │
│    (No authentication required - public endpoint)           │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Backend validation                                       │
│    • Required fields present?                               │
│    • Amount > 0?                                            │
│    • Valid tax type?                                        │
│    • Valid email format?                                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Generate unique receipt number                           │
│    Format: TAX-YYYYMMDD-NNNNNN                             │
│    Example: TAX-20250210-000123                            │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Create blockchain transaction                            │
│    sender: Generated temporary citizen wallet               │
│    recipient: "TREASURY" (government wallet)                │
│    amount: payment_amount                                   │
│    purpose: f"Tax Payment - {tax_type}"                     │
│    category: "tax_payment"                                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Mine block & get transaction hash                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Save to tax_payments table                               │
│    • All form data                                          │
│    • Receipt number                                         │
│    • Transaction hash                                       │
│    • Status: completed                                      │
│    • Timestamp                                              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Return receipt to citizen                                │
│    {                                                         │
│      receipt_number: "TAX-20250210-000123",                 │
│      transaction_hash: "0xabc123...",                       │
│      amount: 15000.00,                                      │
│      status: "completed",                                   │
│      message: "Payment successful"                          │
│    }                                                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Display confirmation to citizen                         │
│     • Receipt number for record keeping                     │
│     • Transaction hash for blockchain verification          │
│     • Amount paid                                           │
│     • Date/time                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌐 API Design Patterns

### RESTful Principles

```
Resource-based URLs:
  ✅ /ministries          (collection)
  ✅ /ministries/{id}     (specific resource)
  ✅ /ministries/{id}/projects  (nested resource)

HTTP Methods:
  GET    - Retrieve resource(s)
  POST   - Create new resource
  PUT    - Update existing resource (full update)
  PATCH  - Partial update (not used in this project)
  DELETE - Remove resource

Response Codes:
  200 - OK (successful GET/PUT)
  201 - Created (successful POST)
  400 - Bad Request (validation error)
  401 - Unauthorized (invalid/missing token)
  403 - Forbidden (insufficient permissions)
  404 - Not Found (resource doesn't exist)
  500 - Internal Server Error
```

### Request/Response Patterns

#### Successful Response
```json
{
  "id": 1,
  "name": "Ministry of Education",
  "code": "EDU-001",
  "allocated_budget": 1000000.00,
  ...
}
```

#### Error Response
```json
{
  "detail": "Ministry not found"
}

// Or for validation errors:
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

### Pagination (Not currently implemented, but recommended)

```python
@router.get("/transactions")
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return {
        "items": transactions,
        "total": db.query(Transaction).count(),
        "skip": skip,
        "limit": limit
    }
```

---

## 🔌 WebSocket Architecture

### Connection Management

```python
# Active connections dictionary
# Key: wallet_address, Value: WebSocket connection
active_connections: Dict[str, WebSocket] = {}

# Connection manager for broadcasting
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)
```

### WebSocket Endpoint

```python
@app.websocket("/ws/{wallet_address}")
async def websocket_endpoint(
    websocket: WebSocket,
    wallet_address: str
):
    # Accept connection
    await websocket.accept()
    
    # Store connection
    active_connections[wallet_address] = websocket
    await manager.connect(websocket)
    
    try:
        # Keep alive - receive messages
        while True:
            data = await websocket.receive_text()
            # Process if needed
    
    except WebSocketDisconnect:
        # Cleanup on disconnect
        manager.disconnect(websocket)
        if wallet_address in active_connections:
            del active_connections[wallet_address]
```

### Notification System

```python
async def notify_user(wallet_address: str, message: dict):
    """Send notification to specific wallet"""
    if wallet_address in active_connections:
        ws = active_connections[wallet_address]
        try:
            await ws.send_json(message)
        except Exception as e:
            print(f"Failed to notify {wallet_address}: {e}")

# Usage example:
await notify_user(
    ministry.wallet_address,
    {
        "type": "budget_allocated",
        "amount": 100000.00,
        "new_balance": 850000.00,
        "transaction_id": "abc123"
    }
)
```

---

## 📁 File Structure Deep Dive

```
NASA/
│
├── gok_backend/                    # Backend application
│   │
│   ├── main.py                    # FastAPI app entry point
│   │   • CORS setup
│   │   • Router inclusion
│   │   • WebSocket endpoint
│   │   • Uvicorn server config
│   │
│   ├── models.py                  # SQLAlchemy models
│   │   • Base declarative class
│   │   • Enums (roles, statuses, types)
│   │   • DB models (User, Ministry, Project, etc.)
│   │   • Relationships
│   │
│   ├── schemas.py                 # Pydantic schemas
│   │   • Request/response models
│   │   • Data validation
│   │   • Serialization
│   │
│   ├── endpoints.py              # Core API routes
│   │   • /register, /token, /refresh, /logout
│   │   • /blockchain, /transactions, /balance
│   │   • /reports
│   │
│   ├── ministry_endpoints.py     # Ministry management routes
│   │   • /ministries (CRUD)
│   │   • /ministries/{id}/allocate
│   │   • /projects (CRUD)
│   │   • /expense-requests (CRUD)
│   │
│   ├── tax_endpoints.py          # Tax system routes
│   │   • /tax-payments
│   │   • /tax-payments/history
│   │
│   ├── auth.py                   # Authentication utilities
│   │   • JWT token creation/validation
│   │   • Password hashing/verification
│   │   • User authentication
│   │   • Token revocation
│   │   • Activity logging
│   │
│   ├── blockchain.py             # Blockchain engine
│   │   • Block class
│   │   • Blockchain class
│   │   • Transaction validation
│   │   • Mining logic
│   │   • Balance calculation
│   │   • Chain verification
│   │
│   ├── database.py               # Database configuration
│   │   • SQLAlchemy engine
│   │   • SessionLocal
│   │   • get_db dependency
│   │
│   ├── database_init.py          # DB initialization script
│   │   • Create all tables
│   │   • Initialize blockchain
│   │
│   ├── create_test_user.py       # Test user creation
│   │   • Create demo accounts
│   │   • Generate wallets
│   │
│   ├── utils.py                  # Helper functions
│   │   • Notification utilities
│   │   • Validation helpers
│   │
│   ├── connections.py            # WebSocket management
│   │   • Active connections dict
│   │   • ConnectionManager class
│   │
│   ├── requirements.txt          # Python dependencies
│   │
│   └── alembic/                  # Database migrations
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
│           └── a539a4336ede_initial_migration.py
│
├── NASA/                         # Traditional frontend
│   ├── login.html               # Login page
│   ├── login.js                 # Login logic
│   ├── login.css               # Login styles
│   │
│   ├── index.html              # Main dashboard (admin)
│   ├── home.js                 # Dashboard logic
│   ├── home.css                # Dashboard styles
│   │
│   ├── tax-payment.html        # Tax payment form
│   ├── tax-payment.js          # Payment logic
│   │
│   ├── citizen-portal.html     # Citizen interface
│   ├── citizen-portal.js       # Citizen logic
│   │
│   ├── reports.html            # Reports management
│   ├── reports.js              # Reports logic
│   │
│   ├── test-reports.html       # Testing page
│   │
│   └── payment-modal.html      # Payment modal component
│
├── federal-ledger/              # Modern React frontend
│   ├── src/
│   │   ├── main.tsx            # React app entry
│   │   ├── App.tsx             # Main App component
│   │   │
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── MinistriesOverview.tsx
│   │   │   ├── MinistryDashboard.tsx
│   │   │   ├── FinancialOverview.tsx
│   │   │   ├── TaxPaymentsPage.tsx
│   │   │   ├── ReportsManagement.tsx
│   │   │   ├── AuditLogs.tsx
│   │   │   └── citizen/
│   │   │       ├── CitizenDashboard.tsx
│   │   │       ├── PayTax.tsx
│   │   │       ├── SubmitReport.tsx
│   │   │       └── PublicTransparency.tsx
│   │   │
│   │   ├── components/         # Reusable components
│   │   │   ├── layout/
│   │   │   │   ├── AdminLayout.tsx
│   │   │   │   ├── CitizenLayout.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── KPICard.tsx
│   │   │   │   ├── ActivityPanel.tsx
│   │   │   │   └── SystemStatus.tsx
│   │   │   ├── ministry/
│   │   │   │   ├── MinistriesGrid.tsx
│   │   │   │   ├── AddMinistryDialog.tsx
│   │   │   │   ├── AllocateBudgetDialog.tsx
│   │   │   │   └── AddProjectDialog.tsx
│   │   │   └── ui/             # shadcn/ui components
│   │   │
│   │   ├── services/
│   │   │   └── api.ts          # API client with interceptors
│   │   │
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx  # Authentication context
│   │   │
│   │   ├── types/
│   │   │   └── ministry.ts      # TypeScript type definitions
│   │   │
│   │   └── lib/
│   │       ├── utils.ts         # Utility functions
│   │       └── auth-token.ts    # Token management
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
│
├── blockchain.json              # Blockchain persistence
│   • Array of blocks
│   • Each block contains transactions
│
├── validators.json              # Approved validators
│   • List of validator addresses
│
├── wallets.json                 # Wallet balance cache
│   • wallet_address: balance mapping
│
├── START_PROJECT.bat           # Windows startup script
│   • Starts backend server
│   • Starts frontend server
│   • Opens browser
│
├── README_STARTUP.txt          # Startup instructions
├── REPORT_SYSTEM_GUIDE.txt     # Report system guide
├── PROJECT_DOCUMENTATION.md    # This comprehensive doc
└── QUICK_REFERENCE.md          # Quick reference guide
```

---

## 🧪 Testing Strategy

### Unit Testing (Recommended - Not implemented yet)

```python
# tests/test_blockchain.py
import pytest
from blockchain import Blockchain, Block

def test_genesis_block_creation():
    bc = Blockchain()
    assert len(bc.chain) == 1
    assert bc.chain[0].block_id == "0"
    assert bc.chain[0].previous_hash == "0"

def test_add_valid_transaction():
    bc = Blockchain()
    tx = {
        "sender": "SYSTEM",
        "recipient": "0xABC123",
        "amount": 1000.00
    }
    assert bc.add_transaction(tx) == True
    assert len(bc.pending_transactions) == 1

def test_reject_insufficient_balance():
    bc = Blockchain()
    tx = {
        "sender": "0xNOFUNDS",
        "recipient": "0xABC123",
        "amount": 1000.00
    }
    assert bc.add_transaction(tx) == False
```

### Integration Testing

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/token", json={
        "office_name": "FinanceOffice",
        "password": "finance2025"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/token", json={
        "office_name": "BadUser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
```

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Token refresh mechanism
- [ ] Ministry creation and budget allocation
- [ ] Project creation and management
- [ ] Expense request submission and approval
- [ ] Tax payment processing
- [ ] Report submission and review
- [ ] Blockchain transaction recording
- [ ] WebSocket real-time updates
- [ ] Balance calculations
- [ ] Permission checks for different roles

---

## 🚀 Deployment Considerations

### Environment Variables (Production)

```bash
# .env file (NOT in version control)
DATABASE_URL=postgresql://user:pass@host:5432/nasa_db
SECRET_KEY=your-super-secret-key-min-256-bits
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=https://nasa.gov.example,https://admin.nasa.gov.example
```

### Database Migration

```bash
# Switch from SQLite to PostgreSQL
# 1. Update DATABASE_URL in .env
# 2. Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Docker Deployment (Recommended setup)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn main:app --host 0.0.0.0 --port 8000
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nasa_db
      POSTGRES_USER: nasa_user
      POSTGRES_PASSWORD: nasa_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  backend:
    build: ./gok_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://nasa_user:nasa_pass@db:5432/nasa_db
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
  
  frontend:
    build: ./federal-ledger
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Scalability Recommendations

1. **Caching**: Add Redis for session management and frequently accessed data
2. **Load Balancing**: Use Nginx to distribute traffic
3. **Database**: Connection pooling and read replicas
4. **CDN**: Serve static assets from CDN
5. **Monitoring**: Implement logging and monitoring (Prometheus, Grafana)

---

## 📊 Performance Optimization

### Database Indexing

```python
# Already implemented in models:
# • office_name (UNIQUE INDEX)
# • wallet_address (UNIQUE INDEX)
# • ministry code (UNIQUE INDEX)
# • receipt_number (UNIQUE INDEX)

# Additional recommended indexes:
CREATE INDEX idx_transactions_wallet ON transactions(sender);
CREATE INDEX idx_transactions_wallet_recipient ON transactions(recipient);
CREATE INDEX idx_tax_payments_id_number ON tax_payments(id_number);
CREATE INDEX idx_expense_requests_status ON expense_requests(status);
```

### Query Optimization

```python
# Use eager loading for relationships
ministries = db.query(MinistryDB)\
    .options(joinedload(MinistryDB.projects))\
    .all()

# Limit expensive queries
recent_transactions = db.query(Transaction)\
    .order_by(Transaction.timestamp.desc())\
    .limit(100)\
    .all()
```

### Caching Strategy (Future enhancement)

```python
# Redis caching example
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379)

def get_ministry_cached(ministry_id: int):
    # Try cache first
    cached = redis_client.get(f"ministry:{ministry_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from DB
    ministry = db.query(MinistryDB).filter_by(id=ministry_id).first()
    
    # Cache for 5 minutes
    redis_client.setex(
        f"ministry:{ministry_id}",
        300,
        json.dumps(ministry.dict())
    )
    
    return ministry
```

---

## 🔧 Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd NASA

# 2. Backend setup
cd gok_backend
python -m venv ../.venv
..\.venv\Scripts\activate
pip install -r requirements.txt
python database_init.py
python create_test_user.py

# 3. Frontend setup (federal-ledger)
cd ../federal-ledger
npm install

# 4. Run in development
# Terminal 1 - Backend
cd gok_backend
python main.py

# Terminal 2 - Frontend
cd federal-ledger
npm run dev
```

### Git Workflow (Recommended)

```
main (production)
  │
  ├─ develop (staging)
  │    │
  │    ├─ feature/ministry-management
  │    ├─ feature/tax-payment-system
  │    ├─ bugfix/auth-token-expiry
  │    └─ hotfix/critical-bug
  │
  └─ release/v2.0
```

---

## 📝 Code Style Guidelines

### Python (Backend)

```python
# Follow PEP 8
# Use type hints
def create_ministry(
    db: Session,
    ministry_data: MinistryCreate
) -> MinistryDB:
    """
    Create a new ministry in the database.
    
    Args:
        db: Database session
        ministry_data: Ministry creation data
    
    Returns:
        Created ministry object
    
    Raises:
        HTTPException: If ministry with same name exists
    """
    # Implementation

# Use descriptive variable names
allocated_budget = 1000000.00  # ✅
amt = 1000000.00  # ❌

# Use constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # ✅
```

### TypeScript/React (Frontend)

```typescript
// Use TypeScript interfaces
interface Ministry {
  id: number;
  name: string;
  allocated_budget: number;
}

// Functional components with hooks
const Dashboard: React.FC = () => {
  const [ministries, setMinistries] = useState<Ministry[]>([]);
  
  useEffect(() => {
    fetchMinistries();
  }, []);
  
  return (
    <div className="dashboard">
      {/* JSX */}
    </div>
  );
};

// Use meaningful component names
<KPICard title="Total Volume" value={1000000} />  // ✅
<Card1 t="TV" v={1000000} />  // ❌
```

---

## 🎓 Learning Resources

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### SQLAlchemy
- Official Docs: https://docs.sqlalchemy.org/
- ORM Tutorial: https://docs.sqlalchemy.org/en/20/orm/

### React + TypeScript
- React Docs: https://react.dev/
- TypeScript Handbook: https://www.typescriptlang.org/docs/

### Blockchain Concepts
- Blockchain Basics: https://www.investopedia.com/terms/b/blockchain.asp

---

**Document Version**: 1.0  
**Last Updated**: February 10, 2026  
**Maintained By**: Development Team

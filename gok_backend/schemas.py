# schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==================== User & Auth Schemas ====================

class User(BaseModel):
    office_name: str
    password: str

class UserRegister(BaseModel):
    office_name: str
    password: str
    role: Optional[str] = "citizen"
    ministry_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    wallet_address: str
    office_name: str
    role: str
    ministry_id: Optional[int] = None

class RefreshToken(BaseModel):
    refresh_token: str

# ==================== Ministry Schemas ====================

class MinistryCreate(BaseModel):
    name: str
    ministry_type: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    allocated_budget: Optional[float] = 0.0

class MinistryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

class MinistryResponse(BaseModel):
    id: int
    name: str
    code: str
    ministry_type: str
    description: Optional[str]
    wallet_address: str
    allocated_budget: float
    used_funds: float
    remaining_balance: float
    icon: Optional[str]
    color: Optional[str]
    is_active: bool
    created_at: datetime
    active_projects: Optional[int] = 0
    total_projects: Optional[int] = 0
    
    class Config:
        from_attributes = True

class MinistryBudgetAllocate(BaseModel):
    amount: float
    purpose: str
    approved_by: str

class MinistryTransfer(BaseModel):
    recipient_ministry_id: int
    amount: float
    purpose: str
    approved_by: Optional[str] = None

# ==================== Project Schemas ====================

class ProjectCreate(BaseModel):
    ministry_id: int
    name: str
    description: Optional[str] = None
    budget: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectResponse(BaseModel):
    id: int
    ministry_id: int
    name: str
    description: Optional[str]
    budget: float
    spent: float
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Expense Request Schemas ====================

class ExpenseRequestCreate(BaseModel):
    ministry_id: int
    project_id: Optional[int] = None
    amount: float
    purpose: str
    category: Optional[str] = None

class ExpenseRequestUpdate(BaseModel):
    status: str
    rejection_reason: Optional[str] = None

class ExpenseRequestResponse(BaseModel):
    id: int
    ministry_id: int
    project_id: Optional[int]
    amount: float
    purpose: str
    category: Optional[str]
    status: str
    requested_by: str
    requested_at: datetime
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejected_by: Optional[str]
    rejected_at: Optional[datetime]
    rejection_reason: Optional[str]
    transaction_hash: Optional[str]
    
    class Config:
        from_attributes = True

# ==================== Transaction Schemas ====================

class Transaction(BaseModel):
    recipient: str
    amount: float
    purpose: Optional[str] = Field(default="No purpose specified")
    approved_by: Optional[str] = Field(default="Not specified")
    extra_info: Optional[str] = Field(default="")
    ministry_id: Optional[int] = None
    project_id: Optional[int] = None
    category: Optional[str] = None

# ==================== Report Schemas ====================

class Report(BaseModel):
    report_type: str  # 'tax_payment' or 'citizen_portal'
    reported_by: str  # Email or name
    subject: str
    description: str
    transaction_hash: Optional[str] = None

class ReportUpdate(BaseModel):
    status: str  # 'pending', 'reviewed', 'resolved'
    admin_notes: Optional[str] = None

# ==================== Tax Payment Schemas ====================

class TaxPaymentCreate(BaseModel):
    taxpayer_name: str
    id_number: str
    tax_type: str  # income, vat, corporate, property, excise
    amount: float
    phone_number: Optional[str] = None
    email: Optional[str] = None
    payment_method: Optional[str] = None  # M-Pesa, Card

class TaxPaymentResponse(BaseModel):
    id: int
    receipt_number: str
    taxpayer_name: str
    id_number: str
    phone_number: Optional[str]
    email: Optional[str]
    tax_type: str
    amount: float
    payment_method: Optional[str]
    status: str
    transaction_hash: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

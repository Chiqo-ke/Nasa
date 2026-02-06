# models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Define the Base for SQLAlchemy models
Base = declarative_base()

# Enums for role and status management
class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    MINISTRY_ADMIN = "ministry_admin"
    MINISTRY_OFFICER = "ministry_officer"
    CITIZEN = "citizen"

class MinistryType(str, enum.Enum):
    CONSTRUCTION = "construction"
    EDUCATION = "education"
    HEALTH = "health"
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    FINANCE = "finance"
    AGRICULTURE = "agriculture"
    DEFENSE = "defense"
    TECHNOLOGY = "technology"
    ENVIRONMENT = "environment"
    CUSTOM = "custom"

class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class ExpenseStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"

class TaxType(str, enum.Enum):
    INCOME = "income"
    VAT = "vat"
    CORPORATE = "corporate"
    PROPERTY = "property"
    EXCISE = "excise"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# Ministry Model - Core entity for government ministries
class MinistryDB(Base):
    __tablename__ = "ministries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "EDU-001", "HLT-001"
    ministry_type = Column(String(100), nullable=False)  # Type from MinistryType enum
    description = Column(Text, nullable=True)
    wallet_address = Column(String(255), unique=True, index=True, nullable=False)
    
    # Budget tracking
    allocated_budget = Column(Float, default=0.0)
    used_funds = Column(Float, default=0.0)
    
    # Metadata
    icon = Column(String(100), nullable=True)  # Icon identifier
    color = Column(String(50), nullable=True)  # Color hex code
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("UserDB", back_populates="ministry")
    projects = relationship("ProjectDB", back_populates="ministry", cascade="all, delete-orphan")
    expense_requests = relationship("ExpenseRequestDB", back_populates="ministry", cascade="all, delete-orphan")

# Project Model - Ministry projects
class ProjectDB(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Budget
    budget = Column(Float, default=0.0)
    spent = Column(Float, default=0.0)
    
    # Status and timeline
    status = Column(String(50), default=ProjectStatus.PLANNING.value)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # Metadata
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ministry = relationship("MinistryDB", back_populates="projects")
    expense_requests = relationship("ExpenseRequestDB", back_populates="project")

# Expense Request Model - Budget allocation requests
class ExpenseRequestDB(Base):
    __tablename__ = "expense_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Request details
    amount = Column(Float, nullable=False)
    purpose = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    
    # Approval workflow
    status = Column(String(50), default=ExpenseStatus.PENDING.value)
    requested_by = Column(String(255), nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    
    approved_by = Column(String(255), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    rejected_by = Column(String(255), nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Blockchain reference
    transaction_hash = Column(String(255), nullable=True)
    
    # Relationships
    ministry = relationship("MinistryDB", back_populates="expense_requests")
    project = relationship("ProjectDB", back_populates="expense_requests")

# SQLAlchemy Model for Database - Enhanced with roles and ministry relationship
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    office_name = Column(String(255), unique=True, index=True)
    wallet_address = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    
    # Role-based access control
    role = Column(String(50), default=UserRole.CITIZEN.value, nullable=False)
    
    # Ministry relationship
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=True)
    ministry = relationship("MinistryDB", back_populates="users")
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

# Report Model for suspicious activity reporting
class ReportDB(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(100))  # 'tax_payment' or 'citizen_portal'
    reported_by = Column(String(255))  # Email or name of reporter
    subject = Column(String(255))
    description = Column(Text)
    transaction_hash = Column(String(255), nullable=True)  # Optional reference
    status = Column(String(50), default="pending")  # pending, reviewed, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(String(255), nullable=True)
    admin_notes = Column(Text, nullable=True)

# Tax Payment Model - For citizen tax payments
class TaxPaymentDB(Base):
    __tablename__ = "tax_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String(100), unique=True, index=True, nullable=False)
    
    # Taxpayer information
    taxpayer_name = Column(String(255), nullable=False)
    id_number = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Payment details
    tax_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=True)  # M-Pesa, Card
    
    # Status and tracking
    status = Column(String(50), default=PaymentStatus.COMPLETED.value)
    transaction_hash = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

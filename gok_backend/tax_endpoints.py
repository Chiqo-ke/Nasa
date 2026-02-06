# tax_endpoints.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import TaxPaymentDB
from schemas import TaxPaymentCreate, TaxPaymentResponse
from typing import List, Optional
from datetime import datetime
import random
import string

router = APIRouter()

def generate_receipt_number():
    """Generate a unique receipt number"""
    year = datetime.now().year
    random_part = ''.join(random.choices(string.digits, k=6))
    return f"TX-{year}-{random_part}"

@router.post("/tax-payments", response_model=TaxPaymentResponse)
def create_tax_payment(
    payment: TaxPaymentCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a new tax payment from citizen portal
    """
    try:
        # Generate unique receipt number
        receipt_number = generate_receipt_number()
        
        # Ensure receipt is unique
        while db.query(TaxPaymentDB).filter(TaxPaymentDB.receipt_number == receipt_number).first():
            receipt_number = generate_receipt_number()
        
        # Create tax payment record
        db_payment = TaxPaymentDB(
            receipt_number=receipt_number,
            taxpayer_name=payment.taxpayer_name,
            id_number=payment.id_number,
            phone_number=payment.phone_number,
            email=payment.email,
            tax_type=payment.tax_type,
            amount=payment.amount,
            payment_method=payment.payment_method,
            status="completed"
        )
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        
        return db_payment
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process tax payment: {str(e)}")

@router.get("/tax-payments", response_model=List[TaxPaymentResponse])
def get_tax_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    tax_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all tax payments for admin portal
    """
    query = db.query(TaxPaymentDB)
    
    if status:
        query = query.filter(TaxPaymentDB.status == status)
    
    if tax_type:
        query = query.filter(TaxPaymentDB.tax_type == tax_type)
    
    payments = query.order_by(TaxPaymentDB.created_at.desc()).offset(skip).limit(limit).all()
    return payments

@router.get("/tax-payments/stats/summary")
def get_tax_payment_stats(
    db: Session = Depends(get_db)
):
    """
    Get tax payment statistics for dashboard
    """
    from sqlalchemy import func
    
    total_payments = db.query(func.count(TaxPaymentDB.id)).scalar() or 0
    total_revenue = db.query(func.sum(TaxPaymentDB.amount)).scalar() or 0
    
    # By tax type
    by_type = db.query(
        TaxPaymentDB.tax_type,
        func.count(TaxPaymentDB.id).label('count'),
        func.sum(TaxPaymentDB.amount).label('total')
    ).group_by(TaxPaymentDB.tax_type).all()
    
    # Recent payments count (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_count = db.query(func.count(TaxPaymentDB.id)).filter(
        TaxPaymentDB.created_at >= thirty_days_ago
    ).scalar() or 0
    
    return {
        "total_payments": total_payments,
        "total_revenue": float(total_revenue),
        "recent_payments_30days": recent_count,
        "by_tax_type": [
            {
                "tax_type": item[0],
                "count": item[1],
                "total_amount": float(item[2]) if item[2] else 0
            }
            for item in by_type
        ]
    }

@router.get("/tax-payments/receipt/{receipt_number}", response_model=TaxPaymentResponse)
def get_tax_payment_by_receipt(
    receipt_number: str,
    db: Session = Depends(get_db)
):
    """
    Get a tax payment by receipt number
    """
    payment = db.query(TaxPaymentDB).filter(TaxPaymentDB.receipt_number == receipt_number).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Tax payment not found")
    
    return payment

@router.get("/tax-payments/{payment_id}", response_model=TaxPaymentResponse)
def get_tax_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tax payment by ID
    """
    payment = db.query(TaxPaymentDB).filter(TaxPaymentDB.id == payment_id).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Tax payment not found")
    
    return payment

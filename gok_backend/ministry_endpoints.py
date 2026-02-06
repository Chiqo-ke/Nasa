# ministry_endpoints.py
# API endpoints for Ministry, Project, and Expense Management

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import secrets

from database import get_db
from models import MinistryDB, ProjectDB, ExpenseRequestDB, UserDB
from schemas import (
    MinistryCreate, MinistryUpdate, MinistryResponse, MinistryBudgetAllocate,
    MinistryTransfer, ProjectCreate, ProjectUpdate, ProjectResponse,
    ExpenseRequestCreate, ExpenseRequestUpdate, ExpenseRequestResponse
)
from auth import (
    get_current_user, require_super_admin, require_ministry_admin,
    require_ministry_access, check_ministry_permission, generate_wallet_address
)
from blockchain import Blockchain
from connections import manager

# Create router
router = APIRouter()

# Initialize blockchain (shared instance)
blockchain = Blockchain()

# ==================== Utility Functions ====================

def generate_ministry_code(ministry_type: str, db: Session) -> str:
    """Generate unique ministry code like EDU-001, HLT-001, etc."""
    # Get first 3 letters of ministry type
    prefix = ministry_type[:3].upper()
    
    # Count existing ministries with this prefix
    existing_count = db.query(MinistryDB).filter(
        MinistryDB.code.like(f"{prefix}%")
    ).count()
    
    # Generate code
    number = str(existing_count + 1).zfill(3)
    return f"{prefix}-{number}"

# ==================== Ministry Endpoints ====================

@router.post("/ministries", response_model=MinistryResponse, status_code=status.HTTP_201_CREATED)
async def create_ministry(
    ministry: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_super_admin)
):
    """
    Create a new ministry (Super Admin only).
    Automatically generates wallet address and ministry code.
    """
    # Check if ministry with same name exists
    existing = db.query(MinistryDB).filter(MinistryDB.name == ministry.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ministry with this name already exists"
        )
    
    # Generate unique code and wallet
    ministry_code = generate_ministry_code(ministry.ministry_type, db)
    wallet_address = generate_wallet_address()
    
    # Create ministry
    db_ministry = MinistryDB(
        name=ministry.name,
        code=ministry_code,
        ministry_type=ministry.ministry_type,
        description=ministry.description,
        wallet_address=wallet_address,
        allocated_budget=ministry.allocated_budget or 0.0,
        used_funds=0.0,
        icon=ministry.icon,
        color=ministry.color,
        is_active=True
    )
    
    db.add(db_ministry)
    db.commit()
    db.refresh(db_ministry)
    
    # Prepare response
    response = MinistryResponse(
        id=db_ministry.id,
        name=db_ministry.name,
        code=db_ministry.code,
        ministry_type=db_ministry.ministry_type,
        description=db_ministry.description,
        wallet_address=db_ministry.wallet_address,
        allocated_budget=db_ministry.allocated_budget,
        used_funds=db_ministry.used_funds,
        remaining_balance=db_ministry.allocated_budget - db_ministry.used_funds,
        icon=db_ministry.icon,
        color=db_ministry.color,
        is_active=db_ministry.is_active,
        created_at=db_ministry.created_at,
        active_projects=0,
        total_projects=0
    )
    
    # Broadcast ministry creation via WebSocket
    await manager.broadcast({
        "type": "ministry_created",
        "data": {
            "id": db_ministry.id,
            "name": db_ministry.name,
            "code": db_ministry.code,
            "wallet_address": db_ministry.wallet_address
        }
    })
    
    return response

@router.get("/ministries", response_model=List[MinistryResponse])
async def list_ministries(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    List all ministries.
    Super admins see all, ministry users see only their own.
    """
    query = db.query(MinistryDB)
    
    # Filter by active status
    if not include_inactive:
        query = query.filter(MinistryDB.is_active == True)
    
    # Ministry users can only see their own ministry
    if current_user.role in ["ministry_admin", "ministry_officer"]:
        if current_user.ministry_id:
            query = query.filter(MinistryDB.id == current_user.ministry_id)
        else:
            return []
    
    ministries = query.offset(skip).limit(limit).all()
    
    # Build responses with project counts
    responses = []
    for ministry in ministries:
        project_count = db.query(ProjectDB).filter(ProjectDB.ministry_id == ministry.id).count()
        active_project_count = db.query(ProjectDB).filter(
            ProjectDB.ministry_id == ministry.id,
            ProjectDB.status.in_(["planning", "in_progress"])
        ).count()
        
        responses.append(MinistryResponse(
            id=ministry.id,
            name=ministry.name,
            code=ministry.code,
            ministry_type=ministry.ministry_type,
            description=ministry.description,
            wallet_address=ministry.wallet_address,
            allocated_budget=ministry.allocated_budget,
            used_funds=ministry.used_funds,
            remaining_balance=ministry.allocated_budget - ministry.used_funds,
            icon=ministry.icon,
            color=ministry.color,
            is_active=ministry.is_active,
            created_at=ministry.created_at,
            active_projects=active_project_count,
            total_projects=project_count
        ))
    
    return responses

@router.get("/ministries/{ministry_id}", response_model=MinistryResponse)
async def get_ministry(
    ministry_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Get specific ministry details."""
    ministry = db.query(MinistryDB).filter(MinistryDB.id == ministry_id).first()
    
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    # Check permission
    if not check_ministry_permission(current_user, ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this ministry"
        )
    
    # Get project counts
    project_count = db.query(ProjectDB).filter(ProjectDB.ministry_id == ministry.id).count()
    active_project_count = db.query(ProjectDB).filter(
        ProjectDB.ministry_id == ministry.id,
        ProjectDB.status.in_(["planning", "in_progress"])
    ).count()
    
    return MinistryResponse(
        id=ministry.id,
        name=ministry.name,
        code=ministry.code,
        ministry_type=ministry.ministry_type,
        description=ministry.description,
        wallet_address=ministry.wallet_address,
        allocated_budget=ministry.allocated_budget,
        used_funds=ministry.used_funds,
        remaining_balance=ministry.allocated_budget - ministry.used_funds,
        icon=ministry.icon,
        color=ministry.color,
        is_active=ministry.is_active,
        created_at=ministry.created_at,
        active_projects=active_project_count,
        total_projects=project_count
    )

@router.put("/ministries/{ministry_id}", response_model=MinistryResponse)
async def update_ministry(
    ministry_id: int,
    ministry_update: MinistryUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_super_admin)
):
    """Update ministry details (Super Admin only)."""
    ministry = db.query(MinistryDB).filter(MinistryDB.id == ministry_id).first()
    
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    # Update fields
    if ministry_update.name is not None:
        ministry.name = ministry_update.name
    if ministry_update.description is not None:
        ministry.description = ministry_update.description
    if ministry_update.icon is not None:
        ministry.icon = ministry_update.icon
    if ministry_update.color is not None:
        ministry.color = ministry_update.color
    if ministry_update.is_active is not None:
        ministry.is_active = ministry_update.is_active
    
    ministry.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ministry)
    
    # Get project counts
    project_count = db.query(ProjectDB).filter(ProjectDB.ministry_id == ministry.id).count()
    active_project_count = db.query(ProjectDB).filter(
        ProjectDB.ministry_id == ministry.id,
        ProjectDB.status.in_(["planning", "in_progress"])
    ).count()
    
    return MinistryResponse(
        id=ministry.id,
        name=ministry.name,
        code=ministry.code,
        ministry_type=ministry.ministry_type,
        description=ministry.description,
        wallet_address=ministry.wallet_address,
        allocated_budget=ministry.allocated_budget,
        used_funds=ministry.used_funds,
        remaining_balance=ministry.allocated_budget - ministry.used_funds,
        icon=ministry.icon,
        color=ministry.color,
        is_active=ministry.is_active,
        created_at=ministry.created_at,
        active_projects=active_project_count,
        total_projects=project_count
    )

@router.post("/ministries/{ministry_id}/allocate-budget")
async def allocate_budget(
    ministry_id: int,
    allocation: MinistryBudgetAllocate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_super_admin)
):
    """
    Allocate budget to a ministry (Super Admin only).
    Creates blockchain transaction from National Treasury.
    """
    ministry = db.query(MinistryDB).filter(MinistryDB.id == ministry_id).first()
    
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    if allocation.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Allocation amount must be positive"
        )
    
    # Get national treasury wallet (admin's wallet)
    treasury_wallet = current_user.wallet_address
    
    # Create blockchain transaction
    transaction = {
        "sender": treasury_wallet,
        "recipient": ministry.wallet_address,
        "amount": allocation.amount,
        "timestamp": datetime.utcnow().isoformat(),
        "purpose": allocation.purpose,
        "approved_by": allocation.approved_by or current_user.office_name,
        "ministry_id": ministry_id,
        "ministry_name": ministry.name,
        "category": "budget_allocation"
    }
    
    # Add transaction to blockchain
    if not blockchain.add_transaction(transaction):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction validation failed"
        )
    
    # Mine block
    try:
        await blockchain.mine_block(treasury_wallet, {})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mine block: {str(e)}"
        )
    
    # Get the latest block
    latest_block = blockchain.chain[-1] if blockchain.chain else None
    
    # Update ministry budget
    ministry.allocated_budget += allocation.amount
    ministry.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ministry)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "budget_allocated",
        "data": {
            "ministry_id": ministry_id,
            "ministry_name": ministry.name,
            "amount": allocation.amount,
            "new_balance": ministry.allocated_budget,
            "block_hash": latest_block.current_hash if latest_block else None
        }
    })
    
    return {
        "message": "Budget allocated successfully",
        "ministry": ministry.name,
        "amount_allocated": allocation.amount,
        "new_total_budget": ministry.allocated_budget,
        "remaining_balance": ministry.allocated_budget - ministry.used_funds,
        "block_hash": latest_block.current_hash if latest_block else None,
        "block_index": latest_block.block_id if latest_block else None
    }

@router.post("/ministries/transfer")
async def transfer_to_ministry(
    transfer: MinistryTransfer,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Transfer funds from National Financial Administration to another ministry.
    Only users from the National Financial Administration ministry can initiate transfers.
    """
    # Verify current user is from National Financial Administration
    if not current_user.ministry_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ministry users can perform transfers"
        )
    
    sender_ministry = db.query(MinistryDB).filter(MinistryDB.id == current_user.ministry_id).first()
    
    if not sender_ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sender ministry not found"
        )
    
    # Check if sender is National Financial Administration (by ministry_type or name)
    is_finance_ministry = (
        sender_ministry.ministry_type.lower() == "finance" or
        "finance" in sender_ministry.name.lower() or
        "treasury" in sender_ministry.name.lower() or
        "national" in sender_ministry.name.lower()
    )
    
    if not is_finance_ministry:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only National Financial Administration can transfer funds to other ministries"
        )
    
    # Check if user has admin permissions
    if current_user.role not in ["super_admin", "ministry_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform transfers"
        )
    
    # Get recipient ministry
    recipient_ministry = db.query(MinistryDB).filter(
        MinistryDB.id == transfer.recipient_ministry_id
    ).first()
    
    if not recipient_ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient ministry not found"
        )
    
    # Prevent self-transfer
    if sender_ministry.id == recipient_ministry.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to the same ministry"
        )
    
    # Validate amount
    if transfer.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfer amount must be positive"
        )
    
    # Check if sender has sufficient balance
    sender_balance = sender_ministry.allocated_budget - sender_ministry.used_funds
    if sender_balance < transfer.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Available: {sender_balance}, Requested: {transfer.amount}"
        )
    
    # Create blockchain transaction
    transaction = {
        "sender": sender_ministry.wallet_address,
        "recipient": recipient_ministry.wallet_address,
        "amount": transfer.amount,
        "timestamp": datetime.utcnow().isoformat(),
        "purpose": transfer.purpose,
        "approved_by": transfer.approved_by or current_user.office_name,
        "ministry_id": sender_ministry.id,
        "ministry_name": sender_ministry.name,
        "from_ministry_id": sender_ministry.id,
        "to_ministry_id": recipient_ministry.id,
        "from_ministry_name": sender_ministry.name,
        "to_ministry_name": recipient_ministry.name,
        "category": "ministry_transfer"
    }
    
    # Add transaction to blockchain
    if not blockchain.add_transaction(transaction):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction validation failed"
        )
    
    # Mine block
    try:
        await blockchain.mine_block(sender_ministry.wallet_address, {})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mine block: {str(e)}"
        )
    
    # Get the latest block
    latest_block = blockchain.chain[-1] if blockchain.chain else None
    
    # Update ministry balances
    sender_ministry.used_funds += transfer.amount
    recipient_ministry.allocated_budget += transfer.amount
    sender_ministry.updated_at = datetime.utcnow()
    recipient_ministry.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(sender_ministry)
    db.refresh(recipient_ministry)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "ministry_transfer",
        "data": {
            "from_ministry": sender_ministry.name,
            "to_ministry": recipient_ministry.name,
            "amount": transfer.amount,
            "purpose": transfer.purpose,
            "sender_new_balance": sender_ministry.allocated_budget - sender_ministry.used_funds,
            "recipient_new_balance": recipient_ministry.allocated_budget - recipient_ministry.used_funds,
            "block_hash": latest_block.current_hash if latest_block else None
        }
    })
    
    return {
        "message": "Transfer completed successfully",
        "from_ministry": sender_ministry.name,
        "to_ministry": recipient_ministry.name,
        "amount_transferred": transfer.amount,
        "sender_remaining_balance": sender_ministry.allocated_budget - sender_ministry.used_funds,
        "recipient_new_balance": recipient_ministry.allocated_budget - recipient_ministry.used_funds,
        "block_hash": latest_block.current_hash if latest_block else None,
        "block_index": latest_block.block_id if latest_block else None,
        "transaction_id": blockchain.chain[-1].transactions[-1].get("transaction_id") if blockchain.chain and blockchain.chain[-1].transactions else None
    }

@router.get("/ministries/{ministry_id}/transactions")
async def get_ministry_transactions(
    ministry_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Get all transactions for a specific ministry."""
    ministry = db.query(MinistryDB).filter(MinistryDB.id == ministry_id).first()
    
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    # Check permission
    if not check_ministry_permission(current_user, ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this ministry's transactions"
        )
    
    # Filter transactions by ministry wallet
    ministry_transactions = []
    for block in blockchain[1:]:  # Skip genesis block
        for transaction in block.get("transactions", []):
            if (transaction.get("sender") == ministry.wallet_address or
                transaction.get("recipient") == ministry.wallet_address or
                transaction.get("ministry_id") == ministry_id):
                ministry_transactions.append({
                    "block_index": block["index"],
                    "block_hash": block["hash"],
                    "timestamp": transaction.get("timestamp"),
                    "sender": transaction.get("sender"),
                    "recipient": transaction.get("recipient"),
                    "amount": transaction.get("amount"),
                    "purpose": transaction.get("purpose"),
                    "category": transaction.get("category"),
                    "approved_by": transaction.get("approved_by")
                })
    
    # Sort by timestamp descending
    ministry_transactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return {
        "ministry": ministry.name,
        "wallet_address": ministry.wallet_address,
        "total_transactions": len(ministry_transactions),
        "transactions": ministry_transactions
    }

# ==================== Project Endpoints ====================

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_ministry_access)
):
    """Create a new project for a ministry."""
    # Verify ministry exists
    ministry = db.query(MinistryDB).filter(MinistryDB.id == project.ministry_id).first()
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    # Check permission
    if not check_ministry_permission(current_user, project.ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create projects for this ministry"
        )
    
    # Create project
    db_project = ProjectDB(
        ministry_id=project.ministry_id,
        name=project.name,
        description=project.description,
        budget=project.budget,
        spent=0.0,
        status="planning",
        start_date=project.start_date,
        end_date=project.end_date,
        created_by=current_user.office_name
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return ProjectResponse.from_orm(db_project)

@router.get("/ministries/{ministry_id}/projects", response_model=List[ProjectResponse])
async def list_ministry_projects(
    ministry_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """List all projects for a ministry."""
    # Check permission
    if not check_ministry_permission(current_user, ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this ministry's projects"
        )
    
    projects = db.query(ProjectDB).filter(ProjectDB.ministry_id == ministry_id).all()
    return [ProjectResponse.from_orm(p) for p in projects]

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_ministry_access)
):
    """Update project details."""
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permission
    if not check_ministry_permission(current_user, project.ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this project"
        )
    
    # Update fields
    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.budget is not None:
        project.budget = project_update.budget
    if project_update.status is not None:
        project.status = project_update.status
    if project_update.start_date is not None:
        project.start_date = project_update.start_date
    if project_update.end_date is not None:
        project.end_date = project_update.end_date
    
    project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.from_orm(project)

# ==================== Expense Request Endpoints ====================

@router.post("/expense-requests", response_model=ExpenseRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_expense_request(
    expense: ExpenseRequestCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_ministry_access)
):
    """Create a new expense request."""
    # Verify ministry exists
    ministry = db.query(MinistryDB).filter(MinistryDB.id == expense.ministry_id).first()
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    # Check permission
    if not check_ministry_permission(current_user, expense.ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create expense requests for this ministry"
        )
    
    # Verify project if specified
    if expense.project_id:
        project = db.query(ProjectDB).filter(ProjectDB.id == expense.project_id).first()
        if not project or project.ministry_id != expense.ministry_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project not found or doesn't belong to this ministry"
            )
    
    # Create expense request
    db_expense = ExpenseRequestDB(
        ministry_id=expense.ministry_id,
        project_id=expense.project_id,
        amount=expense.amount,
        purpose=expense.purpose,
        category=expense.category,
        status="pending",
        requested_by=current_user.office_name
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "expense_request_created",
        "data": {
            "id": db_expense.id,
            "ministry_id": expense.ministry_id,
            "amount": expense.amount,
            "requested_by": current_user.office_name
        }
    })
    
    return ExpenseRequestResponse.from_orm(db_expense)

@router.get("/ministries/{ministry_id}/expense-requests", response_model=List[ExpenseRequestResponse])
async def list_ministry_expense_requests(
    ministry_id: int,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """List expense requests for a ministry."""
    # Check permission
    if not check_ministry_permission(current_user, ministry_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this ministry's expense requests"
        )
    
    query = db.query(ExpenseRequestDB).filter(ExpenseRequestDB.ministry_id == ministry_id)
    
    if status_filter:
        query = query.filter(ExpenseRequestDB.status == status_filter)
    
    expenses = query.order_by(ExpenseRequestDB.requested_at.desc()).all()
    return [ExpenseRequestResponse.from_orm(e) for e in expenses]

@router.put("/expense-requests/{expense_id}/approve")
async def approve_expense_request(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_ministry_admin)
):
    """Approve an expense request and create blockchain transaction."""
    expense = db.query(ExpenseRequestDB).filter(ExpenseRequestDB.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense request not found"
        )
    
    if expense.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expense request is already {expense.status}"
        )
    
    # Get ministry
    ministry = db.query(MinistryDB).filter(MinistryDB.id == expense.ministry_id).first()
    
    # Check if ministry has sufficient budget
    remaining_budget = ministry.allocated_budget - ministry.used_funds
    if expense.amount > remaining_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient budget. Available: {remaining_budget}, Requested: {expense.amount}"
        )
    
    # Create blockchain transaction
    transaction = {
        "sender": ministry.wallet_address,
        "recipient": "EXPENSE_PAID",
        "amount": expense.amount,
        "timestamp": datetime.utcnow().isoformat(),
        "purpose": expense.purpose,
        "approved_by": current_user.office_name,
        "ministry_id": ministry.id,
        "project_id": expense.project_id,
        "expense_request_id": expense_id,
        "category": expense.category or "general_expense"
    }
    
    # Add transaction to blockchain
    if not blockchain.add_transaction(transaction):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction validation failed"
        )
    
    # Mine block
    try:
        await blockchain.mine_block(ministry.wallet_address, {})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mine block: {str(e)}"
        )
    
    # Get the latest block
    latest_block = blockchain.chain[-1] if blockchain.chain else None
    
    # Update expense request
    expense.status = "approved"
    expense.approved_by = current_user.office_name
    expense.approved_at = datetime.utcnow()
    expense.transaction_hash = latest_block.current_hash if latest_block else None
    
    # Update ministry used funds
    ministry.used_funds += expense.amount
    
    # Update project spent if applicable
    if expense.project_id:
        project = db.query(ProjectDB).filter(ProjectDB.id == expense.project_id).first()
        if project:
            project.spent += expense.amount
    
    db.commit()
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "expense_approved",
        "data": {
            "expense_id": expense_id,
            "ministry_id": ministry.id,
            "amount": expense.amount,
            "block_hash": new_block["hash"],
            "new_remaining_budget": ministry.allocated_budget - ministry.used_funds
        }
    })
    
    return {
        "message": "Expense approved and transaction recorded",
        "expense_id": expense_id,
        "amount": expense.amount,
        "block_hash": new_block["hash"],
        "ministry_remaining_budget": ministry.allocated_budget - ministry.used_funds
    }

@router.put("/expense-requests/{expense_id}/reject")
async def reject_expense_request(
    expense_id: int,
    update: ExpenseRequestUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_ministry_admin)
):
    """Reject an expense request."""
    expense = db.query(ExpenseRequestDB).filter(ExpenseRequestDB.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense request not found"
        )
    
    if expense.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expense request is already {expense.status}"
        )
    
    # Update expense request
    expense.status = "rejected"
    expense.rejected_by = current_user.office_name
    expense.rejected_at = datetime.utcnow()
    expense.rejection_reason = update.rejection_reason
    
    db.commit()
    
    return {
        "message": "Expense request rejected",
        "expense_id": expense_id
    }

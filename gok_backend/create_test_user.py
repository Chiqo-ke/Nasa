from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import UserDB
from auth import get_password_hash, generate_wallet_address

# Initialize database first
init_db()

# Create a session
db = SessionLocal()

try:
    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.office_name == "FinanceOffice").first()
    
    if existing_user:
        print("User 'FinanceOffice' already exists!")
        print(f"Office Name: FinanceOffice")
        print(f"Wallet Address: {existing_user.wallet_address}")
        print("If you forgot the password, delete the database file and run this script again.")
    else:
        # Create new user
        office_name = "FinanceOffice"
        password = "finance2025"  # Simple password for testing
        wallet_address = generate_wallet_address()
        hashed_password = get_password_hash(password)
        
        new_user = UserDB(
            office_name=office_name,
            wallet_address=wallet_address,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ Test user created successfully!")
        print("=" * 50)
        print(f"Office Name: {office_name}")
        print(f"Password: {password}")
        print(f"Wallet Address: {wallet_address}")
        print("=" * 50)
        print("\nYou can now login with these credentials!")
        
except Exception as e:
    print(f"Error creating user: {e}")
    db.rollback()
finally:
    db.close()

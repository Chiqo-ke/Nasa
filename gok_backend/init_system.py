# init_system.py
# Initialize the National Financial Platform with database tables and super admin

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserDB
from auth import generate_wallet_address, get_password_hash

# Database URL with SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./gok_db.sqlite"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Create all database tables."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("   - users")
        print("   - ministries")
        print("   - projects")
        print("   - expense_requests")
        print("   - reports")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def create_super_admin():
    """Create a super admin user if it doesn't exist."""
    print("\nCreating super admin user...")
    db = SessionLocal()
    
    try:
        # Check if super admin already exists
        existing_admin = db.query(UserDB).filter(UserDB.office_name == "FinanceOffice").first()
        if existing_admin:
            print("⚠️  Super admin already exists!")
            print(f"   Office Name: {existing_admin.office_name}")
            print(f"   Wallet: {existing_admin.wallet_address}")
            print(f"   Role: {existing_admin.role}")
            return True
        
        # Create super admin
        wallet_address = generate_wallet_address()
        hashed_password = get_password_hash("admin123")  # Default password
        
        admin_user = UserDB(
            office_name="FinanceOffice",
            wallet_address=wallet_address,
            hashed_password=hashed_password,
            role="super_admin",
            ministry_id=None,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Super admin created successfully!")
        print(f"   Office Name: FinanceOffice")
        print(f"   Password: admin123")
        print(f"   Wallet: {wallet_address}")
        print(f"   Role: super_admin")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating super admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main initialization function."""
    print("=" * 60)
    print("National Financial Blockchain Administration Portal")
    print("System Initialization")
    print("=" * 60)
    
    # Step 1: Create database tables
    if not init_database():
        print("\n❌ Initialization failed: Could not create database tables")
        sys.exit(1)
    
    # Step 2: Create super admin
    if not create_super_admin():
        print("\n❌ Initialization failed: Could not create super admin")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ System initialization completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the backend server: uvicorn main:app --reload")
    print("2. Login with:")
    print("   - Office Name: FinanceOffice")
    print("   - Password: admin123")
    print("3. Create your first ministry via /ministries endpoint")
    print("4. Start the frontend: npm run dev")
    print("\n🚀 Your National Financial Platform is ready!")

if __name__ == "__main__":
    main()

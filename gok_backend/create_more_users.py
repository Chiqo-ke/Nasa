from sqlalchemy.orm import Session
from database import SessionLocal
from models import UserDB
from auth import get_password_hash, generate_wallet_address

# Create a session
db = SessionLocal()

try:
    # Create second office - Education Department
    office_name = "EducationOffice"
    existing_user = db.query(UserDB).filter(UserDB.office_name == office_name).first()
    
    if existing_user:
        print(f"User '{office_name}' already exists!")
        print(f"Wallet Address: {existing_user.wallet_address}")
    else:
        password = "education2025"
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
        
        print("✅ Education Office created successfully!")
        print("=" * 50)
        print(f"Office Name: {office_name}")
        print(f"Password: {password}")
        print(f"Wallet Address: {wallet_address}")
        print("=" * 50)

    # Create third office - Healthcare Department
    office_name2 = "HealthcareOffice"
    existing_user2 = db.query(UserDB).filter(UserDB.office_name == office_name2).first()
    
    if existing_user2:
        print(f"\nUser '{office_name2}' already exists!")
        print(f"Wallet Address: {existing_user2.wallet_address}")
    else:
        password2 = "healthcare2025"
        wallet_address2 = generate_wallet_address()
        hashed_password2 = get_password_hash(password2)
        
        new_user2 = UserDB(
            office_name=office_name2,
            wallet_address=wallet_address2,
            hashed_password=hashed_password2
        )
        
        db.add(new_user2)
        db.commit()
        db.refresh(new_user2)
        
        print("\n✅ Healthcare Office created successfully!")
        print("=" * 50)
        print(f"Office Name: {office_name2}")
        print(f"Password: {password2}")
        print(f"Wallet Address: {wallet_address2}")
        print("=" * 50)

    # Show all wallets
    print("\n" + "=" * 50)
    print("ALL GOVERNMENT OFFICE WALLETS:")
    print("=" * 50)
    all_users = db.query(UserDB).all()
    for user in all_users:
        print(f"{user.office_name}: {user.wallet_address}")
    print("=" * 50)
        
except Exception as e:
    print(f"Error creating users: {e}")
    db.rollback()
finally:
    db.close()

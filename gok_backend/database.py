from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database URL with MySQL and root user
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:8844@127.0.0.1/gok_db"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    init_db()
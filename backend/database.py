from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Database configuration - URL encode the password to handle special characters
password = quote_plus("Swami@1919")  # URL encode the password
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://postgres:{password}@localhost:5432/real_estate_db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    echo=True  # Set to False in production
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    try:
        # Import models at function level to avoid circular imports
        from backend.models import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Drop all tables
def drop_tables():
    try:
        # Import models at function level to avoid circular imports
        from backend.models import Base
        Base.metadata.drop_all(bind=engine)
        print("✅ Database tables dropped successfully!")
    except Exception as e:
        print(f"❌ Error dropping database tables: {e}")

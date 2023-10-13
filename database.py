from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://postgres:postgres@localhost/shop_db"
# DATABASE_URL = "postgresql://postgres:postgres@host.docker.internal/financial_db"


engine = create_engine(DATABASE_URL)

try:
    engine.connect()
    print("Connection to PostgreSQL successful")
except OperationalError as e:
    print(f"Error connecting to PostgreSQL: {e}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to create database tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# user_db = SQLAlchemyUserDatabase(User, SessionLocal)


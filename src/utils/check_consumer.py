from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.models import ClientRequest

DATABASE_URL = "sqlite:///./quotations.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
entries = db.query(ClientRequest).all()

for entry in entries:
    print(entry.customer_id, entry.company_name)
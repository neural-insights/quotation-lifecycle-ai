from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from utils.db import get_db
from utils.models import ClientRequest as SQLClientRequest
from utils.schemas import ClientRequestSchema as PydanticClientRequest
from utils.synthetic_data import generate_bulk_requests

app = FastAPI()

# Endpoint to simulate CRM data reception (HubSpot inquiries)
@app.get("/hubspot/simulate_requests", response_model=List[PydanticClientRequest])
def simulate_crm_requests():
    """
    Simulates CRM entries like those from HubSpot.
    This route dynamically generates synthetic client requests.
    """
    return generate_bulk_requests(n=10)

@app.get("/hubspot/client_requests", response_model=List[PydanticClientRequest])
def get_saved_requests(db: Session = Depends(get_db)):
    """
    Fetches all saved client requests from the database.
    """
    return db.query(SQLClientRequest).all()


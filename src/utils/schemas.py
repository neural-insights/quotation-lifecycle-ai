from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClientRequestSchema(BaseModel):
    customer_id: str
    company_name: str
    contact_email: str
    product_type: str
    specifications: str
    quantity: int
    color_spec: str
    delivery_deadline: date
    special_requirements: Optional[str] = None
    request_date: date

    # orm_mode = True allows FastAPI to automatically convert SQLAlchemy objects into Pydantic responses.
    class Config:
        from_attributes = True # orm_mode has been renamed to from_attributes
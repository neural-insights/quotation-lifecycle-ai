import random
import datetime
from sqlalchemy.orm import Session
from models import Supplier, RFQSent, QuotationResponse, RealQuotationData  
from db import SessionLocal

def calculate_rfq_complexity(product_type: str, quantity: int) -> float:
    """Calculate complexity score based on product type and quantity."""
    base = 1.0 if quantity < 50 else 2.0 if quantity < 200 else 3.0
    if "custom" in product_type.lower():
        base += 1.0
    return round(base + random.uniform(-0.3, 0.3), 2)

def is_urgent(deadline: datetime.datetime, sent_at: datetime.datetime) -> bool:
    """Determine if RFQ is urgent based on deadline proximity."""
    return (deadline - sent_at).days <= 2

def compile_test_dataset(db: Session):
    rfqs = db.query(RFQSent).all()
    count = 0

    for rfq in rfqs:
        # Skip if essential linked data is missing
        if not rfq.quotation_response or not rfq.rfq_details:
            continue

        quote = rfq.quotation_response
        supplier = rfq.supplier
        details = rfq.rfq_details

        response_time = (quote.received_at - rfq.sent_at).total_seconds() / 3600.0  # in hours
        perf_score = supplier.performance_score
        complexity = calculate_rfq_complexity(
            rfq.client_request.product_type,
            rfq.client_request.quantity
        )
        urgent = is_urgent(details.response_deadline, rfq.sent_at)
        is_custom = "custom" in rfq.client_request.product_type.lower()


        # Prepare TrainingQuotation object but DO NOT set 'won' field
        training_entry = RealQuotationData(
            unit_price=quote.unit_price,
            delivery_days=quote.delivery_days,
            performance_score=perf_score,
            response_time=round(response_time, 2),
            rfq_complexity_score=complexity,
            is_urgent=urgent,
            is_custom=is_custom,
            won=None  # or just omit this field if your model allows nullable
        )

        db.add(training_entry)
        count += 1

    db.commit()
    print(f"{count} x 8 dataset compiled.")

if __name__ == "__main__":
    db = SessionLocal()
    compile_test_dataset(db)
    db.close()

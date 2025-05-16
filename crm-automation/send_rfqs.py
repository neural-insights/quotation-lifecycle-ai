from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from models import RFQSent, RFQDetails, ClientRequest, Supplier
from db import SessionLocal

# Possible standard RFQ values
EXPECTED_FORMAT_OPTIONS = ["PDF", "DOCX", "XLSX"]
PAYMENT_TERMS_OPTIONS = ["Net 30", "Net 15", "Due on receipt"]
NOTES_OPTIONS = [
    "Please include shipping costs and delivery schedule.",
    "Specify if you offer bulk discounts for large orders.",
    "Include production and delivery timelines in your response.",
    "Make sure to detail packaging requirements if applicable.",
    "Let us know about any additional service fees or charges."
]

def send_rfqs():
    db: Session = SessionLocal()
    client_requests = db.query(ClientRequest).all()
    suppliers = db.query(Supplier).all()

    rfq_count = 0

    for request in client_requests:
        for supplier in suppliers:
            supported = [p.strip() for p in supplier.supported_products.split(",")]
            if request.product_type not in supported:
                continue

            rfq = RFQSent(
                client_request_id=request.id,
                supplier_id=supplier.id,
                status="sent",
                sent_at=datetime.utcnow()
            )
            db.add(rfq)
            db.commit()
            db.refresh(rfq)

            # Randomize standardized RFQ details
            rfq_details = RFQDetails(
                rfq_id=rfq.id,
                expected_format=random.choice(EXPECTED_FORMAT_OPTIONS),
                payment_terms=random.choice(PAYMENT_TERMS_OPTIONS),
                response_deadline=datetime.utcnow() + timedelta(days=random.randint(1, 7)),
                notes=random.choice(NOTES_OPTIONS),
                product_type=request.product_type,
                specifications=request.specifications,
                color_spec=request.color_spec
            )
            db.add(rfq_details)

            rfq_count += 1

    db.commit()
    db.close()

    print(f"{len(client_requests)} RFQs sent to {len(suppliers)} suppliers ({rfq_count} total)")

if __name__ == "__main__":
    send_rfqs()


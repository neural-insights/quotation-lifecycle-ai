import random
from utils.db import SessionLocal
from utils.models import ClientRequest, RFQSent, QuotationResponse
from datetime import datetime

# Base price matrix: product type + color specification
BASE_PRICE_MATRIX = {
    "Flyer": {"4x4": 10.0, "4x0": 9.5, "Full color": 10.5, "B&W": 9.0},
    "Poster": {"4x4": 11.0, "4x0": 10.0, "Full color": 11.5, "B&W": 9.8},
    "T-shirt": {"4x4": 12.0, "4x0": 11.0, "Full color": 13.0, "B&W": 10.5},
    "Sticker": {"4x4": 9.5, "4x0": 9.0, "Full color": 10.0, "B&W": 8.5},
    "Brochure": {"4x4": 11.5, "4x0": 10.5, "Full color": 12.0, "B&W": 10.0},
    "Banner": {"4x4": 13.0, "4x0": 12.0, "Full color": 13.5, "B&W": 11.5},
}

def simulate_quotation(product_type, color_spec, quantity, is_custom=False):
    base_price = BASE_PRICE_MATRIX.get(product_type, {}).get(color_spec)

    if base_price is None:
        # fallback if combination not found
        base_price = 10.0

    multiplier = 1.2 if is_custom else 1.0
    unit_price = round(base_price * random.uniform(0.9, 1.2) * multiplier, 2)
    
    return {
        "unit_price": unit_price,
        "total_price": round(unit_price * quantity, 2),
        "estimated_delivery_days": int(random.randint(3, 10) * multiplier),
    }

def generate_quotations():
    db = SessionLocal()
    rfqs = db.query(RFQSent).filter_by(status="sent").all()

    for rfq in rfqs:
        if db.query(QuotationResponse).filter_by(rfq_id=rfq.id).first():
            continue

        request = db.query(ClientRequest).filter_by(id=rfq.client_request_id).first()
        if not request:
            continue

        is_custom = request.is_custom

        quote = simulate_quotation(
            product_type=request.product_type,
            color_spec=request.color_spec,
            quantity=request.quantity,
            is_custom=is_custom
        )

        quotation = QuotationResponse(
            rfq_id=rfq.id,
            unit_price=quote["unit_price"],
            delivery_days=quote["estimated_delivery_days"],
            received_at=datetime.now()
        )
        
        db.add(quotation)

    db.commit()
    db.close()
    print("Quotations simulated and saved.")

if __name__ == "__main__":
    generate_quotations()


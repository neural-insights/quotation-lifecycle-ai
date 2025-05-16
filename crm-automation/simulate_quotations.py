import random
from db import SessionLocal
from models import ClientRequest, RFQSent, QuotationResponse
from datetime import datetime

# Base price table per product type
PRODUCT_BASE_PRICES = {
    "Flyer": 0.12,
    "Banner": 2.50,
    "T-shirt": 4.00,
    "Poster": 1.80,
    "Sticker": 0.30
}

# Price modifiers by color specification
COLOR_PRICE_MODIFIERS = {
    "CMYK": 1.0,
    "Pantone": 1.2,
    "RGB": 0.9,
    "Grayscale": 0.8,
}

def simulate_quotation(product_type, color_spec, quantity, is_custom=False):
    base_price = PRODUCT_BASE_PRICES.get(product_type, 1.00)  # generic fallback
    color_modifier = COLOR_PRICE_MODIFIERS.get(color_spec, 1.0)

    multiplier = 1.2 if is_custom else 1.0
    unit_price = round(base_price * color_modifier * random.uniform(0.9, 1.2) * multiplier, 2)
    
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




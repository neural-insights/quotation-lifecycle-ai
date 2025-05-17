import requests
import random
from datetime import datetime
from utils.db import SessionLocal
from utils.models import ClientRequest

def fetch_crm_data():
    """Fetch simulated CRM requests from the local API endpoint."""
    response = requests.get("http://localhost:8000/hubspot/simulate_requests")
    return response.json()

def save_to_db(data):
    """Insert CRM data into the database, avoiding duplicate entries per customer."""
    db = SessionLocal()
    for entry in data:

        deadline_str = entry.get("delivery_deadline")
        if not deadline_str:
            print("Skipping entry without delivery_deadline.")
            continue

        try:
            deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Skipping entry with invalid deadline format: {deadline_str}")
            continue

        customer_id = entry.get("customer_id")
        if not customer_id:
            print("Skipping entry without customer_id.")
            continue
        
        is_custom = random.random() < 0.2

        # Avoid duplicate entries for the same customer
        existing = db.query(ClientRequest).filter_by(customer_id=customer_id).first()
        if not existing:
            new_request = ClientRequest(
                product_type=entry.get("product_type", "unknown"),
                quantity=entry.get("quantity", 0),
                deadline=deadline_date,
                specifications=entry.get("specifications", ""),
                color_spec=entry.get("color_spec", ""),
                is_custom=is_custom,
                customer_id=customer_id
            )
            db.add(new_request)

    db.commit()
    db.close()

if __name__ == "__main__":
    data = fetch_crm_data()
    save_to_db(data)
    print(f"{len(data)} CRM entries processed and saved.")



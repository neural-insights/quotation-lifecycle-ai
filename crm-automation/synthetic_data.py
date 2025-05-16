import random
from datetime import datetime, timedelta

# Generates a single random client quotation request
def generate_synthetic_request():
    companies = ["Acme Inc", "Bravo Ltd", "Printify", "ColorLab"]
    products = ["Flyer", "Poster", "T-shirt", "Sticker", "Brochure", "Banner"]
    specs = ["A5, 170g", "A3, glossy", "Cotton, size L", "Vinyl, 10x10cm"]
    colors = ["4x4", "4x0", "Full color", "B&W"]

    company = random.choice(companies)
    product = random.choice(products)
    spec = random.choice(specs)
    color = random.choice(colors)

    return {
        "customer_id": f"C{random.randint(100, 999)}",
        "company_name": company,
        "contact_email": f"client@{company.lower().replace(' ', '')}.com",
        "product_type": product,
        "specifications": spec,
        "quantity": random.choice([100, 500, 1000, 2000]),
        "color_spec": color,
        "delivery_deadline": (datetime.today() + timedelta(days=random.randint(3, 14))).date().isoformat(),
        "special_requirements": random.choice(["", "Include size mix", "Urgent", "Double check color match"]),
        "request_date": datetime.today().date().isoformat(),
        "is_custom": random.random() < 0.2  # ~20% chance of being True
    }


# Generates a batch of synthetic client requests
def generate_bulk_requests(n=10):
    return [generate_synthetic_request() for _ in range(n)]


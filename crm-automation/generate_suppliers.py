from db import SessionLocal
from models import Supplier
import random

def generate_suppliers(n=20):
    supplier_names = [
        "AlphaPrint", "BetaColor", "GigaPress", "FlyerFactory", "TeeMasters",
        "VinylKing", "ExpressInk", "ColorSprint", "FlexiPrint", "ZetaGraphics",
        "RapidPress", "InkFusion", "NeoPrint", "ArtifyPress", "MetroPrints",
        "NovaPrint", "EcoFlyers", "PremiumInk", "BoldPress", "SigmaPrint"
    ]
    product_types = ["Flyer", "Poster", "T-shirt", "Sticker", "Brochure", "Banner"]

    db = SessionLocal()

    for i in range(n):
        name = supplier_names[i % len(supplier_names)]
        email = f"{name.lower()}@supplier.com"

        # Check if supplier already exists
        existing = db.query(Supplier).filter_by(email=email).first()
        if existing:
            continue  # Skip if already exists

        supported = random.sample(product_types, k=random.randint(1, len(product_types)))
        supported_str = ", ".join(supported)  

        new_supplier = Supplier(
            name=name,
            email=email,
            supported_products=supported_str,
            performance_score=round(random.uniform(3.0, 5.0), 2)
        )

        db.add(new_supplier)

    db.commit()
    db.close()
    print(f"{n} synthetic suppliers generated successfully.")

if __name__ == "__main__":
    generate_suppliers(n=20)



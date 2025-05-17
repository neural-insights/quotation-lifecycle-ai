import random
import math
from datetime import datetime, timedelta
from utils.db import SessionLocal
from utils.models import TrainingQuotation

NUM_SAMPLES = 10000
TARGET_WIN_RATE = 0.20
MAX_WON = int(NUM_SAMPLES * TARGET_WIN_RATE)

PRODUCT_TYPES = ["Flyer", "Poster", "T-shirt", "Sticker", "Brochure", "Banner"]
SPECIFICATIONS = ["A5, 170g", "A3, glossy", "Cotton, size L", "Vinyl, 10x10cm"]
COLORS = ["4x4", "4x0", "Full color", "B&W"]

BASE_PRICE_MATRIX = {
    "Flyer": {"4x4": 10.0, "4x0": 9.5, "Full color": 10.5, "B&W": 9.0},
    "Poster": {"4x4": 11.0, "4x0": 10.0, "Full color": 11.5, "B&W": 9.8},
    "T-shirt": {"4x4": 12.0, "4x0": 11.0, "Full color": 13.0, "B&W": 10.5},
    "Sticker": {"4x4": 9.5, "4x0": 9.0, "Full color": 10.0, "B&W": 8.5},
    "Brochure": {"4x4": 11.5, "4x0": 10.5, "Full color": 12.0, "B&W": 10.0},
    "Banner": {"4x4": 13.0, "4x0": 12.0, "Full color": 13.5, "B&W": 11.5},
}

def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val <= min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)

def calculate_rfq_complexity(description: str, quantity: int) -> float:
    base = 1.0 if quantity < 50 else 2.0 if quantity < 200 else 3.0
    if "custom" in description.lower():
        base += 1.0
    return round(base + random.uniform(-0.3, 0.3), 2)

def is_urgent(deadline: datetime, sent_at: datetime) -> bool:
    return (deadline - sent_at).days <= 2

def generate_synthetic_training_data():
    db = SessionLocal()
    records = []
    num_won = 0

    for _ in range(NUM_SAMPLES):
        quantity = random.randint(50, 1000)
        base_product_type = random.choice(PRODUCT_TYPES)
        color_spec = random.choice(COLORS)

        is_custom = random.random() < 0.2
        description = f"custom {base_product_type}" if is_custom else base_product_type

        sent_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        deadline = sent_at + timedelta(days=random.randint(1, 15))

        complexity = calculate_rfq_complexity(description, quantity)
        urgent = is_urgent(deadline, sent_at)

        base_price = BASE_PRICE_MATRIX[base_product_type][color_spec]
        base_price *= 1.2 if is_custom else 1.0
        unit_price = round(random.uniform(base_price * 0.9, base_price * 1.1), 2)

        delivery_days = random.randint(3, 10)
        performance_score = round(random.uniform(0.0, 5.0), 2)
        response_time = round(random.uniform(1, 72), 2)
        spec = random.choice(SPECIFICATIONS)

        norm_price = normalize(unit_price, 8.0, 14.0)
        norm_days = normalize(delivery_days, 3, 10)
        norm_quantity = normalize(quantity, 50, 1000)

        base_score = (1 - norm_price) * 0.5 + (1 - norm_days) * 0.3 + norm_quantity * 0.2
        prob_win = sigmoid(base_score * 6 + random.uniform(-1, 1))

        score = 100
        score -= unit_price * 2
        score -= delivery_days * 1.5
        score -= response_time * (5 if urgent else 2)
        score += performance_score * 4
        score -= complexity * 1.5
        if urgent and (delivery_days > 3 or response_time > 24):
            score -= 15
        score += random.uniform(-20, 20)

        decision_noise = score + random.uniform(-15, 15) > 50
        win_chance = random.random() < prob_win + random.uniform(-0.2, 0.2)

        if decision_noise and win_chance and num_won < MAX_WON:
            won = 1
            num_won += 1
        else:
            won = 0

        record = TrainingQuotation(
            unit_price=unit_price,
            delivery_days=delivery_days,
            performance_score=performance_score,
            response_time=response_time,
            rfq_complexity_score=complexity,
            is_urgent=urgent,
            is_custom=is_custom,
            won=won
        )

        records.append(record)

    # 🔁 Label flipping: introduce noise by flipping 1% of each class
    won_ones = [r for r in records if r.won == 1]
    won_zeros = [r for r in records if r.won == 0]

    flip_count_1_to_0 = max(1, int(len(won_ones) * 0.01))
    flip_count_0_to_1 = max(1, int(len(won_zeros) * 0.01))

    for r in random.sample(won_ones, flip_count_1_to_0):
        r.won = 0

    for r in random.sample(won_zeros, flip_count_0_to_1):
        r.won = 1

    # Adiciona todos os registros com as labels já flipadas
    db.add_all(records)
    db.commit()
    db.close()

    print(f"{NUM_SAMPLES} samples generated (~{TARGET_WIN_RATE*100}% win rate + 1% flipped noise).")

if __name__ == "__main__":
    generate_synthetic_training_data()






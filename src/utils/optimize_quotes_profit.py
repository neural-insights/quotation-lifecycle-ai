from sqlalchemy.orm import Session
from utils.db import SessionLocal
from utils.models import MergedQuote, SelectedQuote
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def optimize_quotes_simple():
    db: Session = SessionLocal()

    try:
        # Fetch all merged quotes from the database
        data = db.query(MergedQuote).all()
        df = pd.DataFrame([{
            'client_request_id': q.client_request_id,
            'customer_id': q.customer_id,
            'supplier_id': q.supplier_id,
            'supplier_name': q.supplier_name,
            'supplier_performance_score': q.supplier_performance_score,
            'quotation_response_id': q.quotation_response_id,
            'unit_price': q.unit_price,
            'ml_score': q.ml_score,
            'heuristic_score': q.heuristic_score,
            'rfq_sent_at': q.rfq_sent_at,
            'delivery_days': q.delivery_days
        } for q in data])

        if df.empty:
            print("No quotes found.")
            return

        # Define minimum and maximum markup (e.g., 5% to 20% markup)
        MIN_MARKUP = 1.05  # 5% margin
        MAX_MARKUP = 1.20  # 20% margin

        # Normalize ml_score to [0, 1] range
        scaler = MinMaxScaler()
        df['ml_score_norm'] = scaler.fit_transform(df[['ml_score']])

        # Calculate markup proportionally to normalized ml_score
        df['markup'] = MIN_MARKUP + df['ml_score_norm'] * (MAX_MARKUP - MIN_MARKUP)

        # Calculate selling price and profit margin based on dynamic markup
        df['selling_price'] = df['unit_price'] * df['markup']
        df['profit_margin'] = (df['selling_price'] - df['unit_price']) / df['selling_price']

        # Normalize ml_score_norm and profit_margin to [0,1] range for weighted scoring
        df[['ml_score_norm_scaled', 'profit_margin_norm']] = scaler.fit_transform(df[['ml_score_norm', 'profit_margin']])

        # Define weights: higher for ml_score, lower for profit margin
        WEIGHTS = {'ml_score_norm_scaled': 0.7, 'profit_margin_norm': 0.3}

        # Compute final weighted score
        df['final_score'] = (
            df['ml_score_norm_scaled'] * WEIGHTS['ml_score_norm_scaled'] +
            df['profit_margin_norm'] * WEIGHTS['profit_margin_norm']
        )

        # Select the best quote per client_request based on final_score
        best_quotes = df.loc[df.groupby('client_request_id')['final_score'].idxmax()]

        # Sanity check: ensure only one quote per client_request (supplier must be different)
        assert best_quotes['client_request_id'].nunique() == len(best_quotes), "More than one quote per client_request found!"
        assert best_quotes.groupby('client_request_id')['supplier_id'].nunique().eq(1).all(), "Multiple suppliers selected for the same client_request!"

        # Clear previous selections and save new best quotes (excluding ml_score)
        db.query(SelectedQuote).delete()
        db.commit()

        selected = [
            SelectedQuote(
                client_request_id=row.client_request_id,
                customer_id=row.customer_id,
                supplier_id=row.supplier_id,
                supplier_name=row.supplier_name,
                supplier_performance_score=row.supplier_performance_score,
                quotation_response_id=row.quotation_response_id,
                unit_price=row.unit_price,
                profit_margin=row.profit_margin,
                rfq_sent_at=row.rfq_sent_at,
                heuristic_score=row.heuristic_score,
                delivery_days=row.delivery_days
            )
            for _, row in best_quotes.iterrows()
        ]

        db.bulk_save_objects(selected)
        db.commit()

        print(f"Optimization complete. {len(selected)} quotes selected and saved.")

    except Exception as e:
        db.rollback()
        print(f"Error during optimization: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    optimize_quotes_simple()


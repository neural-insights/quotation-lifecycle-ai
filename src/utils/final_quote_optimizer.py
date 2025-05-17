from sqlalchemy.orm import Session
from utils.db import SessionLocal
from utils.models import (
    ClientRequest, Supplier, RFQSent,
    QuotationResponse, QuoteScore, MergedQuote
)
from sqlalchemy.exc import SQLAlchemyError

def build_merged_quotes_table():
    db: Session = SessionLocal()

    try:
        results = (
            db.query(
                ClientRequest.id.label("client_request_id"),
                ClientRequest.customer_id.label("customer_id"),  
                Supplier.id.label("supplier_id"),
                Supplier.name.label("supplier_name"),
                Supplier.performance_score.label("supplier_performance_score"),
                QuotationResponse.id.label("quotation_response_id"),
                QuotationResponse.unit_price,
                QuotationResponse.delivery_days,
                RFQSent.sent_at.label("rfq_sent_at"),
                QuoteScore.won.label("ml_score"),
                QuoteScore.performance_score.label("heuristic_score"),
            )
            .join(RFQSent, RFQSent.client_request_id == ClientRequest.id)
            .join(Supplier, Supplier.id == RFQSent.supplier_id)
            .join(QuotationResponse, QuotationResponse.rfq_id == RFQSent.id)
            .join(QuoteScore, QuoteScore.id == QuotationResponse.id)
            .all()
        )

        # Clear existing data in merged_quotes table to avoid duplicates
        db.query(MergedQuote).delete()
        db.commit()

        # Insert fetched data into MergedQuote table
        merged_quotes = [
            MergedQuote(
                client_request_id=row.client_request_id,
                customer_id=row.customer_id,
                supplier_id=row.supplier_id,
                supplier_name=row.supplier_name,
                supplier_performance_score=row.supplier_performance_score,
                quotation_response_id=row.quotation_response_id,
                unit_price=row.unit_price,
                delivery_days=row.delivery_days,
                rfq_sent_at=row.rfq_sent_at,
                ml_score=row.ml_score,
                heuristic_score=row.heuristic_score,
            )
            for row in results
        ]

        db.bulk_save_objects(merged_quotes)
        db.commit()

        print(f"Successfully saved {len(merged_quotes)} merged quotes to the database.")

    except SQLAlchemyError as e:
        db.rollback()
        print("An error occurred while saving merged quotes:", e)

    finally:
        db.close()

if __name__ == "__main__":
    build_merged_quotes_table()



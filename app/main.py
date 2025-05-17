from flask import Flask, jsonify, render_template
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.utils.db import SessionLocal
from src.utils.models import SelectedQuote, MergedQuote
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
print("Template folder:", app.template_folder)

@app.route("/selected_quotes")
def selected_quotes_html():
    db: Session = SessionLocal()
    print("Template folder:", app.template_folder)
    try:
        quotes = db.query(SelectedQuote).all()
        return render_template("selected_quotes.html", quotes=quotes)
    finally:
        db.close()

@app.route("/api/selected_quotes")
def selected_quotes_api():
    db: Session = SessionLocal()
    try:
        quotes = db.query(SelectedQuote).all()
        result = [
            {
                "client_request_id": q.client_request_id,
                "customer_id": q.customer_id,
                "supplier_id": q.supplier_id,
                "supplier_name": q.supplier_name,
                "quotation_response_id": q.quotation_response_id,
                "unit_price": q.unit_price,
                "profit_margin": q.profit_margin,
                "delivery_days": q.delivery_days,
                "rfq_sent_at": q.rfq_sent_at.isoformat() if q.rfq_sent_at else None,
                "supplier_performance_score": q.supplier_performance_score,
                "heuristic_score": q.heuristic_score,
            }
            for q in quotes
        ]
        return jsonify(result)
    finally:
        db.close()

@app.route("/supplier_performance")
def supplier_performance():
    db = SessionLocal()
    try:
        # Exemplo: agregação simples por supplier
        query = (
            db.query(
                MergedQuote.supplier_name,
                func.count(SelectedQuote.id).label("quotes_selected"),
                func.avg(SelectedQuote.profit_margin).label("avg_profit_margin"),
                func.avg(SelectedQuote.heuristic_score).label("avg_heuristic_score")
            )
            .join(SelectedQuote, SelectedQuote.supplier_id == MergedQuote.supplier_id)
            .group_by(MergedQuote.supplier_name)
            .all()
        )

        # Converte para lista de dicts para passar pro template
        performance = [
            {
                "supplier_name": row.supplier_name,
                "quotes_selected": row.quotes_selected,
                "avg_profit_margin": row.avg_profit_margin,
                "avg_heuristic_score": row.avg_heuristic_score,
            }
            for row in query
        ]
        return render_template("supplier_performance.html", performance=performance)
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)




from flask import Flask, jsonify, render_template, send_from_directory
from sqlalchemy.orm import Session
from sqlalchemy import func
from utils.db import SessionLocal
from utils.models import SelectedQuote, MergedQuote
from utils.paths import DB_PATH
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, roc_auc_score, classification_report

# Define Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/selected_quotes")
def selected_quotes_html():
    db: Session = SessionLocal()
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

@app.route("/model_dashboard")
def model_dashboard():
    from sklearn.model_selection import train_test_split
    from sklearn.calibration import calibration_curve

    # Load model and scaler
    model = joblib.load("src/models/best_logistic_model.pkl")
    scaler = joblib.load("src/models/minmax_scaler.pkl")

    # Load and prepare data
    df = pd.read_sql_query("SELECT * FROM training_quotations", f"sqlite:///{DB_PATH}")
    X = df.drop(columns=["id", "won"])
    y = df["won"]

    non_binary_columns = ['unit_price', 'delivery_days', 'performance_score', 'response_time', 'rfq_complexity_score']

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_scaled = X_train.copy()
    X_train_scaled[non_binary_columns] = scaler.transform(X_train[non_binary_columns])
    X_val_scaled = X_val.copy()
    X_val_scaled[non_binary_columns] = scaler.transform(X_val[non_binary_columns])

    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_val_pred = model.predict(X_val_scaled)
    y_train_proba = model.predict_proba(X_train_scaled)[:, 1]
    y_val_proba = model.predict_proba(X_val_scaled)[:, 1]

    # Classification reports
    class_report_train = classification_report(y_train, y_train_pred, output_dict=True)
    class_report_val = classification_report(y_val, y_val_pred, output_dict=True)

    os.makedirs(app.static_folder, exist_ok=True)

    # Confusion matrices
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ConfusionMatrixDisplay.from_predictions(y_train, y_train_pred, ax=ax[0], cmap="Blues", colorbar=False)
    ax[0].set_title("Confusion Matrix - Train Set")
    ConfusionMatrixDisplay.from_predictions(y_val, y_val_pred, ax=ax[1], cmap="Greens", colorbar=False)
    ax[1].set_title("Confusion Matrix - Validation Set")
    cm_path = os.path.join(app.static_folder, "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(cm_path)
    plt.close()

    # ROC curve
    fpr, tpr, _ = roc_curve(y_val, y_val_proba)
    auc_score = roc_auc_score(y_val, y_val_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve (Validation)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    roc_path = os.path.join(app.static_folder, "roc_curve.png")
    plt.savefig(roc_path)
    plt.close()

    # Feature importance
    coefs = model.coef_[0]
    features = X.columns
    coef_df = pd.DataFrame({'Feature': features, 'Coefficient': coefs})
    coef_df['Abs_Coefficient'] = coef_df['Coefficient'].abs()
    coef_df.sort_values(by='Abs_Coefficient', ascending=False, inplace=True)
    feat_imp_path = os.path.join(app.static_folder, "feature_importance.png")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=coef_df.head(10), x='Coefficient', y='Feature', palette='coolwarm')
    plt.title("Top 10 Most Influential Features - Logistic Regression")
    plt.xlabel("Coefficient Value")
    plt.ylabel("Feature")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(feat_imp_path)
    plt.close()

    # Calibration curve
    true_fraction, predicted_prob = calibration_curve(y_val, y_val_proba, n_bins=10)
    plt.figure(figsize=(6, 6))
    plt.plot(predicted_prob, true_fraction, marker='o', label='Model')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Calibration')
    plt.xlabel('Predicted Probability')
    plt.ylabel('Observed Frequency of Positives')
    plt.title('Calibration Curve - Validation Set')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    calib_path = os.path.join(app.static_folder, "calibration_curve.png")
    plt.savefig(calib_path)
    plt.close()

    # Probability distribution histogram
    proba_df = pd.DataFrame({
        'Predicted_Probability': y_val_proba,
        'Actual_Label': y_val
    })
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=proba_df,
        x='Predicted_Probability',
        hue='Actual_Label',
        bins=20,
        kde=False,
        stat='density',
        palette='Set2',
        multiple='stack'
    )
    plt.title('Predicted Probability Distribution by Class')
    plt.xlabel('Predicted Probability (Class = 1)')
    plt.ylabel('Density')
    plt.legend(title='True Class', labels=['Negative (0)', 'Positive (1)'])
    plt.grid(True)
    plt.tight_layout()
    proba_hist_path = os.path.join(app.static_folder, "proba_histogram.png")
    plt.savefig(proba_hist_path)
    plt.close()

    return render_template("model_dashboard.html",
        confusion_matrix_image="static/confusion_matrix.png",
        roc_curve_image="static/roc_curve.png",
        feature_importance_image="static/feature_importance.png",
        calibration_curve_image="static/calibration_curve.png",
        proba_histogram_image="static/proba_histogram.png",
        class_report_train=class_report_train,
        class_report_val=class_report_val
    )


if __name__ == "__main__":
    app.run(debug=True)

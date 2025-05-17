from pathlib import Path
import pandas as pd
import numpy as np
import sqlite3
import joblib
import os

from utils.paths import DB_PATH 

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_logistic_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "minmax_scaler.pkl"

# === Load model and scaler ===
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# === Define expected columns ===
binary_columns = ['is_urgent', 'is_custom']
non_binary_columns = ['unit_price', 'delivery_days', 'performance_score', 'response_time', 'rfq_complexity_score']
feature_columns =  non_binary_columns + binary_columns

# === Connect to database ===
conn = sqlite3.connect(DB_PATH) 

# === Load table ===
df_all = pd.read_sql_query("SELECT * FROM real_quotation_data", conn)
#df_all.drop(columns=['id'], inplace=True)

# === Filter only new rows (not yet scored) ===
df_new = df_all[df_all['won'].isnull()].copy()

# If no new data, stop early
if df_new.empty:
    print("✅ No new data to process.")
    conn.close()
    exit()

# === Basic validation ===
for col in feature_columns:
    if col not in df_new.columns:
        raise ValueError(f"Missing expected column: {col}")

# Handle unexpected data types or missing values
df_new = df_new[feature_columns].copy()

# Fill any missing values with safe defaults (optional tuning)
df_new[non_binary_columns] = df_new[non_binary_columns].fillna(0)
df_new[binary_columns] = df_new[binary_columns].fillna(0).astype(int)

# === Scale non-binary columns ===
X_new_scaled = df_new.copy()
X_new_scaled[non_binary_columns] = scaler.transform(df_new[non_binary_columns])

# === Predict probabilities ===
X_input = X_new_scaled[feature_columns]
acceptance_probs = model.predict_proba(X_input)[:, 1]

# === Insert predictions back into df_all ===
df_all.loc[df_all['won'].isnull(), 'won'] = acceptance_probs

# === Save updated table ===
df_all[["id", "won", "performance_score"]].to_sql("quote_scores", conn, if_exists="append", index=False)
conn.close()

print("✅ Scoring pipeline completed and database updated.")


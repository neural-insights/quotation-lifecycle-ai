import pandas as pd
import numpy as np
import sqlite3
import joblib
import os

# === Load model and scaler ===
model = joblib.load("best_logistic_model.pkl")
scaler = joblib.load("minmax_scaler.pkl")

# === Define expected columns ===
binary_columns = ['is_urgent', 'is_custom']
non_binary_columns = ['unit_price', 'delivery_days', 'performance_score', 'response_time', 'rfq_complexity_score']
feature_columns = binary_columns + non_binary_columns

# === Connect to database ===
db_path = "quotations.db"
conn = sqlite3.connect(db_path)

# === Load table ===
df_all = pd.read_sql_query("SELECT * FROM real_quotation_data", conn)

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
df_new = df_new[feature_columns + ['id']].copy()

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
df_all.to_sql("real_quotation_data", conn, if_exists="replace", index=False)
conn.close()

print("✅ Scoring pipeline completed and database updated.")

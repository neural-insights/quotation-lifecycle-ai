from pathlib import Path
import os
import pandas as pd
import sqlite3
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from imblearn.under_sampling import RandomUnderSampler

from utils.paths import DB_PATH

# === Load data from SQLite database ===
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM training_quotations", conn)
df_test = pd.read_sql_query("SELECT * FROM real_quotation_data", conn)
conn.close()

# === Define feature and target columns ===
binary_columns = ['is_urgent', 'is_custom']
non_binary_columns = ['unit_price', 'delivery_days', 'performance_score', 'response_time', 'rfq_complexity_score']

X = df.drop(columns=['id', 'won'])
y = df['won']

# === Split data ===
X_train_full, X_val_full, y_train, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === Undersample training data ===
undersampler = RandomUnderSampler(random_state=42)
X_train_us, y_train_us = undersampler.fit_resample(X_train_full, y_train)

# === Scale non-binary columns ===
scaler = MinMaxScaler()
X_train_us_scaled = X_train_us.copy()
X_val_scaled = X_val_full.copy()

X_train_us_scaled[non_binary_columns] = scaler.fit_transform(X_train_us[non_binary_columns])
X_val_scaled[non_binary_columns] = scaler.transform(X_val_full[non_binary_columns])

# === Logistic Regression with Grid Search ===
param_grid = {
    'penalty': ['l1', 'l2'],
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'saga']
}

logreg = LogisticRegression(max_iter=1000, random_state=42)
grid_search = GridSearchCV(logreg, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=0)
grid_search.fit(X_train_us_scaled, y_train_us)

# === Save best model and scaler ===
BASE_DIR = Path(__file__).resolve().parent.parent
models_dir = BASE_DIR / "models"
models_dir.mkdir(exist_ok=True)

joblib.dump(grid_search.best_estimator_, models_dir / "best_logistic_model.pkl")
joblib.dump(scaler, models_dir / "minmax_scaler.pkl")

print("✅ Model and scaler saved successfully in models/")


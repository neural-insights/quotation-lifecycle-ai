# 🧠 Quotation Lifecycle AI

A **lifecycle AI** solution for intelligent quotation scoring — integrating synthetic data generation, training pipeline automation, and Flask-based deployment for seamless monitoring and visualization.

---

## 📚 Table of Contents

- [📦 Project Setup](#-project-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Set the Python Path](#4-set-the-python-path)
  - [5. Run the Full Pipeline](#5-run-the-full-pipeline)
- [⚠️ Model Selection Note](#️-model-selection-note)
- [🌐 Launch the Flask App](#-launch-the-flask-app)
  - [Available Routes](#available-routes)
- [📄 License](#-license)
- [🤝 Contribution](#-contribution)

---

## 📦 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/neural-insights/quotation-lifecycle-ai.git
cd quotation-lifecycle-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

- **Linux/macOS**
  ```bash
  source .venv/bin/activate
  ```

- **Windows**
  ```cmd
  .venv\Scripts\activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set the Python Path

All internal modules use relative imports based on the `src/` directory.

- **Linux/macOS**
  ```bash
  export PYTHONPATH="$(pwd)/src"
  ```

- **Windows CMD**
  ```cmd
  set PYTHONPATH=%cd%\src
  ```

- **PowerShell**
  ```powershell
  $env:PYTHONPATH="$PWD/src"
  ```

### 5. Run the Full Pipeline

```bash
python run_all.py
```

This will:

1. Generate a SQLite database at `./src/data/quotations.db`  
2. Train a Logistic Regression model and save it to `./src/models/`  
3. Save a MinMax Scaler for future use  
4. Prepare all assets needed for Flask deployment  

---

## ⚠️ Model Selection Note

The final model was selected based on tests from the notebook `quotation_scoring_model.ipynb`, comparing Logistic Regression, Random Forest, XGBoost, and LightGBM classifiers.

Although Logistic Regression performed slightly worse, it was chosen for its **simplicity, interpretability, and low computational cost**—valuable features in business scenarios. Hyperparameters were optimized via GridSearch and persisted.

---

## 🌐 Launch the Flask App

To launch the dashboard locally:

```bash
python app/main.py
```

This will serve the app at:  
➡️ **http://127.0.0.1:5000/**

### Available Routes

| Route                   | Description                                      |
|-------------------------|--------------------------------------------------|
| `/selected_quotes`      | Display all selected quotes                      |
| `/api/selected_quotes`  | API endpoint returning selected quotes as JSON   |
| `/supplier_performance` | Supplier statistics and average metrics          |
| `/model_dashboard`      | Visual evaluation of model performance (ROC, CM) |

---

## 📄 License

This project is licensed under the terms of the **MIT License**.

---

## 🤝 Contribution

Pull requests and issues are welcome.  
Please ensure code quality, readability, and consistency with the current architecture.

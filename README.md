# 🧠 Quotation Lifecycle AI

A **lifecycle AI** solution for intelligent quotation scoring — integrating synthetic data generation, training pipeline automation, and Flask-based deployment for seamless monitoring and visualization.

![AI Visualization](https://github.com/neural-insights/quotation-lifecycle-ai/blob/master/src/img/openart-image_Cii8lQqE_1747523132664_raw.png)

💡 This project simulates an AI-powered quotation lifecycle system designed to automate B2B quoting processes, optimize supplier selection, and maximize profit margins. By replacing manual workflows with intelligent data-driven automation, it significantly reduces processing time and labor effort across the end-to-end quotation pipeline—enabling faster, smarter commercial decision-making.

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

### 5. Run the FastAPI App
To launch the interactive API (for simulating RFQ requests and viewing responses):

```bash
uvicorn src.utils.main:app --reload
```
This will start the app at http://127.0.0.1:8000, with automatic reload for development.

*Access the interactive Swagger UI at: http://127.0.0.1:8000/docs


### 6. Run the Full Pipeline

With the server running, open another terminal, activate the virtual environment, set the Python path, and then run:

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

## Tree Structure

```bash
.
├── .gitignore                  # Git exclusions
├── LICENSE.txt                # Project license (MIT)
├── README.md
├── requirements.txt           # All Python dependencies
├── run_all.py                 # Full pipeline executor (end-to-end)
├── app/                       # Flask dashboard application
│   ├── main.py                # Entry point for the Flask app
│   ├── static/                # Static assets for visualization
│   │   ├── ...
│   └── templates/             # HTML templates (Jinja2)
│       ├── ...
├── src/                       # Core source code
│   ├── data/                  # Contains the SQLite database
│   │   └── quotations.db
│   ├── img/                   # Project or report images
│   ├── models/                # Trained models and scalers
│   │   ├── best_logistic_model.pkl
│   │   └── minmax_scaler.pkl
│   ├── notebooks/             # Jupyter notebook experiments
│   │   └── quotation_scoring_model.ipynb
│   ├── pipelines/             # (Optional) Custom pipeline orchestration
│   └── utils/                 # FastAPI + supporting logic
│       ├── ...
└── tree_structure.txt         # Output of the folder structure
```

---

## 📄 License

This project is licensed under the terms of the **MIT License**.

---


### 🤝 How to Contribute
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/some-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/some-feature`)
5. Open a Pull Request

Pull requests and issues are welcome.  
Please ensure code quality, readability, and consistency with the current architecture.



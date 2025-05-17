# Quotation Lifecycle AI

A full lifecycle AI-driven quotation selection and scoring prototype, integrating data simulation, training pipeline automation, and deployment via Flask for visualization and performance monitoring.

## 📁 Repository Structure


```text
.
├── app/                   # Flask deployment (UI)
│   ├── main.py            # Flask app with all routes
│   ├── static/            # Generated plots (confusion matrix, ROC)
│   └── templates/         # HTML templates for UI
├── src/                   # Core logic and data/model handling
│   ├── data/              # SQLite database generated here
│   ├── img/               # (optional) images or outputs
│   ├── models/            # Trained ML models (.pkl)
│   ├── notebooks/         # Exploratory notebooks
│   ├── pipelines/         # (optional) pipeline definitions
│   └── utils/             # Scripts and ML pipeline components
├── run_all.py             # Complete automation pipeline script
├── requirements.txt       # Python dependencies
├── .gitignore
├── LICENSE.txt
└── tree_structure.txt     # Project structure overview
```


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/neural-insights/quotation-lifecycle-ai.git
cd quotation-lifecycle-ai


### 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# OR
.venv\Scripts\activate           # Windows


### 3. Install dependencies

pip install -r requirements.txt



### 4. Set the Python path
All internal modules use relative imports based on the src/ directory. Set your PYTHONPATH as follows:
export PYTHONPATH="$(pwd)/src"     # Linux/macOS
# OR
set PYTHONPATH=%cd%\src            # Windows CMD
$env:PYTHONPATH="$PWD/src"         # PowerShell


### 5. Run the Full Pipeline
Run the entire machine learning pipeline with:



This will:

1. Generate a SQLite database at ./src/data/quotations.db

2. Train a Logistic Regression model and save it to ./src/models/

3. Save a MinMax Scaler for future use

4. Prepare all assets needed for Flask deployment


## ⚠️ Model Selection Note
The final model was selected based on tests from the notebook quotation_scoring_model.ipynb, comparing Logistic Regression, Random Forest, XGBoost, and LightGBM classifiers. Although Logistic Regression performed slightly worse, it was chosen for its simplicity, interpretability, and low computational cost—valuable features in business scenarios. Hyperparameters were optimized via GridSearch and persisted.


## 🌐 Launch Flask App
To launch the Flask dashboard:

python app/main.py



This will serve the app at '''http://127.0.0.1:5000'''


| Route                   | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `/selected_quotes`      | Display all selected quotes                      |
| `/api/selected_quotes`  | API endpoint returning selected quotes as JSON   |
| `/supplier_performance` | Supplier statistics and average metrics          |
| `/model_dashboard`      | Visual evaluation of model performance (ROC, CM) |


## 📄 License
This project is licensed under the terms of the MIT License.

## 🤝 Contribution
Pull requests and issues are welcome. Please ensure code quality, readability, and consistency with the current architecture.



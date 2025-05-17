import os

# Get the root directory of the repository
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to the SQLite database
DB_PATH = os.path.join(BASE_DIR, "data", "quotations.db")

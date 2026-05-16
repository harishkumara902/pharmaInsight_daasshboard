import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "pharmainsight.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "pharmainsight-dev-secret")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-key-here")
DEFAULT_YEAR = 2024
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]

import os
from dotenv import load_dotenv

# Load key-value pairs from .env into the system environment
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Automated Airfare Price Index System"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://postgres:postgres@localhost:5432/airfare_db"
    )

settings = Settings()
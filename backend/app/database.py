import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger(__name__)

# Try connecting to configured database (PostgreSQL); if authentication/connection fails, fallback to SQLite
engine = None
try:
    temp_engine = create_engine(settings.DATABASE_URL)
    with temp_engine.connect() as conn:
        pass
    engine = temp_engine
    logger.info("Connected to PostgreSQL database successfully.")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite ('airfare_db.db') for local development.")
    engine = create_engine(
        "sqlite:///./airfare_db.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency: opens a database session for each request,
    and guarantees it closes when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
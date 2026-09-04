from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from app.database import Base

class AirfareIndex(Base):
    """
    SQLAlchemy ORM Model representing the 'airfare_index' table in PostgreSQL.
    Stores aggregated, precomputed index values over time.
    """
    __tablename__ = "airfare_index"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    route = Column(String(20), nullable=False, index=True) # e.g. "DEL-BOM" or "COMPOSITE"
    index_value = Column(Float, nullable=False) # e.g. 106.42
    base_value = Column(Float, default=100.0)
    calculation_method = Column(String(50), default="Jevons_Laspeyres")
    sample_size = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

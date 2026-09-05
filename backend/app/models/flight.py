from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from app.database import Base

class FlightPrice(Base):
    """
    SQLAlchemy ORM Model representing the 'flight_prices' table in PostgreSQL.
    Stores micro-level flight pricing observations.
    """
    __tablename__ = "flight_prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route = Column(String(10), nullable=False, index=True)         # e.g., 'DEL-BOM'
    airline = Column(String(50), nullable=False, index=True)       # e.g., 'IndiGo'
    flight_number = Column(String(20), nullable=False)             # e.g., '6E-2054'
    departure_date = Column(Date, nullable=False, index=True)      # e.g., 2026-09-11
    departure_time = Column(String(10), nullable=False)            # e.g., '08:30'
    arrival_time = Column(String(10), nullable=False)              # e.g., '10:45'
    booking_date = Column(Date, nullable=False)                    # Observation date
    advance_days = Column(Integer, nullable=False, index=True)     # 1, 7, 15, 30
    cabin_class = Column(String(20), default="Economy")
    base_fare = Column(Float, nullable=False)                      # Fare without taxes
    taxes = Column(Float, nullable=False)                          # Airport fees, GST
    total_fare = Column(Float, nullable=False)                     # Total paid price
    source = Column(String(50), nullable=False)                    # Collector source
    scraped_at = Column(DateTime, default=datetime.utcnow)        # Timestamp saved
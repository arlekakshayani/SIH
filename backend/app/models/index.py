from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, Date, DateTime

try:
    from app.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class AirfareIndex(Base):
    """
    SQLAlchemy model representing the Airfare Price Index for domestic routes.
    
    Stores calculated index values for specific routes (e.g., DEL-BOM) or 
    the overall COMPOSITE benchmark on a given date.
    """
    __tablename__ = "airfare_index"

    # Primary key identifier
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Date for which this index is calculated
    date = Column(Date, nullable=False, index=True)

    # Route identifier (e.g., 'DEL-BOM', 'BLR-DEL', 'HYD-MAA', or 'COMPOSITE')
    route = Column(String(50), nullable=False, index=True)

    # The calculated price index value (e.g., 104.25 relative to base 100.0)
    index_value = Column(Float, nullable=False)

    # The benchmark base value against which current prices are compared (normally 100.0)
    base_value = Column(Float, nullable=False, default=100.0)

    # Methodology used for this calculation (e.g., 'Jevons_Advance_Weighted')
    calculation_method = Column(String(100), nullable=False, default="Jevons_Advance_Weighted")

    # Total number of fare observations / samples included in this calculation
    sample_size = Column(Integer, nullable=False, default=0)

    # System timestamp when this index record was generated
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return (
            f"<AirfareIndex(id={self.id}, date={self.date}, route='{self.route}', "
            f"index_value={self.index_value}, base_value={self.base_value}, "
            f"sample_size={self.sample_size})>"
        )

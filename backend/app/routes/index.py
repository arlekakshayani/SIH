from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app.database import get_db
from app.models.index import AirfareIndex
from app.schemas.index import IndexResponseSchema
from app.services.index_calculator import IndexCalculatorService

router = APIRouter(prefix="/api/index", tags=["Index"])

@router.post("/calculate")
def trigger_index_calculation(
    target_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """Calculates and stores index metrics for a given date."""
    calc_date = target_date or date.today()
    created = IndexCalculatorService.calculate_daily_index(db, calc_date)
    return {
        "status": "success",
        "date": calc_date,
        "indices_created": created
    }

@router.get("/latest", response_model=List[IndexResponseSchema])
def get_latest_indices(db: Session = Depends(get_db)):
    """Returns the most recently compiled index figures."""
    return db.query(AirfareIndex).order_by(AirfareIndex.date.desc()).limit(10).all()

@router.get("/history", response_model=List[IndexResponseSchema])
def get_index_history(
    route: str = Query("COMPOSITE", description="Corridor code or 'COMPOSITE'"),
    db: Session = Depends(get_db)
):
    """Returns historical index trendlines for frontend charts."""
    return db.query(AirfareIndex).filter(
        AirfareIndex.route == route.upper()
    ).order_by(AirfareIndex.date.asc()).all()

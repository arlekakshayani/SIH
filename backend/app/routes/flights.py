from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.flight import FlightPrice
from app.schemas.flight import FlightCreateSchema, FlightResponseSchema
from app.services.cleaning import FlightCleaningService

router = APIRouter(prefix="/api/flights", tags=["Flights"])

@router.post("/batch", status_code=status.HTTP_201_CREATED)
def ingest_flight_batch(
    payload: List[FlightCreateSchema],
    db: Session = Depends(get_db)
):
    """
    Receives a batch of flight price observations from the scraper,
    validates each item, cleans duplicates, and commits to PostgreSQL.
    """
    saved_count = FlightCleaningService.clean_and_save_batch(db, payload)
    return {
        "status": "success",
        "records_received": len(payload),
        "records_saved": saved_count
    }

@router.get("/", response_model=List[FlightResponseSchema])
def list_flights(
    route: Optional[str] = Query(None, pattern=r"^[A-Za-z]{3}-[A-Za-z]{3}$", description="Filter by route, e.g., DEL-BOM"),
    advance_days: Optional[int] = Query(None, ge=0, le=365, description="Filter by horizon (1, 7, 15, 30)"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """
    Returns stored flight pricing observations from PostgreSQL with optional filtering.
    """
    query = db.query(FlightPrice)
    if route:
        query = query.filter(FlightPrice.route == route.upper())
    if advance_days is not None:
        query = query.filter(FlightPrice.advance_days == advance_days)

    return query.order_by(FlightPrice.scraped_at.desc()).limit(limit).all()

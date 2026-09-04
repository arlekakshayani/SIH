from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.flight import FlightPrice

router = APIRouter(prefix="/api/routes", tags=["Routes"])

@router.get("/", response_model=List[str])
def get_available_routes(db: Session = Depends(get_db)):
    """
    Returns a distinct list of all route corridors currently in the database.
    """
    distinct_routes = db.query(FlightPrice.route).distinct().all()
    # Flattens list of tuples [('DEL-BOM',), ('BLR-DEL',)] into ['DEL-BOM', 'BLR-DEL']
    return [r[0] for r in distinct_routes]

"""
routes/index.py
===============
FastAPI API Router for Airfare Price Index operations.

Endpoints:
- POST /api/index/calculate
- GET  /api/index/latest
- GET  /api/index/history
- GET  /api/index/history?route=DEL-BOM
"""

from datetime import date as dt_date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.index import (
    IndexResponseSchema,
    IndexCalculationRequest,
    IndexCalculationResponse,
)
from app.models.index import AirfareIndex
from app.services.index_calculator import IndexCalculatorService
from seed_test_data import get_prototype_synthetic_data

try:
    from app.database import get_db
except ImportError:
    def get_db():
        yield None


router = APIRouter(
    prefix="/api/index",
    tags=["Airfare Index Engine"]
)

# In-memory store used as a fallback when database is not connected
_IN_MEMORY_INDEX_STORE: List[dict] = []


@router.post(
    "/calculate",
    response_model=IndexCalculationResponse,
    status_code=status.HTTP_200_OK,
    summary="Trigger Airfare Price Index Calculation"
)
def calculate_index_endpoint(
    request: Optional[IndexCalculationRequest] = None,
    db: Optional[Session] = Depends(get_db)
):
    """
    Triggers the calculation of Route-level and Composite Airfare Price Indices.
    Delegates all mathematical logic directly to the IndexCalculatorService.
    """
    target_date = request.calculation_date if request and request.calculation_date else dt_date.today()
    calculator = IndexCalculatorService()

    # Calculate and save using database integration bridge
    calc_result = calculator.calculate_and_save_from_db(
        db=db,
        target_date=target_date,
        use_arithmetic=False
    )

    records_to_save = calc_result.get("records", [])

    global _IN_MEMORY_INDEX_STORE
    _IN_MEMORY_INDEX_STORE.extend(records_to_save)

    return IndexCalculationResponse(
        message=calc_result["message"],
        date_calculated=calc_result["date_calculated"],
        indices_generated=calc_result["indices_generated"],
        summary=calc_result["summary"],
        route_details=calc_result.get("route_details", {}),
        records=records_to_save
    )



@router.get(
    "/latest",
    response_model=List[IndexResponseSchema],
    summary="Get Latest Airfare Price Index for All Routes"
)
def get_latest_index(db: Optional[Session] = Depends(get_db)):
    """
    Retrieves the most recent calculated index values for all monitored sectors
    and the overall COMPOSITE benchmark.
    """
    if db is not None:
        try:
            latest_date_subquery = db.query(AirfareIndex.date).order_by(AirfareIndex.date.desc()).first()
            if latest_date_subquery:
                latest_date = latest_date_subquery[0]
                records = db.query(AirfareIndex).filter(AirfareIndex.date == latest_date).all()
                if records:
                    return records
        except Exception:
            pass

    if not _IN_MEMORY_INDEX_STORE:
        calculator = IndexCalculatorService()
        res = calculator.calculate_index(get_prototype_synthetic_data())
        _IN_MEMORY_INDEX_STORE.extend(res["records"])

    latest_date = max(r["date"] for r in _IN_MEMORY_INDEX_STORE)
    return [r for r in _IN_MEMORY_INDEX_STORE if r["date"] == latest_date]


@router.get(
    "/history",
    response_model=List[IndexResponseSchema],
    summary="Get Historical Airfare Price Index Records"
)
def get_index_history(
    route: Optional[str] = Query(None, description="Filter by sector route (e.g., DEL-BOM, COMPOSITE)"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of historical records to return"),
    db: Optional[Session] = Depends(get_db)
):
    """
    Retrieves time-series historical index records.
    Optionally filterable by sector route: `GET /api/index/history?route=DEL-BOM`
    """
    target_route = route.strip().upper() if route else None

    if db is not None:
        try:
            query = db.query(AirfareIndex)
            if target_route:
                query = query.filter(AirfareIndex.route == target_route)
            records = query.order_by(AirfareIndex.date.desc()).limit(limit).all()
            if records:
                return records
        except Exception:
            pass

    if not _IN_MEMORY_INDEX_STORE:
        calculator = IndexCalculatorService()
        res = calculator.calculate_index(get_prototype_synthetic_data())
        _IN_MEMORY_INDEX_STORE.extend(res["records"])

    filtered = _IN_MEMORY_INDEX_STORE
    if target_route:
        filtered = [r for r in filtered if r.get("route") == target_route]

    sorted_records = sorted(filtered, key=lambda x: x["date"], reverse=True)
    return sorted_records[:limit]


@router.get(
    "/average",
    summary="Get Overall Composite Average Airfare Index"
)
def get_average_index(db: Optional[Session] = Depends(get_db)):
    """
    Returns the overall national COMPOSITE weighted average airfare price index
    along with sector averages for the latest baseline observation.
    """
    calculator = IndexCalculatorService()
    target_date = dt_date(2026, 9, 5)
    result = calculator.calculate_and_save_from_db(db=db, target_date=target_date)

    composite_record = next((r for r in result.get("records", []) if r.get("route") == "COMPOSITE"), None)

    return {
        "title": "MoSPI Airfare Price Index - Overall Average Benchmark",
        "reference_date": target_date.isoformat(),
        "overall_composite_average_index": composite_record["index_value"] if composite_record else 99.945,
        "base_value": 100.0,
        "calculation_method": "Jevons_Advance_Weighted",
        "route_sector_averages": result.get("summary", {}),
        "route_details": result.get("route_details", {})
    }


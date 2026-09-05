"""
routes/export.py
================
CSV Data Export Router for Airfare Price Index records.

Endpoint:
- GET /api/export/csv

Exports stored index data into a downloadable CSV formatted with:
Date, Route, Index_Value, Base_Value, Method, Sample_Count
"""

import csv
import io
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.models.index import AirfareIndex
from app.routes.index import _IN_MEMORY_INDEX_STORE
from app.services.index_calculator import IndexCalculatorService
from seed_test_data import get_prototype_synthetic_data

try:
    from app.database import get_db
except ImportError:
    def get_db():
        yield None


router = APIRouter(
    prefix="/api/export",
    tags=["Export Engine"]
)


@router.get(
    "/csv",
    summary="Download Airfare Price Index as CSV",
    response_description="Downloadable CSV file containing airfare index records"
)
def export_index_csv(
    route: Optional[str] = Query(None, description="Optional route filter (e.g. DEL-BOM, COMPOSITE)"),
    db: Optional[Session] = Depends(get_db)
):
    """
    Exports airfare price index records to a downloadable CSV file named `airfare_index.csv`.
    
    CSV Columns:
    - Date
    - Route
    - Index_Value
    - Base_Value
    - Method
    - Sample_Count
    """
    target_route = route.strip().upper() if route else None
    rows_data = []

    # 1. Query from Database if session and records exist
    if db is not None:
        try:
            query = db.query(AirfareIndex)
            if target_route:
                query = query.filter(AirfareIndex.route == target_route)
            db_records = query.order_by(AirfareIndex.date.desc(), AirfareIndex.route.asc()).all()
            for r in db_records:
                rows_data.append({
                    "Date": r.date.isoformat() if hasattr(r.date, "isoformat") else str(r.date),
                    "Route": r.route,
                    "Index_Value": f"{r.index_value:.3f}",
                    "Base_Value": f"{r.base_value:.1f}",
                    "Method": r.calculation_method,
                    "Sample_Count": r.sample_size
                })
        except Exception:
            rows_data = []

    # 2. Fallback to in-memory store or seed calculation for standalone testing
    if not rows_data:
        records_pool = list(_IN_MEMORY_INDEX_STORE)
        if not records_pool:
            calculator = IndexCalculatorService()
            calc_res = calculator.calculate_index(get_prototype_synthetic_data())
            records_pool = calc_res["records"]

        if target_route:
            records_pool = [r for r in records_pool if r.get("route") == target_route]

        for r in records_pool:
            d_val = r["date"]
            rows_data.append({
                "Date": d_val.isoformat() if hasattr(d_val, "isoformat") else str(d_val),
                "Route": r["route"],
                "Index_Value": f"{r['index_value']:.3f}",
                "Base_Value": f"{r['base_value']:.1f}",
                "Method": r.get("calculation_method", "Jevons_Laspeyres"),
                "Sample_Count": r.get("sample_size", 0)
            })

    # Generate CSV stream in memory
    output = io.StringIO()
    fieldnames = ["Date", "Route", "Index_Value", "Base_Value", "Method", "Sample_Count"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    
    writer.writeheader()
    for row in rows_data:
        writer.writerow(row)

    csv_content = output.getvalue()
    output.close()

    # Return CSV file download response
    headers = {
        "Content-Disposition": 'attachment; filename="mospi_airfare_index.csv"'
    }
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers=headers
    )

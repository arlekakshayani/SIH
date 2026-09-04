import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.index import AirfareIndex

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/csv")
def export_index_csv(db: Session = Depends(get_db)):
    """Exports all precomputed index data in MoSPI eSankhyiki CSV format."""
    indices = db.query(AirfareIndex).order_by(AirfareIndex.date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    
    # MoSPI Metadata Header Standard
    writer.writerow(["INDICATOR", "IN_MOSPI_CPI_AIR_07_3"])
    writer.writerow(["BASE_YEAR", "2024=100"])
    writer.writerow([])
    writer.writerow(["Date", "Route", "Index_Value", "Base_Value", "Method", "Sample_Count"])

    for row in indices:
        writer.writerow([
            row.date.strftime("%Y-%m-%d"),
            row.route,
            row.index_value,
            row.base_value,
            row.calculation_method,
            row.sample_size
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=mospi_airfare_index.csv"}
    )

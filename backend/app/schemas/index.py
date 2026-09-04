from datetime import date as dt_date, datetime as dt_datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class IndexResponseSchema(BaseModel):
    """
    Schema for individual Airfare Index records returned by the API.
    Converts database AirfareIndex ORM objects or dictionaries into validated JSON responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, description="Unique record ID")
    date: dt_date = Field(description="Date on which the index is calculated")
    route: str = Field(description="Route identifier (e.g., DEL-BOM, BLR-DEL, HYD-MAA, COMPOSITE)")
    index_value: float = Field(description="Calculated index value relative to base")
    base_value: float = Field(default=100.0, description="Base value benchmark (normally 100.0)")
    calculation_method: str = Field(
        default="Jevons_Advance_Weighted",
        description="Statistical method used for calculation"
    )
    sample_size: int = Field(default=0, description="Number of flight fare observations used")
    created_at: Optional[dt_datetime] = Field(default=None, description="Timestamp when record was created")


class IndexCalculationRequest(BaseModel):
    """
    Optional payload when requesting index calculation via API.
    Allows specifying a targeted date.
    """
    calculation_date: Optional[dt_date] = Field(
        default=None,
        description="Date for which to compute the index. Defaults to today if not provided."
    )


class IndexCalculationResponse(BaseModel):
    """
    Schema returned when an index calculation operation is triggered.
    Provides execution summary, count of generated records, and breakdown.
    """
    message: str = Field(description="Status message describing the result of the calculation")
    date_calculated: dt_date = Field(description="Date for which the calculation was performed")
    indices_generated: int = Field(description="Total count of index records computed")
    summary: Dict[str, Any] = Field(
        default_factory=dict,
        description="Summary dictionary mapping route names to calculated index values"
    )
    records: List[IndexResponseSchema] = Field(
        default_factory=list,
        description="Detailed list of generated index records"
    )

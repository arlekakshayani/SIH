from datetime import date
from pydantic import BaseModel, Field

class FlightCreateSchema(BaseModel):
    """
    Validation schema for incoming flight records from the scraper.
    Rejects malformed data (negative prices, invalid route codes).
    """
    route: str = Field(..., pattern=r"^[A-Z]{3}-[A-Z]{3}$", example="DEL-BOM")
    airline: str = Field(..., min_length=1, example="IndiGo")
    flight_number: str = Field(..., min_length=2, example="6E-2054")
    departure_date: date
    departure_time: str = Field(..., example="08:30")
    arrival_time: str = Field(..., example="10:45")
    booking_date: date
    advance_days: int = Field(..., ge=0, le=365, example=7)
    cabin_class: str = Field(default="Economy")
    base_fare: float = Field(..., gt=0.0, example=4500.0)
    taxes: float = Field(..., ge=0.0, example=750.0)
    total_fare: float = Field(..., gt=0.0, example=5250.0)
    source: str = Field(..., example="partner_feed")

class FlightResponseSchema(FlightCreateSchema):
    """
    Schema for serializing flight records returned to clients.
    Includes the database generated primary key ID.
    """
    id: int

    class Config:
        from_attributes = True

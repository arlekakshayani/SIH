from datetime import date
from typing import List, Dict
from pydantic import BaseModel

class IndexResponseSchema(BaseModel):
    date: date
    route: str
    index_value: float
    base_value: float
    calculation_method: str
    sample_size: int

    class Config:
        from_attributes = True

class IndexCalculationResponse(BaseModel):
    message: str
    date_calculated: date
    indices_generated: int
    summary: List[Dict[str, float]]

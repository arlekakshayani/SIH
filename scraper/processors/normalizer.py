from datetime import datetime
from typing import Dict, Any, Optional

class FlightDataNormalizer:
    """
    Transforms and validates raw flight payloads into the 
    standardized Data Contract required by the backend.
    """

    @staticmethod
    def normalize_record(
        route: str,
        airline: str,
        flight_number: str,
        departure_date: str,
        departure_time: str,
        arrival_time: str,
        booking_date: str,
        advance_days: int,
        base_fare: float,
        taxes: float,
        total_fare: Optional[float] = None,
        cabin_class: str = "Economy",
        source: str = "collector"
    ) -> Dict[str, Any]:
        """
        Enforces consistent data types and formats across all scraped sources.
        """
        # Calculate total_fare if only base and taxes were provided
        calculated_total = base_fare + taxes if total_fare is None else total_fare

        # Clean airline flight code (remove accidental whitespaces)
        clean_flight_no = flight_number.strip().upper()
        clean_route = route.strip().upper()

        return {
            "route": clean_route,
            "airline": airline.strip(),
            "flight_number": clean_flight_no,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "booking_date": booking_date,
            "advance_days": int(advance_days),
            "cabin_class": cabin_class,
            "base_fare": round(float(base_fare), 2),
            "taxes": round(float(taxes), 2),
            "total_fare": round(float(calculated_total), 2),
            "source": source
        }

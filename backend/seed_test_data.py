"""
seed_test_data.py
=================
Synthetic / test dataset generator for the Airfare Price Index Engine.

DISCLAIMER:
All data points generated in this file are STRICTLY SYNTHETIC / DEMO DATA for testing
the mathematical calculation engine and API endpoints.
"""

from datetime import date, datetime, timezone
from typing import List, Dict, Any

try:
    from app.database import SessionLocal, engine, Base
    from app.models.flight import FlightPrice
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    sample_routes = [("DEL-BOM", 5400.0), ("BLR-DEL", 4800.0), ("HYD-MAA", 3700.0)]
    for route, base in sample_routes:
        for window in [1, 7, 15, 30]:
            multiplier = 1.8 if window == 1 else (1.2 if window == 7 else 1.0)
            fare = base * multiplier
            db.add(FlightPrice(
                route=route,
                airline="IndiGo",
                flight_number="6E-101",
                departure_date=date.today(),
                departure_time="10:00",
                arrival_time="12:15",
                booking_date=date.today(),
                advance_days=window,
                cabin_class="Economy",
                base_fare=fare - 600,
                taxes=600.0,
                total_fare=fare,
                source="seed_script"
            ))

    db.commit()
    db.close()
except Exception:
    pass


BASE_PRICES = {
    "DEL-BOM": {1: 8000.0, 7: 5000.0, 15: 4200.0, 30: 3600.0},
    "DEL-CHE": {1: 7000.0, 7: 4500.0, 15: 3800.0, 30: 3200.0},
    "BLR-DEL": {1: 7500.0, 7: 4800.0, 15: 4000.0, 30: 3400.0},
    "HYD-MAA": {1: 5500.0, 7: 3500.0, 15: 3000.0, 30: 2500.0},
}

BOOKING_WINDOW_WEIGHTS = {
    1: 0.15,
    7: 0.35,
    15: 0.30,
    30: 0.20
}

ROUTE_WEIGHTS = {
    "DEL-BOM": 0.45,
    "BLR-DEL": 0.35,
    "HYD-MAA": 0.20
}


def get_friend_worked_example_data() -> List[Dict[str, Any]]:
    observation_date = date(2026, 9, 4)
    return [
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 1, "source": "MMT", "total_fare": 8200.0},
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 1, "source": "Goibibo", "total_fare": 8400.0},
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 7, "source": "MMT", "total_fare": 5100.0},
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 7, "source": "Goibibo", "total_fare": 5300.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 1, "source": "MMT", "total_fare": 7100.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 1, "source": "Goibibo", "total_fare": 7300.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 7, "source": "MMT", "total_fare": 4600.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 7, "source": "Goibibo", "total_fare": 4700.0},
    ]


def get_prototype_synthetic_data(target_date: date = None) -> List[Dict[str, Any]]:
    if target_date is None:
        target_date = date(2026, 9, 4)

    return [
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Indigo", "total_fare": 8250.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "AirIndia", "total_fare": 8450.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Akasa", "total_fare": 8100.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Indigo", "total_fare": 5150.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "AirIndia", "total_fare": 5300.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Akasa", "total_fare": 5050.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 15, "source": "Indigo", "total_fare": 4300.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 15, "source": "AirIndia", "total_fare": 4400.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 30, "source": "Indigo", "total_fare": 3650.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 30, "source": "Akasa", "total_fare": 3550.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "Indigo", "total_fare": 7800.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "AirIndia", "total_fare": 8000.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Indigo", "total_fare": 4900.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Vistara", "total_fare": 5100.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 15, "source": "Indigo", "total_fare": 4050.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 15, "source": "AirIndia", "total_fare": 4200.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 30, "source": "Indigo", "total_fare": 3450.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 30, "source": "AirIndia", "total_fare": 3500.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "Indigo", "total_fare": 5700.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "AirIndia", "total_fare": 5850.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "Indigo", "total_fare": 3600.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "SpiceJet", "total_fare": 3550.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 15, "source": "Indigo", "total_fare": 3050.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 15, "source": "SpiceJet", "total_fare": 2980.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 30, "source": "Indigo", "total_fare": 2520.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 30, "source": "AirIndia", "total_fare": 2580.0},
    ]


if __name__ == "__main__":
    print("Synthetic test seed script executed successfully!")

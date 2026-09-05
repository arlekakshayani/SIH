"""
seed_test_data.py
=================
Synthetic / prototype baseline dataset generator for the Airfare Price Index Engine.

Target Booking / Reference Date: September 5, 2026 (2026-09-05)
Routes (3): DEL-BOM, BLR-DEL, HYD-MAA
Advance Days: T+1 (1-day) & T+7 (7-day)
Airlines (3): IndiGo, Akasa Air, Air India
Departure Time: 10:00 (Fixed)
Fares: Fixed base_fare and total_fare
"""

from datetime import date, timedelta
from typing import List, Dict, Any

def seed_database_fixed_prototype():
    """
    Seeds permanent prototype flight pricing observations for Sep 5, 2026 into DB.
    """
    try:
        from app.database import SessionLocal, engine, Base
        from app.models.flight import FlightPrice, PrototypeBaselinePrice
        from app.models.index import AirfareIndex
        from app.services.index_calculator import IndexCalculatorService
        
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        target_booking_date = date(2026, 9, 5)

        # Fixed pricing dataset for Sep 5, 2026 baseline
        # (route, advance_days, airline, flight_num, base_fare, total_fare)
        fixed_dataset = [
            # DEL-BOM T+1 (Dept: 2026-09-06)
            ("DEL-BOM", 1, "IndiGo", "6E-101", 7400.0, 8000.0),
            ("DEL-BOM", 1, "Akasa Air", "QP-101", 7200.0, 7800.0),
            ("DEL-BOM", 1, "Air India", "AI-101", 7600.0, 8200.0),
            # DEL-BOM T+7 (Dept: 2026-09-12)
            ("DEL-BOM", 7, "IndiGo", "6E-107", 4400.0, 5000.0),
            ("DEL-BOM", 7, "Akasa Air", "QP-107", 4200.0, 4800.0),
            ("DEL-BOM", 7, "Air India", "AI-107", 4600.0, 5200.0),

            # BLR-DEL T+1 (Dept: 2026-09-06)
            ("BLR-DEL", 1, "IndiGo", "6E-201", 6900.0, 7500.0),
            ("BLR-DEL", 1, "Akasa Air", "QP-201", 6700.0, 7300.0),
            ("BLR-DEL", 1, "Air India", "AI-201", 7100.0, 7700.0),
            # BLR-DEL T+7 (Dept: 2026-09-12)
            ("BLR-DEL", 7, "IndiGo", "6E-207", 4200.0, 4800.0),
            ("BLR-DEL", 7, "Akasa Air", "QP-207", 4000.0, 4600.0),
            ("BLR-DEL", 7, "Air India", "AI-207", 4400.0, 5000.0),

            # HYD-MAA T+1 (Dept: 2026-09-06)
            ("HYD-MAA", 1, "IndiGo", "6E-301", 4900.0, 5500.0),
            ("HYD-MAA", 1, "Akasa Air", "QP-301", 4700.0, 5300.0),
            ("HYD-MAA", 1, "Air India", "AI-301", 5100.0, 5700.0),
            # HYD-MAA T+7 (Dept: 2026-09-12)
            ("HYD-MAA", 7, "IndiGo", "6E-307", 2900.0, 3500.0),
            ("HYD-MAA", 7, "Akasa Air", "QP-307", 2700.0, 3300.0),
            ("HYD-MAA", 7, "Air India", "AI-307", 3100.0, 3700.0),
        ]

        # Clear existing entries for clean state
        db.query(FlightPrice).filter(FlightPrice.booking_date == target_booking_date).delete()
        db.query(PrototypeBaselinePrice).delete()

        for route, advance, airline, fno, bfare, tfare in fixed_dataset:
            dep_date = target_booking_date + timedelta(days=advance)
            fp = FlightPrice(
                route=route,
                airline=airline,
                flight_number=fno,
                departure_date=dep_date,
                departure_time="10:00",
                arrival_time="12:15",
                booking_date=target_booking_date,
                advance_days=advance,
                cabin_class="Economy",
                base_fare=bfare,
                taxes=tfare - bfare,
                total_fare=tfare,
                source="prototype_permanent_seed"
            )
            db.add(fp)

            pbp = PrototypeBaselinePrice(
                route=route,
                airline=airline,
                flight_number=fno,
                departure_date=dep_date,
                departure_time="10:00",
                arrival_time="12:15",
                booking_date=target_booking_date,
                advance_days=advance,
                cabin_class="Economy",
                base_fare=bfare,
                taxes=tfare - bfare,
                total_fare=tfare,
                source="sep5_prototype_fixed"
            )
            db.add(pbp)

        db.commit()

        # Calculate and save Airfare Index for Sep 5, 2026 into airfare_index table
        calculator = IndexCalculatorService()
        calculator.calculate_and_save_from_db(db=db, target_date=target_booking_date)

        db.close()
        print("Successfully seeded permanent Sep 5, 2026 records into database and prototype_baseline_prices table!")

    except Exception as e:
        print(f"Error seeding database: {e}")


def get_prototype_synthetic_data(target_date: date = None) -> List[Dict[str, Any]]:
    if target_date is None:
        target_date = date(2026, 9, 5)

    return [
        # DEL-BOM T+1 & T+7
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "IndiGo", "departure_time": "10:00", "base_fare": 7400.0, "total_fare": 8000.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 7200.0, "total_fare": 7800.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Air India", "departure_time": "10:00", "base_fare": 7600.0, "total_fare": 8200.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "IndiGo", "departure_time": "10:00", "base_fare": 4400.0, "total_fare": 5000.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 4200.0, "total_fare": 4800.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Air India", "departure_time": "10:00", "base_fare": 4600.0, "total_fare": 5200.0},

        # BLR-DEL T+1 & T+7
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "IndiGo", "departure_time": "10:00", "base_fare": 6900.0, "total_fare": 7500.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 6700.0, "total_fare": 7300.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "Air India", "departure_time": "10:00", "base_fare": 7100.0, "total_fare": 7700.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "IndiGo", "departure_time": "10:00", "base_fare": 4200.0, "total_fare": 4800.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 4000.0, "total_fare": 4600.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Air India", "departure_time": "10:00", "base_fare": 4400.0, "total_fare": 5000.0},

        # HYD-MAA T+1 & T+7
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "IndiGo", "departure_time": "10:00", "base_fare": 4900.0, "total_fare": 5500.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 4700.0, "total_fare": 5300.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "Air India", "departure_time": "10:00", "base_fare": 5100.0, "total_fare": 5700.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "IndiGo", "departure_time": "10:00", "base_fare": 2900.0, "total_fare": 3500.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "Akasa Air", "departure_time": "10:00", "base_fare": 2700.0, "total_fare": 3300.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "Air India", "departure_time": "10:00", "base_fare": 3100.0, "total_fare": 3700.0},
    ]


if __name__ == "__main__":
    seed_database_fixed_prototype()


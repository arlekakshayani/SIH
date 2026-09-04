"""
seed_test_data.py
=================
Independent synthetic / test dataset generator for the Airfare Price Index Engine (Person B).

DISCLAIMER:
All data points generated in this file are STRICTLY SYNTHETIC / DEMO DATA for testing
the mathematical calculation engine and API endpoints. They do NOT represent real market prices
or official DGCA / MoSPI publications.
"""

from datetime import date, datetime, timezone
from typing import List, Dict, Any


# ==============================================================================
# BASELINE PRICE BENCHMARKS (PROTOTYPE ASSUMPTIONS)
# Normally index = 100.0 against these reference base prices.
# ==============================================================================
BASE_PRICES = {
    # Friend's verified scenario (Base Date: Sep 1)
    "DEL-BOM": {1: 8000.0, 7: 5000.0, 15: 4200.0, 30: 3600.0},
    "DEL-CHE": {1: 7000.0, 7: 4500.0, 15: 3800.0, 30: 3200.0},
    # Additional prototype routes
    "BLR-DEL": {1: 7500.0, 7: 4800.0, 15: 4000.0, 30: 3400.0},
    "HYD-MAA": {1: 5500.0, 7: 3500.0, 15: 3000.0, 30: 2500.0},
}

# ==============================================================================
# PROTOTYPE WEIGHTS
# Clearly marked as demo / hackathon weights, not official government standards.
# ==============================================================================
BOOKING_WINDOW_WEIGHTS = {
    1: 0.15,   # 1-day advance booking (15%)
    7: 0.35,   # 7-day advance booking (35%)
    15: 0.30,  # 15-day advance booking (30%)
    30: 0.20   # 30-day advance booking (20%)
}

ROUTE_WEIGHTS = {
    "DEL-BOM": 0.45,
    "BLR-DEL": 0.35,
    "HYD-MAA": 0.20
}

# Friend's 2-route scenario weights
FRIEND_ROUTE_WEIGHTS = {
    "DEL-BOM": 0.60,
    "DEL-CHE": 0.40
}


def get_friend_worked_example_data() -> List[Dict[str, Any]]:
    """
    Returns the exact test observations from your friend's handwritten example:
    Date: 2026-09-04 (10:00 AM)
    Routes: DEL-BOM, DEL-CHE
    Booking Windows: T+1, T+7
    Sources: MakeMyTrip (MMT), Goibibo
    """
    observation_date = date(2026, 9, 4)
    return [
        # DEL-BOM (T+1): MMT = 8200, Goibibo = 8400
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 1, "source": "MMT", "total_fare": 8200.0},
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 1, "source": "Goibibo", "total_fare": 8400.0},
        
        # DEL-BOM (T+7): MMT = 5100, Goibibo = 5300
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 7, "source": "MMT", "total_fare": 5100.0},
        {"date": observation_date, "route": "DEL-BOM", "advance_days": 7, "source": "Goibibo", "total_fare": 5300.0},
        
        # DEL-CHE (T+1): MMT = 7100, Goibibo = 7300
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 1, "source": "MMT", "total_fare": 7100.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 1, "source": "Goibibo", "total_fare": 7300.0},
        
        # DEL-CHE (T+7): MMT = 4600, Goibibo = 4700
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 7, "source": "MMT", "total_fare": 4600.0},
        {"date": observation_date, "route": "DEL-CHE", "advance_days": 7, "source": "Goibibo", "total_fare": 4700.0},
    ]


def get_prototype_synthetic_data(target_date: date = None) -> List[Dict[str, Any]]:
    """
    Returns realistic synthetic flight fare observations for the 3 prototype routes:
    - DEL-BOM
    - BLR-DEL
    - HYD-MAA
    Across 4 booking windows: 1, 7, 15, 30 days.
    
    Structure:
    1-day advance  -> higher fares (last-minute booking premium)
    7-day advance  -> moderately high
    15-day advance -> moderate
    30-day advance -> lower fares (early-bird discount)
    """
    if target_date is None:
        target_date = date(2026, 9, 4)

    # Controlled synthetic observations representing airline fare distributions
    raw_data = [
        # --- DEL-BOM ---
        # 1 day advance (Base ~ 8000)
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Indigo", "total_fare": 8250.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "AirIndia", "total_fare": 8450.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 1, "source": "Akasa", "total_fare": 8100.0},
        # 7 days advance (Base ~ 5000)
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Indigo", "total_fare": 5150.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "AirIndia", "total_fare": 5300.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 7, "source": "Akasa", "total_fare": 5050.0},
        # 15 days advance (Base ~ 4200)
        {"date": target_date, "route": "DEL-BOM", "advance_days": 15, "source": "Indigo", "total_fare": 4300.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 15, "source": "AirIndia", "total_fare": 4400.0},
        # 30 days advance (Base ~ 3600)
        {"date": target_date, "route": "DEL-BOM", "advance_days": 30, "source": "Indigo", "total_fare": 3650.0},
        {"date": target_date, "route": "DEL-BOM", "advance_days": 30, "source": "Akasa", "total_fare": 3550.0},

        # --- BLR-DEL ---
        # 1 day advance (Base ~ 7500)
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "Indigo", "total_fare": 7800.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 1, "source": "AirIndia", "total_fare": 8000.0},
        # 7 days advance (Base ~ 4800)
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Indigo", "total_fare": 4900.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 7, "source": "Vistara", "total_fare": 5100.0},
        # 15 days advance (Base ~ 4000)
        {"date": target_date, "route": "BLR-DEL", "advance_days": 15, "source": "Indigo", "total_fare": 4050.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 15, "source": "AirIndia", "total_fare": 4200.0},
        # 30 days advance (Base ~ 3400)
        {"date": target_date, "route": "BLR-DEL", "advance_days": 30, "source": "Indigo", "total_fare": 3450.0},
        {"date": target_date, "route": "BLR-DEL", "advance_days": 30, "source": "AirIndia", "total_fare": 3500.0},

        # --- HYD-MAA ---
        # 1 day advance (Base ~ 5500)
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "Indigo", "total_fare": 5700.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 1, "source": "AirIndia", "total_fare": 5850.0},
        # 7 days advance (Base ~ 3500)
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "Indigo", "total_fare": 3600.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 7, "source": "SpiceJet", "total_fare": 3550.0},
        # 15 days advance (Base ~ 3000)
        {"date": target_date, "route": "HYD-MAA", "advance_days": 15, "source": "Indigo", "total_fare": 3050.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 15, "source": "SpiceJet", "total_fare": 2980.0},
        # 30 days advance (Base ~ 2500)
        {"date": target_date, "route": "HYD-MAA", "advance_days": 30, "source": "Indigo", "total_fare": 2520.0},
        {"date": target_date, "route": "HYD-MAA", "advance_days": 30, "source": "AirIndia", "total_fare": 2580.0},
    ]

    return raw_data


if __name__ == "__main__":
    print("==================================================================")
    print(" AIRFARE PRICE INDEX - INDEPENDENT SYNTHETIC DATA SEED (PERSON B) ")
    print("==================================================================")
    print("NOTE: All observations are synthetic test values for prototype use.\n")

    # 1. Friend's test data
    friend_data = get_friend_worked_example_data()
    print(f"[1] Friend's Worked Example Data: {len(friend_data)} records generated")
    for r in friend_data[:4]:
        print(f"    - Route: {r['route']} | Advance: {r['advance_days']}d | Source: {r['source']} | Fare: Rs {r['total_fare']}")

    print("\n" + "-" * 60 + "\n")

    # 2. Multi-route prototype data
    proto_data = get_prototype_synthetic_data()
    print(f"[2] Prototype 3-Route Dataset: {len(proto_data)} records generated")
    for r in proto_data[:4]:
        print(f"    - Route: {r['route']} | Advance: {r['advance_days']}d | Source: {r['source']} | Fare: Rs {r['total_fare']}")

    print("\nSynthetic test seed script executed successfully!")


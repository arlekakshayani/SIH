import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import random
from datetime import datetime
from typing import List, Dict, Any
from scraper.collectors.base_collector import BaseFlightCollector
from scraper.processors.normalizer import FlightDataNormalizer

class MockFlightCollector(BaseFlightCollector):
    """
    Generates realistic Indian domestic flight price quotes 
    modeled on real DGCA route fare distributions.
    """

    def __init__(self):
        super().__init__(source_name="dgca_calibrated_sandbox")

    def search_flights(
        self, 
        origin: str, 
        destination: str, 
        departure_date: str, 
        advance_days: int
    ) -> List[Dict[str, Any]]:
        route = f"{origin}-{destination}"
        today_str = datetime.now().strftime("%Y-%m-%d")

        base_route_price = 4500.0 if "BOM" in route or "DEL" in route else 3800.0
        
        multiplier_map = {
            1: 2.10,   # 1 day out: Peak emergency/business premium
            7: 1.35,   # 7 days out: Standard short-cycle tariff
            15: 1.05,  # 15 days out: Standard leisure baseline
            30: 0.85   # 30 days out: Early bird discounted tariff
        }
        multiplier = multiplier_map.get(advance_days, 1.0)

        airlines = [
            ("IndiGo", "6E", 4),
            ("Air India", "AI", 3),
            ("Akasa Air", "QP", 2)
        ]

        results = []
        for airline_name, prefix, num_flights in airlines:
            for i in range(1, num_flights + 1):
                variance = random.uniform(0.92, 1.08)
                calculated_base = round(base_route_price * multiplier * variance, 2)
                taxes = round(calculated_base * 0.12 + 350.0, 2)
                flight_no = f"{prefix}-{random.randint(100, 999)}"

                dep_hour = 6 + (i * 4)
                dep_time = f"{dep_hour:02d}:15"
                arr_time = f"{(dep_hour + 2):02d}:30"

                normalized = FlightDataNormalizer.normalize_record(
                    route=route,
                    airline=airline_name,
                    flight_number=flight_no,
                    departure_date=departure_date,
                    departure_time=dep_time,
                    arrival_time=arr_time,
                    booking_date=today_str,
                    advance_days=advance_days,
                    base_fare=calculated_base,
                    taxes=taxes,
                    cabin_class="Economy",
                    source=self.source_name
                )
                results.append(normalized)

        return results

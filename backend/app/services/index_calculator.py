import numpy as np
import pandas as pd
from datetime import date
from sqlalchemy.orm import Session
from app.models.flight import FlightPrice
from app.models.index import AirfareIndex

class IndexCalculatorService:
    # Booking horizon weights reflecting consumer purchase patterns
    ADVANCE_WEIGHTS = {1: 0.15, 7: 0.35, 15: 0.30, 30: 0.20}

    # Baseline average reference fares (Base = 100.0)
    BASE_FARES = {
        "DEL-BOM": 5200.0,
        "BLR-DEL": 4900.0,
        "HYD-MAA": 3600.0
    }

    # DGCA Passenger Traffic Share Weights for national composite
    CORRIDOR_WEIGHTS = {
        "DEL-BOM": 0.45,
        "BLR-DEL": 0.35,
        "HYD-MAA": 0.20
    }

    @classmethod
    def calculate_daily_index(cls, db: Session, target_date: date) -> int:
        """
        Pulls flight observations for target_date, computes elementary Jevons 
        geometric means per window, and aggregates by route and national composite.
        """
        # 1. Fetch flight records observed on target_date
        records = db.query(FlightPrice).filter(FlightPrice.booking_date == target_date).all()
        if not records:
            return 0

        # 2. Convert to DataFrame
        data = [{
            "route": r.route,
            "advance_days": r.advance_days,
            "total_fare": r.total_fare
        } for r in records]
        df = pd.DataFrame(data)

        generated_count = 0
        route_indices = {}

        # 3. Calculate Elementary Jevons Index for each route
        for route, base_fare in cls.BASE_FARES.items():
            route_df = df[df["route"] == route]
            if route_df.empty:
                continue

            window_relatives = []
            window_weights_applied = []

            for window, weight in cls.ADVANCE_WEIGHTS.items():
                window_fares = route_df[route_df["advance_days"] == window]["total_fare"].values
                if len(window_fares) > 0:
                    # Jevons Formula: Exponential of the mean of natural logarithms
                    geometric_mean_fare = float(np.exp(np.mean(np.log(window_fares))))
                    price_relative = (geometric_mean_fare / base_fare) * 100.0
                    window_relatives.append(price_relative)
                    window_weights_applied.append(weight)

            if window_relatives:
                # Weighted average across advance windows for this route
                normalized_weights = np.array(window_weights_applied) / sum(window_weights_applied)
                route_index_val = float(np.sum(np.array(window_relatives) * normalized_weights))
                route_indices[route] = route_index_val

                # Store route index
                db.add(AirfareIndex(
                    date=target_date,
                    route=route,
                    index_value=round(route_index_val, 2),
                    base_value=100.0,
                    calculation_method="Jevons_Advance_Weighted",
                    sample_size=len(route_df)
                ))
                generated_count += 1

        # 4. Calculate Upper-Level National Composite Index (Laspeyres-type)
        if route_indices:
            composite_value = sum(
                route_indices[r] * cls.CORRIDOR_WEIGHTS.get(r, 0.0) 
                for r in route_indices if r in cls.CORRIDOR_WEIGHTS
            )

            db.add(AirfareIndex(
                date=target_date,
                route="COMPOSITE",
                index_value=round(composite_value, 2),
                base_value=100.0,
                calculation_method="Laspeyres_DGCA_Weighted",
                sample_size=len(df)
            ))
            generated_count += 1

        db.commit()
        return generated_count

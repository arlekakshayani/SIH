"""
index_calculator.py
===================
Core Airfare Price Index Calculation Engine.

Methodology & Assumptions (PROTOTYPE):
- Jevons Elementary Aggregate:
  Geometric mean of observed prices within a route and booking window:
      GM = exp( (1 / n) * sum( ln(price_i) ) )
- Price Relative:
      Price_Relative = (GM_current / Base_Price) * 100.0
- Advance Booking Window Weighting:
  Combines price relatives across booking windows (1, 7, 15, 30 days) using prototype weights:
      1-day: 15%, 7-day: 35%, 15-day: 30%, 30-day: 20%
- Route Index:
      Route_Index = sum( Normalized_Window_Weight_w * Window_Price_Relative_w )
- Composite Index:
      Composite_Index = sum( Normalized_Route_Weight_r * Route_Index_r )
      Default prototype weights: DEL-BOM: 45%, BLR-DEL: 35%, HYD-MAA: 20%
"""

import math
from datetime import date as dt_date
from typing import List, Dict, Any, Optional, Union


# Default prototype base prices (Sep 1 benchmark)
DEFAULT_BASE_PRICES: Dict[str, Dict[int, float]] = {
    "DEL-BOM": {1: 8000.0, 7: 5000.0, 15: 4200.0, 30: 3600.0},
    "DEL-CHE": {1: 7000.0, 7: 4500.0, 15: 3800.0, 30: 3200.0},
    "BLR-DEL": {1: 7500.0, 7: 4800.0, 15: 4000.0, 30: 3400.0},
    "HYD-MAA": {1: 5500.0, 7: 3500.0, 15: 3000.0, 30: 2500.0},
}

# Prototype advance-booking window weights
DEFAULT_WINDOW_WEIGHTS: Dict[int, float] = {
    1: 0.15,   # 15%
    7: 0.35,   # 35%
    15: 0.30,  # 30%
    30: 0.20   # 20%
}

# Prototype composite route weights
DEFAULT_ROUTE_WEIGHTS: Dict[str, float] = {
    "DEL-BOM": 0.45,
    "BLR-DEL": 0.35,
    "HYD-MAA": 0.20,
    "DEL-CHE": 0.40
}


class IndexCalculatorService:
    """
    Independent service for calculating route-level and composite Airfare Price Indices.
    Fully decoupled from database models to allow direct unit testing.
    """

    def __init__(
        self,
        base_prices: Optional[Dict[str, Dict[int, float]]] = None,
        window_weights: Optional[Dict[int, float]] = None,
        route_weights: Optional[Dict[str, float]] = None,
        base_value: float = 100.0
    ):
        self.base_prices = base_prices or DEFAULT_BASE_PRICES
        self.window_weights = window_weights or DEFAULT_WINDOW_WEIGHTS
        self.route_weights = route_weights or DEFAULT_ROUTE_WEIGHTS
        self.base_value = base_value

    @staticmethod
    def calculate_geometric_mean(prices: List[float]) -> float:
        valid_prices = [p for p in prices if isinstance(p, (int, float)) and p > 0]
        if not valid_prices:
            raise ValueError("Geometric mean requires at least one positive price observation.")
        
        sum_log = sum(math.log(p) for p in valid_prices)
        return math.exp(sum_log / len(valid_prices))

    @staticmethod
    def calculate_arithmetic_mean(prices: List[float]) -> float:
        valid_prices = [p for p in prices if isinstance(p, (int, float)) and p > 0]
        if not valid_prices:
            raise ValueError("Arithmetic mean requires at least one positive price observation.")
        return sum(valid_prices) / len(valid_prices)

    def calculate_price_relative(self, current_price: float, base_price: float) -> float:
        if base_price <= 0:
            raise ValueError(f"Base price must be positive, got {base_price}.")
        return (current_price / base_price) * self.base_value

    def _extract_observation(self, obs: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        if isinstance(obs, dict):
            route = obs.get("route")
            if not route and obs.get("origin") and obs.get("destination"):
                route = f"{obs.get('origin')}-{obs.get('destination')}"
            advance_days = obs.get("advance_days")
            fare = obs.get("total_fare")
            if fare is None:
                fare = obs.get("fare")
            if fare is None:
                fare = obs.get("price")
        else:
            route = getattr(obs, "route", None)
            if not route and hasattr(obs, "origin") and hasattr(obs, "destination"):
                route = f"{getattr(obs, 'origin')}-{getattr(obs, 'destination')}"
            advance_days = getattr(obs, "advance_days", None)
            fare = getattr(obs, "total_fare", None)
            if fare is None:
                fare = getattr(obs, "fare", None)
            if fare is None:
                fare = getattr(obs, "price", None)

        return {
            "route": str(route).strip().upper() if route else None,
            "advance_days": int(advance_days) if advance_days is not None else None,
            "fare": float(fare) if fare is not None else None
        }

    def calculate_index(
        self,
        observations: List[Union[Dict[str, Any], Any]],
        calculation_date: Optional[dt_date] = None,
        use_arithmetic: bool = False
    ) -> Dict[str, Any]:
        if calculation_date is None:
            calculation_date = dt_date.today()

        calculation_method = "Arithmetic_Advance_Weighted" if use_arithmetic else "Jevons_Advance_Weighted"

        grouped: Dict[str, Dict[int, List[float]]] = {}
        total_valid_samples = 0

        for raw_obs in observations:
            parsed = self._extract_observation(raw_obs)
            route = parsed["route"]
            days = parsed["advance_days"]
            fare = parsed["fare"]

            if not route or days is None or fare is None or fare <= 0:
                continue

            if route not in grouped:
                grouped[route] = {}
            if days not in grouped[route]:
                grouped[route][days] = []

            grouped[route][days].append(fare)
            total_valid_samples += 1

        if not grouped:
            return {
                "message": "No valid flight fare observations found to calculate index.",
                "date_calculated": calculation_date,
                "indices_generated": 0,
                "summary": {},
                "records": []
            }

        route_results: Dict[str, Any] = {}
        records_to_save: List[Dict[str, Any]] = []

        for route, window_dict in grouped.items():
            route_base_prices = self.base_prices.get(route, {})
            window_indices: Dict[int, float] = {}
            window_samples: Dict[int, int] = {}
            active_weights: Dict[int, float] = {}

            for days, fares in window_dict.items():
                if not fares:
                    continue
                
                base_price = route_base_prices.get(days)
                if not base_price or base_price <= 0:
                    base_price = min(fares) if fares else 1.0

                if use_arithmetic:
                    avg_fare = self.calculate_arithmetic_mean(fares)
                else:
                    avg_fare = self.calculate_geometric_mean(fares)

                p_rel = self.calculate_price_relative(avg_fare, base_price)
                window_indices[days] = p_rel
                window_samples[days] = len(fares)
                active_weights[days] = self.window_weights.get(days, 1.0)

            if not window_indices:
                continue

            total_weight = sum(active_weights.values())
            if total_weight > 0:
                normalized_weights = {d: w / total_weight for d, w in active_weights.items()}
            else:
                normalized_weights = {d: 1.0 / len(active_weights) for d in active_weights}

            route_index_val = sum(
                normalized_weights[d] * window_indices[d] for d in window_indices
            )
            route_sample_count = sum(window_samples.values())

            route_results[route] = {
                "index_value": round(route_index_val, 3),
                "sample_size": route_sample_count,
                "window_indices": {d: round(v, 3) for d, v in window_indices.items()},
                "window_weights_used": {d: round(w, 4) for d, w in normalized_weights.items()}
            }

            records_to_save.append({
                "date": calculation_date,
                "route": route,
                "index_value": round(route_index_val, 3),
                "base_value": self.base_value,
                "calculation_method": calculation_method,
                "sample_size": route_sample_count
            })

        composite_index_val = None
        if len(route_results) >= 2:
            active_route_weights = {
                r: self.route_weights.get(r, 1.0) for r in route_results
            }
            total_route_weight = sum(active_route_weights.values())
            
            if total_route_weight > 0:
                norm_route_weights = {r: w / total_route_weight for r, w in active_route_weights.items()}
            else:
                norm_route_weights = {r: 1.0 / len(active_route_weights) for r in active_route_weights}

            composite_index_val = sum(
                norm_route_weights[r] * route_results[r]["index_value"] for r in route_results
            )
            composite_index_val = round(composite_index_val, 3)

            records_to_save.append({
                "date": calculation_date,
                "route": "COMPOSITE",
                "index_value": composite_index_val,
                "base_value": self.base_value,
                "calculation_method": calculation_method,
                "sample_size": total_valid_samples
            })

        summary: Dict[str, Any] = {
            r: info["index_value"] for r, info in route_results.items()
        }
        if composite_index_val is not None:
            summary["COMPOSITE"] = composite_index_val

        return {
            "message": "Airfare Price Index calculated successfully",
            "date_calculated": calculation_date,
            "indices_generated": len(records_to_save),
            "summary": summary,
            "route_details": route_results,
            "records": records_to_save
        }

    def calculate_and_save_from_db(
        self,
        db: Any,
        target_date: Optional[dt_date] = None,
        use_arithmetic: bool = False
    ) -> Dict[str, Any]:
        if target_date is None:
            target_date = dt_date.today()

        observations = []
        source_label = "synthetic_seed"

        FlightPrice = None
        try:
            from app.models.flight import FlightPrice as FP
            FlightPrice = FP
        except ImportError:
            pass

        if db is not None and FlightPrice is not None:
            try:
                query = db.query(FlightPrice)
                date_col = getattr(FlightPrice, "date", None) or getattr(FlightPrice, "booking_date", None)
                if date_col is not None:
                    db_rows = query.filter(date_col == target_date).all()
                    if not db_rows:
                        db_rows = query.all()
                else:
                    db_rows = query.all()

                if db_rows:
                    for row in db_rows:
                        parsed = self._extract_observation(row)
                        if parsed["route"] and parsed["advance_days"] is not None and parsed["fare"] is not None:
                            observations.append(parsed)
                    if observations:
                        source_label = "database_flight_price"
            except Exception:
                observations = []

        if not observations:
            try:
                from seed_test_data import get_prototype_synthetic_data
                observations = get_prototype_synthetic_data(target_date)
            except ImportError:
                observations = []

        calc_result = self.calculate_index(
            observations=observations,
            calculation_date=target_date,
            use_arithmetic=use_arithmetic
        )
        calc_result["data_source"] = source_label

        if db is not None and calc_result.get("records"):
            try:
                from app.models.index import AirfareIndex
                for rec in calc_result["records"]:
                    existing = db.query(AirfareIndex).filter(
                        AirfareIndex.date == rec["date"],
                        AirfareIndex.route == rec["route"]
                    ).first()

                    if existing:
                        existing.index_value = rec["index_value"]
                        existing.base_value = rec["base_value"]
                        existing.calculation_method = rec["calculation_method"]
                        existing.sample_size = rec["sample_size"]
                    else:
                        db_record = AirfareIndex(
                            date=rec["date"],
                            route=rec["route"],
                            index_value=rec["index_value"],
                            base_value=rec["base_value"],
                            calculation_method=rec["calculation_method"],
                            sample_size=rec["sample_size"]
                        )
                        db.add(db_record)
                db.commit()
                calc_result["db_saved"] = True
            except Exception as e:
                db.rollback()
                calc_result["db_saved"] = False
                calc_result["db_error"] = str(e)
        else:
            calc_result["db_saved"] = False

        return calc_result

    @classmethod
    def calculate_daily_index(cls, db: Any, target_date: Optional[dt_date] = None) -> int:
        service = cls()
        res = service.calculate_and_save_from_db(db=db, target_date=target_date)
        return res.get("indices_generated", 0)

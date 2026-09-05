"""
test_index.py
=============
Comprehensive unit tests for the Airfare Price Index Calculation Engine.
Verifies all mathematical formulations, weighting pipelines, and edge cases independently.
"""

import math
import pytest
from datetime import date

from app.services.index_calculator import (
    IndexCalculatorService,
    DEFAULT_BASE_PRICES,
    DEFAULT_WINDOW_WEIGHTS,
    DEFAULT_ROUTE_WEIGHTS
)
from seed_test_data import (
    get_friend_worked_example_data,
    get_prototype_synthetic_data,
    BOOKING_WINDOW_WEIGHTS
)


class TestIndexMathematics:
    """Unit tests for the mathematical foundations of the index engine."""

    def test_geometric_mean_basic(self):
        prices = [100.0, 400.0]
        gm = IndexCalculatorService.calculate_geometric_mean(prices)
        assert pytest.approx(gm, rel=1e-5) == 200.0
        assert pytest.approx(IndexCalculatorService.calculate_geometric_mean([2.0, 8.0, 32.0]), rel=1e-5) == 8.0

    def test_geometric_mean_invalid_and_empty(self):
        with pytest.raises(ValueError):
            IndexCalculatorService.calculate_geometric_mean([])

        with pytest.raises(ValueError):
            IndexCalculatorService.calculate_geometric_mean([0.0, -500.0])

    def test_price_relative_calculation(self):
        calc = IndexCalculatorService(base_value=100.0)
        p_rel = calc.calculate_price_relative(8800.0, 8000.0)
        assert pytest.approx(p_rel, rel=1e-5) == 110.0

        with pytest.raises(ValueError):
            calc.calculate_price_relative(8800.0, 0.0)

    def test_single_route_single_window(self):
        calc = IndexCalculatorService(base_prices={"DEL-BOM": {1: 8000.0}})
        obs = [{"route": "DEL-BOM", "advance_days": 1, "total_fare": 8000.0}]
        res = calc.calculate_index(obs, calculation_date=date(2026, 9, 4))

        assert res["indices_generated"] == 1
        assert "DEL-BOM" in res["summary"]
        assert pytest.approx(res["summary"]["DEL-BOM"], rel=1e-3) == 100.0

    def test_single_route_multiple_windows_weighted(self):
        calc = IndexCalculatorService()
        obs = [
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 8800.0},
            {"route": "DEL-BOM", "advance_days": 7, "total_fare": 5000.0},
            {"route": "DEL-BOM", "advance_days": 15, "total_fare": 4200.0},
            {"route": "DEL-BOM", "advance_days": 30, "total_fare": 3600.0},
        ]
        res = calc.calculate_index(obs, calculation_date=date(2026, 9, 4))
        assert pytest.approx(res["summary"]["DEL-BOM"], rel=1e-3) == 101.5

    def test_advance_window_weight_normalization(self):
        calc = IndexCalculatorService(window_weights={1: 0.15, 7: 0.35, 15: 0.30, 30: 0.20})
        obs = [
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 8800.0},
            {"route": "DEL-BOM", "advance_days": 7, "total_fare": 5000.0},
        ]
        res = calc.calculate_index(obs, calculation_date=date(2026, 9, 4))
        assert pytest.approx(res["summary"]["DEL-BOM"], rel=1e-3) == 103.0

    def test_multiple_routes_and_composite(self):
        calc = IndexCalculatorService()
        data = get_prototype_synthetic_data()
        res = calc.calculate_index(data)

        assert res["indices_generated"] == 4
        assert "DEL-BOM" in res["summary"]
        assert "BLR-DEL" in res["summary"]
        assert "HYD-MAA" in res["summary"]
        assert "COMPOSITE" in res["summary"]

    def test_empty_dataset_handling(self):
        calc = IndexCalculatorService()
        res = calc.calculate_index([])
        assert res["indices_generated"] == 0
        assert res["records"] == []
        assert "No valid flight fare observations" in res["message"]

    def test_invalid_zero_negative_fares_filtered(self):
        calc = IndexCalculatorService()
        dirty_obs = [
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": -1000.0},
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 0.0},
            {"route": None, "advance_days": 1, "total_fare": 5000.0},
            {"route": "DEL-BOM", "advance_days": None, "total_fare": 5000.0},
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 8000.0},
        ]
        res = calc.calculate_index(dirty_obs)
        assert res["indices_generated"] == 1
        assert res["summary"]["DEL-BOM"] == 100.0

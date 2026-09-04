"""
test_index.py
=============
Comprehensive unit tests for the Airfare Price Index Calculation Engine (Person B).
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
    FRIEND_ROUTE_WEIGHTS
)


class TestIndexMathematics:
    """Unit tests for the mathematical foundations of the index engine."""

    def test_geometric_mean_basic(self):
        """
        Tests Jevons geometric mean: GM = exp( (1/n) * sum(ln(p_i)) ).
        For 100 and 400, GM = sqrt(100 * 400) = 200.0.
        """
        prices = [100.0, 400.0]
        gm = IndexCalculatorService.calculate_geometric_mean(prices)
        assert pytest.approx(gm, rel=1e-5) == 200.0

        # 3 values: 2, 8, 32 -> GM = (2 * 8 * 32)**(1/3) = 512**(1/3) = 8.0
        assert pytest.approx(IndexCalculatorService.calculate_geometric_mean([2.0, 8.0, 32.0]), rel=1e-5) == 8.0

    def test_geometric_mean_invalid_and_empty(self):
        """Tests that non-positive prices or empty lists raise appropriate ValueError."""
        with pytest.raises(ValueError):
            IndexCalculatorService.calculate_geometric_mean([])

        with pytest.raises(ValueError):
            IndexCalculatorService.calculate_geometric_mean([0.0, -500.0])

    def test_price_relative_calculation(self):
        """
        Tests price relative: (current_price / base_price) * 100.
        E.g., current = 8800, base = 8000 -> 110.0
        """
        calc = IndexCalculatorService(base_value=100.0)
        p_rel = calc.calculate_price_relative(8800.0, 8000.0)
        assert pytest.approx(p_rel, rel=1e-5) == 110.0

        with pytest.raises(ValueError):
            calc.calculate_price_relative(8800.0, 0.0)

    def test_single_route_single_window(self):
        """
        Tests index calculation for 1 route with 1 booking window.
        Base price = 8000, observed fare = 8000 -> Index should be exactly 100.0.
        """
        calc = IndexCalculatorService(base_prices={"DEL-BOM": {1: 8000.0}})
        obs = [{"route": "DEL-BOM", "advance_days": 1, "total_fare": 8000.0}]
        res = calc.calculate_index(obs, calculation_date=date(2026, 9, 4))

        assert res["indices_generated"] == 1
        assert "DEL-BOM" in res["summary"]
        assert pytest.approx(res["summary"]["DEL-BOM"], rel=1e-3) == 100.0

    def test_single_route_multiple_windows_weighted(self):
        """
        Tests combining multiple booking windows using advance weights:
        1d: 15% (fare: 8800 / base: 8000 -> 110.0)
        7d: 35% (fare: 5000 / base: 5000 -> 100.0)
        15d: 30% (fare: 4200 / base: 4200 -> 100.0)
        30d: 20% (fare: 3600 / base: 3600 -> 100.0)
        Expected Route Index = (0.15 * 110) + (0.35 * 100) + (0.30 * 100) + (0.20 * 100)
                             = 16.5 + 35 + 30 + 20 = 101.5
        """
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
        """
        When only a subset of windows is present (e.g. 1d and 7d only),
        weights must dynamically renormalize to sum to 1.0.
        Given raw weights: 1d=0.15, 7d=0.35 (Total = 0.50)
        Normalized weights: 1d = 0.15 / 0.5 = 0.30, 7d = 0.35 / 0.5 = 0.70
        Price relatives: 1d = 110.0, 7d = 100.0
        Expected = (0.30 * 110.0) + (0.70 * 100.0) = 33.0 + 70.0 = 103.0
        """
        calc = IndexCalculatorService(window_weights={1: 0.15, 7: 0.35, 15: 0.30, 30: 0.20})
        obs = [
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 8800.0},
            {"route": "DEL-BOM", "advance_days": 7, "total_fare": 5000.0},
        ]
        res = calc.calculate_index(obs, calculation_date=date(2026, 9, 4))
        assert pytest.approx(res["summary"]["DEL-BOM"], rel=1e-3) == 103.0

    def test_friend_worked_example_exact_match(self):
        """
        Verifies the engine against the friend's exact handwritten notes.
        - DEL-BOM: T+1 (8200, 8400 -> avg 8300, base 8000 -> 103.75)
                   T+7 (5100, 5300 -> avg 5200, base 5000 -> 104.0)
                   Route Index = (103.75 + 104.0) / 2 = 103.875
        - DEL-CHE: T+1 (7100, 7300 -> avg 7200, base 7000 -> 102.857)
                   T+7 (4600, 4700 -> avg 4650, base 4500 -> 103.333)
                   Route Index = (102.857 + 103.333) / 2 = 103.095
        - Composite (60% DEL-BOM, 40% DEL-CHE):
                   = (103.875 * 0.6) + (103.095 * 0.4) = 103.563
        """
        calc = IndexCalculatorService(
            window_weights={1: 0.5, 7: 0.5},
            route_weights=FRIEND_ROUTE_WEIGHTS
        )
        data = get_friend_worked_example_data()

        # 1. Using arithmetic average (matches notebook exactly)
        res_arith = calc.calculate_index(data, use_arithmetic=True)
        assert pytest.approx(res_arith["summary"]["DEL-BOM"], rel=1e-3) == 103.875
        assert pytest.approx(res_arith["summary"]["DEL-CHE"], rel=1e-3) == 103.095
        assert pytest.approx(res_arith["summary"]["COMPOSITE"], rel=1e-3) == 103.563

        # 2. Using official Jevons geometric mean
        res_jevons = calc.calculate_index(data, use_arithmetic=False)
        assert pytest.approx(res_jevons["summary"]["DEL-BOM"], rel=1e-3) == 103.862
        assert pytest.approx(res_jevons["summary"]["DEL-CHE"], rel=1e-3) == 103.087
        assert pytest.approx(res_jevons["summary"]["COMPOSITE"], rel=1e-3) == 103.552

    def test_multiple_routes_and_composite(self):
        """
        Tests prototype 3-route dataset with full COMPOSITE index generation.
        """
        calc = IndexCalculatorService()
        data = get_prototype_synthetic_data()
        res = calc.calculate_index(data)

        assert res["indices_generated"] == 4  # DEL-BOM, BLR-DEL, HYD-MAA + COMPOSITE
        assert "DEL-BOM" in res["summary"]
        assert "BLR-DEL" in res["summary"]
        assert "HYD-MAA" in res["summary"]
        assert "COMPOSITE" in res["summary"]

        # Composite should be the weighted combination of the 3 routes
        expected_comp = (
            0.45 * res["summary"]["DEL-BOM"] +
            0.35 * res["summary"]["BLR-DEL"] +
            0.20 * res["summary"]["HYD-MAA"]
        )
        assert pytest.approx(res["summary"]["COMPOSITE"], rel=1e-3) == expected_comp

    def test_empty_dataset_handling(self):
        """Tests that passing an empty list does not crash and returns clean metadata."""
        calc = IndexCalculatorService()
        res = calc.calculate_index([])
        assert res["indices_generated"] == 0
        assert res["records"] == []
        assert "No valid flight fare observations" in res["message"]

    def test_invalid_zero_negative_fares_filtered(self):
        """Tests that non-numeric, zero, negative, or incomplete records are ignored."""
        calc = IndexCalculatorService()
        dirty_obs = [
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": -1000.0},
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 0.0},
            {"route": None, "advance_days": 1, "total_fare": 5000.0},
            {"route": "DEL-BOM", "advance_days": None, "total_fare": 5000.0},
            {"route": "DEL-BOM", "advance_days": 1, "total_fare": 8000.0},  # valid
        ]
        res = calc.calculate_index(dirty_obs)
        assert res["indices_generated"] == 1
        assert res["summary"]["DEL-BOM"] == 100.0

    def test_database_integration_and_duplicate_prevention(self):
        """
        Tests persisting calculation results to SQLite database session
        and verifies duplicate prevention (upsert behavior).
        """
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.index import Base, AirfareIndex

        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        calc = IndexCalculatorService()
        calc_date = date(2026, 9, 4)

        # 1st calculation run: should insert 4 records (3 routes + COMPOSITE)
        res1 = calc.calculate_and_save_from_db(db, target_date=calc_date)
        assert res1["db_saved"] is True
        rows1 = db.query(AirfareIndex).all()
        assert len(rows1) == 4

        # 2nd calculation run on the same date: should update, NOT create duplicate rows
        res2 = calc.calculate_and_save_from_db(db, target_date=calc_date)
        assert res2["db_saved"] is True
        rows2 = db.query(AirfareIndex).all()
        assert len(rows2) == 4  # Still exactly 4 rows



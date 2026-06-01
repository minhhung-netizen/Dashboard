import unittest
from datetime import date

from app.services.manual_portfolio import (
    build_daily_performance_record,
    build_manual_portfolio,
    is_after_daily_cutoff,
    is_after_manual_price_refresh_time,
    market_date_iso,
)


class ManualPortfolioTest(unittest.TestCase):
    def test_builds_weighted_return_and_equity_curve(self):
        result = build_manual_portfolio(
            [
                {
                    "id": 1,
                    "ticker": "VPB",
                    "weight_pct": 60,
                    "entry_price": 10,
                    "current_price": 11,
                    "quantity": None,
                    "entry_date": "2026-05-18T00:00:00+00:00",
                    "status": "open",
                    "exit_price": None,
                    "closed_at": None,
                    "note": None,
                    "created_at": "2026-05-18T00:00:00+00:00",
                    "updated_at": "2026-05-24T11:05:00+00:00",
                    "snapshots": [
                        {"price": 10, "recorded_at": "2026-05-18T00:00:00+00:00"},
                        {"price": 11, "recorded_at": "2026-05-24T11:05:00+00:00"},
                    ],
                },
                {
                    "id": 2,
                    "ticker": "TCB",
                    "weight_pct": 40,
                    "entry_price": 20,
                    "current_price": 19,
                    "quantity": None,
                    "entry_date": "2026-05-18T00:00:00+00:00",
                    "status": "open",
                    "exit_price": None,
                    "closed_at": None,
                    "note": None,
                    "created_at": "2026-05-18T00:00:00+00:00",
                    "updated_at": "2026-05-24T11:05:00+00:00",
                    "snapshots": [
                        {"price": 20, "recorded_at": "2026-05-18T00:00:00+00:00"},
                        {"price": 19, "recorded_at": "2026-05-24T11:05:00+00:00"},
                    ],
                },
            ]
        )

        self.assertAlmostEqual(result["summary"]["portfolio_return_pct"], 4)
        self.assertEqual(result["summary"]["open_count"], 2)
        self.assertAlmostEqual(result["positions"][0]["return_pct"], 10)
        self.assertAlmostEqual(result["equity_curve"][-1]["value"], 104)

    def test_equity_curve_uses_only_daily_snapshots_after_6pm_vietnam_time(self):
        result = build_manual_portfolio(
            [
                {
                    "id": 1,
                    "ticker": "VPB",
                    "weight_pct": 100,
                    "entry_price": 10,
                    "current_price": 12,
                    "quantity": None,
                    "entry_date": "2026-05-18",
                    "status": "open",
                    "exit_price": None,
                    "closed_at": None,
                    "note": None,
                    "created_at": "2026-05-18T00:00:00+00:00",
                    "updated_at": "2026-05-25T11:10:00+00:00",
                    "snapshots": [
                        {"price": 11, "recorded_at": "2026-05-25T10:59:00+00:00"},
                        {"price": 12, "recorded_at": "2026-05-25T11:10:00+00:00"},
                    ],
                },
            ]
        )

        self.assertEqual(len(result["equity_curve"]), 2)
        self.assertEqual(result["equity_curve"][-1]["time"], "2026-05-25T11:10:00+00:00")
        self.assertAlmostEqual(result["equity_curve"][-1]["value"], 120)

    def test_stored_daily_performance_drives_equity_curve_when_available(self):
        result = build_manual_portfolio(
            [],
            [
                {
                    "trade_date": "2026-05-24",
                    "portfolio_return_pct": 2,
                    "equity_value": 102,
                    "recorded_at": "2026-05-24T08:05:00+00:00",
                },
                {
                    "trade_date": "2026-05-25",
                    "portfolio_return_pct": 4,
                    "equity_value": 104,
                    "recorded_at": "2026-05-25T08:10:00+00:00",
                },
            ],
        )

        self.assertEqual(len(result["equity_curve"]), 2)
        self.assertEqual(result["equity_curve"][0]["trade_date"], "2026-05-24")
        self.assertAlmostEqual(result["equity_curve"][-1]["value"], 104)

    def test_build_daily_performance_record_uses_market_day_after_cutoff(self):
        positions = [
            {
                "id": 1,
                "ticker": "VPB",
                "weight_pct": 100,
                "entry_price": 10,
                "current_price": 12,
                "quantity": None,
                "entry_date": "2026-05-18",
                "status": "open",
                "exit_price": None,
                "closed_at": None,
                "note": None,
                "created_at": "2026-05-18T00:00:00+00:00",
                "updated_at": "2026-05-25T08:10:00+00:00",
                "snapshots": [],
            },
        ]

        record = build_daily_performance_record(
            positions,
            recorded_at="2026-05-25T18:05:00+07:00",
        )

        self.assertEqual(record["trade_date"], "2026-05-25")
        self.assertAlmostEqual(record["portfolio_return_pct"], 20)
        self.assertAlmostEqual(record["equity_value"], 120)
        self.assertTrue(is_after_daily_cutoff("2026-05-25T18:05:00+07:00"))
        self.assertFalse(is_after_daily_cutoff("2026-05-25T17:59:00+07:00"))
        self.assertTrue(is_after_manual_price_refresh_time("2026-05-25T16:05:00+07:00"))
        self.assertFalse(is_after_manual_price_refresh_time("2026-05-25T15:59:00+07:00"))
        self.assertEqual(market_date_iso("2026-05-25T16:05:00+07:00"), "2026-05-25")

    def test_manual_position_uses_adjusted_entry_after_dividend_ex_date(self):
        result = build_manual_portfolio(
            [
                {
                    "id": 1,
                    "ticker": "VPB",
                    "weight_pct": 100,
                    "entry_price": 100,
                    "current_price": 110,
                    "quantity": 10,
                    "entry_date": "2026-01-01",
                    "status": "open",
                    "exit_price": None,
                    "closed_at": None,
                    "note": None,
                    "created_at": "2026-01-01T00:00:00+07:00",
                    "updated_at": "2026-01-12T00:00:00+07:00",
                    "snapshots": [],
                },
            ],
            dividend_events=[
                {
                    "ticker": "VPB",
                    "ex_date": "2026-01-10",
                    "cash_amount": 10,
                    "stock_ratio_pct": None,
                    "note": "cash dividend",
                }
            ],
            as_of_date=date(2026, 1, 12),
        )

        position = result["positions"][0]
        self.assertAlmostEqual(position["entry_price"], 90)
        self.assertAlmostEqual(position["return_pct"], 22.222222, places=5)
        self.assertAlmostEqual(position["cost_value"], 900)
        self.assertEqual(position["dividend_notes"][0]["status"], "applied")


if __name__ == "__main__":
    unittest.main()

import unittest

from app.services.manual_portfolio import build_manual_portfolio


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
                    "updated_at": "2026-05-24T08:05:00+00:00",
                    "snapshots": [
                        {"price": 10, "recorded_at": "2026-05-18T00:00:00+00:00"},
                        {"price": 11, "recorded_at": "2026-05-24T08:05:00+00:00"},
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
                    "updated_at": "2026-05-24T08:05:00+00:00",
                    "snapshots": [
                        {"price": 20, "recorded_at": "2026-05-18T00:00:00+00:00"},
                        {"price": 19, "recorded_at": "2026-05-24T08:05:00+00:00"},
                    ],
                },
            ]
        )

        self.assertAlmostEqual(result["summary"]["portfolio_return_pct"], 4)
        self.assertEqual(result["summary"]["open_count"], 2)
        self.assertAlmostEqual(result["positions"][0]["return_pct"], 10)
        self.assertAlmostEqual(result["equity_curve"][-1]["value"], 104)

    def test_equity_curve_uses_only_daily_snapshots_after_3pm_vietnam_time(self):
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
                    "updated_at": "2026-05-25T08:10:00+00:00",
                    "snapshots": [
                        {"price": 11, "recorded_at": "2026-05-25T07:59:00+00:00"},
                        {"price": 12, "recorded_at": "2026-05-25T08:10:00+00:00"},
                    ],
                },
            ]
        )

        self.assertEqual(len(result["equity_curve"]), 2)
        self.assertEqual(result["equity_curve"][-1]["time"], "2026-05-25T08:10:00+00:00")
        self.assertAlmostEqual(result["equity_curve"][-1]["value"], 120)


if __name__ == "__main__":
    unittest.main()

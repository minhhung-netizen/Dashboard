import unittest

from app.services.derivatives import (
    build_derivative_performance,
    normalize_derivative_action,
)


def event(
    event_id,
    action,
    price,
    quantity=1,
    *,
    symbol="VN30F1M",
    strategy="VN30 Modern DCA",
    reason=None,
):
    return {
        "id": event_id,
        "symbol": symbol,
        "action": action,
        "price": price,
        "quantity": quantity,
        "contract_multiplier": 100000,
        "strategy": strategy,
        "reason": reason,
        "source_time": f"2026-06-0{event_id}T09:00:00+07:00",
        "received_at": f"2026-06-0{event_id}T02:00:00+00:00",
        "payload": {},
    }


class DerivativePerformanceTest(unittest.TestCase):
    def test_normalizes_derivative_actions(self):
        self.assertEqual(normalize_derivative_action("long"), "long_start")
        self.assertEqual(normalize_derivative_action("DCA Long"), "dca_long")
        self.assertEqual(normalize_derivative_action("exit-short"), "close_short")

    def test_tracks_long_dca_average_and_open_pnl(self):
        result = build_derivative_performance(
            [
                event(1, "long_start", 1300, 1),
                event(2, "dca_long", 1290, 2),
                event(3, "dca_long", 1280, 1),
            ]
        )

        position = result["open_positions"][0]
        self.assertEqual(position["side"], "long")
        self.assertEqual(position["quantity"], 4)
        self.assertEqual(position["layer_count"], 3)
        self.assertAlmostEqual(position["average_price"], 1290)
        self.assertAlmostEqual(position["pnl_points"], -40)
        self.assertAlmostEqual(position["pnl_vnd"], -4000000)

    def test_closes_short_position_and_calculates_realized_pnl(self):
        result = build_derivative_performance(
            [
                event(1, "short_start", 1300, 1),
                event(2, "dca_short", 1310, 1),
                event(3, "close_short", 1290, 1, reason="TP"),
            ]
        )

        trade = result["closed_trades"][0]
        self.assertEqual(result["open_positions"], [])
        self.assertAlmostEqual(trade["average_price"], 1305)
        self.assertAlmostEqual(trade["pnl_points"], 30)
        self.assertAlmostEqual(trade["pnl_vnd"], 3000000)
        self.assertEqual(trade["exit_reason"], "TP")
        self.assertEqual(result["summary"]["wins"], 1)

    def test_ignores_dca_without_matching_position(self):
        result = build_derivative_performance([event(1, "dca_long", 1300, 1)])

        self.assertEqual(result["open_positions"], [])
        self.assertEqual(result["ignored_events"][0]["reason"], "dca_without_matching_position")

    def test_mark_updates_open_position_price_without_adding_layer(self):
        result = build_derivative_performance(
            [
                event(1, "long_start", 1300, 1),
                event(2, "mark", 1312, 1),
            ]
        )

        position = result["open_positions"][0]
        self.assertEqual(position["layer_count"], 1)
        self.assertEqual(position["current_price"], 1312)
        self.assertEqual(position["pnl_points"], 12)
        self.assertEqual(position["pnl_vnd"], 1200000)
        self.assertEqual([row["action"] for row in result["events"]], ["long_start"])

    def test_calculates_maximum_drawdown_from_closed_trade_equity(self):
        result = build_derivative_performance(
            [
                event(1, "long_start", 100, 1),
                event(2, "close_long", 90, 1),
                event(3, "long_start", 100, 1),
                event(4, "close_long", 120, 1),
            ],
            initial_capital=10000000,
        )

        summary = result["summary"]
        self.assertEqual(summary["initial_capital"], 10000000)
        self.assertEqual(summary["realized_pnl_vnd"], 1000000)
        self.assertEqual(summary["current_equity"], 11000000)
        self.assertEqual(summary["max_drawdown_vnd"], 1000000)
        self.assertEqual(summary["max_drawdown_pct"], 10)


if __name__ == "__main__":
    unittest.main()

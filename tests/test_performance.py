import unittest

from app.services.performance import build_performance


def signal(
    signal_id,
    ticker,
    action,
    price,
    strategy="RS",
    received_at=None,
    source_time=None,
    payload=None,
):
    return {
        "id": signal_id,
        "ticker": ticker,
        "action": action,
        "price": price,
        "strategy": strategy,
        "source_time": source_time,
        "received_at": received_at or f"2026-01-0{signal_id}T00:00:00+00:00",
        "enrichment": {},
        "payload": payload or {},
    }


class PerformanceTest(unittest.TestCase):
    def test_pairs_buy_then_sell_by_strategy(self):
        result = build_performance(
            [
                signal(1, "VPB", "buy", 10, "Breakout", "2026-01-01T09:00:00+00:00"),
                signal(2, "VPB", "sell", 11, "Breakout", "2026-01-03T10:30:00+00:00"),
            ]
        )

        self.assertEqual(result["closed_trades"][0]["return_pct"], 10)
        self.assertEqual(result["closed_trades"][0]["holding_seconds"], 178200)
        self.assertEqual(result["strategies"][0]["strategy"], "Breakout")
        self.assertEqual(result["strategies"][0]["closed_trades"], 1)
        self.assertEqual(result["strategies"][0]["win_rate_pct"], 100)

    def test_keeps_open_trade_with_latest_signal_price(self):
        result = build_performance(
            [
                signal(1, "VCB", "buy", 100, "Swing"),
                signal(2, "VCB", "note", 105, "Swing"),
            ]
        )

        self.assertEqual(result["open_trades"][0]["return_pct"], 5)
        self.assertEqual(result["strategies"][0]["open_trades"], 1)
        self.assertAlmostEqual(result["strategies"][0]["current_return_pct"], 5)

    def test_sell_without_buy_is_ignored(self):
        result = build_performance([signal(1, "VCB", "sell", 99, "Swing")])

        self.assertEqual(result["closed_trades"], [])
        self.assertEqual(result["ignored_signals"][0]["reason"], "sell_without_open_buy")
        self.assertEqual(result["strategies"], [])

    def test_same_strategy_is_split_by_ticker(self):
        result = build_performance(
            [
                signal(1, "VPB", "buy", 10, "Breakout"),
                signal(2, "VPB", "sell", 11, "Breakout"),
                signal(3, "VCB", "buy", 100, "Breakout"),
                signal(4, "VCB", "sell", 98, "Breakout"),
            ]
        )

        rows = {(row["ticker"], row["strategy"]): row for row in result["strategies"]}
        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(rows[("VPB", "Breakout")]["realized_return_pct"], 10)
        self.assertAlmostEqual(rows[("VCB", "Breakout")]["realized_return_pct"], -2)

    def test_open_trade_prefers_refreshed_enrichment_price(self):
        buy = signal(1, "VPB", "buy", 10, "Breakout")
        buy["enrichment"] = {
            "refreshed_at": "2026-01-01T10:00:00+00:00",
            "history": [{"close": 12}],
        }
        later_signal = signal(2, "VPB", "note", 11, "Breakout")

        result = build_performance([buy, later_signal])

        self.assertAlmostEqual(result["open_trades"][0]["return_pct"], 20)

    def test_open_trade_is_marked_when_confirm_buy_matches_base_strategy(self):
        result = build_performance(
            [
                signal(1, "MSB", "buy", 10, "STxanhdo"),
                signal(
                    2,
                    "MSB",
                    "confirm_buy",
                    11,
                    "HMA",
                    payload={"base_strategy": "STxanhdo"},
                ),
            ]
        )

        trade = result["open_trades"][0]
        self.assertTrue(trade["has_confirm_buy"])
        self.assertEqual(trade["confirmations"][0]["strategy"], "HMA")
        self.assertEqual(trade["confirmations"][0]["action"], "confirm_buy")

    def test_confirmation_stats_compare_confirmed_and_unconfirmed_closed_trades(self):
        result = build_performance(
            [
                signal(1, "MSB", "buy", 10, "STxanhdo"),
                signal(
                    2,
                    "MSB",
                    "confirm_buy",
                    11,
                    "HMA",
                    payload={"base_strategy": "STxanhdo"},
                ),
                signal(3, "MSB", "sell", 12, "STxanhdo"),
                signal(4, "FPT", "buy", 100, "STxanhdo"),
                signal(5, "FPT", "sell", 95, "STxanhdo"),
            ]
        )

        stats = {row["status"]: row for row in result["confirmation_stats"]}
        self.assertEqual(stats["confirmed"]["closed_trades"], 1)
        self.assertAlmostEqual(stats["confirmed"]["avg_return_pct"], 20)
        self.assertEqual(stats["unconfirmed"]["closed_trades"], 1)
        self.assertAlmostEqual(stats["unconfirmed"]["avg_return_pct"], -5)

    def test_uses_source_time_for_trade_timing_when_available(self):
        result = build_performance(
            [
                signal(
                    1,
                    "POW",
                    "buy",
                    13.95,
                    "STxanhdo",
                    received_at="2026-05-25T09:32:00+00:00",
                    source_time="2026-04-09T13:59:37+07:00",
                ),
                signal(
                    2,
                    "POW",
                    "sell",
                    14.5,
                    "STxanhdo",
                    received_at="2026-05-25T09:33:00+00:00",
                    source_time="2026-04-10T13:59:37+07:00",
                ),
            ]
        )

        trade = result["closed_trades"][0]
        self.assertEqual(trade["entry_time"], "2026-04-09T13:59:37+07:00")
        self.assertEqual(trade["exit_time"], "2026-04-10T13:59:37+07:00")
        self.assertEqual(trade["holding_seconds"], 86400)

    def test_uses_pinescript_time_close_iso_payload(self):
        result = build_performance(
            [
                signal(
                    1,
                    "POW",
                    "buy",
                    13.95,
                    "STxanhdo",
                    received_at="2026-05-25T09:32:00+00:00",
                    source_time="2026-04-09T15:00:00+07:00",
                ),
                signal(
                    2,
                    "POW",
                    "sell",
                    14.5,
                    "STxanhdo",
                    received_at="2026-05-25T09:33:00+00:00",
                    source_time="2026-04-09T17:00:00+07:00",
                ),
            ]
        )

        self.assertEqual(result["closed_trades"][0]["holding_seconds"], 7200)


if __name__ == "__main__":
    unittest.main()

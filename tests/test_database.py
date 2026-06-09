import tempfile
import unittest
from pathlib import Path

from app.database import SignalStore


class SignalStoreTest(unittest.TestCase):
    def test_delete_signal_removes_existing_row(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            signal = store.insert_signal(
                ticker="VPB",
                exchange="HOSE",
                action="buy",
                price=19.5,
                timeframe="1D",
                strategy="manual-test",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )

            self.assertTrue(store.delete_signal(signal["id"]))
            self.assertEqual(store.list_signals(), [])

    def test_delete_signal_returns_false_for_missing_row(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")

            self.assertFalse(store.delete_signal(999))

    def test_init_normalizes_existing_vnd_signal_prices(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "signals.db"
            store = SignalStore(db_path)
            signal = store.insert_signal(
                ticker="MSN",
                exchange="HOSE",
                action="sell",
                price=74400,
                timeframe="2H",
                strategy="STxanhdo",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )

            self.assertEqual(signal["price"], 74400)
            migrated = SignalStore(db_path).get_signal(signal["id"])
            self.assertEqual(migrated["price"], 74.4)

    def test_init_normalizes_existing_malformed_confirm_actions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "signals.db"
            store = SignalStore(db_path)
            buy_signal = store.insert_signal(
                ticker="FPT",
                exchange="HOSE",
                action="confi m_buy",
                price=74.8,
                timeframe="2H",
                strategy="HMA",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )
            sell_signal = store.insert_signal(
                ticker="FPT",
                exchange="HOSE",
                action="confim_sell",
                price=74.8,
                timeframe="2H",
                strategy="HMA",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )

            migrated_store = SignalStore(db_path)

            self.assertEqual(migrated_store.get_signal(buy_signal["id"])["action"], "confirm_buy")
            self.assertEqual(
                migrated_store.get_signal(sell_signal["id"])["action"],
                "confirm_sell",
            )

    def test_find_duplicate_signal_uses_source_time_when_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            signal = store.insert_signal(
                ticker="VPB",
                exchange="HOSE",
                action="buy",
                price=19.5,
                timeframe="1D",
                strategy="RS",
                note=None,
                source_time="2026-05-24T14:45:00Z",
                payload={},
                enrichment={},
            )

            duplicate = store.find_duplicate_signal(
                ticker="VPB",
                action="buy",
                timeframe="1D",
                strategy="RS",
                source_time="2026-05-24T14:45:00Z",
                window_minutes=5,
            )

            self.assertIsNotNone(duplicate)
            self.assertEqual(duplicate["id"], signal["id"])

    def test_find_duplicate_signal_uses_recent_window_without_source_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            store.insert_signal(
                ticker="TCB",
                exchange="HOSE",
                action="sell",
                price=30.5,
                timeframe="1D",
                strategy="manual-test",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )

            duplicate = store.find_duplicate_signal(
                ticker="TCB",
                action="sell",
                timeframe="1D",
                strategy="manual-test",
                source_time=None,
                window_minutes=5,
            )

            self.assertIsNotNone(duplicate)

    def test_derivative_signal_lifecycle_and_duplicate_lookup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            signal = store.insert_derivative_signal(
                symbol="VN30F1M",
                exchange="HNX",
                action="long_start",
                price=1300,
                quantity=2,
                contract_multiplier=100000,
                timeframe="5",
                strategy="VN30 Modern DCA",
                reason=None,
                source_time="2026-06-09T09:00:00+07:00",
                payload={"asset_type": "derivative"},
            )

            duplicate = store.find_duplicate_derivative_signal(
                symbol="VN30F1M",
                action="long_start",
                timeframe="5",
                strategy="VN30 Modern DCA",
                source_time="2026-06-09T09:00:00+07:00",
                window_minutes=5,
            )

            self.assertEqual(store.list_all_derivative_signals()[0]["id"], signal["id"])
            self.assertEqual(duplicate["id"], signal["id"])
            self.assertTrue(store.delete_derivative_signal(signal["id"]))
            self.assertEqual(store.list_all_derivative_signals(), [])

    def test_record_and_list_invalid_signal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            recorded = store.record_invalid_signal(
                ticker="VPB",
                action="buy",
                timeframe="1D",
                strategy="RS",
                reason="duplicate_webhook",
                source_time="2026-05-24T14:45:00Z",
                payload={"ticker": "HOSE:VPB"},
            )

            invalid_signals = store.list_invalid_signals()

            self.assertEqual(invalid_signals[0]["id"], recorded["id"])
            self.assertEqual(invalid_signals[0]["reason"], "duplicate_webhook")
            self.assertEqual(invalid_signals[0]["payload"]["ticker"], "HOSE:VPB")

    def test_manual_position_lifecycle_records_snapshots(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            position = store.insert_manual_position(
                ticker="VPB",
                weight_pct=10,
                entry_price=20,
                current_price=21,
                quantity=100,
                entry_date="2026-05-18T02:00:00+00:00",
                note="core",
            )

            updated = store.update_manual_position(position["id"], {"current_price": 22})
            closed = store.close_manual_position(
                position["id"],
                exit_price=23,
                closed_at="2026-05-24T08:00:00+00:00",
            )

            self.assertEqual(updated["current_price"], 22)
            self.assertEqual(closed["status"], "closed")
            self.assertEqual(closed["exit_price"], 23)
            self.assertGreaterEqual(len(closed["snapshots"]), 4)

    def test_update_manual_market_price_updates_only_open_positions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            open_position = store.insert_manual_position(
                ticker="VPB",
                weight_pct=10,
                entry_price=20,
                current_price=None,
                quantity=None,
                entry_date=None,
                note=None,
            )
            closed_position = store.insert_manual_position(
                ticker="VPB",
                weight_pct=10,
                entry_price=30,
                current_price=None,
                quantity=None,
                entry_date=None,
                note=None,
            )
            store.close_manual_position(closed_position["id"], exit_price=31, closed_at=None)

            updated = store.update_manual_market_price(
                ticker="VPB",
                price=22,
                recorded_at="2026-05-24T09:30:00+00:00",
            )
            positions = {item["id"]: item for item in store.list_manual_positions()}

            self.assertEqual(updated, 1)
            self.assertEqual(positions[open_position["id"]]["current_price"], 22)
            self.assertEqual(positions[closed_position["id"]]["current_price"], 31)
            self.assertIn("VPB", store.list_open_manual_tickers())

    def test_upserts_manual_daily_performance_by_trade_date(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            first = store.upsert_manual_daily_performance(
                trade_date="2026-05-25",
                portfolio_return_pct=2,
                equity_value=102,
                total_weight_pct=50,
                open_count=1,
                closed_count=0,
                cost_value=None,
                market_value=None,
                pnl_value=None,
                recorded_at="2026-05-25T15:01:00+07:00",
            )
            second = store.upsert_manual_daily_performance(
                trade_date="2026-05-25",
                portfolio_return_pct=3,
                equity_value=103,
                total_weight_pct=60,
                open_count=2,
                closed_count=0,
                cost_value=None,
                market_value=None,
                pnl_value=None,
                recorded_at="2026-05-25T15:10:00+07:00",
            )
            rows = store.list_manual_daily_performance()

            self.assertEqual(first["trade_date"], "2026-05-25")
            self.assertEqual(len(rows), 1)
            self.assertEqual(second["id"], rows[0]["id"])
            self.assertAlmostEqual(rows[0]["portfolio_return_pct"], 3)
            self.assertAlmostEqual(rows[0]["equity_value"], 103)
            self.assertTrue(store.delete_manual_daily_performance("2026-05-25"))
            self.assertFalse(store.delete_manual_daily_performance("2026-05-25"))
            self.assertEqual(store.list_manual_daily_performance(), [])

    def test_dividend_event_lifecycle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            event = store.insert_dividend_event(
                ticker="vpb",
                ex_date="2026-06-10",
                cash_amount=1,
                stock_ratio_pct=10,
                issue_ratio_pct=20,
                issue_price=10,
                note="cash and stock",
            )

            rows = store.list_dividend_events("VPB")

            self.assertEqual(event["ticker"], "VPB")
            self.assertEqual(rows[0]["id"], event["id"])
            self.assertEqual(rows[0]["ex_date"], "2026-06-10")
            self.assertEqual(rows[0]["issue_ratio_pct"], 20)
            self.assertEqual(rows[0]["issue_price"], 10)
            self.assertTrue(store.delete_dividend_event(event["id"]))
            self.assertFalse(store.delete_dividend_event(event["id"]))


if __name__ == "__main__":
    unittest.main()

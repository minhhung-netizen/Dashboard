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


if __name__ == "__main__":
    unittest.main()

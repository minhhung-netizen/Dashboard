from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from app.database import BacktestStore
from app.services.backtesting import BacktestConfig, run_backtest


class BacktestingTests(unittest.TestCase):
    def _sample_prices(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "date": pd.date_range("2024-01-02", periods=8, freq="B"),
                "open": [10, 10.5, 11, 12, 13, 12, 11, 10],
                "high": [10.5, 11, 12, 13, 14, 13, 12, 11],
                "low": [9.5, 10, 10.5, 11, 12, 11, 10, 9.5],
                "close": [10, 11, 12, 13, 12, 11, 10, 9],
                "volume": [100_000] * 8,
            }
        )

    def test_engine_fills_next_open_and_never_shorts(self) -> None:
        result = run_backtest(
            {"FPT": self._sample_prices()},
            BacktestConfig(
                strategy_name="ma_crossover",
                fast_window=1,
                slow_window=2,
                initial_cash=1_000_000,
                commission_rate=0,
                sell_tax_rate=0,
                slippage_bps=0,
                lot_size=100,
                max_participation_rate=1,
            ),
        )
        self.assertFalse(result.trades.empty)
        self.assertEqual(result.trades.iloc[0]["side"], "BUY")
        self.assertEqual(result.trades.iloc[0]["date"].date().isoformat(), "2024-01-04")
        self.assertTrue(set(result.trades["side"]).issubset({"BUY", "SELL"}))
        self.assertGreaterEqual(result.metrics["ending_equity"], 0)

    def test_store_persists_completed_run_and_price_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = BacktestStore(Path(directory) / "backtests.db")
            run = store.create_backtest_run(
                created_by_user_id=None,
                symbols=["FPT"],
                strategy="ma_crossover",
                config={"strategy_name": "ma_crossover"},
                start_date="2024-01-01",
                end_date="2024-12-31",
            )
            store.mark_backtest_running(run["id"])
            store.complete_backtest_run(
                run["id"],
                metrics={"total_return": 0.12},
                equity_points=[{
                    "date": "2024-01-02", "equity": 1_000_000,
                    "cash": 1_000_000, "invested_symbols": 0,
                }],
                trades=[],
            )
            store.upsert_backtest_price_bars(
                ticker="FPT",
                provider="vnstock",
                bars=[{
                    "date": "2024-01-02", "open": 100, "high": 110,
                    "low": 95, "close": 105, "volume": 1_000,
                }],
            )
            saved = store.get_backtest_run(run["id"])
            self.assertEqual(saved["status"], "completed")
            self.assertEqual(saved["metrics"]["total_return"], 0.12)
            self.assertEqual(len(store.list_backtest_equity_points(run["id"])), 1)
            self.assertEqual(
                store.list_backtest_price_bars(
                    ticker="FPT", start_date="2024-01-01", end_date="2024-01-03"
                )[0]["close"],
                105,
            )

    def test_store_classifies_signals_and_marks_a_standard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = BacktestStore(Path(directory) / "backtests.db")
            filters = store.update_signal_filter_settings(
                allowed_tickers=["FPT"], allowed_strategies=["MA crossover"],
                allow_buy=True, allow_sell=False,
            )
            self.assertEqual(filters["allowed_tickers"], ["FPT"])
            signal = store.create_signal(
                ticker="FPT", exchange="HOSE", action="buy", timeframe="1D",
                strategy="MA crossover", note=None, source_time=None,
                status="pending", category="watch", classification_note=None,
                rejection_reason=None, payload={"ticker": "HOSE:FPT"},
            )
            classified = store.classify_signal(
                signal["id"], status="accepted", category="entry", classification_note=None
            )
            self.assertEqual(classified["status"], "accepted")
            self.assertEqual(store.signal_summary()["accepted"], 1)
            run = store.create_backtest_run(
                created_by_user_id=None, symbols=["FPT"], strategy="MA crossover",
                config={}, start_date="2024-01-01", end_date="2024-12-31",
                data_source="local_import",
            )
            store.complete_backtest_run(
                run["id"], metrics={"total_return": 0.2}, equity_points=[], trades=[]
            )
            standard = store.set_backtest_standard(run["id"])
            self.assertEqual(standard["is_standard"], 1)
            self.assertEqual(store.list_backtest_standards()[0]["id"], run["id"])


if __name__ == "__main__":
    unittest.main()

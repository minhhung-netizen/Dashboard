import tempfile
import unittest
import sqlite3
from pathlib import Path

from app.database import SignalStore


class SignalStoreTest(unittest.TestCase):
    def test_init_migrates_existing_dividend_table_for_external_events(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "signals.db"
            conn = sqlite3.connect(database_path)
            try:
                conn.execute(
                    """
                    CREATE TABLE dividend_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticker TEXT NOT NULL,
                        ex_date TEXT NOT NULL,
                        cash_amount REAL,
                        stock_ratio_pct REAL,
                        issue_ratio_pct REAL,
                        issue_price REAL,
                        note TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
            finally:
                conn.close()

            store = SignalStore(database_path)
            store.upsert_external_dividend_events(
                [
                    {
                        "ticker": "FPT",
                        "ex_date": "2026-06-20",
                        "source": "fireant",
                        "external_id": "FPT:1",
                    }
                ]
            )

            self.assertEqual(store.list_dividend_events("FPT")[0]["source"], "fireant")

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

    def test_init_keeps_and_repairs_vnindex_point_prices(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "signals.db"
            store = SignalStore(db_path)
            normalized = store.insert_signal(
                ticker="VNINDEX",
                exchange="HOSE",
                action="buy",
                price=1.876,
                timeframe="60",
                strategy="Modern Stock EMA",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )
            raw = store.insert_signal(
                ticker="VNINDEX",
                exchange="HOSE",
                action="sell",
                price=1876.75,
                timeframe="60",
                strategy="Modern Stock EMA",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )

            migrated_store = SignalStore(db_path)
            self.assertEqual(migrated_store.get_signal(normalized["id"])["price"], 1876)
            self.assertEqual(migrated_store.get_signal(raw["id"])["price"], 1876.75)

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

    def test_app_setting_is_persisted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "signals.db"
            store = SignalStore(db_path)

            store.set_app_setting("derivative_initial_capital", "250000000")

            reloaded = SignalStore(db_path)
            self.assertEqual(
                reloaded.get_app_setting("derivative_initial_capital"),
                "250000000",
            )

    def test_database_uses_wal_and_busy_timeout(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")

            status = store.database_status()

            self.assertEqual(status["journal_mode"].lower(), "wal")
            self.assertEqual(status["busy_timeout_ms"], 10000)
            self.assertGreater(status["size_bytes"], 0)

    def test_user_preferences_are_persisted_per_account(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            user = store.create_user(
                username="viewer",
                password_hash="hash",
                role="user",
                features=["overview"],
            )

            saved = store.upsert_user_preferences(
                user_id=user["id"],
                watchlist=["vpb", "FPT", "VPB"],
                theme="light",
                language="en",
            )
            reloaded = SignalStore(store.database_path).get_user_preferences(user["id"])

            self.assertEqual(saved["watchlist"], ["FPT", "VPB"])
            self.assertEqual(reloaded["theme"], "light")
            self.assertEqual(reloaded["language"], "en")

    def test_database_backup_is_a_readable_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            store.set_app_setting("snapshot", "ready")
            destination = Path(temp_dir) / "backups" / "signals.db"

            store.backup_database(destination)
            restored = SignalStore(destination)

            self.assertEqual(restored.get_app_setting("snapshot"), "ready")

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

    def test_upserts_strategy_backtest_stats_by_ticker_strategy_metric(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            first = store.upsert_strategy_backtest_stat(
                ticker="vpb",
                strategy="STxanhdo",
                metric_name="Price Drawdown % From BUY",
                closed_trades=100,
                negative_trades=40,
                max_loss_pct=-12.2,
                min_loss_pct=-0.56,
                avg_loss_pct=-4.39,
                max_gain_pct=47.59,
                avg_gain_pct=16.64,
                tp1_hits=1,
                tp1_total=7,
                tp2_hits=1,
                tp2_total=7,
                tp3_hits=1,
                tp3_total=7,
                avg_hold_bars=91.44,
                avg_hold_days=26.47,
                note="initial backtest",
            )
            second = store.upsert_strategy_backtest_stat(
                ticker="VPB",
                strategy="STxanhdo",
                metric_name="Price Drawdown % From BUY",
                closed_trades=120,
                negative_trades=45,
                max_loss_pct=-10,
                min_loss_pct=-0.5,
                avg_loss_pct=-3.9,
                max_gain_pct=50,
                avg_gain_pct=18.2,
                tp1_hits=2,
                tp1_total=8,
                tp2_hits=1,
                tp2_total=8,
                tp3_hits=1,
                tp3_total=8,
                avg_hold_bars=80,
                avg_hold_days=20,
                note="updated backtest",
            )
            rows = store.list_strategy_backtest_stats(ticker="VPB", strategy="STxanhdo")

            self.assertEqual(first["ticker"], "VPB")
            self.assertEqual(len(rows), 1)
            self.assertEqual(second["id"], rows[0]["id"])
            self.assertEqual(rows[0]["closed_trades"], 120)
            self.assertAlmostEqual(rows[0]["avg_loss_pct"], -3.9)
            self.assertAlmostEqual(rows[0]["max_gain_pct"], 50)
            self.assertEqual(rows[0]["tp1_hits"], 2)
            self.assertEqual(rows[0]["tp1_total"], 8)
            self.assertEqual(rows[0]["note"], "updated backtest")
            self.assertTrue(store.delete_strategy_backtest_stat(rows[0]["id"]))
            self.assertFalse(store.delete_strategy_backtest_stat(rows[0]["id"]))

    def test_upserts_kelly_entries_by_ticker_and_strategy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            first = store.upsert_kelly_entry(
                ticker="vpb",
                strategy="STxanhdo",
                win_rate=40.11,
                winning_trades=73,
                total_trades=182,
                profit_factor=1.616,
                max_drawdown=5.83,
                target_drawdown=3,
                fraction=50,
                max_allocation=10,
            )
            second = store.upsert_kelly_entry(
                ticker="VPB",
                strategy="STxanhdo",
                win_rate=45,
                winning_trades=80,
                total_trades=190,
                profit_factor=1.7,
                max_drawdown=6,
                target_drawdown=3,
                fraction=40,
                max_allocation=12,
            )
            rows = store.list_kelly_entries(ticker="VPB", strategy="STxanhdo")

            self.assertEqual(first["ticker"], "VPB")
            self.assertEqual(len(rows), 1)
            self.assertEqual(second["id"], rows[0]["id"])
            self.assertAlmostEqual(rows[0]["win_rate"], 45)
            self.assertAlmostEqual(rows[0]["max_allocation"], 12)
            self.assertTrue(store.delete_kelly_entry(rows[0]["id"]))
            self.assertFalse(store.delete_kelly_entry(rows[0]["id"]))

    def test_updates_dca_plan_for_owner_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            owner = store.create_user(
                username="owner",
                password_hash="hash",
                role="user",
                features=["dcaSizing"],
            )
            other = store.create_user(
                username="other",
                password_hash="hash",
                role="user",
                features=["dcaSizing"],
            )
            plan = store.insert_dca_plan(
                user_id=owner["id"],
                ticker="vpb",
                strategy="STxanhdo",
                initial_capital=500000000,
                allocation_pct=10,
                entry_price=20,
                distance_mode="percent",
                max_loss_pct=12,
                lot_size=100,
                levels=[{"distancePct": 0, "multiplier": 1}],
                result={"rows": [{"index": 1, "buyPrice": 20}]},
            )

            updated = store.update_dca_plan(
                plan_id=plan["id"],
                user_id=owner["id"],
                ticker="fpt",
                strategy="Swing",
                initial_capital=600000000,
                allocation_pct=12,
                entry_price=75,
                distance_mode="priceStep",
                max_loss_pct=8,
                lot_size=100,
                levels=[{"distancePct": 2, "multiplier": 1.2}],
                result={"rows": [{"index": 1, "buyPrice": 75}], "priceStep": 100},
            )

            self.assertEqual(updated["id"], plan["id"])
            self.assertEqual(updated["ticker"], "FPT")
            self.assertEqual(updated["strategy"], "Swing")
            self.assertEqual(updated["distance_mode"], "priceStep")
            self.assertEqual(updated["levels"][0]["multiplier"], 1.2)
            self.assertEqual(updated["result"]["priceStep"], 100)
            with self.assertRaises(KeyError):
                store.update_dca_plan(
                    plan_id=plan["id"],
                    user_id=other["id"],
                    ticker="VCB",
                    strategy="Swing",
                    initial_capital=None,
                    allocation_pct=None,
                    entry_price=None,
                    distance_mode="percent",
                    max_loss_pct=None,
                    lot_size=None,
                    levels=[],
                    result={},
                )

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

    def test_deletes_all_dividend_events_for_ticker_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            for ticker, ex_date in [
                ("FPT", "2026-06-15"),
                ("FPT", "2026-07-15"),
                ("VCB", "2026-06-20"),
            ]:
                store.insert_dividend_event(
                    ticker=ticker,
                    ex_date=ex_date,
                    cash_amount=1,
                    stock_ratio_pct=None,
                    note=None,
                )

            removed = store.delete_dividend_events_for_ticker("fpt")

            self.assertEqual(removed, 2)
            self.assertEqual(store.list_dividend_events("FPT"), [])
            self.assertEqual(len(store.list_dividend_events("VCB")), 1)

    def test_deletes_dividend_events_except_keep_ids(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            keep = store.insert_dividend_event(
                ticker="FPT",
                ex_date="2026-06-15",
                cash_amount=1,
                stock_ratio_pct=None,
                note=None,
            )
            store.insert_dividend_event(
                ticker="VCB",
                ex_date="2026-06-20",
                cash_amount=1,
                stock_ratio_pct=None,
                note=None,
            )

            removed = store.delete_dividend_events_except_ids({keep["id"]})
            rows = store.list_dividend_events()

            self.assertEqual(removed, 1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["id"], keep["id"])

    def test_external_dividend_events_are_upserted_without_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            event = {
                "ticker": "FPT",
                "ex_date": "2026-06-20",
                "note": "FireAnt: Cổ tức",
                "source": "fireant",
                "external_id": "FPT:event-1",
            }

            store.upsert_external_dividend_events([event])
            event["note"] = "FireAnt: Cổ tức cập nhật"
            store.upsert_external_dividend_events([event])

            rows = store.list_dividend_events("FPT")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["note"], "FireAnt: Cổ tức cập nhật")

    def test_external_dividend_events_do_not_duplicate_same_ex_date(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            # A manual entry with the real cash amount.
            store.insert_dividend_event(
                ticker="VPB", ex_date="2026-05-15", cash_amount=0.5,
                stock_ratio_pct=None, note="manual",
            )
            # An auto event for the same ticker + ex_date must not create a second row.
            store.upsert_external_dividend_events([
                {
                    "ticker": "VPB", "ex_date": "2026-05-15", "cash_amount": 0.5,
                    "stock_ratio_pct": None, "issue_ratio_pct": None, "issue_price": None,
                    "note": "VNStock", "source": "vnstock", "external_id": "VPB:evt-1",
                }
            ])
            rows = store.list_dividend_events("VPB")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["note"], "manual")
            # A different ex_date is still added.
            store.upsert_external_dividend_events([
                {
                    "ticker": "VPB", "ex_date": "2026-08-01", "cash_amount": 1.0,
                    "stock_ratio_pct": None, "issue_ratio_pct": None, "issue_price": None,
                    "note": "VNStock later", "source": "vnstock", "external_id": "VPB:evt-2",
                }
            ])
            self.assertEqual(len(store.list_dividend_events("VPB")), 2)

    def test_sector_mappings_seed_upsert_and_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SignalStore(Path(tmp) / "signals.db")

            seeded = store.sector_map()
            self.assertEqual(seeded.get("VCB"), "Ngân hàng")
            self.assertEqual(seeded.get("FPT"), "Công nghệ")

            mapping = store.upsert_sector_mapping(ticker="abc", sector="Thử nghiệm")
            self.assertEqual(mapping["ticker"], "ABC")
            self.assertEqual(store.sector_map()["ABC"], "Thử nghiệm")

            store.upsert_sector_mapping(ticker="ABC", sector="Cập nhật")
            self.assertEqual(store.sector_map()["ABC"], "Cập nhật")

            self.assertTrue(store.delete_sector_mapping("abc"))
            self.assertNotIn("ABC", store.sector_map())
            self.assertFalse(store.delete_sector_mapping("ABC"))

    def test_apply_auto_sector_mappings_protects_manual_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SignalStore(Path(tmp) / "signals.db")
            # Seeded rows are source='seed' and should be overwritable.
            self.assertEqual(store.sector_map()["VCB"], "Ngân hàng")
            store.upsert_sector_mapping(ticker="FPT", sector="Manual choice")

            result = store.apply_auto_sector_mappings(
                {"VCB": "Ngân hàng ICB", "FPT": "Should not overwrite", "ZZZ": "Mới", "": "skip"}
            )
            self.assertEqual(result["added"], 1)  # ZZZ is new
            self.assertEqual(result["updated"], 1)  # VCB seed overwritten
            self.assertEqual(store.sector_map()["VCB"], "Ngân hàng ICB")
            self.assertEqual(store.sector_map()["FPT"], "Manual choice")  # protected
            self.assertEqual(store.sector_map()["ZZZ"], "Mới")
            self.assertEqual(store.apply_auto_sector_mappings({}), {"added": 0, "updated": 0})

    def test_foreign_flow_daily_records_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SignalStore(Path(tmp) / "signals.db")
            store.record_foreign_flow_daily(
                {"VPB": {"buy_value": 3e11, "sell_value": 5e10, "net_value": 2.5e11}},
                "2026-07-01",
            )
            store.record_foreign_flow_daily(
                {"VPB": {"net_value": -1e11}, "FPT": {"net_value": 5e10}},
                "2026-07-02",
            )
            # Re-record same day updates instead of duplicating.
            store.record_foreign_flow_daily({"VPB": {"net_value": -1.2e11}}, "2026-07-02")

            history = store.foreign_flow_history(["VPB", "FPT"], days=5)
            self.assertEqual(history["VPB"], [-1.2e11, 2.5e11])  # newest first
            self.assertEqual(history["FPT"], [5e10])
            self.assertEqual(store.foreign_flow_history([]), {})

    def test_latest_signal_received_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SignalStore(Path(tmp) / "signals.db")
            self.assertIsNone(store.latest_signal_received_at())
            store.insert_signal(
                ticker="FPT",
                exchange="HOSE",
                action="buy",
                price=100,
                timeframe="1D",
                strategy="RS",
                note=None,
                source_time=None,
                payload={},
                enrichment={},
            )
            self.assertIsNotNone(store.latest_signal_received_at())


if __name__ == "__main__":
    unittest.main()

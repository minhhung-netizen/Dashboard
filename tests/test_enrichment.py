import unittest

from app.services.enrichment import (
    VnstockEnricher,
    coerce_float,
    normalize_action,
    normalize_stock_price,
    normalize_ticker,
)


class EnrichmentHelpersTest(unittest.TestCase):
    def test_normalize_ticker_removes_exchange_prefix(self):
        self.assertEqual(normalize_ticker("HOSE:VPB"), ("VPB", "HOSE"))

    def test_normalize_ticker_keeps_plain_symbol(self):
        self.assertEqual(normalize_ticker(" vpb "), ("VPB", None))

    def test_normalize_ticker_accepts_tradingview_adjusted_symbol_object(self):
        self.assertEqual(
            normalize_ticker({"adjustment": "dividends", "symbol": "HOSE:HHS"}),
            ("HHS", "HOSE"),
        )

    def test_normalize_ticker_accepts_tradingview_adjusted_symbol_string(self):
        self.assertEqual(
            normalize_ticker('={"adjustment":"dividends","symbol":"HOSE:HHS"}'),
            ("HHS", "HOSE"),
        )

    def test_normalize_action_aliases(self):
        self.assertEqual(normalize_action("long"), "buy")
        self.assertEqual(normalize_action("exit"), "sell")
        self.assertEqual(normalize_action("confirm-buy"), "confirm_buy")
        self.assertEqual(normalize_action("confirmation_sell"), "confirm_sell")

    def test_coerce_float_accepts_tradingview_strings(self):
        self.assertEqual(coerce_float("19,500"), 19500.0)
        self.assertIsNone(coerce_float(""))

    def test_normalize_stock_price_converts_vnd_to_thousand_unit(self):
        self.assertEqual(normalize_stock_price("74400"), 74.4)
        self.assertEqual(normalize_stock_price("13.95"), 13.95)

    def test_enricher_handles_non_exception_vnstock_failures(self):
        class ExplodingEnricher(VnstockEnricher):
            def _enrich_with_vnstock(self, ticker):
                raise SystemExit("vnstock exited")

        result = ExplodingEnricher().enrich("VPB")

        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["ticker"], "VPB")
        self.assertEqual(result["history"], [])
        self.assertEqual(result["metrics"], {})

    def test_enricher_caches_by_ticker(self):
        class CountingEnricher(VnstockEnricher):
            def __init__(self):
                super().__init__(cache_ttl_seconds=60, min_request_interval_seconds=0)
                self.calls = 0

            def _enrich_with_vnstock(self, ticker):
                self.calls += 1
                return {
                    "status": "ok",
                    "ticker": ticker,
                    "history": [{"close": 10}],
                    "metrics": {},
                }

        enricher = CountingEnricher()

        first = enricher.enrich("VPB")
        second = enricher.enrich("VPB")
        first["history"][0]["close"] = 99

        self.assertEqual(enricher.calls, 1)
        self.assertEqual(second["history"][0]["close"], 10)


if __name__ == "__main__":
    unittest.main()

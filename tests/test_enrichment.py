import unittest

from app.services.enrichment import coerce_float, normalize_action, normalize_ticker


class EnrichmentHelpersTest(unittest.TestCase):
    def test_normalize_ticker_removes_exchange_prefix(self):
        self.assertEqual(normalize_ticker("HOSE:VPB"), ("VPB", "HOSE"))

    def test_normalize_ticker_keeps_plain_symbol(self):
        self.assertEqual(normalize_ticker(" vpb "), ("VPB", None))

    def test_normalize_action_aliases(self):
        self.assertEqual(normalize_action("long"), "buy")
        self.assertEqual(normalize_action("exit"), "sell")

    def test_coerce_float_accepts_tradingview_strings(self):
        self.assertEqual(coerce_float("19,500"), 19500.0)
        self.assertIsNone(coerce_float(""))


if __name__ == "__main__":
    unittest.main()

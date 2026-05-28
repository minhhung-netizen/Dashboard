import unittest

from app.services.webhook_payload import parse_forgiving_json


class WebhookPayloadParsingTest(unittest.TestCase):
    def test_repairs_tradingview_equals_after_key(self):
        data = parse_forgiving_json(
            '{"ticker":={"adjustment":"dividends","symbol":"HOSE:HHS"},'
            '"action":"sell","price":"11700"}'
        )

        self.assertEqual(data["ticker"]["symbol"], "HOSE:HHS")
        self.assertEqual(data["action"], "sell")

    def test_repairs_leading_equals_before_json(self):
        data = parse_forgiving_json(
            '={"ticker":{"adjustment":"dividends","symbol":"HOSE:GVR"},'
            '"action":"buy"}'
        )

        self.assertEqual(data["ticker"]["symbol"], "HOSE:GVR")
        self.assertEqual(data["action"], "buy")

    def test_repairs_misquoted_json_with_adjusted_ticker(self):
        data = parse_forgiving_json(
            '"{"ticker":={"adjustment":"dividends","symbol":"HOSE:VRE"},'
            '"action":"sell","price":"31400"}"'
        )

        self.assertEqual(data["ticker"]["symbol"], "HOSE:VRE")
        self.assertEqual(data["action"], "sell")


if __name__ == "__main__":
    unittest.main()

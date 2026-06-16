import unittest

from app.main import (
    WebhookPayload,
    confirmation_base_strategy,
    is_confirmation_signal,
    required_open_strategy_for_signal,
)


class WebhookRoutingTest(unittest.TestCase):
    def test_base_strategy_on_regular_buy_does_not_make_it_confirmation(self):
        payload = WebhookPayload(
            ticker="HOSE:FTS",
            action="buy",
            price="24950",
            timeframe="60",
            strategy="Modern Stock EMA",
            base_strategy="Modern Stock EMA",
            signal_type="entry",
            secret="change-me",
        )

        self.assertFalse(is_confirmation_signal(payload, "buy"))
        self.assertEqual(confirmation_base_strategy(payload), "Modern Stock EMA")
        self.assertIsNone(required_open_strategy_for_signal(payload, "buy"))

    def test_confirm_buy_is_confirmation(self):
        payload = WebhookPayload(
            ticker="HOSE:FTS",
            action="confirm_buy",
            price="24950",
            strategy="HMA",
            base_strategy="Modern Stock EMA",
            signal_type="confirm",
            secret="change-me",
        )

        self.assertTrue(is_confirmation_signal(payload, "confirm_buy"))
        self.assertEqual(confirmation_base_strategy(payload), "Modern Stock EMA")
        self.assertEqual(
            required_open_strategy_for_signal(payload, "confirm_buy"),
            "Modern Stock EMA",
        )


if __name__ == "__main__":
    unittest.main()

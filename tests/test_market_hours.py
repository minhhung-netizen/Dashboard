import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.market_hours import is_market_open, parse_market_sessions


VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


class MarketHoursTest(unittest.TestCase):
    def test_market_is_open_during_configured_sessions(self):
        now = datetime(2026, 5, 25, 9, 30, tzinfo=VN_TZ)

        self.assertTrue(is_market_open(now))

    def test_market_is_closed_during_lunch_break(self):
        now = datetime(2026, 5, 25, 12, 0, tzinfo=VN_TZ)

        self.assertFalse(is_market_open(now))

    def test_market_is_closed_on_weekends(self):
        now = datetime(2026, 5, 24, 10, 0, tzinfo=VN_TZ)

        self.assertFalse(is_market_open(now))

    def test_market_sessions_are_configurable(self):
        sessions = parse_market_sessions("09:15-11:30,13:00-14:45")

        self.assertEqual(len(sessions), 2)
        self.assertEqual(sessions[0][0].hour, 9)
        self.assertEqual(sessions[0][0].minute, 15)


if __name__ == "__main__":
    unittest.main()

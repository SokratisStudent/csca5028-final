from unittest import TestCase

from backend.public_holidays.src.public_holidays_http_request import PublicHolidayRequest
from settings import settings_data


class TestPublicHolidaysHttpRequest(TestCase):
    def test_load_country_results(self):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data("CY", 2024)

        assert len(holidays) == 11

        holidays = holiday_request.fetch_data("US", 2023)

        assert len(holidays) == 3

        holidays = holiday_request.fetch_data("SP", 2024)

        assert len(holidays) == 8

from unittest import TestCase

from components.public_holidays.src.public_holidays_http_request import PublicHolidayRequest
from settings import settings_data


class TestPublicHolidaysHttpRequest(TestCase):
    def test_load_country_results(self):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data("CY", 2024)

        assert 11 == len(holidays)

        holidays = holiday_request.fetch_data("US", 2023)

        assert 3 == len(holidays)

        holidays = holiday_request.fetch_data("SP", 2024)

        assert 8 == len(holidays)

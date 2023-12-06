from unittest import TestCase

from components.public_holidays.src.public_holidays_http_request import PublicHolidayRequest
from settings import settings_data

class TestPublicHolidaysHttpRequest(TestCase):
    def test_load_cyprus_2024_results(self):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data("CY", "2024")

        assert 11 == len(holidays)

    def test_load_us_2023_results(self):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data("US", "2023")

        assert 3 == len(holidays)

    def test_load_sp_2024_results(self):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data("SP", "2024")

        assert 8 == len(holidays)

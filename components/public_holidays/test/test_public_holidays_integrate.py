import json
from unittest import TestCase

from components.database.main import db
from webapp.app import create_test_app
from components.public_holidays.src.public_holiday_control import getHolidays
from components.public_holidays.src.country_db_model import Country
from components.public_holidays.src.public_holidays_db_model import PublicHoliday


class TestPublicHolidayIntegrate(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_getHolidays(self):
        with self.app.app_context():
            # Ensure no entries for test country CY
            holiday_entries_before = len(PublicHoliday.query.all())
            country_entry = Country.query.filter_by(country_code="CY").all()
            assert len(country_entry) == 0

            holidays = getHolidays("CY", 2024)
            assert len(holidays) == 11

            # Ensure test country CY was added with all its holidays
            country_entry = Country.query.filter_by(country_code="CY").all()
            assert len(country_entry) == 1

            holiday_entries_mid = len(PublicHoliday.query.all())
            assert (holiday_entries_before == (holiday_entries_mid - 11))

            holidays = getHolidays("CY", 2024)
            assert len(holidays) == 11

            # Ensure the test country or its holidays were not added twice
            country_entry = Country.query.filter_by(country_code="CY").all()
            assert len(country_entry) == 1

            holiday_entries_after = len(PublicHoliday.query.all())
            assert (holiday_entries_mid == holiday_entries_after)


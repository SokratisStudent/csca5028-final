from unittest import TestCase
from datetime import datetime

from backend.database.main import db
from webapp.src.init_app import create_test_app
from backend.public_holidays.src.public_holiday_control import parseRequest


class TestPublicHolidayControl(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_parseData(self):
        data = []
        result = parseRequest('AB', data)

        assert len(result) == 0

        data = [{'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-03-25', 'day': 'Monday', 'name': 'Greek Independence Day', 'type': 'NATIONAL_HOLIDAY'}]
        result = parseRequest('CY', data)

        assert len(result) == 1
        assert result[0].name == 'Greek Independence Day'
        assert result[0].type == 'NATIONAL_HOLIDAY'
        assert result[0].date == datetime.strptime('2024-03-25', "%Y-%m-%d")

        data = [{'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-08-15', 'day': 'Thursday', 'name': 'Assumption of the Virgin Mary', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-03-25', 'day': 'Monday', 'name': 'Greek Independence Day', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-05-01', 'day': 'Wednesday', 'name': 'Labour Day/May Day', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-04-01', 'day': 'Monday', 'name': 'Cyprus National Holiday', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-10-01', 'day': 'Tuesday', 'name': 'Cyprus Independence Day', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-12-26', 'day': 'Thursday', 'name': 'Boxing Day', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-01-06', 'day': 'Saturday', 'name': 'Epiphany', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-03-18', 'day': 'Monday', 'name': 'Green Monday', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-12-25', 'day': 'Wednesday', 'name': 'Christmas Day', 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-01-01', 'day': 'Monday', 'name': "New Year's Day", 'type': 'NATIONAL_HOLIDAY'}, {'country': 'Cyprus', 'iso': 'CY', 'year': 2024, 'date': '2024-10-28', 'day': 'Monday', 'name': 'Ochi Day', 'type': 'NATIONAL_HOLIDAY'}]
        result = parseRequest('CY', data)

        assert len(result) == 11
        assert result[1].name == 'Greek Independence Day'
        assert result[1].type == 'NATIONAL_HOLIDAY'
        assert result[1].date == datetime.strptime('2024-03-25', "%Y-%m-%d")
        assert result[10].name == 'Ochi Day'
        assert result[10].type == 'NATIONAL_HOLIDAY'
        assert result[10].date == datetime.strptime('2024-10-28', "%Y-%m-%d")

        def test_getHolidays():
            pass





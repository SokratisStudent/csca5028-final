from unittest import TestCase
from datetime import datetime

from components.database.main import db
from webapp.src.init_app import create_test_app
from components.personal_vacations.src.person_control import createPerson
from components.personal_vacations.src.person_db_model import Person
from components.public_holidays.src.public_holidays_db_model import PublicHoliday


class TestPersonalVacationIntegration(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_createPerson_checkHolidays(self):
        with self.app.app_context():
            person = createPerson("TestGuy2", "TV")
            assert person is not None
            assert person.country_name == "Tuvalu"

            person_entry = Person.query.filter_by(name=person.name).all()
            assert len(person_entry) == 1
            assert person_entry[0].country_code == "TV"

            holidays = PublicHoliday.query.filter_by(country_code="TV").all()
            assert len(holidays) > 0
            for holiday in holidays:
                current_year = datetime.now().year
                current_month = datetime.now().month
                holiday_date = holiday.date.date()
                assert holiday_date.year == current_year or (current_month > 10 and holiday_date.year == current_year+1)


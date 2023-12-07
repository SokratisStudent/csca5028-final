from unittest import TestCase
from datetime import datetime

from components.database.main import db
from webapp.src.init_app import create_test_app
from components.person.src.person_control import PersonalVacationObj, createPerson, createVacations
from components.person.src.person_db_model import Person
from components.person.src.personal_vacations_db_model import PersonalVacation


class TestPersonalVacationController(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_createPerson(self):
        with self.app.app_context():
            person = createPerson("TestGuy", "US")
            assert person is not None
            assert person.country_name == "United States"

            person_entry = Person.query.filter_by(name=person.name).all()
            assert len(person_entry) == 1
            assert person_entry[0].country_code == "US"

            person = createPerson("TestGuy", "SP")
            assert person is None

    def test_personal_vacation_class(self):
        vacation = PersonalVacationObj("John", datetime.strptime("20231207", "%Y%m%d"), datetime.strptime("20231217", "%Y%m%d"))
        to_string = vacation.__str__()
        assert to_string == 'John: from 12/07/23 to 12/17/23' or vacation == 'John: from 07/12/23 to 17/12/23'

    def test_createVacations(self):
        with self.app.app_context():
            person = createPerson("TestGuy", "US")
            person_entry = Person.query.filter_by(name="TestGuy").first()
            vacations = [PersonalVacationObj("TestGuy", datetime.strptime("20231207", "%Y%m%d"),datetime.strptime("20231217", "%Y%m%d"))]
            createVacations(person_entry, vacations)

            vacation_entries = PersonalVacation.query.filter_by(person_id=person_entry.id).all()

            assert len(vacation_entries) == 1
            assert vacation_entries[0].start_date == datetime.strptime("20231207", "%Y%m%d")
            assert vacation_entries[0].end_date == datetime.strptime("20231217", "%Y%m%d")

            more_vacations = [PersonalVacationObj("TestGuy", datetime.strptime("20240102", "%Y%m%d"),datetime.strptime("20230104", "%Y%m%d")), PersonalVacationObj("TestGuy", datetime.strptime("20240202", "%Y%m%d"),datetime.strptime("20230204", "%Y%m%d"))]
            createVacations(person_entry, more_vacations)

            vacation_entries = PersonalVacation.query.filter_by(person_id=person_entry.id).all()

            assert len(vacation_entries) == 3




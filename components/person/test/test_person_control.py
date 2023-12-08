import datetime
from unittest import TestCase
from unittest.mock import Mock

from components.database.main import db
from webapp.src.init_app import create_test_app
from components.person.src.person_control import PersonalVacationObj, createPerson, createVacations, getAllAbsencesForPerson
from components.person.src.person_db_model import Person
from components.person.src.personal_vacations_db_model import PersonalVacation
from components.project.src.project_control import createProject


class TestPersonController(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)
        with self.app.app_context():
            createProject("TestProject")

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_createPerson(self):
        with self.app.app_context():
            person = createPerson("TestGuy", "US", "TestProject")
            assert person is not None
            assert person.country_name == "United States"

            person_entry = Person.query.filter_by(name=person.name).all()
            assert len(person_entry) == 1
            assert person_entry[0].country_code == "US"

            person = createPerson("TestGuy", "SP", "TestProject")
            assert person is None

    def test_createPersonMockDate(self):
        with self.app.app_context():
            global datetime
            mock_today = datetime.datetime.strptime('2020-01-07', '%Y-%m-%d')
            datetime = Mock()
            datetime.datetime.today.return_value = mock_today
            person = createPerson("TestGuy2", "GB", "TestProject")
            person_entry = Person.query.filter_by(name=person.name).first()
            dates = getAllAbsencesForPerson(person_entry)

            for date in dates:
                assert date.year == 2020

    def test_createPersonMockDate2(self):
        with self.app.app_context():
            global datetime
            mock_today = datetime.datetime.strptime('2020-10-01', '%Y-%m-%d')
            datetime = Mock()
            datetime.datetime.today.return_value = mock_today
            person = createPerson("TestGuy2", "GB", "TestProject")
            person_entry = Person.query.filter_by(name=person.name).first()
            dates = getAllAbsencesForPerson(person_entry)

            for date in dates:
                assert date.year == 2020 or date.year == 2021

    def test_personal_vacation_class(self):
        vacation = PersonalVacationObj("John", "2023-12-07", "2023-12-17")
        to_string = vacation.__str__()
        assert to_string == 'John: from 12/07/23 to 12/17/23' or vacation == 'John: from 07/12/23 to 17/12/23'

    def test_createVacations(self):
        with self.app.app_context():
            createPerson("TestGuy", "US", "TestProject")
            person_entry = Person.query.filter_by(name="TestGuy").first()
            vacations = [PersonalVacationObj("TestGuy", "2023-12-07", "2023-12-17")]
            createVacations(person_entry, vacations)

            vacation_entries = PersonalVacation.query.filter_by(person_id=person_entry.id).all()

            assert len(vacation_entries) == 1
            assert vacation_entries[0].start_date == datetime.strptime("20231207", "%Y%m%d")
            assert vacation_entries[0].end_date == datetime.strptime("20231217", "%Y%m%d")

            more_vacations = [PersonalVacationObj("TestGuy", "2024-01-02", "2024-01-04"), PersonalVacationObj("TestGuy", "2024-02-02", "2024-02-04")]
            createVacations(person_entry, more_vacations)

            vacation_entries = PersonalVacation.query.filter_by(person_id=person_entry.id).all()

            assert len(vacation_entries) == 3

from unittest import TestCase

from components.database.main import db
from webapp.src.init_app import create_test_app

from components.person.src.person_control import createPerson, parseVacationsRequest, createVacations, PersonalVacationObj, getAllAbsencesForPerson
from components.project.src.project_control import getActiveProjects, createProject, getAllPeopleInProject

from main import projects

class TestMain(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def testProjects(self):
        with self.app.app_context():
            createProject("Iron Man")
            createPerson("Tony Stark", "US", "Iron Man")

            return_value = projects(test_mode=True)
            print(return_value)

from unittest import TestCase

from backend.database.main import db
from webapp.src.init_app import create_test_app

from backend.person.src.person_control import createPerson
from backend.project.src.project_control import createProject

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
            assert return_value.startswith('<table><tr><th width=120>Iron Man')

from unittest import TestCase
from datetime import datetime

from components.database.main import db
from webapp.src.init_app import create_test_app
from components.project.src.project_control import createProject, getActiveProjects, getAllPeopleInProject
from components.person.src.person_control import createPerson


class TestProjectControl(TestCase):
    def setup_class(self):
        self.app = create_test_app(db)

    def teardown_class(self):
        with self.app.app_context():
            db.drop_all()
            db.session.close()

    def test_projects(self):
        with self.app.app_context():
            project_list = getActiveProjects()
            initial_count = len(project_list)
            result = createProject("RandomProject1")
            assert result is not None
            project_list = getActiveProjects()
            assert len(project_list) == (1 + initial_count)
            assert "RandomProject1" in [project.name for project in project_list]
            result = createProject("RandomProject2")
            assert result is not None
            project_list = getActiveProjects()
            assert len(project_list) == (2 + initial_count)
            result = createProject("RandomProject1")
            assert result is None
            project_list = getActiveProjects()
            assert len(project_list) == (2 + initial_count)

    def test_getAllPeopleInProject(self):
        with self.app.app_context():
            project1 = createProject("RandomProject4")
            createProject("RandomProject5")
            createPerson("TestPerson1", "US", "RandomProject4")
            createPerson("TestPerson2", "GB", "RandomProject5")
            createPerson("TestPerson3", "GR", "RandomProject4")
            people = getAllPeopleInProject(project1)
            assert len(people) == 2
            assert people[0].name == "TestPerson1" or people[1].name == "TestPerson1"
            assert people[0].name == "TestPerson3" or people[1].name == "TestPerson3"






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
            assert len(project_list) == 0
            result = createProject("RandomProject1")
            assert result is not None
            project_list = getActiveProjects()
            assert len(project_list) == 1
            assert project_list[0].name == "RandomProject1"
            result = createProject("RandomProject2")
            assert result is not None
            project_list = getActiveProjects()
            assert len(project_list) == 2
            result = createProject("RandomProject1")
            assert result is None
            project_list = getActiveProjects()
            assert len(project_list) == 2

    def test_getAllPeopleInProject(self):
        with self.app.app_context():
            project1 = createProject("RandomProject1")
            project2 = createProject("RandomProject2")
            createPerson("TestPerson1", "US", "RandomProject1")
            createPerson("TestPerson2", "GB", "RandomProject2")
            createPerson("TestPerson3", "GR", "RandomProject1")
            people = getAllPeopleInProject(project1)
            assert len(people) == 2
            assert people[0].name == "TestPerson1" or people[1].name == "TestPerson1"
            assert people[0].name == "TestPerson3" or people[1].name == "TestPerson3"






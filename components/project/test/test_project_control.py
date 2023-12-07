from unittest import TestCase
from datetime import datetime

from components.database.main import db
from webapp.src.init_app import create_test_app
from components.project.src.project_control import createProject, getActiveProjects
from components.project.src.project_model import Project


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
            assert result is True
            project_list = getActiveProjects()
            assert len(project_list) == 1
            assert project_list[0].name == "RandomProject1"
            result = createProject("RandomProject2")
            assert result is True
            project_list = getActiveProjects()
            assert len(project_list) == 2
            result = createProject("RandomProject1")
            assert result is False
            project_list = getActiveProjects()
            assert len(project_list) == 2



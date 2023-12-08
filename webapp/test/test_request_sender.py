from unittest import TestCase
from webapp.src.request_sender import RabbitRequestSender


class TestCaseRequestSender(TestCase):
    def setup_class(self):
        self.request_sender = RabbitRequestSender()

    def test_addProject(self):
        assert self.request_sender.createProject("TCRS_Project_1", True) is True

    def test_addPerson(self):
        assert self.request_sender.createPerson("TCRS_Person_1", "GR", "TCRS_Project_1", True) is True
